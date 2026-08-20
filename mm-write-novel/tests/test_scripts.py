from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


class ScriptTests(unittest.TestCase):
    def run_script(self, name: str, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run([sys.executable, str(SCRIPTS / name), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_single_language_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "novel"
            self.run_script("init_project.py", str(project), "--title", "测试小说", "--mode", "short")
            self.run_script("validate_project.py", str(project))
            self.run_script("continuity_checks.py", str(project))
            self.run_script("foreshadowing_checks.py", str(project))
            self.run_script("index_manuscript.py", str(project))
            self.run_script("build_context_pack.py", str(project), "--chapters", "CH001")
            self.assertTrue((project / "context-packs/context-CH001.md").exists())

    def test_bilingual_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "bilingual"
            self.run_script("init_project.py", str(project), "--language", "bilingual")
            self.run_script("validate_project.py", str(project))
            self.assertTrue((project / "manuscript-zh").is_dir())
            self.assertTrue((project / "manuscript-en").is_dir())
            self.assertTrue((project / "bilingual/chapter-map.csv").exists())

    def test_chapter_index_and_stats(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "novel"
            self.run_script("init_project.py", str(project))
            chapter = project / "manuscript/CH001.md"
            chapter.write_text(
                "# 第 001 章《潮声》\n\n## 章节控制信息\n\n- POV：林汐\n- 时间：2026-08-20 06:00\n- 地点：旧水闸\n\n## 正文\n\n潮水越过警戒线。 The tide was early.\n\n## 连续性更新\n\n- 新增事实：潮位异常。\n",
                encoding="utf-8",
            )
            self.run_script("index_manuscript.py", str(project))
            result = self.run_script("manuscript_stats.py", str(project))
            self.run_script("compile_manuscript.py", str(project))
            index = (project / "summaries/manuscript-index.csv").read_text(encoding="utf-8")
            compiled = (project / "exports/manuscript.md").read_text(encoding="utf-8")
            self.assertIn("CH001", index)
            self.assertIn("林汐", index)
            self.assertIn("manuscript,1", result.stdout)
            self.assertNotIn("\r", index)
            self.assertIn("潮水越过警戒线", compiled)
            self.assertNotIn("章节控制信息", compiled)

    def test_overdue_foreshadowing_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "novel"
            self.run_script("init_project.py", str(project))
            ledger = project / "continuity/foreshadowing-ledger.csv"
            with ledger.open("a", encoding="utf-8") as handle:
                handle.write("F-001,门后的声音,CH001,半明示,听见声音,无人知情,,CH002-CH003,揭示录音来源,,active,\n")
            result = self.run_script("foreshadowing_checks.py", str(project), "--current-chapter", "CH004", expected=1)
            self.assertIn("超过回收窗口", result.stdout)

    def test_repeated_character_with_distinct_facts_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "novel"
            self.run_script("init_project.py", str(project))
            ledger = project / "continuity/knowledge-state.csv"
            with ledger.open("a", encoding="utf-8") as handle:
                handle.write("C-001,F-001,known,CH001,目击,高,\n")
                handle.write("C-001,F-002,unknown,CH001,,高,\n")
            self.run_script("validate_project.py", str(project))

    def test_short_chapter_matrix_row_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "novel"
            self.run_script("init_project.py", str(project))
            matrix = project / "08-chapter-matrix.csv"
            with matrix.open("a", encoding="utf-8") as handle:
                handle.write("CH001,缺列\n")
            result = self.run_script("validate_project.py", str(project), expected=1)
            self.assertIn("缺少列", result.stdout)

    def test_initializer_refuses_nonempty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "keep.txt").write_text("keep", encoding="utf-8")
            self.run_script("init_project.py", str(project), expected=2)
            self.assertEqual((project / "keep.txt").read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
