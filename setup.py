#!/usr/bin/env python3
"""
Setup script for Advanced Job Engine

This setup.py is maintained for backwards compatibility.
Modern installations should use pyproject.toml.
"""

import os
import sys
from pathlib import Path
from setuptools import setup, find_packages

# Ensure minimum Python version
if sys.version_info < (3, 8):
    sys.exit("Python 3.8 or higher is required.")

# Read the long description from README
here = Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

# Read version from a version file or module
def get_version():
    """Get version from package."""
    version_file = here / "src" / "__init__.py"
    if version_file.exists():
        with open(version_file, encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"

# Core dependencies
INSTALL_REQUIRES = [
    "PyPDF2>=3.0.0",
    "python-docx>=0.8.11",
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "jinja2>=3.1.0",
    "click>=8.1.0",
    "rich>=13.0.0",
    "tabulate>=0.9.0",
]

# Development dependencies
DEV_REQUIRES = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-xdist>=3.3.0",
    "pytest-mock>=3.11.0",
    "black>=23.7.0",
    "flake8>=6.1.0",
    "pylint>=2.17.0",
    "mypy>=1.5.0",
    "isort>=5.12.0",
    "pre-commit>=3.3.0",
]

# Documentation dependencies
DOCS_REQUIRES = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
    "sphinx-autodoc-typehints>=1.24.0",
    "myst-parser>=2.0.0",
]

# Test dependencies
TEST_REQUIRES = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-xdist>=3.3.0",
    "pytest-mock>=3.11.0",
    "coverage>=7.3.0",
]

# Extra dependencies
EXTRAS_REQUIRE = {
    "dev": DEV_REQUIRES,
    "docs": DOCS_REQUIRES,
    "test": TEST_REQUIRES,
    "all": DEV_REQUIRES + DOCS_REQUIRES + TEST_REQUIRES,
}

setup(
    # Basic package information
    name="advanced-job-engine",
    version=get_version(),
    description="Advanced Job Engine for CV analysis, skill gap identification, and career development planning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Author information
    author="Your Name",
    author_email="your.email@example.com",
    
    # URLs
    url="https://github.com/yourusername/advanced-job-engine",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/advanced-job-engine/issues",
        "Documentation": "https://advanced-job-engine.readthedocs.io",
        "Source Code": "https://github.com/yourusername/advanced-job-engine",
        "Changelog": "https://github.com/yourusername/advanced-job-engine/blob/main/CHANGELOG.md",
    },
    
    # Package discovery
    packages=find_packages(exclude=["tests", "tests.*", "docs", "examples"]),
    package_dir={"": "."},
    
    # Include additional files
    package_data={
        "": ["*.txt", "*.md", "*.json", "*.yaml", "*.yml"],
    },
    include_package_data=True,
    
    # Dependencies
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    
    # Entry points for command-line scripts
    entry_points={
        "console_scripts": [
            "job-engine=src.python_advanced_job_engine:main",
            "job-analyze=src.python_advanced_job_engine:analyze_job",
            "job-export=src.python_advanced_job_engine:export_results",
        ],
    },
    
    # Package classification
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Office/Business",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    
    # Keywords for PyPI
    keywords=[
        "job-search",
        "cv-analysis",
        "skill-matching",
        "career-development",
        "learning-plan",
        "automation",
        "job-application",
        "resume",
        "recruitment",
    ],
    
    # License
    license="MIT",
    
    # Zip safe
    zip_safe=False,
)
