"""
Unit tests for learning plan generation
Tests learning plan creation and resource recommendation
"""

import pytest
from pathlib import Path
import sys
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from learning.plan_generator import LearningPlanGenerator


class TestLearningPlanGenerator:
    """Test suite for learning plan generation"""
    
    @pytest.fixture
    def generator(self):
        """Create a learning plan generator instance"""
        return LearningPlanGenerator()
    
    @pytest.fixture
    def sample_gaps(self):
        """Sample skill gaps for testing"""
        return {
            'missing_required_skills': ['Kubernetes', 'AWS', 'CI/CD'],
            'missing_preferred_skills': ['React', 'Redis'],
            'weak_skills': ['Docker']  # Has basic knowledge but needs improvement
        }
    
    @pytest.fixture
    def sample_match_analysis(self):
        """Sample match analysis data"""
        return {
            'score': {'total_score': 65},
            'gaps': {
                'missing_required_skills': ['Kubernetes', 'AWS'],
                'missing_preferred_skills': ['React'],
                'weak_areas': []
            },
            'matching_skills': ['Python', 'Django', 'PostgreSQL']
        }
    
    def test_create_learning_plan(self, generator, sample_match_analysis):
        """Test basic learning plan creation"""
        plan = generator.create_plan(sample_match_analysis)
        
        assert 'skills_to_learn' in plan
        assert 'estimated_duration' in plan
        assert 'levels' in plan
        assert len(plan['skills_to_learn']) > 0
        
    def test_skill_prioritization(self, generator, sample_gaps):
        """Test skill learning prioritization"""
        prioritized = generator.prioritize_skills(sample_gaps)
        
        # Required skills should come before preferred
        required_indices = [i for i, s in enumerate(prioritized) 
                          if s in sample_gaps['missing_required_skills']]
        preferred_indices = [i for i, s in enumerate(prioritized) 
                           if s in sample_gaps['missing_preferred_skills']]
        
        if required_indices and preferred_indices:
            assert max(required_indices) < min(preferred_indices)
        
    def test_estimate_learning_duration(self, generator):
        """Test learning duration estimation"""
        skills = ['Kubernetes', 'AWS', 'React']
        
        duration = generator.estimate_duration(skills)
        
        assert 'weeks' in duration or 'months' in duration
        assert isinstance(duration['total_hours'], (int, float))
        assert duration['total_hours'] > 0
        
    def test_skill_dependency_ordering(self, generator):
        """Test skills ordered by dependencies"""
        skills = ['Django', 'Python', 'REST APIs', 'PostgreSQL']
        
        ordered = generator.order_by_dependencies(skills)
        
        # Python should come before Django
        python_idx = ordered.index('Python') if 'Python' in ordered else -1
        django_idx = ordered.index('Django') if 'Django' in ordered else -1
        
        if python_idx >= 0 and django_idx >= 0:
            assert python_idx < django_idx
            
    def test_create_study_levels(self, generator, sample_match_analysis):
        """Test creation of learning levels (study/practice/master)"""
        plan = generator.create_plan(sample_match_analysis)
        
        assert 'study' in plan['levels']
        assert 'practice' in plan['levels']
        assert 'master' in plan['levels']
        
        # Each level should have skills assigned
        assert len(plan['levels']['study']) > 0
        
    def test_resource_recommendations(self, generator):
        """Test learning resource recommendations"""
        skill = 'Kubernetes'
        
        resources = generator.recommend_resources(skill)
        
        assert len(resources) > 0
        assert all('title' in r for r in resources)
        assert all('type' in r for r in resources)
        assert all('url' in r for r in resources)
        
    def test_create_milestone_plan(self, generator, sample_match_analysis):
        """Test milestone creation in learning plan"""
        plan = generator.create_plan(sample_match_analysis)
        
        assert 'milestones' in plan
        assert len(plan['milestones']) > 0
        
        for milestone in plan['milestones']:
            assert 'name' in milestone
            assert 'target_date' in milestone
            assert 'skills_required' in milestone
            
    def test_reverse_mode_plan(self, generator, sample_match_analysis):
        """Test learning plan in reverse mode (skill-building focus)"""
        plan = generator.create_plan(sample_match_analysis, mode='reverse')
        
        assert plan['mode'] == 'reverse'
        # Reverse mode should prioritize foundational skills
        assert len(plan['skills_to_learn']) > 0
        
    def test_standard_mode_plan(self, generator, sample_match_analysis):
        """Test learning plan in standard mode (job-targeting focus)"""
        plan = generator.create_plan(sample_match_analysis, mode='standard')
        
        assert plan['mode'] == 'standard'
        # Standard mode should focus on job requirements
        
    def test_time_constraints(self, generator, sample_match_analysis):
        """Test learning plan with time constraints"""
        constraints = {
            'hours_per_week': 10,
            'deadline_months': 3
        }
        
        plan = generator.create_plan(sample_match_analysis, constraints=constraints)
        
        assert 'schedule' in plan
        # Should fit within 3 months
        
    def test_empty_gaps(self, generator):
        """Test plan generation with no skill gaps"""
        no_gaps = {
            'score': {'total_score': 95},
            'gaps': {
                'missing_required_skills': [],
                'missing_preferred_skills': [],
                'weak_areas': []
            },
            'matching_skills': ['Python', 'Django', 'PostgreSQL', 'Docker']
        }
        
        plan = generator.create_plan(no_gaps)
        
        # Should still create a plan (for advanced topics or polish)
        assert plan is not None
        assert 'skills_to_learn' in plan


class TestLearningPlanResources:
    """Test learning resource database and recommendations"""
    
    @pytest.fixture
    def generator(self):
        return LearningPlanGenerator()
    
    def test_resource_types(self, generator):
        """Test different resource type recommendations"""
        skill = 'Python'
        
        resources = generator.recommend_resources(skill)
        
        resource_types = set(r['type'] for r in resources)
        
        # Should include various types
        expected_types = {'course', 'documentation', 'tutorial', 'video', 'book'}
        assert len(resource_types & expected_types) > 0
        
    def test_resource_quality_filtering(self, generator):
        """Test filtering of high-quality resources"""
        skill = 'React'
        
        resources = generator.recommend_resources(skill, quality_threshold='high')
        
        # All resources should have quality ratings
        assert all('quality' in r for r in resources)
        
    def test_free_resources_only(self, generator):
        """Test filtering for free resources"""
        skill = 'AWS'
        
        resources = generator.recommend_resources(skill, free_only=True)
        
        assert all(r.get('cost', 'free') == 'free' for r in resources)
        
    def test_beginner_resources(self, generator):
        """Test beginner-level resource recommendations"""
        skill = 'Kubernetes'
        
        resources = generator.recommend_resources(skill, level='beginner')
        
        assert all(r.get('level') in ['beginner', 'all'] for r in resources)
        
    def test_certification_paths(self, generator):
        """Test certification recommendation"""
        skill = 'AWS'
        
        certs = generator.recommend_certifications(skill)
        
        assert len(certs) > 0
        assert all('name' in c for c in certs)
        assert all('provider' in c for c in certs)


class TestLearningPlanScheduling:
    """Test learning schedule generation"""
    
    @pytest.fixture
    def generator(self):
        return LearningPlanGenerator()
    
    def test_weekly_schedule(self, generator):
        """Test weekly learning schedule creation"""
        skills = ['Python', 'Django']
        hours_per_week = 10
        
        schedule = generator.create_weekly_schedule(skills, hours_per_week)
        
        assert len(schedule) == 7  # 7 days
        total_hours = sum(day['hours'] for day in schedule)
        assert total_hours <= hours_per_week
        
    def test_sprint_planning(self, generator):
        """Test 2-week sprint planning"""
        skills = ['Docker', 'Kubernetes']
        
        sprint = generator.create_sprint_plan(skills, duration_weeks=2)
        
        assert 'week_1' in sprint
        assert 'week_2' in sprint
        assert 'project_goal' in sprint
        
    def test_realistic_time_allocation(self, generator):
        """Test realistic time allocation per skill"""
        skills = ['React', 'Redux', 'TypeScript', 'Testing']
        hours_per_week = 5
        
        schedule = generator.create_weekly_schedule(skills, hours_per_week)
        
        # Should not overload any single day
        for day in schedule:
            assert day['hours'] <= 3  # Max 3 hours per day
            
    def test_rest_days(self, generator):
        """Test inclusion of rest days in schedule"""
        skills = ['Python']
        hours_per_week = 10
        
        schedule = generator.create_weekly_schedule(skills, hours_per_week, rest_days=2)
        
        rest_count = sum(1 for day in schedule if day['hours'] == 0)
        assert rest_count >= 2


class TestLearningPlanValidation:
    """Test learning plan validation"""
    
    @pytest.fixture
    def generator(self):
        return LearningPlanGenerator()
    
    def test_validate_plan_structure(self, generator, sample_match_analysis):
        """Test plan structure validation"""
        plan = generator.create_plan(sample_match_analysis)
        
        is_valid = generator.validate_plan(plan)
        
        assert is_valid is True
        
    def test_invalid_plan_detection(self, generator):
        """Test detection of invalid plans"""
        invalid_plan = {
            'skills_to_learn': [],  # Empty skills
            'estimated_duration': 'invalid'
        }
        
        is_valid = generator.validate_plan(invalid_plan)
        
        assert is_valid is False
        
    def test_plan_feasibility_check(self, generator):
        """Test checking if plan is feasible within timeframe"""
        overambitious_plan = {
            'skills_to_learn': ['Skill1', 'Skill2', 'Skill3', 'Skill4', 'Skill5'],
            'estimated_duration': {'weeks': 1}  # Too short
        }
        
        is_feasible = generator.check_feasibility(overambitious_plan)
        
        assert is_feasible is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
