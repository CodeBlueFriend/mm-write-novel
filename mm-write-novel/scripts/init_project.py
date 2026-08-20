#!/usr/bin/env python3
"""Create a novel project with canonical ledgers and manuscript directories."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

MODE_LABELS = {"short": "短篇", "novella": "中篇", "long": "长篇", "serial": "超长连载"}

FILES = {
    "00-project-brief.md": "project-brief-template.md",
    "01-market-brief.md": "market-brief-template.md",
    "02-author-intent.md": "author-intent-template.md",
    "03-story-bible.md": "story-bible-template.md",
    "04-character-bible.md": "character-template.md",
    "05-world-bible.md": "world-bible-template.md",
    "07-volume-arcs.md": "volume-arc-template.md",
    "08-chapter-matrix.csv": "chapter-matrix-template.csv",
    "continuity/timeline.csv": "timeline-template.csv",
    "continuity/character-state.csv": "character-state-template.csv",
    "continuity/knowledge-state.csv": "knowledge-state-template.csv",
    "continuity/relationship-ledger.csv": "relationship-ledger-template.csv",
    "continuity/location-ledger.csv": "location-ledger-template.csv",
    "continuity/props-resources.csv": "props-resources-template.csv",
    "continuity/plot-thread-ledger.csv": "plot-thread-ledger-template.csv",
    "continuity/foreshadowing-ledger.csv": "foreshadowing-ledger-template.csv",
    "continuity/reader-question-ledger.csv": "reader-question-ledger-template.csv",
    "continuity/bilingual-sync-ledger.csv": "bilingual-sync-ledger-template.csv",
}

SIMPLE_FILES = {
    "06-series-architecture.md": "# 总体结构\n\n待完成审核门 C。\n",
    "continuity/canon.yaml": "project:\n  title: \"{{TITLE}}\"\n  canon_version: 0\nlocked_facts: []\ncharacters: []\nworld_rules: []\ncore_secrets: []\n",
    "summaries/chapter-summaries.md": "# 章节摘要\n",
    "summaries/volume-summaries.md": "# 分卷摘要\n",
    "research/sources.md": "# 研究来源\n\n| ID | 主题 | 状态 | 来源 | 访问日期 | 适用位置 | 备注 |\n|---|---|---|---|---|---|---|\n",
    "research/fact-check.md": "# 事实核验\n\n状态使用 verified / inferred / fictionalized / pending。\n",
    "locked-decisions.md": "# 锁定决策\n\n记录 L0/L1 决策、确认人和日期。\n",
    "change-log.md": "# 变更日志\n\n重大变更记录事实、影响范围、处理和批准状态。\n",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="要创建的项目目录")
    parser.add_argument("--title", default="未命名小说")
    parser.add_argument("--mode", choices=MODE_LABELS, default="long")
    parser.add_argument("--language", choices=["zh-CN", "en", "bilingual"], default="zh-CN")
    parser.add_argument("--force", action="store_true", help="允许已存在目录；仍不覆盖文件")
    args = parser.parse_args()

    target = Path(args.project).expanduser().resolve()
    if target.exists() and any(target.iterdir()) and not args.force:
        print(f"错误：目标目录非空：{target}；如需补齐缺失文件请加 --force", file=sys.stderr)
        return 2
    target.mkdir(parents=True, exist_ok=True)
    assets = Path(__file__).resolve().parent.parent / "assets"
    created: list[Path] = []

    replacements = {"{{TITLE}}": args.title, "{{MODE}}": MODE_LABELS[args.mode], "{{LANGUAGE}}": args.language}
    for relative, template in FILES.items():
        output = target / relative
        if output.exists():
            continue
        text = (assets / template).read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        created.append(output)

    for relative, text in SIMPLE_FILES.items():
        output = target / relative
        if output.exists():
            continue
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text.replace("{{TITLE}}", args.title), encoding="utf-8")
        created.append(output)

    for directory in ["reviews", "context-packs", "bilingual/consistency-reports"]:
        (target / directory).mkdir(parents=True, exist_ok=True)
    if args.language == "bilingual":
        for directory in ["manuscript-zh", "manuscript-en"]:
            (target / directory).mkdir(exist_ok=True)
        map_path = target / "bilingual/chapter-map.csv"
        if not map_path.exists():
            shutil.copyfile(assets / "bilingual-chapter-map-template.csv", map_path)
            created.append(map_path)
        for relative, heading in [("bilingual/adaptation-differences.csv", "chapter_id,scene_id,difference_type,summary,approval_status\n"), ("bilingual/localization-decisions.md", "# 本地化决定\n")]:
            path = target / relative
            if not path.exists():
                path.write_text(heading, encoding="utf-8")
                created.append(path)
    else:
        (target / "manuscript").mkdir(exist_ok=True)

    print(f"已创建/补齐项目：{target}")
    print(f"新增文件：{len(created)}；语言模式：{args.language}；篇幅模式：{MODE_LABELS[args.mode]}")
    print("下一步：完成 00-project-brief.md，并确认审核门 A；不要直接开始长篇正文。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
