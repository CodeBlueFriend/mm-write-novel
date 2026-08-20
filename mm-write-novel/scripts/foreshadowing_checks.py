#!/usr/bin/env python3
"""Check foreshadowing lifecycle, payoff windows, and fairness evidence."""

from __future__ import annotations

import argparse
import sys

from _common import chapter_number, project_path, read_csv

VALID = {"planned", "seeded", "active", "reinforced", "paid-off", "open-approved", "计划", "已埋", "已推进", "已回收", "有意开放"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--current-chapter", help="例如 CH030；缺省从章节矩阵推断")
    args = parser.parse_args()
    try:
        project = project_path(args.project)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 2
    path = project / "continuity/foreshadowing-ledger.csv"
    if not path.exists():
        print(f"缺少伏笔账本：{path}", file=sys.stderr)
        return 2
    _, rows = read_csv(path)
    current = chapter_number(args.current_chapter or "") or 0
    matrix = project / "08-chapter-matrix.csv"
    if not current and matrix.exists():
        _, chapter_rows = read_csv(matrix)
        current = max([chapter_number(row.get("chapter_id", "")) or 0 for row in chapter_rows] or [0])
    issues: list[str] = []
    for line, row in enumerate(rows, 2):
        item = row.get("foreshadow_id", "").strip() or f"第{line}行"
        status = row.get("status", "").strip()
        if status and status not in VALID:
            issues.append(f"MINOR {item} 使用未知状态：{status}")
        if status in {"paid-off", "已回收"}:
            if not row.get("actual_payoff", "").strip():
                issues.append(f"MAJOR {item} 标记已回收但缺少 actual_payoff")
            if not row.get("fairness_evidence", "").strip():
                issues.append(f"MAJOR {item} 已回收但缺少 fairness_evidence")
        if status not in {"paid-off", "open-approved", "已回收", "有意开放"}:
            window = row.get("payoff_window", "")
            numbers = [chapter_number(part) for part in window.replace("—", "-").split("-")]
            end = max([number for number in numbers if number is not None] or [0])
            if current and end and current > end:
                issues.append(f"MAJOR {item} 已超过回收窗口 {window}（当前 CH{current:03d}）")
    if issues:
        print(f"伏笔检查发现 {len(issues)} 个问题：")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"伏笔结构检查通过：{len(rows)} 条记录；当前章节 CH{current:03d}。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
