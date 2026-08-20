#!/usr/bin/env python3
"""Validate project structure, ledger headers, IDs, and bilingual mappings."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _common import BILINGUAL_MAP_HEADER, CHAPTER_MATRIX_HEADER, LEDGER_HEADERS, canonical_chapter_ids, project_path, read_csv

REQUIRED = [
    "00-project-brief.md", "01-market-brief.md", "02-author-intent.md", "03-story-bible.md",
    "04-character-bible.md", "05-world-bible.md", "06-series-architecture.md", "07-volume-arcs.md",
    "08-chapter-matrix.csv", "continuity/canon.yaml", "locked-decisions.md", "change-log.md",
]

UNIQUE_KEYS = {
    "timeline.csv": ("event_id",),
    "character-state.csv": ("character_id", "as_of_chapter"),
    "knowledge-state.csv": ("character_id", "fact_id"),
    "relationship-ledger.csv": ("relationship_id", "as_of_chapter"),
    "location-ledger.csv": ("location_id",),
    "props-resources.csv": ("item_id",),
    "plot-thread-ledger.csv": ("thread_id",),
    "foreshadowing-ledger.csv": ("foreshadow_id",),
    "reader-question-ledger.csv": ("question_id",),
    "bilingual-sync-ledger.csv": ("chapter_id", "scene_id"),
}


def check_csv(path: Path, expected: list[str], issues: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        issues.append(f"BLOCKER 缺少文件：{path.relative_to(path.parents[1])}")
        return []
    header, rows = read_csv(path)
    missing = [name for name in expected if name not in header]
    if missing:
        issues.append(f"BLOCKER {path.name} 缺少字段：{', '.join(missing)}")
    for row_number, row in enumerate(rows, 2):
        if None in row:
            issues.append(f"BLOCKER {path.name} 第 {row_number} 行包含超出表头的字段")
        missing_cells = [name for name in expected if row.get(name) is None]
        if missing_cells:
            issues.append(f"BLOCKER {path.name} 第 {row_number} 行缺少列：{', '.join(missing_cells)}")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    args = parser.parse_args()
    try:
        project = project_path(args.project)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 2

    issues: list[str] = []
    for relative in REQUIRED:
        if not (project / relative).exists():
            issues.append(f"BLOCKER 缺少文件：{relative}")

    matrix_rows = check_csv(project / "08-chapter-matrix.csv", CHAPTER_MATRIX_HEADER, issues)
    seen: set[str] = set()
    for row_number, row in enumerate(matrix_rows, 2):
        chapter_id = row.get("chapter_id", "").strip().upper()
        if not chapter_id:
            issues.append(f"MAJOR 章节矩阵第 {row_number} 行缺少 chapter_id")
        elif chapter_id in seen:
            issues.append(f"BLOCKER 章节矩阵重复 ID：{chapter_id}")
        seen.add(chapter_id)

    for filename, header in LEDGER_HEADERS.items():
        rows = check_csv(project / "continuity" / filename, header, issues)
        key_fields = UNIQUE_KEYS[filename]
        ids: set[tuple[str, ...]] = set()
        for row_number, row in enumerate(rows, 2):
            value = tuple(row.get(field, "").strip() for field in key_fields)
            if all(value) and value in ids:
                label = " / ".join(f"{field}={part}" for field, part in zip(key_fields, value))
                issues.append(f"BLOCKER {filename} 第 {row_number} 行重复复合键：{label}")
            ids.add(value)

    bilingual = (project / "manuscript-zh").is_dir() or (project / "manuscript-en").is_dir()
    if bilingual:
        mapping = project / "bilingual/chapter-map.csv"
        map_rows = check_csv(mapping, BILINGUAL_MAP_HEADER, issues)
        known = canonical_chapter_ids(project)
        for row_number, row in enumerate(map_rows, 2):
            chapter_id = row.get("chapter_id", "").strip().upper()
            if chapter_id and known and chapter_id not in known:
                issues.append(f"MAJOR 双语映射第 {row_number} 行引用未知章节：{chapter_id}")

    if issues:
        print(f"项目检查发现 {len(issues)} 个问题：")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("项目结构检查通过：必需文件、CSV 字段、稳定 ID 与双语骨架均有效。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
