#!/usr/bin/env python3
"""Shared helpers for mm-write-novel scripts (standard library only)."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Iterable

CHAPTER_RE = re.compile(r"CH(\d+)", re.IGNORECASE)

LEDGER_HEADERS = {
    "timeline.csv": ["event_id", "date", "time", "duration", "location", "participants", "event", "causes", "results", "source_chapter", "status"],
    "character-state.csv": ["character_id", "as_of_chapter", "physical_state", "emotional_state", "identity", "status_goal", "resources", "location", "notes"],
    "knowledge-state.csv": ["character_id", "fact_id", "knowledge_state", "learned_at", "source", "reliability", "notes"],
    "relationship-ledger.csv": ["relationship_id", "party_a", "party_b", "as_of_chapter", "stage", "trust", "debt", "conflict", "address_terms", "change_reason"],
    "location-ledger.csv": ["location_id", "name", "description", "distance_from", "travel_time", "access_rules", "first_seen", "last_confirmed"],
    "props-resources.csv": ["item_id", "name", "owner", "location", "quantity", "state", "acquired_at", "last_seen", "rule_or_cost", "notes"],
    "plot-thread-ledger.csv": ["thread_id", "type", "promise", "status", "opened_at", "last_advanced", "planned_resolution", "actual_resolution", "dependencies", "notes"],
    "foreshadowing-ledger.csv": ["foreshadow_id", "promise", "seed_location", "visibility", "reader_knows", "characters_know", "reinforcement", "payoff_window", "payoff", "fairness_evidence", "status", "actual_payoff"],
    "reader-question-ledger.csv": ["question_id", "question", "horizon", "opened_at", "priority", "answer_window", "status", "answered_at", "notes"],
    "bilingual-sync-ledger.csv": ["chapter_id", "scene_id", "zh_status", "en_status", "shared_facts_consistent", "event_order_consistent", "knowledge_consistent", "foreshadowing_consistent", "difference_type", "approval_status", "notes"],
}

CHAPTER_MATRIX_HEADER = ["chapter_id", "title", "volume_id", "arc_id", "pov", "time", "location", "entry_state", "desire", "obstacle", "action_counteraction", "turn", "exit_state", "reader_info", "character_info", "emotion_shift", "foreshadowing_action", "reading_drive", "status"]
BILINGUAL_MAP_HEADER = ["chapter_id", "scene_id", "zh_file", "en_file", "shared_event_hash", "difference_type", "difference_summary", "approval_status", "checked_at"]


def project_path(raw: str) -> Path:
    path = Path(raw).expanduser().resolve()
    if not path.is_dir():
        raise FileNotFoundError(f"项目目录不存在：{path}")
    return path


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, header: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def chapter_number(value: str) -> int | None:
    match = CHAPTER_RE.search(value or "")
    return int(match.group(1)) if match else None


def manuscript_dirs(project: Path) -> list[Path]:
    candidates = [project / "manuscript", project / "manuscript-zh", project / "manuscript-en"]
    return [path for path in candidates if path.is_dir()]


def chapter_files(project: Path) -> list[Path]:
    files: list[Path] = []
    for directory in manuscript_dirs(project):
        files.extend(path for path in directory.rglob("CH*.md") if path.is_file())
    return sorted(files, key=lambda p: (p.parent.name, chapter_number(p.name) or 0, p.name))


def extract_control(text: str, field: str) -> str:
    match = re.search(rf"^-\s*{re.escape(field)}[：:]\s*(.*)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def body_text(text: str) -> str:
    body = text.split("## 正文", 1)[-1]
    body = body.split("## 连续性更新", 1)[0]
    return body.strip()


def canonical_chapter_ids(project: Path) -> set[str]:
    result: set[str] = set()
    matrix = project / "08-chapter-matrix.csv"
    if matrix.exists():
        _, rows = read_csv(matrix)
        result.update(row.get("chapter_id", "").strip().upper() for row in rows if row.get("chapter_id", "").strip())
    result.update(path.stem.upper() for path in chapter_files(project))
    return result
