#!/usr/bin/env python3
"""Compile managed chapter files into a clean, single Markdown manuscript."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _common import body_text, chapter_files, project_path


def project_title(project: Path) -> str:
    brief = project / "00-project-brief.md"
    if brief.exists():
        match = re.search(r"^-\s*项目名[：:]\s*(.+)$", brief.read_text(encoding="utf-8"), re.MULTILINE)
        if match:
            return match.group(1).strip()
    return project.name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--source", choices=["manuscript", "manuscript-zh", "manuscript-en"], default="manuscript")
    parser.add_argument("--output", help="输出 Markdown；默认写入 exports/<source>.md")
    args = parser.parse_args()
    try:
        project = project_path(args.project)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 2

    files = [path for path in chapter_files(project) if path.parent.name == args.source]
    if not files:
        print(f"未在 {args.source}/ 找到 CH*.md", file=sys.stderr)
        return 2
    parts = [f"# {project_title(project)}"]
    for path in files:
        text = path.read_text(encoding="utf-8")
        title = text.splitlines()[0].strip() if text.splitlines() else f"# {path.stem}"
        parts.extend([title, body_text(text)])
    output = Path(args.output).expanduser().resolve() if args.output else project / "exports" / f"{args.source}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n\n".join(parts).strip() + "\n", encoding="utf-8")
    print(f"已合并 {len(files)} 章：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
