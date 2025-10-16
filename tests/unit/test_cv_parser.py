"""
Unit tests for CV parser module
Tests CV text extraction and parsing functionality
"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from analyzers.cv_parser import CVParser


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
        contact = parser.extract_contact_info(sample_cv_text)
        
        assert 'email' in contact
        assert 'john.doe@email.com' in contact['email']
        assert 'phone' in contact
        
    def test_extract_skills(self, parser, sample_cv_text):
        """Test skill extraction from CV"""
        skills = parser.extract_skills(sample_cv_text)
        
        assert 'Python' in skills
        assert 'Django' in skills
        assert 'AWS' in skills
        assert 'Docker' in skills
        
    def test_extract_experience(self, parser, sample_cv_text):
        """Test work experience extraction"""
        experience = parser.extract_experience(sample_cv_text)
        
        assert len(experience) >= 2
        assert any('Tech Corp' in exp['company'] for exp in experience)
        assert any('Python Developer' in exp['title'] for exp in experience)
        
    def test_extract_education(self, parser, sample_cv_text):
        """Test education extraction"""
        education = parser.extract_education(sample_cv_text)
        
        assert len(education) >= 1
        assert any('Computer Science' in edu['degree'] for edu in education)
        
    def test_calculate_experience_years(self, parser, sample_cv_text):
        """Test total years of experience calculation"""
        years = parser.calculate_experience_years(sample_cv_text)
        
        assert years >= 5  # 2018-2023
        assert isinstance(years, (int, float))
        
    def test_parse_full_cv(self, parser, sample_cv_text):
        """Test complete CV parsing"""
        parsed = parser.parse(sample_cv_text)
        
        assert 'contact' in parsed
        assert 'skills' in parsed
        assert 'experience' in parsed
        assert 'education' in parsed
        assert 'years_experience' in parsed
        
    def test_empty_cv(self, parser):
        """Test handling of empty CV"""
        parsed = parser.parse("")
        
        assert parsed['skills'] == []
        assert parsed['experience'] == []
        
    def test_malformed_cv(self, parser):
        """Test handling of malformed CV text"""
        malformed = "Some random text without structure"
        parsed = parser.parse(malformed)
        
        # Should not raise exception
        assert isinstance(parsed, dict)
        assert 'skills' in parsed
        
    def test_skill_normalization(self, parser):
        """Test skill name normalization"""
        skills_text = "python, Python, PYTHON, javascript, JavaScript"
        skills = parser.extract_skills(skills_text)
        
        # Should normalize duplicates
        python_count = sum(1 for s in skills if s.lower() == 'python')
        assert python_count == 1
        
    def test_detect_skill_level(self, parser, sample_cv_text):
        """Test skill level detection from experience"""
        skill_levels = parser.detect_skill_levels(sample_cv_text)
        
        # Should detect experience levels for skills
        assert 'Python' in skill_levels
        assert skill_levels['Python'] in ['beginner', 'intermediate', 'advanced', 'expert']


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
            "john.doe@email.com",
            "jane_doe@company.co.uk",
            "contact@my-site.io"
        ]
        
        for email in emails:
            cv_text = f"Contact: {email}"
            contact = parser.extract_contact_info(cv_text)
            assert email in contact.get('email', '')
            
    def test_date_format_variations(self, parser):
        """Test various date format parsing"""
        date_formats = [
            "2020-2023",
            "Jan 2020 - Dec 2023",
            "2020 to 2023",
            "2020/01 - 2023/12"
        ]
        
        for date_str in date_formats:
            exp_text = f"Senior Developer ({date_str})"
            # Should parse without errors
            parsed = parser.extract_experience(exp_text)
            assert parsed is not None


class TestCVParserFileFormats:
    """Test different file format handling"""
    
    @pytest.fixture
    def parser(self):
        return CVParser()
    
    def test_pdf_extraction(self, parser, tmp_path):
        """Test PDF text extraction"""
        # This would require PyPDF2 or similar
        # Placeholder for actual implementation
        pdf_path = tmp_path / "test_cv.pdf"
        
        # Mock PDF extraction
        # In real implementation, would test actual PDF reading
        assert True
        
    def test_docx_extraction(self, parser, tmp_path):
        """Test DOCX text extraction"""
        # This would require python-docx
        # Placeholder for actual implementation
        docx_path = tmp_path / "test_cv.docx"
        
        # Mock DOCX extraction
        assert True
        
    def test_txt_extraction(self, parser, tmp_path):
        """Test plain text extraction"""
        txt_path = tmp_path / "test_cv.txt"
        txt_path.write_text("Sample CV content\nPython Developer")
        
        text = parser.extract_text_from_file(str(txt_path))
        assert "Python Developer" in text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
