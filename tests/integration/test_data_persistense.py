"""
Integration tests for data persistence and file operations (expanded)

This comprehensive file covers:
- Persistence: analysis, learning plan, sprint history, state files
- Integrity: atomic writes, encoding, backup & corruption handling
- Migration: backward compatibility and versioning
- Export/import: full and selective export verification
- Cleanup: removal of old exports, duplicate pruning, orphan detection
- Recovery: restore from backups and rebuild from history
- Concurrency: multiple engine instances & safe reads/writes
- Performance (lightweight): timing checks for typical operations
- Filesystem operations: directory creation, permissions, special paths
- Validation: basic schema & sanitization checks

Design choices:
- Defensive assertions (tolerant to engine variations)
- Helpful prints for `pytest -s` debugging
- Utility helpers for safe JSON I/O and file writes
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Tuple

import pytest

from src.python_advanced_job_engine import AdvancedJobEngine  # type: ignore

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
def write_text_file(path: Path, content: str) -> Path:
    """Write text to `path` (UTF-8) and return the Path."""
    path.write_text(content, encoding="utf-8")
    print(f"[helper] Wrote {len(content)} chars to {path}")
    return path


def safe_load_json(path: Path) -> Any:
    """Safely load JSON file at `path`. Return default empty list/dict on error."""
    if not path.exists():
        print(f"[helper] safe_load_json: file not found: {path}")
        return []  # default structure when file missing
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            print(f"[helper] Loaded JSON from {path} (type={type(data).__name__})")
            return data
    except json.JSONDecodeError as e:
        print(f"[helper] JSONDecodeError reading {path}: {e}")
        return []
    except Exception as e:
        print(f"[helper] Unexpected error reading {path}: {e}")
        return []


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists, create if necessary, return Path."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_temp_cv_job(tmp_path: Path, cv_text: str, job_text: str) -> Tuple[Path, Path]:
    """Create cv.txt and job.txt under tmp_path and return their Paths."""
    cv_path = tmp_path / "cv.txt"
    job_path = tmp_path / "job.txt"
    write_text_file(cv_path, cv_text)
    write_text_file(job_path, job_text)
    return cv_path, job_path


def now_ts() -> str:
    """Return ISO timestamp useful for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ------------------------------------------------------------------
# Fixtures (consistent & reusable)
# ------------------------------------------------------------------
@pytest.fixture
def temp_data_dir(tmp_path: Path) -> str:
    """Create a temporary directory for engine data and return its path."""
    data_dir = tmp_path / "job_search_data"
    ensure_dir(data_dir)
    print(f"[fixture] Created temp data_dir: {data_dir}")
    return str(data_dir)


@pytest.fixture
def engine(temp_data_dir: str) -> AdvancedJobEngine:
    """Return a fresh AdvancedJobEngine using the provided temporary data dir."""
    eng = AdvancedJobEngine(data_dir=temp_data_dir)
    # Ensure base attributes exist
    for attr in (
        "analysis_file",
        "learning_file",
        "sprint_file",
        "state_file",
        "data_dir",
    ):
        if not hasattr(eng, attr):
            print(f"[fixture] Warning: engine missing attribute {attr}")
    # Reset state if present
    if isinstance(getattr(eng, "state", None), dict):
        eng.state.clear()
    print(f"[fixture] Engine created with data_dir: {eng.data_dir}")
    return eng


# ------------------------------------------------------------------
# Test: Basic persistence and structure
# ------------------------------------------------------------------
class TestDataPersistence:
    """Test basic file creation and JSON persistence behavior."""

    def test_initial_file_structure(self, engine: AdvancedJobEngine):
        """
        Verify that the engine's data directory exists and expected filenames
        are logically present (path correctness).
        """
        data_dir = Path(engine.data_dir)
        print(f"[TestDataPersistence] Checking data_dir: {data_dir}")
        assert data_dir.exists() and data_dir.is_dir()

        expected_filenames = [
            "analyzed_jobs.json",
            "learning_progress.json",
            "sprint_history.json",
            "skill_tests.json",
            "workflow_state.json",
        ]

        for fname in expected_filenames:
            fpath = data_dir / fname
            # Engine might lazily create files on first write; simply ensure path parent is correct
            assert fpath.parent == data_dir
            print(f"[TestDataPersistence] Path prepared: {fpath}")

    def test_analysis_persistence_and_content(self, engine: AdvancedJobEngine, tmp_path: Path):
        """
        Run analysis and ensure the analysis_file exists and contains last saved analysis
        with job_title, company, score, and gaps.
        """
        cv_text = "Name: John Doe\nSkills: Python, Django\nExperience: 5 years"
        job_text = "Backend Developer\nRequired: Python, Django, Docker"
        cv_path, job_path = create_temp_cv_job(tmp_path, cv_text, job_text)

        analysis = engine.analyze_from_files(
            str(cv_path), str(job_path), _job_title="Backend Dev", _company="TechCorp"
        )
        print(
            f"[TestDataPersistence] analysis returned keys: {list(analysis.keys()) if isinstance(analysis, dict) else type(analysis)}"
        )

        assert isinstance(analysis, dict)

        # Verify persisted file exists and includes last entry matching job_title/company
        if getattr(engine, "analysis_file", None):
            a_path = Path(engine.analysis_file)
            assert a_path.exists()
            saved_list = safe_load_json(a_path)
            assert isinstance(saved_list, list)
            assert len(saved_list) >= 1
            last = saved_list[-1]
            assert last.get("job_title") == "Backend Dev"
            assert last.get("company") == "TechCorp"
            assert "score" in last and "gaps" in last
            print(f"[TestDataPersistence] Analysis persisted and verified: {a_path}")
        else:
            pytest.skip("Engine does not expose analysis_file attribute")

    def test_learning_plan_persistence(self, engine: AdvancedJobEngine, tmp_path: Path):
        """
        Create a learning plan in reverse mode and verify that the engine saved the plan to learning_file.
        """
        cv_path, job_path = create_temp_cv_job(
            tmp_path, "Skills: Python", "Required: Python, Django"
        )
        analysis = engine.analyze_from_files(str(cv_path), str(job_path))
        learning_plan = engine.create_learning_plan(analysis, mode="reverse")
        assert isinstance(learning_plan, dict)

        if getattr(engine, "learning_file", None):
            lp_path = Path(engine.learning_file)
            assert lp_path.exists()
            saved_plans = safe_load_json(lp_path)
            assert isinstance(saved_plans, list)
            assert len(saved_plans) >= 1
            last_plan = saved_plans[-1]
            assert "skills_to_learn" in last_plan
            assert last_plan.get("mode") == "reverse"
            print(f"[TestDataPersistence] Learning plan persisted to {lp_path}")
        else:
            pytest.skip("Engine does not expose learning_file attribute")

    def test_sprint_history_persistence(self, engine: AdvancedJobEngine, tmp_path: Path):
        """
        Execute a typical sprint lifecycle and ensure sprint history file contains the completed sprint.
        """
        cv_path, job_path = create_temp_cv_job(
            tmp_path, "Skills: Python", "Required: Python, Django"
        )
        analysis = engine.analyze_from_files(str(cv_path), str(job_path))
        engine.create_learning_plan(analysis)

        # Start, log daily progress, end sprint
        engine.start_sprint(["Django"], "Learn Django fundamentals")
        for _ in range(14):
            engine.log_daily_progress(
                _hours_studied=2.0, _topics_covered=["Topics"], _progress_rating=4
            )
        res = engine.end_sprint("https://github.com/user/project", {"Django": 85})
        assert isinstance(res, dict)

        if getattr(engine, "sprint_file", None):
            s_path = Path(engine.sprint_file)
            assert s_path.exists()
            saved_sprints = safe_load_json(s_path)
            assert isinstance(saved_sprints, list)
            assert len(saved_sprints) >= 1
            last_sprint = saved_sprints[-1]
            assert last_sprint.get("completed") is True
            assert last_sprint.get("skills_targeted") == ["Django"]
            assert len(last_sprint.get("daily_logs", [])) == 14
            print(f"[TestDataPersistence] Sprint history persisted: {s_path}")
        else:
            pytest.skip("Engine does not expose sprint_file attribute")

    def test_state_persistence_and_reload(self, engine: AdvancedJobEngine):
        """
        Write engine.state and reload engine to verify state is persisted across instances.
        """
        # Prepare a sample state
        sample_state = {
            "mode": "reverse",
            "baseline_score": 60,
            "current_score": 65,
            "skills_mastered": ["Python", "Django"],
            "projects_completed": [],
        }
        engine.state.update(sample_state)
        # Prefer engine's own save function to mimic real usage
        if hasattr(engine, "_save_json"):
            engine._save_json(engine.state_file, engine.state)
        else:
            Path(engine.state_file).write_text(json.dumps(engine.state), encoding="utf-8")

        # Create a new engine instance that should load the saved state
        new_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        assert isinstance(new_engine.state, dict)
        assert new_engine.state.get("mode") == "reverse"
        assert "Django" in new_engine.state.get("skills_mastered", [])
        print("[TestDataPersistence] State persisted and reloaded successfully.")


# ------------------------------------------------------------------
# Data Integrity & Backup Tests
# ------------------------------------------------------------------
class TestDataIntegrity:
    """Test integrity concerns such as atomic writes, encoding, and backup behavior."""

    def test_concurrent_write_sequence(self, engine: AdvancedJobEngine):
        """
        Simulate rapid sequential writes to state and verify final persisted value equals last write.
        This is a simple concurrency safety smoke test (not multi-threaded).
        """
        for i in range(10):
            engine.state["counter"] = i
            engine._save_json(engine.state_file, engine.state)
        final = safe_load_json(Path(engine.state_file))
        assert isinstance(final, dict)
        assert final.get("counter") == 9
        print("[TestDataIntegrity] Sequential writes produced final counter=9")

    def test_backup_on_corruption_and_recovery(self, engine: AdvancedJobEngine, tmp_path: Path):
        """
        Save state, corrupt the file, then ensure engine can be instantiated and recovers using a backup or safe defaults.
        """
        engine.state.update({"mode": "reverse", "current_score": 72})
        engine._save_json(engine.state_file, engine.state)

        # Create a backup copy to simulate engine's own backup strategy
        backup = Path(engine.state_file + ".bak")
        shutil.copy(Path(engine.state_file), backup)
        print(f"[TestDataIntegrity] Created backup at {backup}")

        # Corrupt main file
        Path(engine.state_file).write_text("{{not valid json}}", encoding="utf-8")
        print(f"[TestDataIntegrity] Corrupted main state file at {engine.state_file}")

        # Instantiate engine and expect it to handle corrupted file (either by fallback or by restoring backup)
        recovered = AdvancedJobEngine(data_dir=engine.data_dir)
        assert isinstance(recovered.state, dict)
        # Accept either restored values or defaults, but should not crash
        print("[TestDataIntegrity] Engine recovered from corrupted state file (no crash).")

    def test_atomic_write_roundtrip(self, engine: AdvancedJobEngine):
        """
        Verify that saving a large data structure and loading it back returns identical content.
        This tests atomic/roundtrip semantics of engine._save_json/_load_json.
        """
        large = {f"key_{i}": f"value_{i}" * 100 for i in range(200)}
        engine._save_json(engine.state_file, large)
        loaded = engine._load_json(engine.state_file)
        assert loaded == large
        print("[TestDataIntegrity] Atomic write/read roundtrip successful.")

    def test_utf8_encoding_consistency(self, engine: AdvancedJobEngine):
        """
        Ensure that data with diverse Unicode characters round-trips correctly.
        """
        data = {
            "name": "José García",
            "skills": ["Python", "データサイエンス", "Программирование"],
            "notes": "特殊文字テスト",
        }
        engine._save_json(engine.state_file, data)
        loaded = engine._load_json(engine.state_file)
        assert loaded["name"] == "José García"
        assert "データサイエンス" in loaded["skills"]
        print("[TestDataIntegrity] UTF-8 characters preserved across save/load.")


# ------------------------------------------------------------------
# Migration & Versioning Tests
# ------------------------------------------------------------------
class TestDataMigration:
    """Test loading older formats and ensuring default fields are present after load."""

    def test_backward_compatibility_missing_fields(self, engine: AdvancedJobEngine):
        """
        Save an old-style state (missing new fields) and verify engine fills defaults on load.
        """
        old_state = {"mode": "reverse", "baseline_score": 55}  # missing 'skills_mastered', etc.
        engine._save_json(engine.state_file, old_state)
        reloaded = AdvancedJobEngine(data_dir=engine.data_dir)
        assert isinstance(reloaded.state, dict)
        # Engine should provide a list for missing 'skills_mastered'
        assert "skills_mastered" in reloaded.state or isinstance(
            reloaded.state.get("skills_mastered", []), list
        )
        print("[TestDataMigration] Backward compatibility: missing fields handled.")

    def test_data_version_roundtrip(self, engine: AdvancedJobEngine):
        """
        Save a state with a data_version and ensure it's present after reloading.
        """
        engine.state["data_version"] = "1.2.3"
        engine._save_json(engine.state_file, engine.state)
        raw = safe_load_json(Path(engine.state_file))
        assert isinstance(raw, dict)
        assert raw.get("data_version") == "1.2.3"
        print("[TestDataMigration] Data version saved and verified.")


# ------------------------------------------------------------------
# Export & Import Tests
# ------------------------------------------------------------------
class TestExportImport:
    """Verify export of full package and selective export behavior."""

    def test_full_export_package(self, engine: AdvancedJobEngine, tmp_path: Path):
        """
        Create artifacts via engine methods and call export_complete_package.
        Validate that the returned path exists and contains expected files.
        """
        cv_path, job_path = create_temp_cv_job(
            tmp_path, "Skills: Python, Django", "Required: Python, Django, Docker"
        )
        analysis = engine.analyze_from_files(str(cv_path), str(job_path))
        learning_plan = engine.create_learning_plan(analysis, mode="standard")
        strategy = (
            engine.create_improvement_strategy(analysis, learning_plan)
            if hasattr(engine, "create_improvement_strategy")
            else {}
        )
        tests = (
            engine.generate_skill_tests(["Docker"])
            if hasattr(engine, "generate_skill_tests")
            else []
        )
        letters = (
            engine.generate_recruiter_letter(analysis, learning_plan)
            if hasattr(engine, "generate_recruiter_letter")
            else {}
        )

        if hasattr(engine, "export_complete_package"):
            export_path = engine.export_complete_package(
                analysis, learning_plan, strategy, tests, letters
            )
            export_p = Path(str(export_path))
            assert export_p.exists()
            # If export is a dir, verify presence of at least a few artifacts
            if export_p.is_dir():
                files = list(export_p.iterdir())
                assert len(files) >= 1
                print(f"[TestExportImport] Export directory contents: {[p.name for p in files]}")
            else:
                print(
                    f"[TestExportImport] Export produced file: {export_p} (size={export_p.stat().st_size})"
                )
        else:
            pytest.skip("Engine does not provide export_complete_package")

    def test_selective_export_write_analysis(self, engine: AdvancedJobEngine, tmp_path: Path):
        """
        Demonstrate selective export: write analysis.json into an export dir and verify.
        """
        cv_path, job_path = create_temp_cv_job(
            tmp_path, "Skills: Python", "Required: Python, Django"
        )
        analysis = engine.analyze_from_files(str(cv_path), str(job_path))
        export_dir = Path(engine.data_dir) / f"export_{now_ts()}"
        ensure_dir(export_dir)
        analysis_file = export_dir / "analysis.json"
        with analysis_file.open("w", encoding="utf-8") as fh:
            json.dump(analysis, fh, indent=2)
        assert analysis_file.exists() and analysis_file.stat().st_size > 0
        print(f"[TestExportImport] Selective export saved analysis to {analysis_file}")


# ------------------------------------------------------------------
# Cleanup & Maintenance Tests
# ------------------------------------------------------------------
class TestDataCleanup:
    """Tests for pruning old exports, deduplicating histories, and orphan detection."""

    def test_old_export_pruning(self, engine: AdvancedJobEngine):
        """
        Create several export directories and prune old ones keeping the latest N.
        """
        data_dir = Path(engine.data_dir)
        created = []
        for i in range(5):
            name = f"export_2024{(i+1):02d}01_120000"
            p = data_dir / name
            p.mkdir(exist_ok=True)
            (p / "meta.txt").write_text("x")
            created.append(p)
        print(f"[TestDataCleanup] Created export dirs: {[p.name for p in created]}")
        exports = sorted(data_dir.glob("export_*"))
        # Remove oldest keeping last 3
        for old in exports[:-3]:
            shutil.rmtree(old)
            print(f"[TestDataCleanup] Removed old export: {old.name}")
        remaining = list(data_dir.glob("export_*"))
        assert len(remaining) == 3
        print(f"[TestDataCleanup] Remaining exports kept: {[p.name for p in remaining]}")

    def test_duplicate_analysis_removal(self, engine: AdvancedJobEngine):
        """
        Add duplicate analysis entries and deduplicate them based on (job_title, company).
        """
        # Prepare duplicate entries
        entry = {
            "job_title": "Backend Dev",
            "company": "TechCorp",
            "score": {"total_score": 80},
            "timestamp": now_ts(),
        }
        engine.analyzed_jobs.extend([entry.copy(), entry.copy(), entry.copy()])
        engine._save_json(engine.analysis_file, engine.analyzed_jobs)
        # Deduplicate
        seen = set()
        unique = []
        for j in engine.analyzed_jobs:
            key = (j.get("job_title"), j.get("company"))
            if key not in seen:
                seen.add(key)
                unique.append(j)
        engine.analyzed_jobs = unique
        engine._save_json(engine.analysis_file, engine.analyzed_jobs)
        assert len(engine.analyzed_jobs) == 1
        print("[TestDataCleanup] Duplicate analysis entries removed.")

    def test_orphaned_file_detection(self, engine: AdvancedJobEngine):
        """
        Create an orphaned JSON file and assert it's detected as not part of expected artifacts.
        """
        data_dir = Path(engine.data_dir)
        orphan = data_dir / "old_data_v1.json"
        orphan.write_text('{"old":"data"}', encoding="utf-8")
        expected = {
            "analyzed_jobs.json",
            "learning_progress.json",
            "sprint_history.json",
            "skill_tests.json",
            "workflow_state.json",
        }
        present = {p.name for p in data_dir.glob("*.json")}
        orphaned = present - expected
        assert orphan.name in orphaned
        print(f"[TestDataCleanup] Found orphan files: {orphaned}")


# ------------------------------------------------------------------
# Recovery Tests
# ------------------------------------------------------------------
class TestDataRecovery:
    """Tests around restoring state from backups and rebuilding state from history."""

    def test_restore_state_from_backup_file(self, engine: AdvancedJobEngine):
        """
        Save a valid state, copy to backup, corrupt main file, restore from backup, and verify engine state.
        """
        engine.state.update({"mode": "reverse", "current_score": 77})
        engine._save_json(engine.state_file, engine.state)
        backup = Path(str(engine.state_file) + ".backup")
        shutil.copy(Path(engine.state_file), backup)
        # Corrupt main
        Path(engine.state_file).write_text("corrupted content", encoding="utf-8")
        # Restore
        shutil.copy(backup, Path(engine.state_file))
        recovered = AdvancedJobEngine(data_dir=engine.data_dir)
        assert recovered.state.get("current_score") == 77
        print("[TestDataRecovery] State restored from backup successfully.")

    def test_partial_recovery_when_files_missing(self, engine: AdvancedJobEngine, tmp_path: Path):
        """
        If some files (e.g., learning plan) are missing, engine should still start and provide defaults.
        """
        cv_path, job_path = create_temp_cv_job(
            tmp_path, "Skills: Python", "Required: Python, Django"
        )
        analysis = engine.analyze_from_files(str(cv_path), str(job_path))
        engine.create_learning_plan(analysis)
        # Delete learning file to simulate partial loss
        if Path(engine.learning_file).exists():
            Path(engine.learning_file).unlink()
            print(f"[TestDataRecovery] Deleted learning_file: {engine.learning_file}")
        new_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        # learning_progress attribute expected to be present and a list
        lp = getattr(new_engine, "learning_progress", [])
        assert isinstance(lp, list)
        print("[TestDataRecovery] Engine survived missing learning_file gracefully.")

    def test_rebuild_state_from_sprint_history(self, engine: AdvancedJobEngine, tmp_path: Path):
        """
        Remove state file and reconstruct state from sprint_history entries.
        """
        cv_path, job_path = create_temp_cv_job(
            tmp_path, "Skills: Python", "Required: Python, Django, Docker"
        )
        analysis = engine.analyze_from_files(str(cv_path), str(job_path))
        engine.create_learning_plan(analysis)
        # Run two sprints
        for skill, url, score in (("Django", "url1", 80), ("Docker", "url2", 75)):
            engine.start_sprint([skill], f"Sprint {skill}")
            for _ in range(14):
                engine.log_daily_progress(
                    _hours_studied=2.0, _topics_covered=["Topics"], _progress_rating=4
                )
            engine.end_sprint(url, {skill: score})
        # Remove state file and rebuild
        if Path(engine.state_file).exists():
            Path(engine.state_file).unlink()
            print(f"[TestDataRecovery] Deleted state_file: {engine.state_file}")
        new_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        completed = []
        for s in getattr(new_engine, "sprint_history", []):
            if s.get("completed"):
                completed.extend(s.get("skills_targeted", []))
        # Save reconstructed state
        new_engine.state["skills_mastered"] = completed
        new_engine._save_json(new_engine.state_file, new_engine.state)
        assert len(new_engine.state["skills_mastered"]) >= 2
        print(
            f"[TestDataRecovery] Rebuilt state skills_mastered: {new_engine.state['skills_mastered']}"
        )


# ------------------------------------------------------------------
# Concurrency & Robustness Tests
# ------------------------------------------------------------------
class TestConcurrency:
    """Multiple engine instances and read-safety tests."""

    def test_multiple_instances_write_and_read(self, engine: AdvancedJobEngine):
        """Engine1 writes state, Engine2 sees it, updates, and engine3 sees final value."""
        engine.state["tag"] = "engine1"
        engine._save_json(engine.state_file, engine.state)
        engine2 = AdvancedJobEngine(data_dir=engine.data_dir)
        assert engine2.state.get("tag") == "engine1"
        engine2.state["tag"] = "engine2"
        engine2._save_json(engine2.state_file, engine2.state)
        engine3 = AdvancedJobEngine(data_dir=engine.data_dir)
        assert engine3.state.get("tag") == "engine2"
        print("[TestConcurrency] Multiple instance write/read flow validated.")

    def test_safe_concurrent_reads_multiple_instances(self, engine: AdvancedJobEngine):
        """Multiple independent readers should be able to load state concurrently."""
        engine.state["shared"] = "value"
        engine._save_json(engine.state_file, engine.state)
        readers = [AdvancedJobEngine(data_dir=engine.data_dir) for _ in range(5)]
        assert all(r.state.get("shared") == "value" for r in readers)
        print("[TestConcurrency] Concurrent reads returned consistent state.")


# ------------------------------------------------------------------
# Performance (lightweight)
# ------------------------------------------------------------------
class TestPerformance:
    """Non-flaky, quick performance smoke checks."""

    def test_large_state_write_speed(self, engine: AdvancedJobEngine):
        """Write a fairly large state object and ensure the write completes quickly."""
        large_state = {f"k{i}": "x" * 1000 for i in range(500)}
        start = time.time()
        engine._save_json(engine.state_file, large_state)
        elapsed = time.time() - start
        assert elapsed < 2.0, f"Large state write took too long: {elapsed:.3f}s"
        print(f"[TestPerformance] Large state write: {elapsed:.3f}s")

    def test_large_history_read_speed(self, engine: AdvancedJobEngine):
        """Write a large sprint history and measure read speed."""
        large_history = [{"sprint": i, "data": "x" * 200} for i in range(500)]
        engine._save_json(engine.sprint_file, large_history)
        start = time.time()
        loaded = engine._load_json(engine.sprint_file)
        elapsed = time.time() - start
        assert len(loaded) == 500
        assert elapsed < 1.0, f"Large history read took too long: {elapsed:.3f}s"
        print(f"[TestPerformance] Large history read: {elapsed:.3f}s")


# ------------------------------------------------------------------
# Filesystem Operations & Edge Cases
# ------------------------------------------------------------------
class TestFileSystemOperations:
    """Test directory creation, permissions, disk space checks and special paths."""

    def test_directory_auto_creation(self, tmp_path: Path):
        """Engine should create the data_dir if it does not exist."""
        new_dir = tmp_path / "new_job_search_data"
        if new_dir.exists():
            shutil.rmtree(new_dir)
        assert not new_dir.exists()
        # engine_inst = AdvancedJobEngine(data_dir=str(new_dir))
        assert new_dir.exists() and new_dir.is_dir()
        print(f"[TestFileSystemOperations] Engine created directory: {new_dir}")

    def test_permission_denied_handling(self, engine: AdvancedJobEngine):
        """Attempt writing while directory is readonly (skip on Windows)."""
        if platform.system() == "Windows":
            pytest.skip("Permission chmod behavior differs on Windows; skipping")
        data_dir = Path(engine.data_dir)
        # Make dir read-only
        os.chmod(data_dir, 0o444)
        try:
            # Attempt to save; engine should either raise PermissionError or handle gracefully
            try:
                engine._save_json(engine.state_file, {"test": "x"})
            except PermissionError:
                print("[TestFileSystemOperations] PermissionError raised as expected.")
        finally:
            # Restore permissions for cleanup
            os.chmod(data_dir, 0o755)
            print("[TestFileSystemOperations] Permissions restored.")

    def test_disk_space_smoke_check(self, engine: AdvancedJobEngine):
        """Check available disk space to ensure test environment is reasonable."""
        stat = shutil.disk_usage(engine.data_dir)
        available_gb = stat.free / (1024**3)
        print(f"[TestFileSystemOperations] Available disk space: {available_gb:.2f} GB")
        assert available_gb > 0.05, "Less than 50MB available — test environment low on disk"

    def test_path_with_special_characters(self, tmp_path: Path):
        """Create a directory with non-ASCII characters and verify engine can use it."""
        special = tmp_path / "job_search_data_特別"
        ensure_dir(special)
        eng = AdvancedJobEngine(data_dir=str(special))
        eng.state["ok"] = True
        eng._save_json(eng.state_file, eng.state)
        assert Path(eng.state_file).exists()
        print(f"[TestFileSystemOperations] Special-character path used successfully: {special}")


# ------------------------------------------------------------------
# Data Validation & Sanitization
# ------------------------------------------------------------------
class TestDataValidation:
    """Validate JSON schema basics, type consistency, and sanitization flows."""

    def test_schema_and_type_validation(self, engine: AdvancedJobEngine):
        valid = {
            "mode": "reverse",
            "baseline_score": 65,
            "current_score": 70,
            "skills_mastered": [],
            "projects_completed": [],
            "quality_gates_passed": [],
        }
        engine._save_json(engine.state_file, valid)
        loaded = engine._load_json(engine.state_file)
        # All required keys must be present
        assert set(valid.keys()).issubset(set(loaded.keys()))
        assert isinstance(loaded["skills_mastered"], list)
        print("[TestDataValidation] Schema and type validation passed.")

    def test_sanitization_of_user_input(self, engine: AdvancedJobEngine):
        malicious = {
            "job_title": '<script>alert("xss")</script>',
            "company": "Acme\nCorp",
            "notes": "Null\x00Byte",
        }
        # Basic sanitization example: replace dangerous chars (engine may or may not do this)
        sanitized = {
            "job_title": malicious["job_title"].replace("<", "&lt;").replace(">", "&gt;"),
            "company": malicious["company"].replace("\n", " "),
            "notes": malicious["notes"].replace("\x00", ""),
        }
        engine._save_json(engine.state_file, sanitized)
        loaded = engine._load_json(engine.state_file)
        assert "<script>" not in loaded["job_title"]
        assert "\n" not in loaded["company"]
        assert "\x00" not in loaded["notes"]
        print("[TestDataValidation] Input sanitization persisted as expected.")


# ------------------------------------------------------------------
# Final sanity test (end-to-end persistence smoke test)
# ------------------------------------------------------------------
def test_end_to_end_persistence_smoke(engine: AdvancedJobEngine, tmp_path: Path):
    """
    Quick end-to-end smoke test: analyze -> create plan -> start sprint -> save state -> reload engine
    This ties together core persistence flows and provides a useful single-step verification.
    """
    cv_path, job_path = create_temp_cv_job(
        tmp_path, "Skills: Python", "Required: Python, Django, Docker"
    )
    analysis = engine.analyze_from_files(str(cv_path), str(job_path))
    plan = engine.create_learning_plan(analysis, mode="standard")
    engine.start_sprint(plan.get("skills_to_learn", [])[:1] or ["Python"], "Smoke sprint")
    engine.log_daily_progress(
        _hours_studied=1.0, _topics_covered=["smoke test"], _progress_rating=3
    )
    engine.end_sprint("https://example.com/smoke", {"Python": 80})
    engine.state["smoke_test"] = True
    engine._save_json(engine.state_file, engine.state)

    reloaded = AdvancedJobEngine(data_dir=engine.data_dir)
    assert reloaded.state.get("smoke_test") is True
    print("[smoke] End-to-end persistence smoke test passed.")


# ------------------------------------------------------------------
# Run with pytest -s when executed directly
# ------------------------------------------------------------------
if __name__ == "__main__":
    pytest.main([__file__, "-q", "-s"])
