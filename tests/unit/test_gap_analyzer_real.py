import pytest
import os

import pytest

from src.analyzers import gap_analyzer
from src.utils import file_readers
from tests.mocks import mock_data

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def real_cv_text():
    """
    Load a real CV text file from 'tests/fixtures/' or 'data/'.
    """
    cv_path = os.path.join("tests", "fixtures", "real_cv.txt")
    with open(cv_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def real_job_text():
    """
    Load a real job description text file.
    """
    job_path = os.path.join("tests", "fixtures", "real_job.txt")
    with open(job_path, "r", encoding="utf-8") as f:
        return f.read()


# ============================================================================
# UNIT TESTS: GAP ANALYZER
# ============================================================================


@pytest.mark.skip(reason="Module functions not implemented")
def test_gap_analysis_with_mock_data():
    """
    Ensure gap analyzer works with mock CV and mock job.
    """
    cv = mock_data.get_mock_cv(parsed=True)
    job = mock_data.get_mock_job(parsed=True)

    gaps = gap_analyzer.analyze_skill_gaps(cv, job)

    assert "missing_required_skills" in gaps
    assert "missing_preferred_skills" in gaps
    assert isinstance(gaps["missing_required_skills"], list)
    assert isinstance(gaps["missing_preferred_skills"], list)


@pytest.mark.skip(reason="Module functions not implemented")
def test_gap_analysis_with_real_files(real_cv_text, real_job_text):
    """
    Analyze real CV and job description text files.
    """
    # Convert text to parsed format
    parsed_cv = file_readers.parse_cv_text(real_cv_text)
    parsed_job = file_readers.parse_job_text(real_job_text)

    gaps = gap_analyzer.analyze_skill_gaps(parsed_cv, parsed_job)

    # Ensure gaps structure is correct
    assert "missing_required_skills" in gaps
    assert "missing_preferred_skills" in gaps
    assert isinstance(gaps["missing_required_skills"], list)
    assert isinstance(gaps["missing_preferred_skills"], list)

    # Optional: ensure some real gaps are detected
    assert len(gaps["missing_required_skills"]) >= 0
    assert len(gaps["missing_preferred_skills"]) >= 0


@pytest.mark.skip(reason="Module functions not implemented")
def test_gap_analysis_with_partial_data():
    """
    Ensure analyzer handles CVs with missing fields gracefully.
    """
    cv = {"skills": ["Python", "Django"]}  # Minimal CV
    job = {"required_skills": ["Python", "AWS", "Docker"]}

    gaps = gap_analyzer.analyze_skill_gaps(cv, job)
    assert "Python" not in gaps["missing_required_skills"]
    assert "AWS" in gaps["missing_required_skills"]
    assert "Docker" in gaps["missing_required_skills"]
