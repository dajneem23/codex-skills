#!/usr/bin/env python3
"""
Index Solidity PoCs from SunWeb3 DeFiHackLabs src tree.

Source root: /Users/tranthanh/Dev/Security/sunweb3-Defihacklabs/src
Includes all *.sol files (top-level and src/test/**).

Output: defihacklabs_src_index.jsonl entries with:
- id: DHL-SRC-<hash>
- title: filename (with parent directory hint when available)
- severity: Info
- category: defihacklabs-src-index
- root_cause: directory hint (if any), otherwise placeholder
- tags: defihacklabs, solidity, plus path components (excluding "src")
- source: {type: "defihacklabs-src", path: relative path from repo root}
"""
import hashlib
import json
from pathlib import Path

BASE = Path("/Users/tranthanh/Dev/Security/sunweb3-Defihacklabs")
SRC = BASE / "src"
OUT = Path(__file__).resolve().parent.parent / "defihacklabs_src_index.jsonl"


def main():
    records = []
    for path in SRC.rglob("*.sol"):
        rel = path.relative_to(BASE)
        parts = rel.parts
        # Build tags from path components except "src"
        tags = ["defihacklabs", "defihacklabs-src", "solidity"] + [p for p in parts if p not in ("src",)]
        hint = "/".join(parts[:-1]) if len(parts) > 1 else ""
        rid = hashlib.sha1(str(rel).encode()).hexdigest()[:12].upper()
        records.append({
            "id": f"DHL-SRC-{rid}",
            "title": f"{parts[-1]}" if not hint else f"{hint}/{parts[-1]}",
            "severity": "Info",
            "category": "defihacklabs-src-index",
            "root_cause": hint or "See source file for details (not summarized).",
            "attack_path": "",
            "impact": "",
            "mitigation": "",
            "tags": tags,
            "source": {"type": "defihacklabs-src", "path": str(rel)},
        })
    with open(OUT, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} records to {OUT}")


if __name__ == "__main__":
    main()
