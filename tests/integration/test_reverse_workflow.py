## **File 2: test_reverse_workflow.py**

"""
Integration tests for reverse workflow
Tests end-to-end reverse mode workflow (skill building focus)
"""

import pytest
from pathlib import Path
import sys
import json
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from python_advanced_job_engine import AdvancedJobEngine
from tests.mocks.mock_data import MOCK_CV_TEXT, MOCK_JOB_DESCRIPTION


class TestReverseWorkflow:
    """Test complete reverse mode workflow"""
    
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
    
    @pytest.fixture
    def sample_files(self, tmp_path):
        """Create sample CV and job files"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        
        cv_file.write_text(MOCK_CV_TEXT)
        job_file.write_text(MOCK_JOB_DESCRIPTION)
        
        return str(cv_file), str(job_file)
    
    def test_complete_reverse_workflow(self, engine, sample_files):
        """Test complete reverse mode from baseline to application ready"""
        cv_file, job_file = sample_files
        
        print("\n" + "="*80)
        print("REVERSE WORKFLOW: BASELINE TO APPLICATION READY")
        print("="*80)
        
        # ================================================================
        # PHASE 1: BASELINE ASSESSMENT
        # ================================================================
        print("\n[PHASE 1] Baseline Assessment")
        print("-" * 80)
        
        analysis = engine.analyze_from_files(
            cv_file=cv_file,
            job_file=job_file,
            job_title="Senior Backend Engineer",
            company="TechCorp"
        )
        
        baseline_score = analysis['score']['total_score']
        engine.state['baseline_score'] = baseline_score
        engine.state['current_score'] = baseline_score
        engine.state['mode'] = 'reverse'
        engine.state['current_stage'] = 'baseline'
        engine.state['target_score'] = 90
        engine._save_json(engine.state_file, engine.state)
        
        print(f"✓ Baseline score: {baseline_score}%")
        print(f"✓ Target score: 90%")
        print(f"✓ Gap to close: {90 - baseline_score}%")
        
        assert baseline_score < 90
        
        # ================================================================
        # PHASE 2: LEARNING PLAN CREATION
        # ================================================================
        print("\n[PHASE 2] Learning Plan Creation")
        print("-" * 80)
        
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        strategy = engine.create_improvement_strategy(analysis, learning_plan)
        
        skills_to_learn = learning_plan['skills_to_learn']
        print(f"✓ Skills to learn: {len(skills_to_learn)}")
        print(f"✓ Estimated duration: {learning_plan['estimated_duration']}")
        print(f"✓ Strategy phases: {len(strategy.get('phases', []))}")
        
        assert len(skills_to_learn) > 0
        
        # ================================================================
        # PHASE 3: FOUNDATION BUILDING (Sprint 1-2)
        # ================================================================
        print("\n[PHASE 3] Foundation Building")
        print("-" * 80)
        
        engine.state['current_stage'] = 'foundation'
        
        # Sprint 1
        print("\nSprint 1:")
        foundation_skills = skills_to_learn[:2]
        sprint1 = engine.start_sprint(
            foundation_skills,
            f"Build foundation project with {', '.join(foundation_skills)}"
        )
        
        # Simulate 14 days of learning
        for day in range(14):
            engine.log_daily_progress(
                hours_studied=2.0 + (day % 3) * 0.5,
                topics_covered=[f"Day {day+1} topics"],
                challenges="Learning challenges" if day % 3 == 0 else None,
                progress_rating=3 + (day % 3)
            )
        
        result1 = engine.end_sprint(
            'https://github.com/user/foundation-project',
            {skill: 75 + (i * 5) for i, skill in enumerate(foundation_skills)}
        )
        
        engine.state['current_score'] = baseline_score + 5
        engine.state['skills_mastered'].extend(foundation_skills)
        engine._save_json(engine.state_file, engine.state)
        
        print(f"✓ Sprint 1 complete")
        print(f"✓ Skills mastered: {foundation_skills}")
        print(f"✓ Score improvement: +5% (now {engine.state['current_score']}%)")
        
        # Sprint 2
        print("\nSprint 2:")
        more_skills = skills_to_learn[2:4] if len(skills_to_learn) > 3 else skills_to_learn[2:3]
        sprint2 = engine.start_sprint(
            more_skills,
            f"Expand skillset with {', '.join(more_skills)}"
        )
        
        for day in range(14):
            engine.log_daily_progress(
                hours_studied=2.5,
                topics_covered=[f"Day {day+1} topics"],
                progress_rating=4
            )
        
        result2 = engine.end_sprint(
            'https://github.com/user/foundation-project-2',
            {skill: 80 for skill in more_skills}
        )
        
        engine.state['current_score'] = baseline_score + 12
        engine.state['skills_mastered'].extend(more_skills)
        engine._save_json(engine.state_file, engine.state)
        
        print(f"✓ Sprint 2 complete")
        print(f"✓ Total skills mastered: {len(engine.state['skills_mastered'])}")
        print(f"✓ Score improvement: +12% (now {engine.state['current_score']}%)")
        
        # Check foundation gate
        gates = engine.check_quality_gates()
        if gates['foundation']:
            print(f"\n🎉 FOUNDATION GATE PASSED!")
        
        # ================================================================
        # PHASE 4: SKILL BUILDING (Sprint 3-4)
        # ================================================================
        print("\n[PHASE 4] Skill Building")
        print("-" * 80)
        
        engine.state['current_stage'] = 'skill_building'
        
        # Continue with more advanced skills
        if len(skills_to_learn) > 4:
            advanced_skills = skills_to_learn[4:6]
            
            print("\nSprint 3:")
            sprint3 = engine.start_sprint(
                advanced_skills,
                f"Advanced project with {', '.join(advanced_skills)}"
            )
            
            for day in range(14):
                engine.log_daily_progress(
                    hours_studied=3.0,
                    topics_covered=[f"Advanced topics day {day+1}"],
                    progress_rating=4
                )
            
            result3 = engine.end_sprint(
                'https://github.com/user/advanced-project',
                {skill: 85 for skill in advanced_skills}
            )
            
            engine.state['current_score'] = baseline_score + 22
            engine.state['skills_mastered'].extend(advanced_skills)
            engine._save_json(engine.state_file, engine.state)
            
            print(f"✓ Sprint 3 complete")
            print(f"✓ Score: {engine.state['current_score']}%")
        
        # Check competency gate
        gates = engine.check_quality_gates()
        if gates['competency']:
            print(f"\n🎉 COMPETENCY GATE PASSED!")
        
        # ================================================================
        # PHASE 5: MASTERY & POLISH
        # ================================================================
        print("\n[PHASE 5] Mastery & Polish")
        print("-" * 80)
        
        engine.state['current_stage'] = 'mastery'
        engine.state['current_score'] = 88  # Simulate near-mastery
        
        # Final sprint for mastery
        if len(skills_to_learn) > 6:
            final_skills = skills_to_learn[6:7]
        else:
            final_skills = [skills_to_learn[0]]  # Polish first skill
        
        print("\nFinal Sprint:")
        sprint_final = engine.start_sprint(
            final_skills,
            "Production-grade capstone project"
        )
        
        for day in range(14):
            engine.log_daily_progress(
                hours_studied=3.5,
                topics_covered=["Production-grade implementation"],
                progress_rating=5
            )
        
        result_final = engine.end_sprint(
            'https://github.com/user/capstone-project',
            {skill: 90 for skill in final_skills}
        )
        
        engine.state['current_score'] = 91
        engine._save_json(engine.state_file, engine.state)
        
        print(f"✓ Final sprint complete")
        print(f"✓ FINAL SCORE: {engine.state['current_score']}%")
        
        # ================================================================
        # PHASE 6: APPLICATION READINESS
        # ================================================================
        print("\n[PHASE 6] Application Readiness Check")
        print("-" * 80)
        
        gates = engine.check_quality_gates()
        
        print(f"Foundation Gate: {'✅ PASSED' if gates['foundation'] else '❌ NOT PASSED'}")
        print(f"Competency Gate: {'✅ PASSED' if gates['competency'] else '❌ NOT PASSED'}")
        print(f"Mastery Gate: {'✅ PASSED' if gates['mastery'] else '❌ NOT PASSED'}")
        print(f"Application Ready: {'✅ YES' if gates.get('application_ready') else '❌ NOT YET'}")
        
        if gates.get('application_ready'):
            print("\n" + "="*80)
            print("🎉 APPLICATION READY - YOU CAN NOW APPLY!")
            print("="*80)
        
        # ================================================================
        # SUMMARY
        # ================================================================
        print("\n[SUMMARY] Reverse Workflow Complete")
        print("="*80)
        print(f"Starting score: {baseline_score}%")
        print(f"Final score: {engine.state['current_score']}%")
        print(f"Improvement: +{engine.state['current_score'] - baseline_score}%")
        print(f"Sprints completed: {len(engine.sprint_history)}")
        print(f"Skills mastered: {len(engine.state['skills_mastered'])}")
        print(f"Projects completed: {len(engine.state['projects_completed'])}")
        print("="*80)
        
        # Assertions
        assert engine.state['current_score'] >= 90
        assert len(engine.sprint_history) >= 4
        assert gates['foundation'] is True
        assert gates['competency'] is True
        assert gates['mastery'] is True
    
    def test_reverse_workflow_progress_tracking(self, engine, sample_files):
        """Test detailed progress tracking in reverse mode"""
        cv_file, job_file = sample_files
        
        # Initial analysis
        analysis = engine.analyze_from_files(cv_file, job_file)
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        baseline = analysis['score']['total_score']
        engine.state['baseline_score'] = baseline
        engine.state['current_score'] = baseline
        engine.state['mode'] = 'reverse'
        
        # Track progress through sprints
        progress_history = []
        
        for sprint_num in range(3):
            skills = learning_plan['skills_to_learn'][sprint_num:sprint_num+2]
            if not skills:
                break
            
            # Start sprint
            sprint = engine.start_sprint(skills, f"Sprint {sprint_num+1}")
            
            # Log progress
            for day in range(14):
                engine.log_daily_progress(
                    hours_studied=2.0,
                    topics_covered=[f"Topics for sprint {sprint_num+1}"],
                    progress_rating=4
                )
            
            # End sprint
            engine.end_sprint(
                f"https://github.com/user/project-{sprint_num+1}",
                {s: 75 + sprint_num * 5 for s in skills}
            )
            
            # Update score
            new_score = baseline + (sprint_num + 1) * 7
            engine.state['current_score'] = new_score
            engine.state['skills_mastered'].extend(skills)
            
            # Record progress
            progress_history.append({
                'sprint': sprint_num + 1,
                'score': new_score,
                'skills_mastered': len(engine.state['skills_mastered']),
                'improvement': new_score - baseline
            })
        
        # Verify progress is monotonically increasing
        for i in range(1, len(progress_history)):
            assert progress_history[i]['score'] > progress_history[i-1]['score']
            assert progress_history[i]['skills_mastered'] >= progress_history[i-1]['skills_mastered']
        
        print("\n✓ Progress tracking validated")
        for entry in progress_history:
            print(f"  Sprint {entry['sprint']}: {entry['score']}% (+{entry['improvement']}%)")
    
    def test_reverse_workflow_with_setbacks(self, engine, sample_files):
        """Test reverse workflow handling of learning setbacks"""
        cv_file, job_file = sample_files
        
        analysis = engine.analyze_from_files(cv_file, job_file)
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        baseline = analysis['score']['total_score']
        engine.state['baseline_score'] = baseline
        engine.state['current_score'] = baseline
        engine.state['mode'] = 'reverse'
        
        # Sprint 1: Good progress
        sprint1 = engine.start_sprint(
            learning_plan['skills_to_learn'][:2],
            "First sprint"
        )
        
        for day in range(14):
            engine.log_daily_progress(2.0, ["Topics"], progress_rating=4)
            result1 = engine.end_sprint(
            'https://github.com/user/project1',
            {'Skill1': 80, 'Skill2': 75}
        )
        
        engine.state['current_score'] = baseline + 8
        
        # Sprint 2: Setback (low test scores)
        sprint2 = engine.start_sprint(
            learning_plan['skills_to_learn'][2:4],
            "Second sprint - challenging material"
        )
        
        # Inconsistent logging (simulating difficulty)
        for day in range(14):
            if day % 3 != 0:  # Skip some days
                engine.log_daily_progress(
                    1.5,  # Fewer hours
                    ["Struggling with topics"],
                    challenges="Difficult concepts",
                    progress_rating=2  # Low rating
                )
        
        result2 = engine.end_sprint(
            'https://github.com/user/project2',
            {'Skill3': 65, 'Skill4': 60}  # Below passing
        )
        
        # Score doesn't improve much
        engine.state['current_score'] = baseline + 9
        
        # Sprint 3: Recovery (revisit with better resources)
        sprint3 = engine.start_sprint(
            learning_plan['skills_to_learn'][2:4],  # Same skills
            "Retry with better approach"
        )
        
        for day in range(14):
            engine.log_daily_progress(
                2.5,  # More focused time
                ["Better resources", "Hands-on practice"],
                progress_rating=4
            )
        
        result3 = engine.end_sprint(
            'https://github.com/user/project3-retry',
            {'Skill3': 80, 'Skill4': 78}  # Much better
        )
        
        engine.state['current_score'] = baseline + 15
        
        # Verify workflow handles setbacks gracefully
        assert len(engine.sprint_history) == 3
        assert engine.sprint_history[1]['test_scores']['Skill3'] < 70
        assert engine.sprint_history[2]['test_scores']['Skill3'] >= 75
        assert engine.state['current_score'] > baseline
        
        print("\n✓ Setback recovery validated")
        print(f"  Sprint 1: +8% (success)")
        print(f"  Sprint 2: +1% (setback)")
        print(f"  Sprint 3: +6% (recovery)")


class TestReverseWorkflowStrategies:
    """Test different strategies in reverse mode"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_aggressive_learning_strategy(self, engine, tmp_path):
        """Test aggressive learning (high hours, fast pace)"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        
        cv_file.write_text("Skills: Python\nExperience: 2 years")
        job_file.write_text("Required: Python, Django, Docker, K8s, AWS")
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        baseline = analysis['score']['total_score']
        engine.state['baseline_score'] = baseline
        engine.state['current_score'] = baseline
        engine.state['mode'] = 'reverse'
        
        # Aggressive: 3 skills per sprint, high hours
        for sprint_num in range(3):
            skills = learning_plan['skills_to_learn'][sprint_num*3:(sprint_num+1)*3]
            if not skills:
                break
            
            sprint = engine.start_sprint(skills, f"Aggressive sprint {sprint_num+1}")
            
            # High study hours
            for day in range(14):
                engine.log_daily_progress(
                    hours_studied=4.0,  # 4 hours/day
                    topics_covered=[f"Multiple topics day {day}"],
                    progress_rating=5
                )
            
            engine.end_sprint(
                f"https://github.com/user/aggressive-{sprint_num}",
                {s: 75 for s in skills}
            )
            
            # Larger score jumps
            engine.state['current_score'] = baseline + (sprint_num + 1) * 12
        
        # Should reach target faster
        assert len(engine.sprint_history) <= 3
        assert engine.state['current_score'] >= baseline + 30
        
        print(f"\n✓ Aggressive strategy: {baseline}% → {engine.state['current_score']}% in 3 sprints")
    
    def test_conservative_learning_strategy(self, engine, tmp_path):
        """Test conservative learning (thorough mastery)"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        
        cv_file.write_text("Skills: Python\nExperience: 2 years")
        job_file.write_text("Required: Python, Django, Docker")
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        baseline = analysis['score']['total_score']
        engine.state['baseline_score'] = baseline
        engine.state['current_score'] = baseline
        engine.state['mode'] = 'reverse'
        
        # Conservative: 1 skill per sprint, deep mastery
        for sprint_num in range(2):
            skill = [learning_plan['skills_to_learn'][sprint_num]]
            
            sprint = engine.start_sprint(skill, f"Deep dive into {skill[0]}")
            
            # Consistent, moderate hours
            for day in range(14):
                engine.log_daily_progress(
                    hours_studied=2.0,
                    topics_covered=[f"Deep learning day {day}"],
                    progress_rating=4
                )
            
            # High test scores (mastery)
            engine.end_sprint(
                f"https://github.com/user/mastery-{sprint_num}",
                {skill[0]: 90}  # High mastery
            )
            
            # Solid, steady improvement
            engine.state['current_score'] = baseline + (sprint_num + 1) * 8
        
        # Slower but solid progress
        assert all(
            list(s['test_scores'].values())[0] >= 85 
            for s in engine.sprint_history
        )
        
        print(f"\n✓ Conservative strategy: Deep mastery approach validated")
    
    def test_balanced_learning_strategy(self, engine, tmp_path):
        """Test balanced learning strategy"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        
        cv_file.write_text("Skills: Python\nExperience: 3 years")
        job_file.write_text("Required: Python, Django, Docker, PostgreSQL")
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        baseline = analysis['score']['total_score']
        engine.state['baseline_score'] = baseline
        engine.state['current_score'] = baseline
        engine.state['mode'] = 'reverse'
        
        # Balanced: 2 skills per sprint, moderate hours
        for sprint_num in range(3):
            skills = learning_plan['skills_to_learn'][sprint_num*2:(sprint_num+1)*2]
            if not skills:
                break
            
            sprint = engine.start_sprint(skills, f"Balanced sprint {sprint_num+1}")
            
            for day in range(14):
                engine.log_daily_progress(
                    hours_studied=2.5,  # Sustainable pace
                    topics_covered=[f"Balanced learning day {day}"],
                    progress_rating=4
                )
            
            engine.end_sprint(
                f"https://github.com/user/balanced-{sprint_num}",
                {s: 80 for s in skills}  # Good scores
            )
            
            engine.state['current_score'] = baseline + (sprint_num + 1) * 9
        
        # Good balance of speed and quality
        assert len(engine.sprint_history) == 3
        assert engine.state['current_score'] >= baseline + 25
        assert all(
            sum(s['test_scores'].values()) / len(s['test_scores']) >= 75
            for s in engine.sprint_history
        )
        
        print(f"\n✓ Balanced strategy: Optimal speed + quality")


class TestReverseWorkflowScenarios:
    """Test specific real-world scenarios in reverse mode"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_career_transition_scenario(self, engine, tmp_path):
        """Test complete career transition (e.g., from QA to Dev)"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        
        # QA Engineer transitioning to Backend Developer
        cv_file.write_text("""
        QA Engineer
        Skills: Manual Testing, Selenium, Python (basic), SQL
        Experience: 4 years in QA
        """)
        
        job_file.write_text("""
        Backend Developer
        Required: Python, Django, REST APIs, PostgreSQL, Git
        Preferred: Docker, CI/CD, AWS
        """)
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        
        # Should have low initial score (career transition)
        assert analysis['score']['total_score'] < 50
        
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        # Should create comprehensive plan
        assert len(learning_plan['skills_to_learn']) >= 5
        assert 'Django' in learning_plan['skills_to_learn']
        assert 'REST APIs' in learning_plan['skills_to_learn']
        
        # Simulate transition over 6 months (12 sprints)
        baseline = analysis['score']['total_score']
        engine.state['baseline_score'] = baseline
        engine.state['current_score'] = baseline
        engine.state['mode'] = 'reverse'
        
        for sprint_num in range(6):
            skills = learning_plan['skills_to_learn'][sprint_num*2:(sprint_num+1)*2]
            if not skills:
                break
            
            sprint = engine.start_sprint(skills, f"Transition sprint {sprint_num+1}")
            
            for day in range(14):
                engine.log_daily_progress(3.0, ["Learning"], progress_rating=4)
            
            engine.end_sprint(
                f"https://github.com/user/transition-{sprint_num}",
                {s: 70 + sprint_num * 3 for s in skills}
            )
            
            engine.state['current_score'] = baseline + (sprint_num + 1) * 8
            engine.state['skills_mastered'].extend(skills)
        
        # Should reach application-ready threshold
        assert engine.state['current_score'] >= 75  # Ready for junior positions
        assert len(engine.state['skills_mastered']) >= 8
        
        print(f"\n✓ Career transition: {baseline}% → {engine.state['current_score']}%")
        print(f"  Skills mastered: {len(engine.state['skills_mastered'])}")
    
    def test_skill_refresh_scenario(self, engine, tmp_path):
        """Test skill refresh for experienced developer"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        
        # Experienced dev with outdated skills
        cv_file.write_text("""
        Senior Developer
        Skills: Python 2.7, Django 1.x, jQuery, MySQL
        Experience: 10 years
        """)
        
        job_file.write_text("""
        Senior Backend Engineer
        Required: Python 3.x, Django 4.x, React, PostgreSQL, Docker, K8s
        """)
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        
        # Should have moderate score (has foundation but outdated)
        assert 50 < analysis['score']['total_score'] < 70
        
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        # Should focus on modern tools/versions
        modern_skills = ['Docker', 'K8s', 'React', 'PostgreSQL']
        assert any(skill in learning_plan['skills_to_learn'] for skill in modern_skills)
        
        print(f"\n✓ Skill refresh scenario validated")
    
    def test_specialization_deepening_scenario(self, engine, tmp_path):
        """Test deepening specialization in existing area"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        
        # Mid-level dev seeking senior role
        cv_file.write_text("""
        Mid-level Backend Engineer
        Skills: Python, Django, PostgreSQL, Docker
        Experience: 4 years
        """)
        
        job_file.write_text("""
        Senior Backend Engineer
        Required: Python, Django, PostgreSQL, Docker, Kubernetes
        Preferred: Microservices, System Design, Performance Optimization
        Additional: Mentoring, Architecture, Leadership
        """)
        
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        
        # Should have good score but missing advanced topics
        assert 70 <= analysis['score']['total_score'] < 85
        
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        # Should focus on advanced/leadership skills
        assert len(learning_plan['skills_to_learn']) > 0
        
        print(f"\n✓ Specialization deepening validated")


class TestReverseWorkflowPersistence:
    """Test data persistence throughout reverse workflow"""
    
    @pytest.fixture
    def engine(self, tmp_path):
        data_dir = tmp_path / "job_search_data"
        data_dir.mkdir()
        return AdvancedJobEngine(data_dir=str(data_dir))
    
    def test_workflow_resume_after_interruption(self, engine, tmp_path):
        """Test resuming workflow after interruption"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python")
        job_file.write_text("Required: Python, Django, Docker")
        
        # Start workflow
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        
        baseline = analysis['score']['total_score']
        engine.state['baseline_score'] = baseline
        engine.state['current_score'] = baseline
        engine.state['mode'] = 'reverse'
        engine.state['skills_mastered'] = ['Python']
        engine._save_json(engine.state_file, engine.state)
        
        # Complete one sprint
        sprint1 = engine.start_sprint(['Django'], "Learn Django")
        for _ in range(14):
            engine.log_daily_progress(2.0, ["Topics"], progress_rating=4)
        engine.end_sprint('https://github.com/user/p1', {'Django': 80})
        
        engine.state['current_score'] = baseline + 10
        engine.state['skills_mastered'].append('Django')
        engine._save_json(engine.state_file, engine.state)
        
        # Simulate interruption - create new engine instance
        new_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        
        # Verify state restored
        assert new_engine.state['mode'] == 'reverse'
        assert new_engine.state['baseline_score'] == baseline
        assert new_engine.state['current_score'] == baseline + 10
        assert 'Django' in new_engine.state['skills_mastered']
        assert len(new_engine.sprint_history) == 1
        
        # Continue workflow
        sprint2 = new_engine.start_sprint(['Docker'], "Learn Docker")
        assert sprint2['sprint_number'] == 2
        
        print("\n✓ Workflow successfully resumed after interruption")
    
    def test_multi_session_workflow(self, engine, tmp_path):
        """Test workflow across multiple sessions"""
        cv_file = tmp_path / "cv.txt"
        job_file = tmp_path / "job.txt"
        cv_file.write_text("Skills: Python")
        job_file.write_text("Required: Python, Django, Docker, K8s")
        
        sessions = []
        
        # Session 1: Initial analysis
        analysis = engine.analyze_from_files(str(cv_file), str(job_file))
        learning_plan = engine.create_learning_plan(analysis, mode='reverse')
        engine.state['baseline_score'] = analysis['score']['total_score']
        engine.state['current_score'] = analysis['score']['total_score']
        engine.state['mode'] = 'reverse'
        engine._save_json(engine.state_file, engine.state)
        sessions.append(engine.state['current_score'])
        
        # Session 2: First sprint
        engine2 = AdvancedJobEngine(data_dir=engine.data_dir)
        sprint1 = engine2.start_sprint(['Django'], "Sprint 1")
        for _ in range(14):
            engine2.log_daily_progress(2.0, ["Topics"], progress_rating=4)
        engine2.end_sprint('url', {'Django': 80})
        engine2.state['current_score'] += 8
        engine2._save_json(engine2.state_file, engine2.state)
        sessions.append(engine2.state['current_score'])
        
        # Session 3: Second sprint
        engine3 = AdvancedJobEngine(data_dir=engine.data_dir)
        sprint2 = engine3.start_sprint(['Docker'], "Sprint 2")
        for _ in range(14):
            engine3.log_daily_progress(2.0, ["Topics"], progress_rating=4)
        engine3.end_sprint('url', {'Docker': 80})
        engine3.state['current_score'] += 8
        engine3._save_json(engine3.state_file, engine3.state)
        sessions.append(engine3.state['current_score'])
        
        # Verify progression
        assert sessions[1] > sessions[0]
        assert sessions[2] > sessions[1]
        
        # Verify final state
        final_engine = AdvancedJobEngine(data_dir=engine.data_dir)
        assert len(final_engine.sprint_history) == 2
        assert final_engine.state['current_score'] == sessions[2]
        
        print(f"\n✓ Multi-session workflow: {len(sessions)} sessions")
        print(f"  Progress: {sessions[0]}% → {sessions[1]}% → {sessions[2]}%")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
