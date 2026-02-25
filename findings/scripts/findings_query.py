#!/usr/bin/env python3
import argparse
import json
import os
from typing import List, Dict

HERE = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB = os.path.join(os.path.dirname(HERE), "findings.jsonl")
DEFAULT_INDEXES = [
    os.path.join(os.path.dirname(HERE), "competition_index.jsonl"),
    os.path.join(os.path.dirname(HERE), "pdf_index.jsonl"),
    os.path.join(os.path.dirname(HERE), "defihacklabs_index.jsonl"),
    os.path.join(os.path.dirname(HERE), "defihacklabs_src_index.jsonl"),
]


def load_findings(path: str) -> List[Dict]:
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def matches_tags(entry: Dict, tags: List[str]) -> bool:
    if not tags:
        return True
    entry_tags = set(entry.get("tags", [])) | {entry.get("category", "")}
    return all(tag in entry_tags for tag in tags)


def keyword_score(entry: Dict, query: str) -> int:
    if not query:
        return 0
    hay = " ".join(
        str(entry.get(k, ""))
        for k in ["title", "root_cause", "attack_path", "impact", "mitigation", "tags", "category"]
    ).lower()
    score = 0
    for term in query.lower().split():
        if term in hay:
            score += 1
    return score


def main():
    p = argparse.ArgumentParser(description="Filter findings by tags and keywords (local, no embeddings).")
    p.add_argument("--db", default=DEFAULT_DB, help="Path to findings.jsonl")
    p.add_argument("--indexes", nargs="*", default=[], help="Additional index jsonl files (override defaults)")
    p.add_argument("--tags", nargs="*", default=[], help="Tags to require (AND match)")
    p.add_argument("--query", default="", help="Keyword query (space-separated terms)")
    p.add_argument("--limit", type=int, default=10, help="Max records to return")
    p.add_argument("--no-index", action="store_true", help="Skip loading competition index")
    args = p.parse_args()

    findings = load_findings(args.db)
    if not args.no_index:
        index_paths = args.indexes if args.indexes else DEFAULT_INDEXES
        for idx in index_paths:
            if os.path.exists(idx):
                findings += load_findings(idx)
    scored = []
    for f in findings:
        if not matches_tags(f, args.tags):
            continue
        score = keyword_score(f, args.query)
        scored.append((score, f))

    scored.sort(key=lambda x: (-x[0], x[1].get("severity", "")))
    for score, f in scored[: args.limit]:
        print(json.dumps({
            "id": f.get("id"),
            "title": f.get("title"),
            "severity": f.get("severity"),
            "category": f.get("category"),
            "tags": f.get("tags", []),
            "root_cause": f.get("root_cause"),
            "impact": f.get("impact"),
            "mitigation": f.get("mitigation"),
            "source": f.get("source", {}),
            "score": score,
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
