"""
Unit tests for CV-Job matching algorithm
Tests scoring and matching logic
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from analyzers.matcher import Matcher


class TestMatcher:
    """Test suite for matching algorithm"""
    
    @pytest.fixture
    def matcher(self):
        """Create a matcher instance"""
        return Matcher()
    
    @pytest.fixture
    def sample_cv_data(self):
        """Sample parsed CV data"""
        return {
            'skills': ['Python', 'Django', 'PostgreSQL', 'Docker', 'Git'],
            'experience': [
                {
                    'title': 'Python Developer',
                    'company': 'Tech Corp',
                    'duration_years': 3,
                    'skills_used': ['Python', 'Django', 'PostgreSQL']
                },
                {
                    'title': 'Junior Developer',
                    'company': 'StartupXYZ',
                    'duration_years': 2,
                    'skills_used': ['Python', 'Git']
                }
            ],
            'years_experience': 5,
            'education': 'BS Computer Science'
        }
    
    @pytest.fixture
    def sample_job_data(self):
        """Sample parsed job description"""
        return {
            'required_skills': ['Python', 'Django', 'PostgreSQL', 'Docker', 'Kubernetes'],
            'preferred_skills': ['AWS', 'React', 'CI/CD'],
            'nice_to_have': ['Machine Learning', 'Redis'],
            'experience_years': 3,
            'education': 'Bachelor degree'
        }
    
    def test_calculate_skill_match(self, matcher, sample_cv_data, sample_job_data):
        """Test skill matching calculation"""
        score = matcher.calculate_skill_match(
            sample_cv_data['skills'],
            sample_job_data['required_skills']
        )
        
        assert 0 <= score <= 100
        assert score >= 60  # Should match Python, Django, PostgreSQL, Docker
        
    def test_calculate_experience_match(self, matcher, sample_cv_data, sample_job_data):
        """Test experience matching"""
        score = matcher.calculate_experience_match(
            sample_cv_data['years_experience'],
            sample_job_data['experience_years']
        )
        
        assert 0 <= score <= 100
        assert score >= 80  # 5 years vs 3 required
        
    def test_calculate_education_match(self, matcher, sample_cv_data, sample_job_data):
        """Test education matching"""
        score = matcher.calculate_education_match(
            sample_cv_data['education'],
            sample_job_data['education']
        )
        
        assert 0 <= score <= 100
        assert score >= 80  # BS matches Bachelor
        
    def test_calculate_total_score(self, matcher, sample_cv_data, sample_job_data):
        """Test overall match score calculation"""
        score = matcher.calculate_match_score(sample_cv_data, sample_job_data)
        
        assert 'total_score' in score
        assert 'skill_score' in score
        assert 'experience_score' in score
        assert 'education_score' in score
        
        assert 0 <= score['total_score'] <= 100
        
    def test_identify_missing_skills(self, matcher, sample_cv_data, sample_job_data):
        """Test missing skill identification"""
        missing = matcher.identify_missing_skills(
            sample_cv_data['skills'],
            sample_job_data['required_skills']
        )
        
        assert 'Kubernetes' in missing
        assert 'Python' not in missing
        
    def test_identify_matching_skills(self, matcher, sample_cv_data, sample_job_data):
        """Test matching skill identification"""
        matching = matcher.identify_matching_skills(
            sample_cv_data['skills'],
            sample_job_data['required_skills']
        )
        
        assert 'Python' in matching
        assert 'Django' in matching
        assert 'Kubernetes' not in matching
        
    def test_weighted_scoring(self, matcher, sample_cv_data, sample_job_data):
        """Test weighted score calculation"""
        weights = {
            'required_skills': 1.0,
            'preferred_skills': 0.7,
            'nice_to_have': 0.3
        }
        
        score = matcher.calculate_match_score(
            sample_cv_data,
            sample_job_data,
            weights=weights
        )
        
        assert score['total_score'] <= 100
        
    def test_perfect_match(self, matcher):
        """Test perfect match scenario"""
        cv_data = {
            'skills': ['Python', 'Django', 'Docker'],
            'years_experience': 5,
            'education': 'BS Computer Science'
        }
        
        job_data = {
            'required_skills': ['Python', 'Django', 'Docker'],
            'preferred_skills': [],
            'nice_to_have': [],
            'experience_years': 3,
            'education': 'Bachelor degree'
        }
        
        score = matcher.calculate_match_score(cv_data, job_data)
        
        assert score['skill_score'] == 100
        assert score['total_score'] >= 90
        
    def test_no_match(self, matcher):
        """Test no match scenario"""
        cv_data = {
            'skills': ['Java', 'Spring', 'Oracle'],
            'years_experience': 2,
            'education': 'HS Diploma'
        }
        
        job_data = {
            'required_skills': ['Python', 'Django', 'PostgreSQL'],
            'preferred_skills': [],
            'nice_to_have': [],
            'experience_years': 5,
            'education': 'Master degree'
        }
        
        score = matcher.calculate_match_score(cv_data, job_data)
        
        assert score['skill_score'] < 30
        assert score['total_score'] < 40


class TestMatcherAdvanced:
    """Advanced matching algorithm tests"""
    
    @pytest.fixture
    def matcher(self):
        return Matcher()
    
    def test_fuzzy_skill_matching(self, matcher):
        """Test fuzzy matching for similar skills"""
        cv_skills = ['JavaScript', 'ReactJS', 'Node.js']
        job_skills = ['Javascript', 'React', 'NodeJS']
        
        score = matcher.calculate_skill_match(
            cv_skills,
            job_skills,
            fuzzy=True
        )
        
        assert score >= 90  # Should recognize similar skills
        
    def test_skill_synonyms(self, matcher):
        """Test handling of skill synonyms"""
        cv_skills = ['JS', 'ML', 'K8s']
        job_skills = ['JavaScript', 'Machine Learning', 'Kubernetes']
        
        score = matcher.calculate_skill_match(
            cv_skills,
            job_skills,
            use_synonyms=True
        )
        
        assert score >= 90
        
    def test_experience_quality_weight(self, matcher):
        """Test experience quality weighting"""
        # 2 years of highly relevant experience
        recent_experience = {
            'years_experience': 2,
            'skills': ['Python', 'Django'],
            'experience': [
                {
                    'duration_years': 2,
                    'skills_used': ['Python', 'Django'],
                    'relevance': 'high'
                }
            ]
        }
        
        # 5 years of less relevant experience
        general_experience = {
            'years_experience': 5,
            'skills': ['Python'],
            'experience': [
                {
                    'duration_years': 5,
                    'skills_used': ['Python'],
                    'relevance': 'low'
                }
            ]
        }
        
        job = {
            'required_skills': ['Python', 'Django'],
            'experience_years': 2
        }
        
        score1 = matcher.calculate_match_score(recent_experience, job)
        score2 = matcher.calculate_match_score(general_experience, job)
        
        # Recent relevant experience should score higher
        assert score1['total_score'] >= score2['total_score']
        
    def test_skill_depth_scoring(self, matcher):
        """Test skill depth consideration in scoring"""
        cv_expert = {
            'skills': ['Python'],
            'skill_levels': {'Python': 'expert'},
            'years_experience': 5
        }
        
        cv_beginner = {
            'skills': ['Python'],
            'skill_levels': {'Python': 'beginner'},
            'years_experience': 1
        }
        
        job = {
            'required_skills': ['Python'],
            'experience_years': 3
        }
        
        score_expert = matcher.calculate_match_score(cv_expert, job)
        score_beginner = matcher.calculate_match_score(cv_beginner, job)
        
        assert score_expert['total_score'] > score_beginner['total_score']


class TestMatcherEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.fixture
    def matcher(self):
        return Matcher()
    
    def test_empty_cv(self, matcher):
        """Test matching with empty CV"""
        empty_cv = {'skills': [], 'years_experience': 0, 'education': ''}
        job = {'required_skills': ['Python'], 'experience_years': 2, 'education': 'BS'}
        
        score = matcher.calculate_match_score(empty_cv, job)
        
        assert score['total_score'] == 0
        
    def test_empty_job(self, matcher):
        """Test matching with empty job requirements"""
        cv = {'skills': ['Python'], 'years_experience': 2, 'education': 'BS'}
        empty_job = {'required_skills': [], 'experience_years': 0, 'education': ''}
        
        score = matcher.calculate_match_score(cv, empty_job)
        
        assert score['total_score'] >= 0
        
    def test_case_insensitive_matching(self, matcher):
        """Test case-insensitive skill matching"""
        cv_skills = ['python', 'django', 'docker']
        job_skills = ['Python', 'Django', 'Docker']
        
        score = matcher.calculate_skill_match(cv_skills, job_skills)
        
        assert score == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
