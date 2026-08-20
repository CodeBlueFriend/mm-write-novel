#!/usr/bin/env python3
"""Build summaries/manuscript-index.csv from chapter control metadata."""

from __future__ import annotations

import argparse
import re
import sys

from _common import body_text, chapter_files, extract_control, project_path, write_csv

HEADER = ["language_dir", "chapter_id", "file", "title", "pov", "time", "location", "status", "characters", "english_words"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    args = parser.parse_args()
    try:
        project = project_path(args.project)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 2
    rows = []
    for path in chapter_files(project):
        text = path.read_text(encoding="utf-8")
        first = text.splitlines()[0].lstrip("# ").strip() if text.splitlines() else ""
        body = body_text(text)
        rows.append({
            "language_dir": path.parent.name,
            "chapter_id": path.stem.upper(),
            "file": str(path.relative_to(project)),
            "title": first,
            "pov": extract_control(text, "POV"),
            "time": extract_control(text, "时间"),
            "location": extract_control(text, "地点"),
            "status": "locked" if "- 锁定状态：locked" in text else "draft",
            "characters": len(re.sub(r"\s+", "", body)),
            "english_words": len(re.findall(r"\b[A-Za-z]+(?:['’-][A-Za-z]+)*\b", body)),
        })
    output = project / "summaries/manuscript-index.csv"
    write_csv(output, HEADER, rows)
    print(f"已索引 {len(rows)} 个章节：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
