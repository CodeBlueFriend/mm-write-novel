#!/usr/bin/env python3
"""Run deterministic cross-ledger continuity checks."""

from __future__ import annotations

import argparse
import sys

from _common import canonical_chapter_ids, project_path, read_csv


def rows(project, filename):
    path = project / "continuity" / filename
    return read_csv(path)[1] if path.exists() else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    args = parser.parse_args()
    try:
        project = project_path(args.project)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 2
    known = canonical_chapter_ids(project)
    issues: list[str] = []
    references = {
        "timeline.csv": ["source_chapter"],
        "character-state.csv": ["as_of_chapter"],
        "knowledge-state.csv": ["learned_at"],
        "relationship-ledger.csv": ["as_of_chapter"],
        "props-resources.csv": ["acquired_at", "last_seen"],
        "plot-thread-ledger.csv": ["opened_at", "last_advanced", "planned_resolution", "actual_resolution"],
    }
    for filename, fields in references.items():
        for line, row in enumerate(rows(project, filename), 2):
            for field in fields:
                value = row.get(field, "").strip().upper()
                if value.startswith("CH") and known and value not in known:
                    issues.append(f"MAJOR {filename}:{line} {field} 引用未知章节 {value}")

    ownership: dict[str, tuple[str, str, str]] = {}
    for line, row in enumerate(rows(project, "props-resources.csv"), 2):
        item = row.get("item_id", "").strip()
        state = (row.get("owner", "").strip(), row.get("location", "").strip(), row.get("last_seen", "").strip())
        if item and item in ownership and state != ownership[item]:
            issues.append(f"BLOCKER props-resources.csv:{line} 同一 item_id 同时存在冲突状态：{item}")
        ownership[item] = state

    learned: set[tuple[str, str]] = set()
    for line, row in enumerate(rows(project, "knowledge-state.csv"), 2):
        key = (row.get("character_id", "").strip(), row.get("fact_id", "").strip())
        if all(key) and key in learned:
            issues.append(f"MAJOR knowledge-state.csv:{line} 重复人物/事实记录：{' / '.join(key)}")
        learned.add(key)

    if issues:
        print(f"连续性检查发现 {len(issues)} 个问题：")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("连续性结构检查通过：章节引用、物件状态和认知记录未发现可检测冲突。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
