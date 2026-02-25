#!/usr/bin/env python3
"""
Build a lightweight JSONL index over PDF audit reports in /Users/tranthanh/Dev/Security/web3-audit/audit-reports.

Dependencies: pip install pypdf

Output: competition-style entries in pdf_index.jsonl with minimal fields:
- id: PDF-<hash>
- title: filename stem
- severity: best-effort from filename tokens (Critical/High/Medium/Low/Info)
- category: pdf-index
- root_cause/attack_path/impact/mitigation: empty (not summarized)
- text_excerpt: first 800 chars of extracted text (for quick keyword search)
- source: {type: "pdf", path: relative path}

Note: This does not OCR scanned PDFs. For scanned docs, run OCR beforehand.
"""
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Optional

from pypdf import PdfReader

BASE = Path("/Users/tranthanh/Dev/Security/web3-audit/audit-reports")
OUT = Path(__file__).resolve().parent.parent / "pdf_index.jsonl"

SEV_MAP = {
    "critical": "Critical",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
    "info": "Info",
    "informational": "Info",
    "insight": "Info",
}

SEV_RE = re.compile(r"\[(critical|high|medium|low|info|informational|insight)\]", re.IGNORECASE)


def normalize_severity(name: str) -> str:
    m = SEV_RE.search(name)
    if m:
        return SEV_MAP.get(m.group(1).lower(), "Info")
    # fallback: look for keywords in filename
    lower = name.lower()
    for key in ("critical", "high", "medium", "low", "info"):
        if key in lower:
            return SEV_MAP[key]
    return "Info"


def extract_text(pdf_path: Path) -> str:
    try:
        reader = PdfReader(str(pdf_path))
        texts = []
        for page in reader.pages:
            chunk = page.extract_text() or ""
            texts.append(chunk)
        return "\n".join(texts)
    except Exception as e:
        return f"<extract_error: {e}>"


def main():
    records = []
    for path in BASE.rglob("*.pdf"):
        rel = path.relative_to(BASE)
        name = path.stem
        sev = normalize_severity(path.name)
        rid = hashlib.sha1(str(rel).encode()).hexdigest()[:12].upper()
        text = extract_text(path)
        excerpt = text[:800] if text else ""
        records.append({
            "id": f"PDF-{rid}",
            "title": name,
            "severity": sev,
            "category": "pdf-index",
            "root_cause": "See source PDF for details (not summarized).",
            "attack_path": "",
            "impact": "",
            "mitigation": "",
            "text_excerpt": excerpt,
            "tags": [sev.lower(), "pdf", "index"],
            "source": {"type": "pdf", "path": str(rel)},
        })
    with open(OUT, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} records to {OUT}")


if __name__ == "__main__":
    main()
