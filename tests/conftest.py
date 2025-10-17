"""
conftest.py - Pytest configuration and shared fixtures
"""

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest

# ======================================================
# Fixtures Overview
# ======================================================
# 1. Path Fixtures - Access to project directories
# 2. File Fixtures - Easy access to sample files
# 3. Temporary Directory Fixtures - Clean test environments
# 4. Mock Data Fixtures - Pre-configured test data
# 5. Environment Fixtures - Control environment variables
# 6. File Creation Helpers - Create test files on the fly
# 7. Pytest Configuration - Custom markers and auto-marking
# 8. Session Cleanup - Automatic cleanup after tests

# ============================================================================
# PATH FIXTURES
# ============================================================================


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def fixtures_dir(project_root) -> Path:
    """Return the fixtures directory path."""
    return project_root / "tests" / "fixtures"


@pytest.fixture(scope="session")
def data_dir(project_root) -> Path:
    """Return the data directory path."""
    return project_root / "data"


@pytest.fixture(scope="session")
def templates_dir(project_root) -> Path:
    """Return the templates directory path."""
    return project_root / "templates"


# ============================================================================
# FILE FIXTURES
# ============================================================================


@pytest.fixture(scope="session")
def sample_cv_path(fixtures_dir) -> Path:
    """Return path to sample CV file."""
    return fixtures_dir / "sample_cv.txt"


@pytest.fixture(scope="session")
def sample_job_path(fixtures_dir) -> Path:
    """Return path to sample job description file."""
    return fixtures_dir / "sample_job.txt"


@pytest.fixture(scope="session")
def sample_data_path(fixtures_dir) -> Path:
    """Return path to sample data JSON file."""
    return fixtures_dir / "sample_data.json"


@pytest.fixture
def sample_cv_text(sample_cv_path) -> str:
    """Load and return sample CV text content."""
    with open(sample_cv_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def sample_job_text(sample_job_path) -> str:
    """Load and return sample job description text content."""
    with open(sample_job_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def sample_data_json(sample_data_path) -> Dict[str, Any]:
    """Load and return sample data as dictionary."""
    with open(sample_data_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================================
# TEMPORARY DIRECTORY FIXTURES
# ============================================================================


@pytest.fixture
def temp_dir() -> Path:
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def temp_data_dir(temp_dir) -> Path:
    """Create a temporary data directory structure."""
    data_path = temp_dir / "job_search_data"
    data_path.mkdir(exist_ok=True)
    return data_path


@pytest.fixture
def temp_output_dir(temp_dir) -> Path:
    """Create a temporary output directory."""
    output_path = temp_dir / "output"
    output_path.mkdir(exist_ok=True)
    return output_path


# ============================================================================
# MOCK DATA FIXTURES
# ============================================================================


@pytest.fixture
def mock_cv_data() -> Dict[str, Any]:
    """Return mock CV data structure."""
    return {
        "name": "John Doe",
        "email": "john.doe@email.com",
        "phone": "+1-555-0123",
        "location": "San Francisco, CA",
        "summary": "Experienced Software Engineer with 5+ years of expertise",
        "skills": {
            "programming_languages": ["Python", "JavaScript", "TypeScript", "Java", "SQL"],
            "frameworks": ["Django", "Flask", "React", "Node.js", "Express"],
            "databases": ["PostgreSQL", "MongoDB", "Redis", "MySQL"],
            "cloud_devops": ["AWS", "Docker", "Kubernetes", "CI/CD", "GitHub Actions"],
        },
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "TechCorp Inc.",
                "location": "San Francisco, CA",
                "start_date": "June 2021",
                "end_date": "Present",
                "responsibilities": [
                    "Led development of microservices architecture",
                    "Designed and implemented RESTful APIs",
                    "Mentored team of 4 junior developers",
                ],
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Science in Computer Science",
                "institution": "University of California, Berkeley",
                "graduation_year": "2017",
                "gpa": "3.7/4.0",
            }
        ],
        "certifications": [
            "AWS Certified Solutions Architect - Associate",
            "Professional Scrum Master I (PSM I)",
        ],
    }


@pytest.fixture
def mock_job_data() -> Dict[str, Any]:
    """Return mock job description data structure."""
    return {
        "title": "Senior Full Stack Engineer",
        "company": "InnovateTech Solutions",
        "location": "San Francisco, CA",
        "employment_type": "Full-time",
        "salary_range": "$140,000 - $180,000",
        "required_skills": [
            "Python",
            "JavaScript",
            "React",
            "PostgreSQL",
            "MongoDB",
            "Redis",
            "AWS",
            "Docker",
            "Git",
            "CI/CD",
            "Microservices",
            "RESTful API",
            "Data Structures",
            "Algorithms",
        ],
        "preferred_skills": [
            "TypeScript",
            "GraphQL",
            "Kubernetes",
            "Event-driven architecture",
            "RabbitMQ",
            "Kafka",
            "Jest",
            "Pytest",
            "Selenium",
            "OWASP",
            "Fintech experience",
            "Open source contributions",
        ],
        "responsibilities": [
            "Design, develop, and maintain scalable full-stack applications",
            "Write clean, maintainable, and well-tested code",
            "Participate in architectural decisions",
            "Mentor junior team members",
        ],
        "requirements": {
            "years_experience": 5,
            "education": "Bachelor's degree in Computer Science or related field",
        },
    }


@pytest.fixture
def mock_skillset() -> Dict[str, Any]:
    """Return mock master skillset."""
    return {
        "technical_skills": {
            "programming_languages": [
                {"name": "Python", "proficiency": "expert", "years": 5},
                {"name": "JavaScript", "proficiency": "advanced", "years": 5},
                {"name": "TypeScript", "proficiency": "intermediate", "years": 2},
            ],
            "frameworks": [
                {"name": "Django", "proficiency": "expert", "years": 4},
                {"name": "React", "proficiency": "advanced", "years": 4},
            ],
            "databases": [
                {"name": "PostgreSQL", "proficiency": "advanced", "years": 4},
                {"name": "MongoDB", "proficiency": "intermediate", "years": 3},
            ],
            "cloud_devops": [
                {"name": "AWS", "proficiency": "advanced", "years": 3},
                {"name": "Docker", "proficiency": "advanced", "years": 3},
            ],
        },
        "soft_skills": ["Team Leadership", "Technical Documentation", "Code Review", "Mentoring"],
    }


@pytest.fixture
def mock_match_result() -> Dict[str, Any]:
    """Return mock job matching result."""
    return {
        "job_id": "job_001",
        "match_score": 82,
        "required_skills_matched": 18,
        "required_skills_total": 20,
        "preferred_skills_matched": 6,
        "preferred_skills_total": 12,
        "skill_gaps": ["GraphQL", "Event-driven architecture", "Kafka"],
        "strong_matches": ["Python", "JavaScript", "React", "PostgreSQL", "AWS"],
        "recommendations": [
            "Learn GraphQL to improve match score",
            "Gain experience with message queues",
        ],
    }


@pytest.fixture
def mock_learning_plan() -> Dict[str, Any]:
    """Return mock learning plan."""
    return {
        "skill_gaps": [
            {
                "skill": "GraphQL",
                "priority": "high",
                "estimated_hours": 20,
                "resources": ["GraphQL official tutorial", "How to GraphQL course"],
            },
            {
                "skill": "Kubernetes",
                "priority": "medium",
                "estimated_hours": 30,
                "resources": [
                    "Kubernetes official documentation",
                    "Kubernetes for Developers course",
                ],
            },
        ],
        "sprint_plan": {
            "sprint_1": {
                "duration_weeks": 2,
                "goals": ["Learn GraphQL basics", "Build sample project"],
                "skills": ["GraphQL"],
            },
            "sprint_2": {
                "duration_weeks": 2,
                "goals": ["Complete Kubernetes fundamentals"],
                "skills": ["Kubernetes"],
            },
        },
        "total_estimated_hours": 50,
        "estimated_weeks": 4,
    }


@pytest.fixture
def mock_sprint_data() -> Dict[str, Any]:
    """Return mock sprint data."""
    return {
        "sprint_number": 1,
        "start_date": "2024-10-01",
        "end_date": "2024-10-15",
        "goals": ["Learn GraphQL basics", "Complete Kubernetes fundamentals"],
        "skills": ["GraphQL", "Kubernetes"],
        "progress": {"GraphQL": 35, "Kubernetes": 15},
        "status": "in_progress",
    }


# ============================================================================
# ENVIRONMENT FIXTURES
# ============================================================================


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set mock environment variables."""
    test_env = {
        "JOB_ENGINE_DEBUG": "true",
        "JOB_ENGINE_OUTPUT_DIR": "/tmp/test_output",
        "JOB_ENGINE_DATA_DIR": "/tmp/test_data",
    }
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    return test_env


@pytest.fixture
def clean_env(monkeypatch):
    """Remove all JOB_ENGINE_* environment variables."""
    env_vars = [key for key in os.environ if key.startswith("JOB_ENGINE_")]
    for var in env_vars:
        monkeypatch.delenv(var, raising=False)


# ============================================================================
# FILE CREATION HELPERS
# ============================================================================


@pytest.fixture
def create_test_file():
    """Factory fixture to create test files."""

    created_files = []

    def _create_file(path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        created_files.append(path)
        return path

    yield _create_file

    # Cleanup
    for file_path in created_files:
        if file_path.exists():
            file_path.unlink()


@pytest.fixture
def create_test_json():
    """Factory fixture to create test JSON files."""

    created_files = []

    def _create_json(path: Path, data: Dict[str, Any]):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        created_files.append(path)
        return path

    yield _create_json

    # Cleanup
    for file_path in created_files:
        if file_path.exists():
            file_path.unlink()


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================


def pytest_configure(config):
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "requires_files: mark test as requiring external files")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Auto-mark tests based on their location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)


# ============================================================================
# SESSION CLEANUP
# ============================================================================


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_artifacts():
    """Clean up any test artifacts after test session."""
    yield
    test_dirs = [Path("/tmp/test_output"), Path("/tmp/test_data")]
    for test_dir in test_dirs:
        if test_dir.exists():
            shutil.rmtree(test_dir, ignore_errors=True)
