#!/usr/bin/env python3
import hashlib
import json
import os
import re
from pathlib import Path

BASE = Path("/Users/tranthanh/Dev/Security/web3-audit/Past-Audit-Competitions")
OUT = Path(__file__).resolve().parent.parent / "competition_index.jsonl"

SEV_MAP = {
    "critical": "Critical",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
    "insight": "Info",
}

SEV_RE = re.compile(r"\[(?:SC|Smart Contract)\s*-\s*([^\]]+)\]", re.IGNORECASE)

def normalize_severity(raw: str) -> str:
    if not raw:
        return "Info"
    key = raw.strip().lower()
    key = key.replace("smart contract -", "").strip()
    key = key.split()[0]
    return SEV_MAP.get(key, "Info")

def main():
    records = []
    for path in BASE.rglob("*.md"):
        rel = path.relative_to(BASE)
        name = path.stem
        sev_match = SEV_RE.search(name) or SEV_RE.search(path.name)
        sev = normalize_severity(sev_match.group(1) if sev_match else "")
        rid = hashlib.sha1(str(rel).encode()).hexdigest()[:12].upper()
        records.append({
            "id": f"CMP-{rid}",
            "title": name,
            "severity": sev,
            "category": "competition-index",
            "root_cause": "See source report for details (not summarized).",
            "attack_path": "",
            "impact": "",
            "mitigation": "",
            "tags": [sev.lower(), "competition", "index"],
            "source": {"type": "competition", "path": str(rel)},
        })
    with open(OUT, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} records to {OUT}")

if __name__ == "__main__":
    main()
