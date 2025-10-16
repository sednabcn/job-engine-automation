"""
Integration tests for full workflow
Tests end-to-end standard mode workflow from CV analysis to application readiness
"""

import pytest
from pathlib import Path
import sys
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from python_advanced_job_engine import AdvancedJobEngine
from tests.mocks.mock_data import (
    MOCK_CV_TEXT, MOCK_JOB_DESCRIPTION,
    get_mock_cv, get_mock_job
)


class TestFullWorkflow:
    """Test complete workflow from analysis to application"""
    
    @pytest.fixture
    def temp_data_dir(self, tmp_path):
        """Create temporary data directory"""
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return str(data_dir)
    
    @pytest.fixture
    def engine(self, temp_data_dir):
        """Create engine instance with temp directory"""
        return AdvancedJobEngine(data_dir=temp_data_dir)
    
    @pytest.fixture
    def sample_files(self, tmp_path):
        """Create sample CV and job files"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        
        cv_file.write_text(MOCK_CV_TEXT)
        job_file.write_text(MOCK_JOB_DESCRIPTION)
        
        return str(cv_file), str(job_file)
    
    def test_complete_standard_workflow(self, engine, sample_files):
        """Test complete standard mode workflow"""
        cv_file, job_file = sample_files
        
        # Step 1: Analyze job vs CV
        print("\n=== Step 1: Initial Analysis ===")
        analysis = engine.analyze_from_files(
            cv_file=cv_file,
            job_file=job_file,
            job_title="Senior Backend Engineer",
            company="TechCorp"
        )
        
        assert analysis is not None
        assert 'score' in analysis
        assert 'gaps' in analysis
        assert analysis['score']['total_score'] > 0
        
        initial_score = analysis['score']['total_score']
        print(f"Initial match score: {initial_score}%")
        
        # Step 2: Create learning plan
        print("\n=== Step 2: Learning Plan Creation ===")
        learning_plan = engine.create_learning_plan(analysis, mode='standard')
        
        assert learning_plan is not None
        assert 'skills_to_learn' in learning_plan
        assert len(learning_plan['skills_to_learn']) > 0
        print(f"Skills to learn: {len(learning_plan['skills_to_learn'])}")
        
        # Step 3: Create improvement strategy
        print("\n=== Step 3: Improvement Strategy ===")
        strategy = engine.create_improvement_strategy(analysis, learning_plan)
        
        assert strategy is not None
        assert 'phases' in strategy
        print(f"Strategy phases: {len(strategy.get('phases', []))}")
        
        # Step 4: Generate skill tests
        print("\n=== Step 4: Skill Tests ===")
        missing_skills = analysis['gaps']['missing_required_skills'][:3]
        tests = engine.generate_skill_tests(missing_skills)
        
        assert tests is not None
        assert len(tests) > 0
        print(f"Tests generated: {len(tests)}")
        
        # Step 5: Generate application materials
        print("\n=== Step 5: Application Materials ===")
        letters = engine.generate_recruiter_letter(analysis, learning_plan)
        
        assert letters is not None
        assert 'cover_letter' in letters
        assert len(letters['cover_letter']) > 100
        print(f"Cover letter generated: {len(letters['cover_letter'])} chars")
        
        # Step 6: Verify data persistence
        print("\n=== Step 6: Data Persistence ===")
        assert Path(engine.analysis_file).exists()
        assert Path(engine.learning_file).exists()
        assert Path(engine.state_file).exists()
        
        # Load and verify saved data
        with open(engine.analysis_file) as f:
            saved_analysis = json.load(f)
        assert len(saved_analysis) > 0
        
        print("\n=== Workflow Complete ===")
        print(f"✓ Analysis saved")
        print(f"✓ Learning plan created")
        print(f"✓ Strategy developed")
        print(f"✓ Tests generated")
        print(f"✓ Materials ready")
    
    def test_workflow_with_sprints(self, engine, sample_files):
        """Test workflow including sprint execution"""
        cv_file, job_file = sample_files
        
        # Initial analysis
        analysis = engine.analyze_from_files(cv_file, job_file)
        learning_plan = engine.create_learning_plan(analysis, mode='standard')
        
        # Start first sprint
        skills = learning_plan['skills_to_learn'][:2]
        project_goal = f"Build project with {', '.join(skills)}"
        
        sprint = engine.start_sprint(skills, project_goal)
        
        assert sprint is not None
        assert sprint['sprint_number'] == 1
        assert sprint['skills_targeted'] == skills
        
        # Log daily progress for several days
        for day in range(5):
            engine.log_daily_progress(
                hours_studied=2.5,
                topics_covered=[f"Topic {day+1} for {skills[0]}"],
                challenges="Some challenges" if day % 2 == 0 else None,
                progress_rating=4
            )
        
        # Verify logs saved
        current_sprint = engine.sprint_history[-1]
        assert len(current_sprint['daily_logs']) == 5
        
        # End sprint
        project_url = "https://github.com/user/test-project"
        test_scores = {skill: 75 for skill in skills}
        
        result = engine.end_sprint(project_url, test_scores)
        
        assert result['completed'] is True
        assert result['project_url'] == project_url
        assert len(result['test_scores']) == len(skills)
        
        # Verify sprint saved to history
        assert len(engine.sprint_history) == 1
        assert engine.sprint_history[0]['completed'] is True
        
        print("\n✓ Sprint workflow completed successfully")

    def test_workflow_state_management(self, engine, sample_files):
        """Test workflow state tracking and persistence"""
        cv_file, job_file = sample_files
        
        # Initial state
        initial_state = engine.state.copy()
        assert initial_state.get('mode') is None
        
        # Run analysis
        analysis = engine.analyze_from_files(cv_file, job_file)
        
        # Update state
        engine.state['baseline_score'] = analysis['score']['total_score']
        engine.state['current_score'] = analysis['score']['total_score']
        engine.state['mode'] = 'standard'
        engine._save_json(engine.state_file, engine.state)
        
        # Create new engine instance and verify state loaded
        new_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        
        assert new_engine.state['mode'] == 'standard'
        assert new_engine.state['baseline_score'] == analysis['score']['total_score']
        
        print("\n✓ State management working correctly")

    def test_workflow_quality_gates(self, engine, sample_files):
        """Test quality gate progression through workflow"""
        cv_file, job_file = sample_files
        
        # Initial setup
        analysis = engine.analyze_from_files(cv_file, job_file)
        engine.state['current_score'] = 60  # Below all gates
        engine.state['projects_completed'] = []
        
        # Check initial gates - should all fail
        gates = engine.check_quality_gates()
        assert gates['foundation'] is False
        assert gates['competency'] is False
        assert gates['mastery'] is False
        
        # Progress to foundation gate
        engine.state['current_score'] = 65
        engine.state['projects_completed'] = [
            {'name': 'Project 1', 'skills': ['A']},
            {'name': 'Project 2', 'skills': ['B']}
        ]
        
        gates = engine.check_quality_gates()
        assert gates['foundation'] is True
        assert gates['competency'] is False
        
        # Progress to competency gate
        engine.state['current_score'] = 80
        engine.state['projects_completed'].extend([
            {'name': 'Project 3', 'skills': ['C']},
            {'name': 'Project 4', 'skills': ['D']}
        ])
        
        gates = engine.check_quality_gates()
        assert gates['competency'] is True
        assert gates['mastery'] is False
        
        # Progress to mastery gate
        engine.state['current_score'] = 90
        engine.state['projects_completed'].append(
            {'name': 'Project 5', 'skills': ['E']}
        )
        
        gates = engine.check_quality_gates()
        assert gates['mastery'] is True
        
        print("\n✓ Quality gates progression working")

    def test_workflow_export_package(self, engine, sample_files):
        """Test complete export package generation"""
        cv_file, job_file = sample_files
        
        # Setup complete workflow
        analysis = engine.analyze_from_files(cv_file, job_file)
        learning_plan = engine.create_learning_plan(analysis)
        strategy = engine.create_improvement_strategy(analysis, learning_plan)
        tests = engine.generate_skill_tests(
            analysis['gaps']['missing_required_skills'][:2]
        )
        letters = engine.generate_recruiter_letter(analysis, learning_plan)
        
        # Export everything
        export_path = engine.export_complete_package(
            analysis, learning_plan, strategy, tests, letters
        )
        
        assert export_path is not None
        export_dir = Path(export_path)
        assert export_dir.exists()
        
        # Verify all files created
        expected_files = [
            'complete_report.txt',
            'learning_plan.json',
            'improvement_strategy.json',
            'skill_tests.json',
            'cover_letter.txt'
        ]
        
        for filename in expected_files:
            file_path = export_dir / filename
            assert file_path.exists(), f"Missing file: {filename}"
            assert file_path.stat().st_size > 0, f"Empty file: {filename}"
        
        print(f"\n✓ Complete package exported to: {export_path}")


class TestWorkflowEdgeCases:
    """Test workflow edge cases and error handling"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))

    def test_workflow_with_perfect_match(self, engine, tmp_path):
        """Test workflow when CV perfectly matches job"""
        # Create CV and job with identical skills
        cv_text = """
        John Doe
        Skills: Python, Django, PostgreSQL, Docker, AWS
        Experience: 5 years
        """
        job_text = """
        Required Skills: Python, Django, PostgreSQL, Docker, AWS
        Experience: 3 years
        """
        
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text(cv_text)
        job_file.write_text(job_text)
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        
        assert analysis['score']['total_score'] >= 90
        assert len(analysis['gaps']['missing_required_skills']) == 0
        
        # Should still create learning plan for advanced topics
        learning_plan = engine.create_learning_plan(analysis)
        assert learning_plan is not None

    def test_workflow_with_no_match(self, engine, tmp_path):
        """Test workflow when CV has no matching skills"""
        cv_text = """
        Jane Smith
        Skills: Java, Spring, Oracle, Maven
        Experience: 3 years
        """
        job_text = """
        Required Skills: Python, Django, PostgreSQL, Docker
        Experience: 5 years
        """
        
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text(cv_text)
        job_file.write_text(job_text)
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        
        assert analysis['score']['total_score'] < 40
        assert len(analysis['gaps']['missing_required_skills']) > 0
        
        # Should create comprehensive learning plan
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        assert len(learning_plan['skills_to_learn']) >= 4

    def test_workflow_interrupted_sprint(self, engine, tmp_path):
        """Test handling of interrupted sprint"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python")
        job_file.write_text("Required: Python, Django")
        
        # Start sprint
        sprint = engine.start_sprint(['Django'], 'Learn Django')
        
        # Log only 3 days (incomplete)
        for _ in range(3):
            engine.log_daily_progress(
                hours_studied=2.0,
                topics_covered=['Django basics'],
                progress_rating=4
            )
        
        # Try to end sprint early
        result = engine.end_sprint(
            'https://github.com/user/project',
            {'Django': 70}
        )
        
        # Should complete but flag as incomplete
        assert result['completed'] is True
        assert len(result['daily_logs']) < 14
    
    def test_workflow_data_corruption_recovery(self, engine, tmp_path):
        """Test recovery from corrupted data files"""
        # Create corrupted JSON file
        corrupted_file = Path(engine.data_dir) / "analyzed_jobs.json"
        corrupted_file.write_text("{invalid json content")
        
        # Engine should handle gracefully
        try:
            engine._load_json(str(corrupted_file))
            assert False, "Should have raised exception"
        except json.JSONDecodeError:
            # Expected - engine should recover with empty list
            pass
        
        # Verify engine still functional
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python")
        job_file.write_text("Required: Python")
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        assert analysis is not None


class TestWorkflowPerformance:
    """Test workflow performance and optimization"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))

    def test_large_cv_processing(self, engine, tmp_path):
        """Test processing of large CV"""
        # Create CV with extensive experience
        cv_text = "John Doe\n\n"
        cv_text += "Skills: " + ", ".join([f"Skill{i}" for i in range(50)]) + "\n\n"
        cv_text += "Experience:\n"
        for i in range(10):
            cv_text += f"Company {i} (2 years)\n"
            cv_text += f"Did stuff with Skill{i}\n\n"
        
        cv_file = tmp_path / "large_cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text(cv_text)
        job_file.write_text("Required Skills: Skill1, Skill2")
        
        import time
        start = time.time()
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        elapsed = time.time() - start
        
        assert analysis is not None
        assert elapsed < 5.0, f"Processing took too long: {elapsed}s"
        
        print(f"\n✓ Large CV processed in {elapsed:.2f}s")

    def test_batch_analysis(self, engine, tmp_path):
        """Test analyzing multiple jobs efficiently"""
        cv_file = tmp_path / "cv.txt"
        cv_file.write_text("Skills: Python, Django, PostgreSQL")
        
        # Create multiple job files
        job_files = []
        for i in range(5):
            job_file = tmp_path / f"job{i}.txt"
            job_file.write_text(f"Job {i}\nRequired: Python, Skill{i}")
            job_files.append(str(job_file))
        
        import time
        start = time.time()
        
        analyses = []
        for job_file in job_files:
            analysis = engine.analyze_from_files(
                str(cv_file),
                job_file,
                job_title=f"Job {len(analyses)}"
            )
            analyses.append(analysis)
        
        elapsed = time.time() - start
        
        assert len(analyses) == 5
        assert all(a is not None for a in analyses)
        assert elapsed < 10.0, f"Batch processing too slow: {elapsed}s"
        
        print(f"\n✓ Analyzed {len(analyses)} jobs in {elapsed:.2f}s")


class TestWorkflowIntegration:
    """Test integration between workflow components"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))

    def test_learning_plan_to_sprint_integration(self, engine, tmp_path):
        """Test smooth transition from learning plan to sprints"""
        # Setup
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python")
        job_file.write_text("Required: Python, Django, Docker, Kubernetes")
        
        # Create learning plan
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        # Extract skills from plan
        study_skills = [
            item['skill'] 
            for item in learning_plan['levels']['study'][:2]
        ]
        
        # Create sprint from plan
        sprint = engine.start_sprint(
            study_skills,
            f"Master {' and '.join(study_skills)}"
        )
        
        assert sprint['skills_targeted'] == study_skills
        assert all(
            skill in learning_plan['skills_to_learn'] 
            for skill in sprint['skills_targeted']
        )

    def test_sprint_to_quality_gate_integration(self, engine, tmp_path):
        """Test sprint completion affecting quality gates"""
        # Setup initial state
        engine.state['current_score'] = 63
        engine.state['projects_completed'] = [{'name': 'P1', 'skills': ['A']}]
        
        # Should not pass foundation gate yet
        gates_before = engine.check_quality_gates()
        assert gates_before['foundation'] is False
        
        # Complete sprint that pushes over threshold
        sprint = engine.start_sprint(['Django'], 'Learn Django')
        for _ in range(14):
            engine.log_daily_progress(2.0, ['Django'], progress_rating=4)
        
        engine.end_sprint(
            'https://github.com/user/django-project',
            {'Django': 80}
        )
        
        # Update score
        engine.state['current_score'] = 65
        
        # Should now pass foundation gate
        gates_after = engine.check_quality_gates()
        assert gates_after['foundation'] is True

    def test_analysis_to_materials_integration(self, engine, tmp_path):
        """Test analysis data flows correctly to application materials"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        
        cv_file.write_text("""
        John Doe
        john@email.com
        Skills: Python, Django, PostgreSQL
        Experience: 5 years Python development
        """)
        
        job_file.write_text("""
        Senior Python Developer
        TechCorp Inc.
        Required: Python, Django, PostgreSQL, Docker
        Preferred: Kubernetes, AWS
        """)
        
        # Analyze
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis)
        
        # Generate materials
        letters = engine.generate_recruiter_letter(analysis, learning_plan)
        
        # Verify data integration
        cover_letter = letters['cover_letter']
        
        # Should mention company name
        assert 'TechCorp' in cover_letter
        
        # Should mention matching skills
        assert 'Python' in cover_letter
        assert 'Django' in cover_letter
        
        # Should address gaps
        missing = analysis['gaps']['missing_required_skills']
        if missing:
            # Should mention learning plan for gaps
            assert any(skill in cover_letter for skill in missing) or \
                   'learning' in cover_letter.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
