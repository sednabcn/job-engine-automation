"""
Unit tests for job description parser
Tests job requirement extraction and parsing
"""

import sys
from pathlib import Path

import pytest

from src.analyzers.job_parser import JobParser

# Ensure proper module resolution
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestJobParser:
    """Test suite for job description parsing"""

    @pytest.fixture
    def parser(self):
        """Create a job parser instance"""
        return JobParser()

    @pytest.fixture
    def sample_job_description(self):
        """Sample job description for testing"""
        return """
        Senior Python Developer

        We are seeking an experienced Python developer to join our team.

        REQUIRED SKILLS:
        - 5+ years of Python development experience
        - Strong experience with Django or Flask
        - Experience with PostgreSQL and MongoDB
        - Knowledge of Docker and Kubernetes
        - RESTful API design and development

        PREFERRED SKILLS:
        - Experience with AWS or Azure
        - React or Vue.js experience
        - CI/CD pipeline experience
        - Agile/Scrum methodology

        NICE TO HAVE:
        - Machine Learning knowledge
        - Experience with microservices
        - Open source contributions

        RESPONSIBILITIES:
        - Design and develop scalable web applications
        - Collaborate with cross-functional teams
        - Mentor junior developers
        - Participate in code reviews

        QUALIFICATIONS:
        - Bachelor's degree in Computer Science or related field
        - 5+ years professional experience
        - Excellent problem-solving skills
        """

    def test_extract_required_skills(self, parser, sample_job_description):
        """Test extraction of required skills"""
        skills = parser.extract_required_skills(sample_job_description)

        assert "Python" in skills
        assert "Django" in skills or "Flask" in skills
        assert "Docker" in skills
        assert len(skills) >= 5

    def test_extract_preferred_skills(self, parser, sample_job_description):
        """Test extraction of preferred skills"""
        skills = parser.extract_preferred_skills(sample_job_description)

        assert "AWS" in skills or "Azure" in skills
        assert "React" in skills or "Vue.js" in skills

    def test_extract_nice_to_have(self, parser, sample_job_description):
        """Test extraction of nice-to-have skills"""
        skills = parser.extract_nice_to_have(sample_job_description)

        assert "Machine Learning" in skills
        assert "microservices" in skills

    def test_extract_experience_requirements(self, parser, sample_job_description):
        """Test years of experience extraction"""
        years = parser.extract_experience_years(sample_job_description)
        assert isinstance(years, (int, float))
        assert years >= 5

    def test_extract_education_requirements(self, parser, sample_job_description):
        """Test education requirement extraction"""
        education = parser.extract_education(sample_job_description)
        assert any(word in education for word in ["Bachelor", "BS", "BSc"])
        assert "Computer Science" in education

    def test_extract_responsibilities(self, parser, sample_job_description):
        """Test job responsibilities extraction"""
        responsibilities = parser.extract_responsibilities(sample_job_description)
        assert len(responsibilities) >= 3
        assert any("develop" in r.lower() for r in responsibilities)

    def test_parse_full_job(self, parser, sample_job_description):
        """Test complete job description parsing"""
        parsed = parser.parse(sample_job_description)

        assert "required_skills" in parsed
        assert "preferred_skills" in parsed
        assert "nice_to_have" in parsed
        assert "experience_years" in parsed
        assert "education" in parsed
        assert "responsibilities" in parsed

    def test_skill_categorization(self, parser, sample_job_description):
        """Test proper skill categorization"""
        parsed = parser.parse(sample_job_description)

        required = set(parsed.get("required_skills", []))
        preferred = set(parsed.get("preferred_skills", []))
        nice = set(parsed.get("nice_to_have", []))

        assert len(required & preferred) == 0
        assert len(required & nice) == 0

    def test_empty_job_description(self, parser):
        """Test handling of empty job description"""
        parsed = parser.parse("")
        assert parsed["required_skills"] == []
        assert parsed["preferred_skills"] == []
        assert parsed["nice_to_have"] == []

    def test_detect_seniority_level(self, parser, sample_job_description):
        """Test job seniority level detection"""
        level = parser.detect_seniority_level(sample_job_description)
        assert level in ["junior", "mid", "senior", "lead", "principal"]
        assert level == "senior"


class TestJobParserKeywordDetection:
    """Test keyword detection and extraction"""

    @pytest.fixture
    def parser(self):
        return JobParser()

    def test_technology_keywords(self, parser):
        """Test technology keyword detection"""
        job_text = """
        We use Python, React, Docker, and AWS to build scalable systems.
        """
        techs = parser.extract_technologies(job_text)

        assert "Python" in techs
        assert "React" in techs
        assert "Docker" in techs
        assert "AWS" in techs

    def test_soft_skills_detection(self, parser):
        """Test soft skills detection"""
        job_text = """
        Strong communication skills.
        Team player with leadership abilities.
        Problem-solving mindset.
        """
        soft_skills = parser.extract_soft_skills(job_text)

        assert any("communication" in s.lower() for s in soft_skills)
        assert any("leadership" in s.lower() for s in soft_skills)

    def test_industry_specific_terms(self, parser):
        """Test industry-specific term detection"""
        fintech_job = """
        Experience with payment systems, banking APIs, and compliance frameworks.
        """
        terms = parser.extract_domain_terms(fintech_job)

        assert any("payment" in t.lower() for t in terms)
        assert any("compliance" in t.lower() for t in terms)


class TestJobParserNormalization:
    """Test normalization and standardization"""

    @pytest.fixture
    def parser(self):
        return JobParser()

    def test_skill_name_normalization(self, parser):
        """Test skill name standardization"""
        variations = ["javascript", "JS", "JavaScript 2.0"]
        normalized = [parser.normalize_skill(s) for s in variations]

        assert all(n in ["JavaScript", "JS"] for n in normalized)

    def test_framework_version_handling(self, parser):
        """Test handling of framework versions"""
        skills = ["React 18", "Angular 2", "Vue.js 3"]
        normalized = [parser.normalize_skill(s) for s in skills]

        for n in normalized:
            assert isinstance(n, str)
            assert not any(char.isdigit() for char in n.strip())

    def test_remove_experience_numbers(self, parser):
        """Test removal of experience numbers from skills"""
        skill_with_years = "5+ years of Python development"
        cleaned = parser.clean_skill_text(skill_with_years)

        assert "Python" in cleaned
        assert "5+" not in cleaned
        assert "years" not in cleaned


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
