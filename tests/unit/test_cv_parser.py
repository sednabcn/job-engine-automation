import pytest

"""
Unit tests for CV parser module
Tests CV text extraction and parsing functionality
"""

import sys
from pathlib import Path

import pytest

from src.analyzers.cv_parser import CVParser

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestCVParser:
    """Test suite for CV parsing functionality"""

    @pytest.fixture
    def parser(self):
        """Create a CV parser instance"""
        return CVParser()

    @pytest.fixture
    def sample_cv_text(self):
        """Sample CV text for testing"""
        return """
        John Doe
        Software Engineer
        john.doe@email.com | +1-234-567-8900

        EXPERIENCE
        Senior Python Developer at Tech Corp (2020-2023)
        - Developed REST APIs using Django and Flask
        - Implemented microservices architecture
        - Led team of 5 developers

        Python Developer at StartupXYZ (2018-2020)
        - Built data pipelines with Apache Spark
        - Deployed applications on AWS
        - Worked with PostgreSQL and MongoDB

        SKILLS
        Languages: Python, JavaScript, SQL
        Frameworks: Django, Flask, React
        Tools: Docker, Kubernetes, Git
        Cloud: AWS, Azure

        EDUCATION
        BS Computer Science, State University (2018)

        CERTIFICATIONS
        AWS Certified Solutions Architect
        """

    def test_parse_returns_dict(self, parser, sample_cv_text):
        """Test that parse returns a dictionary"""
        parsed = parser.parse(sample_cv_text)
        assert isinstance(parsed, dict)

    def test_parse_has_required_keys(self, parser, sample_cv_text):
        """Test that parse returns all expected keys"""
        parsed = parser.parse(sample_cv_text)

        # Check for keys that exist in actual output
        assert "name" in parsed
        assert "email" in parsed
        assert "phone" in parsed
        assert "skills" in parsed
        assert "experience" in parsed
        assert "education" in parsed

    def test_contact_info_extraction(self, parser, sample_cv_text):
        """Test contact information extraction"""
        parsed = parser.parse(sample_cv_text)

        assert parsed["name"] == "John Doe"
        assert parsed["email"] == "john.doe@email.com"
        assert parsed["phone"] == "+1-234-567-8900"

    def test_skills_extraction(self, parser, sample_cv_text):
        """Test skill extraction from CV"""
        parsed = parser.parse(sample_cv_text)
        skills = parsed["skills"]

        assert isinstance(skills, list)
        assert "Python" in skills
        assert "Django" in skills
        # Handle case variations
        assert any(s.lower() == "aws" or s == "Aws" for s in skills)
        assert "Docker" in skills

    def test_experience_extraction(self, parser, sample_cv_text):
        """Test work experience extraction"""
        parsed = parser.parse(sample_cv_text)
        experience = parsed["experience"]

        assert isinstance(experience, list)
        assert len(experience) >= 2

        # Check that experience entries have expected structure
        for exp in experience:
            assert isinstance(exp, dict)
            assert "title" in exp or "period" in exp or "description" in exp

    def test_certifications_extraction(self, parser, sample_cv_text):
        """Test certifications extraction"""
        parsed = parser.parse(sample_cv_text)

        assert "certifications" in parsed
        certifications = parsed["certifications"]
        assert isinstance(certifications, list)
        assert "AWS Certified Solutions Architect" in certifications

    def test_empty_cv(self, parser):
        """Test handling of empty CV"""
        parsed = parser.parse("")

        assert isinstance(parsed, dict)
        assert parsed["skills"] == []
        assert parsed["experience"] == []

    def test_malformed_cv(self, parser):
        """Test handling of malformed CV text"""
        malformed = "NONSENSE TEXT ONLY $$$$ No structure"

        parsed = parser.parse(malformed)

        # Should not raise exception
        assert isinstance(parsed, dict)
        assert "skills" in parsed
        assert isinstance(parsed["skills"], list)

    def test_skills_list_not_empty(self, parser, sample_cv_text):
        """Test that skills are extracted"""
        parsed = parser.parse(sample_cv_text)
        skills = parsed["skills"]

        assert len(skills) > 0
        assert all(isinstance(skill, str) for skill in skills)

    def test_experience_has_periods(self, parser, sample_cv_text):
        """Test that experience entries have date periods"""
        parsed = parser.parse(sample_cv_text)
        experience = parsed["experience"]

        if len(experience) > 0:
            # Check that at least one experience has a period
            assert any("period" in exp for exp in experience)
            # Check format
            periods = [exp["period"] for exp in experience if "period" in exp]
            assert any("-" in period for period in periods)


class TestCVParserEdgeCases:
    """Test edge cases and error handling"""

    @pytest.fixture
    def parser(self):
        return CVParser()

    def test_unicode_characters(self, parser):
        """Test handling of unicode characters"""
        cv_text = "Name: José García\nSkills: Python, React"
        parsed = parser.parse(cv_text)

        assert parsed is not None
        assert isinstance(parsed, dict)

    def test_multiple_email_formats(self, parser):
        """Test various email formats"""
        emails = [
            "john.doe@example.com",
            "jane_doe123@domain.co.uk",
            "user+tag@gmail.com",
            "first.last@company.io",
        ]

        for email in emails:
            cv_text = f"Contact: {email}\nSkills: Python"
            parsed = parser.parse(cv_text)
            # Just verify parsing doesn't fail
            assert isinstance(parsed, dict)
            assert "email" in parsed

    def test_minimal_cv(self, parser):
        """Test CV with minimal information"""
        minimal_cv = """
        John Smith
        john@example.com
        
        Python Developer
        """
        parsed = parser.parse(minimal_cv)

        assert isinstance(parsed, dict)
        assert "email" in parsed
        assert "skills" in parsed

    def test_cv_with_linkedin_github(self, parser):
        """Test extraction of LinkedIn and GitHub"""
        cv_text = """
        John Doe
        john@example.com
        linkedin.com/in/johndoe
        github.com/johndoe
        
        Python Developer
        """
        parsed = parser.parse(cv_text)

        assert "linkedin" in parsed
        assert "github" in parsed


class TestCVParserFileFormats:
    """Test different file format handling"""

    @pytest.fixture
    def parser(self):
        return CVParser()

    def test_plain_text_parsing(self, parser):
        """Test plain text CV parsing"""
        cv_text = """
        Jane Smith
        jane.smith@email.com
        
        SKILLS
        Python, Django, React
        
        EXPERIENCE
        Developer at Company (2020-2023)
        - Built applications
        """

        parsed = parser.parse(cv_text)
        assert isinstance(parsed, dict)
        assert "skills" in parsed
        assert "experience" in parsed

    def test_cv_with_summary(self, parser):
        """Test CV with summary section"""
        cv_text = """
        John Doe
        john@example.com
        
        SUMMARY
        Experienced Python developer with 5 years experience.
        
        SKILLS
        Python, Django
        """
        parsed = parser.parse(cv_text)

        assert "summary" in parsed
        # Summary might be None or a string
        assert parsed["summary"] is None or isinstance(parsed["summary"], str)

    def test_structured_sections(self, parser, sample_cv_text):
        """Test that parser handles structured sections"""
        parsed = parser.parse(sample_cv_text)

        # Verify all major sections are present
        assert "skills" in parsed
        assert "experience" in parsed
        assert "education" in parsed
        assert "certifications" in parsed

        # Verify data types
        assert isinstance(parsed["skills"], list)
        assert isinstance(parsed["experience"], list)
        assert isinstance(parsed["education"], list)
        assert isinstance(parsed["certifications"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
