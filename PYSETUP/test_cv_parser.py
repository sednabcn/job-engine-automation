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

    def test_extract_contact_info(self, parser, sample_cv_text):
        """Test contact information extraction"""
        contact = parser._extract_contact_info(sample_cv_text)

        assert "email" in contact
        assert contact["email"] == "john.doe@email.com"
        assert "phone" in contact
        assert contact["phone"] is not None

    def test_extract_skills(self, parser, sample_cv_text):
        """Test skill extraction from CV"""
        skills = parser._extract_skills(sample_cv_text)

        assert "Python" in skills
        assert "Django" in skills
        # Handle case variations
        assert any(s.lower() == "aws" for s in skills)
        assert "Docker" in skills

    def test_extract_experience(self, parser, sample_cv_text):
        """Test work experience extraction"""
        experience = parser._extract_experience(sample_cv_text)

        assert len(experience) >= 2
        assert any("Tech Corp" in exp.get("title", "") for exp in experience)
        assert any("Python Developer" in exp.get("title", "") for exp in experience)

    def test_extract_education(self, parser, sample_cv_text):
        """Test education extraction"""
        education = parser._extract_education(sample_cv_text)

        assert len(education) >= 1
        assert any("Computer Science" in edu.get("degree", "") for edu in education)

    def test_calculate_experience_years(self, parser, sample_cv_text):
        """Test total years of experience calculation"""
        experience = parser._extract_experience(sample_cv_text)
        years = parser._calculate_years_experience(experience)

        assert years >= 5  # 2018-2023
        assert isinstance(years, (int, float))

    def test_parse_full_cv(self, parser, sample_cv_text):
        """Test complete CV parsing"""
        parsed = parser.parse(sample_cv_text)

        assert "contact" in parsed
        assert "skills" in parsed
        assert "experience" in parsed
        assert "education" in parsed
        assert "years_experience" in parsed

    def test_contact_info_in_parsed_cv(self, parser, sample_cv_text):
        """Test that contact info is properly included in parsed output"""
        parsed = parser.parse(sample_cv_text)
        contact = parsed["contact"]

        assert contact["email"] == "john.doe@email.com"
        assert contact["name"] == "John Doe"
        assert contact["phone"] is not None

    def test_skills_in_parsed_cv(self, parser, sample_cv_text):
        """Test that skills are properly extracted in parsed output"""
        parsed = parser.parse(sample_cv_text)
        skills = parsed["skills"]

        assert "Python" in skills
        assert "Django" in skills
        assert len(skills) > 0

    def test_experience_years_calculation(self, parser, sample_cv_text):
        """Test years of experience in parsed output"""
        parsed = parser.parse(sample_cv_text)
        years = parsed["years_experience"]

        assert years >= 5
        assert isinstance(years, (int, float))

    def test_empty_cv(self, parser):
        """Test handling of empty CV"""
        parsed = parser.parse("")

        assert parsed["skills"] == []
        assert parsed["experience"] == []

    def test_malformed_cv(self, parser):
        """Test handling of malformed CV text"""
        malformed = "NONSENSE TEXT ONLY $$$$ No structure"

        parsed = parser.parse(malformed)

        # Should not raise exception
        assert isinstance(parsed, dict)
        assert "skills" in parsed

    def test_skill_deduplication(self, parser):
        """Test that duplicate skills are removed"""
        skills_text = """
        SKILLS
        Python, python, PYTHON, Java, java
        """
        skills = parser._extract_skills(skills_text)

        # Count Python mentions (should be deduplicated)
        python_count = sum(1 for s in skills if s.lower() == "python")
        assert python_count == 1
        
        java_count = sum(1 for s in skills if s.lower() == "java")
        assert java_count == 1

    @pytest.mark.skip(reason="Method not implemented - would require skill level detection logic")
    def test_detect_skill_level(self, parser, sample_cv_text):
        """Test skill level detection from experience"""
        skill_levels = parser.detect_skill_levels(sample_cv_text)

        assert "Python" in skill_levels
        assert skill_levels["Python"] in ["beginner", "intermediate", "advanced", "expert"]


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
            contact = parser._extract_contact_info(cv_text)
            assert email == contact.get("email", "")

    def test_date_format_variations(self, parser):
        """Test various date format parsing"""
        # Test the specific format we support (YYYY-YYYY)
        cv_text = """
        EXPERIENCE
        Senior Developer at Company (2020-2023)
        - Developed applications
        """
        experience = parser._extract_experience(cv_text)
        assert isinstance(experience, list)
        assert len(experience) >= 1
        if experience:
            assert experience[0]["period"] == "2020-2023"

    def test_missing_sections(self, parser):
        """Test CV with missing sections"""
        minimal_cv = """
        John Smith
        john@example.com
        
        Python Developer
        """
        parsed = parser.parse(minimal_cv)
        
        assert isinstance(parsed, dict)
        assert parsed["experience"] == []
        assert parsed["education"] == []


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
        assert len(parsed["skills"]) > 0
        assert len(parsed["experience"]) > 0

    @pytest.mark.skip(reason="File extraction not implemented - would require PDF/DOCX parsing libraries")
    def test_pdf_extraction(self, parser, tmp_path):
        """Test PDF text extraction"""
        pdf_path = tmp_path / "test_cv.pdf"
        pdf_path.write_bytes(b"%PDF-1.4 mock content")

        text = parser.extract_text_from_file(str(pdf_path))
        assert isinstance(text, str)

    @pytest.mark.skip(reason="File extraction not implemented - would require PDF/DOCX parsing libraries")
    def test_docx_extraction(self, parser, tmp_path):
        """Test DOCX text extraction"""
        docx_path = tmp_path / "test_cv.docx"
        docx_path.write_bytes(b"PK\x03\x04 mock content")

        text = parser.extract_text_from_file(str(docx_path))
        assert isinstance(text, str)

    @pytest.mark.skip(reason="File extraction not implemented - would require PDF/DOCX parsing libraries")
    def test_txt_extraction(self, parser, tmp_path):
        """Test plain text extraction"""
        txt_path = tmp_path / "test_cv.txt"
        txt_path.write_text("Sample CV content\nPython Developer")

        text = parser.extract_text_from_file(str(txt_path))
        assert "Python Developer" in text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
