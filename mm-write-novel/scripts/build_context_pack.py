#!/usr/bin/env python3
"""Build a bounded Markdown context pack for a requested chapter batch."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _common import chapter_files, project_path, read_csv

CORE = ["00-project-brief.md", "02-author-intent.md", "03-story-bible.md", "06-series-architecture.md", "07-volume-arcs.md", "locked-decisions.md"]
LEDGERS = ["character-state.csv", "knowledge-state.csv", "relationship-ledger.csv", "props-resources.csv", "plot-thread-ledger.csv", "foreshadowing-ledger.csv", "reader-question-ledger.csv"]


def add_file(parts: list[str], project: Path, relative: str, limit: int) -> None:
    path = project / relative
    if path.exists():
        text = path.read_text(encoding="utf-8").strip()
        if len(text) > limit:
            text = text[:limit] + "\n\n[已按上下文包上限截断]"
        parts.extend([f"## {relative}", text])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--chapters", nargs="+", required=True, help="目标章节 ID，例如 CH006 CH007")
    parser.add_argument("--max-chars-per-file", type=int, default=12000)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        project = project_path(args.project)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 2
    wanted = {value.upper() for value in args.chapters}
    parts = ["# 最小上下文包", "目标章节：" + ", ".join(sorted(wanted))]
    for relative in CORE:
        add_file(parts, project, relative, args.max_chars_per_file)

    matrix = project / "08-chapter-matrix.csv"
    if matrix.exists():
        header, rows = read_csv(matrix)
        selected = [row for row in rows if row.get("chapter_id", "").upper() in wanted]
        parts.extend(["## 目标章节卡", "| " + " | ".join(header) + " |", "|" + "---|" * len(header)])
        parts.extend("| " + " | ".join((row.get(key) or "").replace("|", "\\|") for key in header) + " |" for row in selected)

    add_file(parts, project, "summaries/chapter-summaries.md", args.max_chars_per_file)
    for filename in LEDGERS:
        path = project / "continuity" / filename
        if not path.exists():
            continue
        header, rows = read_csv(path)
        active = [row for row in rows if row.get("status", "").lower() not in {"resolved", "paid-off", "abandoned-approved", "已解决", "已回收"}]
        if active:
            parts.extend([f"## continuity/{filename}", "| " + " | ".join(header) + " |", "|" + "---|" * len(header)])
            parts.extend("| " + " | ".join((row.get(key) or "").replace("|", "\\|") for key in header) + " |" for row in active)

    files_by_id = {path.stem.upper(): path for path in chapter_files(project)}
    for chapter_id in sorted(wanted):
        path = files_by_id.get(chapter_id)
        if path:
            text = path.read_text(encoding="utf-8")
            parts.extend([f"## 当前草稿 {path.relative_to(project)}", text[:args.max_chars_per_file]])

    output = Path(args.output).expanduser().resolve() if args.output else project / "context-packs" / ("context-" + "-".join(sorted(wanted)) + ".md")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n\n".join(parts).strip() + "\n", encoding="utf-8")
    print(f"已生成上下文包：{output}（{output.stat().st_size} bytes）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
