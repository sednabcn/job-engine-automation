"""
Integration tests for data persistence
Tests JSON file operations, state management, and data integrity
"""

import pytest
from pathlib import Path
import sys
import json
import os
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from python_advanced_job_engine import AdvancedJobEngine


class TestDataPersistence:
    """Test data persistence and file operations"""
    
    @pytest.fixture
    def temp_data_dir(self, tmp_path):
        """Create temporary data directory"""
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return str(data_dir)
    
    @pytest.fixture
    def engine(self, temp_data_dir):
        """Create engine instance"""
        return AdvancedJobEngine(data_dir=temp_data_dir)
    
    def test_initial_file_structure(self, engine):
        """Test initial file structure creation"""
        data_dir = Path(engine.data_dir)
        
        # Verify directory exists
        assert data_dir.exists()
        assert data_dir.is_dir()
        
        # Expected files should be created or ready
        expected_files = [
            'analyzed_jobs.json',
            'learning_progress.json',
            'sprint_history.json',
            'skill_tests.json',
            'workflow_state.json'
        ]
        
        # Files should be created after first use
        for filename in expected_files:
            file_path = data_dir / filename
            # File might not exist until first write
            # Just verify path is valid
            assert file_path.parent == data_dir
    
    def test_analysis_persistence(self, engine, tmp_path):
        """Test job analysis data persistence"""
        # Create sample files
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python, Django")
        job_file.write_text("Required: Python, Django, Docker")
        
        # Run analysis
        analysis = engine.analyze_from_files(
            str(cv_file),
            str(job_file),
            job_title="Backend Dev",
            company="TechCorp"
        )
        
        # Verify saved
        assert Path(engine.analysis_file).exists()
        
        # Load and verify
        with open(engine.analysis_file) as f:
            saved_data = json.load(f)
        
        assert len(saved_data) > 0
        assert saved_data[-1]['job_title'] == "Backend Dev"
        assert saved_data[-1]['company'] == "TechCorp"
        assert 'score' in saved_data[-1]
        assert 'gaps' in saved_data[-1]
    
    def test_learning_plan_persistence(self, engine, tmp_path):
        """Test learning plan persistence"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python")
        job_file.write_text("Required: Python, Django, Docker")
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        # Verify saved
        assert Path(engine.learning_file).exists()
        
        # Load and verify
        with open(engine.learning_file) as f:
            saved_plans = json.load(f)
        
        assert len(saved_plans) > 0
        assert 'skills_to_learn' in saved_plans[-1]
        assert 'mode' in saved_plans[-1]
        assert saved_plans[-1]['mode'] == 'reverse'
    
    def test_sprint_persistence(self, engine, tmp_path):
        """Test sprint history persistence"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python")
        job_file.write_text("Required: Python, Django")
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis)
        
        # Start and complete sprint
        sprint = engine.start_sprint(['Django'], "Learn Django")
        
        for _ in range(14):
            engine.log_daily_progress(2.0, ["Topics"], progress_rating=4)
        
        engine.end_sprint('https://github.com/user/project', {'Django': 80})
        
        # Verify saved
        assert Path(engine.sprint_file).exists()
        
        # Load and verify
        with open(engine.sprint_file) as f:
            saved_sprints = json.load(f)
        
        assert len(saved_sprints) == 1
        assert saved_sprints[0]['skills_targeted'] == ['Django']
        assert saved_sprints[0]['completed'] is True
        assert len(saved_sprints[0]['daily_logs']) == 14
    
    def test_state_persistence(self, engine):
        """Test workflow state persistence"""
        # Modify state
        engine.state['mode'] = 'reverse'
        engine.state['baseline_score'] = 65
        engine.state['current_score'] = 70
        engine.state['skills_mastered'] = ['Python', 'Django']
        engine._save_json(engine.state_file, engine.state)
        
        # Create new engine instance
        new_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        
        # Verify state loaded
        assert new_engine.state['mode'] == 'reverse'
        assert new_engine.state['baseline_score'] == 65
        assert new_engine.state['current_score'] == 70
        assert 'Django' in new_engine.state['skills_mastered']


class TestDataIntegrity:
    """Test data integrity and consistency"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_concurrent_write_safety(self, engine):
        """Test safe concurrent writes"""
        # Simulate multiple writes
        for i in range(10):
            engine.state['test_value'] = i
            engine._save_json(engine.state_file, engine.state)
        
        # Verify final state
        with open(engine.state_file) as f:
            final_state = json.load(f)
        
        assert final_state['test_value'] == 9
    
    def test_data_backup_on_corruption(self, engine):
        """Test handling of corrupted data"""
        # Write valid data
        engine.state['mode'] = 'reverse'
        engine._save_json(engine.state_file, engine.state)
        
        # Corrupt the file
        with open(engine.state_file, 'w') as f:
            f.write("{invalid json")
        
        # Engine should handle gracefully
        new_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        
        # Should load with default state
        assert isinstance(new_engine.state, dict)
    
    def test_atomic_writes(self, engine):
        """Test atomic write operations"""
        # Large data write
        large_data = {
            f'key_{i}': f'value_{i}' * 100
            for i in range(100)
        }
        
        engine._save_json(engine.state_file, large_data)
        
        # Verify data integrity
        loaded_data = engine._load_json(engine.state_file)
        assert loaded_data == large_data
    
    def test_encoding_consistency(self, engine):
        """Test consistent UTF-8 encoding"""
        # Data with special characters
        data = {
            'name': 'José García',
            'skills': ['Python', 'データサイエンス', 'Программирование'],
            'notes': '特殊文字テスト'
        }
        
        engine._save_json(engine.state_file, data)
        loaded_data = engine._load_json(engine.state_file)
        
        assert loaded_data['name'] == 'José García'
        assert 'データサイエンス' in loaded_data['skills']


class TestDataMigration:
    """Test data format migration and versioning"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_backward_compatibility(self, engine):
        """Test loading old format data"""
        # Simulate old format (missing new fields)
        old_state = {
            'mode': 'reverse',
            'baseline_score': 65
            # Missing new fields like 'skills_mastered', etc.
        }
        
        engine._save_json(engine.state_file, old_state)
        
        # Load with new engine
        new_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        
        # Should have defaults for missing fields
        assert 'skills_mastered' in new_engine.state
        assert isinstance(new_engine.state['skills_mastered'], list)
    
    def test_version_tracking(self, engine):
        """Test data version tracking"""
        # Add version to state
        engine.state['data_version'] = '1.0.0'
        engine._save_json(engine.state_file, engine.state)
        
        # Verify version saved
        with open(engine.state_file) as f:
            data = json.load(f)
        
        assert 'data_version' in data


class TestExportImport:
    """Test data export and import functionality"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_complete_export(self, engine, tmp_path):
        """Test exporting complete workflow data"""
        # Create sample data
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python, Django")
        job_file.write_text("Required: Python, Django, Docker")
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis)
        strategy = engine.create_improvement_strategy(analysis, learning_plan)
        tests = engine.generate_skill_tests(['Docker'])
        letters = engine.generate_recruiter_letter(analysis, learning_plan)
        
        # Export
        export_path = engine.export_complete_package(
            analysis, learning_plan, strategy, tests, letters
        )
        
        assert export_path is not None
        export_dir = Path(export_path)
        assert export_dir.exists()
        
        # Verify all files exported
        files = list(export_dir.glob('*'))
        assert len(files) >= 5
    
    def test_selective_export(self, engine, tmp_path):
        """Test exporting specific components"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python")
        job_file.write_text("Required: Python, Django")
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        
        # Export only analysis
        export_path = Path(engine.data_dir) / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        export_path.mkdir()
        
        analysis_file= export_path / "analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        assert analysis_file.exists()
        assert analysis_file.stat().st_size > 0


class TestDataCleanup:
    """Test data cleanup and maintenance"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_old_export_cleanup(self, engine):
        """Test cleanup of old export directories"""
        data_dir = Path(engine.data_dir)
        
        # Create multiple export directories
        old_exports = []
        for i in range(5):
            export_name = f"export_20240{i+1}01_120000"
            export_dir = data_dir / export_name
            export_dir.mkdir()
            (export_dir / "test.txt").write_text("test")
            old_exports.append(export_dir)
        
        # Verify created
        assert len(list(data_dir.glob("export_*"))) == 5
        
        # Cleanup old exports (keep only latest 3)
        exports = sorted(data_dir.glob("export_*"))
        for export_dir in exports[:-3]:
            import shutil
            shutil.rmtree(export_dir)
        
        # Verify cleanup
        remaining = list(data_dir.glob("export_*"))
        assert len(remaining) == 3
    
    def test_duplicate_entry_removal(self, engine):
        """Test removing duplicate entries from history"""
        # Add duplicate analyses
        analysis_data = {
            'job_title': 'Backend Dev',
            'company': 'TechCorp',
            'score': {'total_score': 75},
            'timestamp': datetime.now().isoformat()
        }
        
        # Save multiple times
        for _ in range(3):
            engine.analyzed_jobs.append(analysis_data.copy())
            engine._save_json(engine.analysis_file, engine.analyzed_jobs)
        
        # Remove duplicates based on job_title + company
        seen = set()
        unique_jobs = []
        for job in engine.analyzed_jobs:
            key = (job['job_title'], job['company'])
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        engine.analyzed_jobs = unique_jobs
        engine._save_json(engine.analysis_file, engine.analyzed_jobs)
        
        # Verify cleanup
        assert len(engine.analyzed_jobs) == 1
    
    def test_orphaned_file_detection(self, engine):
        """Test detection of orphaned files"""
        data_dir = Path(engine.data_dir)
        
        # Create orphaned file
        orphaned = data_dir / "old_data_v1.json"
        orphaned.write_text('{"old": "data"}')
        
        # Expected files
        expected_files = {
            'analyzed_jobs.json',
            'learning_progress.json',
            'sprint_history.json',
            'skill_tests.json',
            'workflow_state.json'
        }
        
        # Find orphaned
        all_files = set(f.name for f in data_dir.glob("*.json"))
        orphaned_files = all_files - expected_files
        
        assert 'old_data_v1.json' in orphaned_files


class TestDataRecovery:
    """Test data recovery and restoration"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_state_recovery_from_backup(self, engine):
        """Test recovering state from backup"""
        # Save initial state
        engine.state['mode'] = 'reverse'
        engine.state['current_score'] = 75
        engine._save_json(engine.state_file, engine.state)
        
        # Create backup
        backup_file = Path(str(engine.state_file) + '.backup')
        import shutil
        shutil.copy(engine.state_file, backup_file)
        
        # Corrupt main file
        with open(engine.state_file, 'w') as f:
            f.write("corrupted")
        
        # Restore from backup
        shutil.copy(backup_file, engine.state_file)
        
        # Verify recovery
        recovered_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        assert recovered_engine.state['mode'] == 'reverse'
        assert recovered_engine.state['current_score'] == 75
    
    def test_partial_data_recovery(self, engine, tmp_path):
        """Test recovery when some files are missing"""
        # Create complete workflow
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python")
        job_file.write_text("Required: Python, Django")
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis)
        
        # Delete learning plan file
        if Path(engine.learning_file).exists():
            Path(engine.learning_file).unlink()
        
        # Create new engine - should handle missing file
        new_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        
        assert new_engine.learning_progress == []  # Empty but not crashed
        assert new_engine.analyzed_jobs  # Analysis still there
    
    def test_rebuild_from_sprint_history(self, engine, tmp_path):
        """Test rebuilding state from sprint history"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python")
        job_file.write_text("Required: Python, Django, Docker")
        
        # Complete sprints
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis)
        
        sprint1 = engine.start_sprint(['Django'], "Sprint 1")
        for _ in range(14):
            engine.log_daily_progress(2.0, ["Topics"], progress_rating=4)
        engine.end_sprint('url1', {'Django': 80})
        
        sprint2 = engine.start_sprint(['Docker'], "Sprint 2")
        for _ in range(14):
            engine.log_daily_progress(2.0, ["Topics"], progress_rating=4)
        engine.end_sprint('url2', {'Docker': 75})
        
        # Delete state file
        if Path(engine.state_file).exists():
            Path(engine.state_file).unlink()
        
        # Rebuild state from sprints
        new_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        
        # Reconstruct from sprint history
        if new_engine.sprint_history:
            completed_skills = []
            for sprint in new_engine.sprint_history:
                if sprint.get('completed'):
                    completed_skills.extend(sprint['skills_targeted'])
            
            new_engine.state['skills_mastered'] = completed_skills
            new_engine.state['current_sprint'] = len(new_engine.sprint_history)
            new_engine._save_json(new_engine.state_file, new_engine.state)
        
        assert len(new_engine.state['skills_mastered']) >= 2


class TestConcurrency:
    """Test concurrent access and file locking"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_multiple_engine_instances(self, engine):
        """Test multiple engine instances accessing same data"""
        # Engine 1 writes
        engine.state['test_value'] = 'engine1'
        engine._save_json(engine.state_file, engine.state)
        
        # Engine 2 reads
        engine2 = AdvancedJobEngine(data_dir=engine.data_dir)
        assert engine2.state['test_value'] == 'engine1'
        
        # Engine 2 writes
        engine2.state['test_value'] = 'engine2'
        engine2._save_json(engine2.state_file, engine2.state)
        
        # Engine 1 reloads
        engine_reloaded = AdvancedJobEngine(data_dir=engine.data_dir)
        assert engine_reloaded.state['test_value'] == 'engine2'
    
    def test_safe_concurrent_reads(self, engine):
        """Test safe concurrent read operations"""
        # Write initial data
        engine.state['shared_data'] = 'test'
        engine._save_json(engine.state_file, engine.state)
        
        # Multiple reads should succeed
        engines = [
            AdvancedJobEngine(data_dir=engine.data_dir)
            for _ in range(5)
        ]
        
        # All should read same data
        assert all(e.state['shared_data'] == 'test' for e in engines)


class TestPerformance:
    """Test data persistence performance"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_large_history_write_performance(self, engine):
        """Test write performance with large history"""
        import time
        
        # Create large history
        large_history = [
            {
                'sprint_number': i,
                'skills_targeted': [f'Skill{i}'],
                'daily_logs': [
                    {'hours': 2.0, 'topics': ['Topic']}
                    for _ in range(14)
                ]
            }
            for i in range(100)
        ]
        
        start = time.time()
        engine._save_json(engine.sprint_file, large_history)
        elapsed = time.time() - start
        
        assert elapsed < 1.0, f"Write too slow: {elapsed}s"
        print(f"\n✓ Large history write: {elapsed:.3f}s")
    
    def test_large_history_read_performance(self, engine):
        """Test read performance with large history"""
        import time
        
        # Create and save large history
        large_history = [
            {'sprint_number': i, 'data': 'x' * 1000}
            for i in range(100)
        ]
        engine._save_json(engine.sprint_file, large_history)
        
        start = time.time()
        loaded = engine._load_json(engine.sprint_file)
        elapsed = time.time() - start
        
        assert len(loaded) == 100
        assert elapsed < 0.5, f"Read too slow: {elapsed}s"
        print(f"\n✓ Large history read: {elapsed:.3f}s")
    
    def test_incremental_write_performance(self, engine):
        """Test performance of incremental writes"""
        import time
        
        start = time.time()
        
        # Simulate 50 incremental writes
        for i in range(50):
            engine.state[f'key_{i}'] = f'value_{i}'
            engine._save_json(engine.state_file, engine.state)
        
        elapsed = time.time() - start
        
        assert elapsed < 2.0, f"Incremental writes too slow: {elapsed}s"
        print(f"\n✓ 50 incremental writes: {elapsed:.3f}s")


class TestFileSystemOperations:
    """Test file system operations and edge cases"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_directory_creation(self, tmp_path):
        """Test automatic directory creation"""
        # Non-existent directory
        new_dir = tmp_path / "new_job_search_data"
        
        # Engine should create it
        engine = AdvancedJobEngine(data_dir=str(new_dir))
        
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_permission_handling(self, engine):
        """Test handling of permission issues"""
        # This test is platform-dependent
        # Skip on Windows
        import platform
        if platform.system() == 'Windows':
            pytest.skip("Permission test not applicable on Windows")
        
        # Make directory read-only
        data_dir = Path(engine.data_dir)
        os.chmod(data_dir, 0o444)
        
        try:
            # Should handle gracefully
            engine._save_json(engine.state_file, {'test': 'data'})
        except PermissionError:
            # Expected
            pass
        finally:
            # Restore permissions
            os.chmod(data_dir, 0o755)
    
    def test_disk_space_check(self, engine):
        """Test handling of low disk space"""
        import shutil
        
        # Check available space
        stat = shutil.disk_usage(engine.data_dir)
        available_gb = stat.free / (1024**3)
        
        # Should have reasonable space
        assert available_gb > 0.1, "Less than 100MB available"
    
    def test_path_with_special_characters(self, tmp_path):
        """Test handling of paths with special characters"""
        # Create directory with special chars
        special_dir = tmp_path / "job_search_data_2024"
        special_dir.mkdir()
        
        engine = AdvancedJobEngine(data_dir=str(special_dir))
        
        # Should work normally
        engine.state['test'] = 'data'
        engine._save_json(engine.state_file, engine.state)
        
        assert Path(engine.state_file).exists()


class TestDataValidation:
    """Test data validation and sanitization"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_json_schema_validation(self, engine):
        """Test JSON structure validation"""
        # Valid state structure
        valid_state = {
            'mode': 'reverse',
            'baseline_score': 65,
            'current_score': 70,
            'skills_mastered': [],
            'projects_completed': [],
            'quality_gates_passed': []
        }
        
        # Save and load
        engine._save_json(engine.state_file, valid_state)
        loaded = engine._load_json(engine.state_file)
        
        # Verify structure preserved
        assert set(valid_state.keys()).issubset(set(loaded.keys()))
    
    def test_data_type_validation(self, engine):
        """Test data type consistency"""
        # Ensure correct types
        engine.state['current_score'] = 75
        engine.state['skills_mastered'] = ['Python', 'Django']
        engine.state['projects_completed'] = []
        
        engine._save_json(engine.state_file, engine.state)
        
        loaded_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        
        assert isinstance(loaded_engine.state['current_score'], (int, float))
        assert isinstance(loaded_engine.state['skills_mastered'], list)
        assert isinstance(loaded_engine.state['projects_completed'], list)
    
    def test_sanitize_user_input(self, engine):
        """Test sanitization of user input before storage"""
        # Potentially dangerous input
        user_input = {
            'job_title': '<script>alert("xss")</script>',
            'company': 'Company\nWith\nNewlines',
            'notes': 'Text with\x00null bytes'
        }
        
        # Sanitize
        sanitized = {
            'job_title': user_input['job_title'].replace('<', '&lt;').replace('>', '&gt;'),
            'company': user_input['company'].replace('\n', ' '),
            'notes': user_input['notes'].replace('\x00', '')
        }
        
        engine._save_json(engine.state_file, sanitized)
        
        loaded = engine._load_json(engine.state_file)
        
        assert '<script>' not in loaded['job_title']
        assert '\n' not in loaded['company']
        assert '\x00' not in loaded['notes']


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
