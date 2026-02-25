#!/usr/bin/env python3
"""
Build a JSONL index over SunWeb3 DeFiHackLabs incidents.

Sources:
- /Users/tranthanh/Dev/Security/sunweb3-Defihacklabs/README.md
- /Users/tranthanh/Dev/Security/sunweb3-Defihacklabs/past/*/README.md

Each incident line is a markdown link like:
[20250815 SizeCredit](past/2025/README.md#20250815-sizecredit---access-control)

We extract:
- date: 20250815
- name: SizeCredit
- anchor fragment: 20250815-sizecredit---access-control → summary="access-control"

Output records (defihacklabs_index.jsonl):
- id: DHL-<hash>
- title: "20250815 SizeCredit"
- severity: Info (unknown, not provided in list)
- category: defihacklabs-index
- summary: from anchor fragment after "---" if present
- tags: ["defihacklabs", summary tokens]
- source: {type: "defihacklabs", path: markdown link target}
"""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

BASE = Path("/Users/tranthanh/Dev/Security/sunweb3-Defihacklabs")
OUT = Path(__file__).resolve().parent.parent / "defihacklabs_index.jsonl"

LINK_RE = re.compile(r"\[(\d{8})\s+([^\]]+)\]\(([^)]+)\)")


def parse_line(line: str):
    m = LINK_RE.search(line)
    if not m:
        return None
    date, name, href = m.groups()
    frag = urlparse(href).fragment  # e.g., 20250815-sizecredit---access-control
    summary = ""
    if "---" in frag:
        summary = frag.split("---", 1)[1].replace("-", " ").strip()
    return {
        "date": date,
        "name": name.strip(),
        "href": href,
        "summary": summary,
    }


def collect_entries(path: Path):
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "[" not in line or "](" not in line:
                continue
            item = parse_line(line)
            if item:
                entries.append(item)
    return entries


def main():
    readmes = [BASE / "README.md"] + list((BASE / "past").rglob("README.md"))
    records = []
    for md in readmes:
        for item in collect_entries(md):
            key = f"{item['date']}::{item['name']}::{item['href']}"
            rid = hashlib.sha1(key.encode()).hexdigest()[:12].upper()
            tags = ["defihacklabs"]
            if item["summary"]:
                tags += [t for t in item["summary"].split() if t]
            records.append({
                "id": f"DHL-{rid}",
                "title": f"{item['date']} {item['name']}",
                "severity": "Info",
                "category": "defihacklabs-index",
                "root_cause": item["summary"] or "See source README for details (not summarized).",
                "attack_path": "",
                "impact": "",
                "mitigation": "",
                "tags": tags,
                "source": {"type": "defihacklabs", "path": item["href"]},
            })
    with open(OUT, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} records to {OUT}")


if __name__ == "__main__":
    main()
