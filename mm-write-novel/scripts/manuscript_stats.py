#!/usr/bin/env python3
"""Report chapter, body-character, and English word statistics."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict

from _common import body_text, chapter_files, project_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    args = parser.parse_args()
    try:
        project = project_path(args.project)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 2
    totals: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
    for path in chapter_files(project):
        body = body_text(path.read_text(encoding="utf-8"))
        chars = len(re.sub(r"\s+", "", body))
        words = len(re.findall(r"\b[A-Za-z]+(?:['’-][A-Za-z]+)*\b", body))
        record = totals[path.parent.name]
        record[0] += 1
        record[1] += chars
        record[2] += words
    if not totals:
        print("未找到 CH*.md 正文章节。")
        return 0
    print("目录,章节数,正文非空白字符,英文词数")
    for name in sorted(totals):
        print(f"{name},{','.join(str(value) for value in totals[name])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
