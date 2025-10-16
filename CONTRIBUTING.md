# Contributing to Advanced Job Engine

🎉 **Thank you for considering contributing!** This project aims to help job seekers worldwide achieve their career goals through data-driven preparation.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for everyone.

### Our Standards

**Positive behaviors:**
- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing viewpoints
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what's best for the community
- ✅ Showing empathy towards others

**Unacceptable behaviors:**
- ❌ Trolling, insulting comments, or personal attacks
- ❌ Public or private harassment
- ❌ Publishing others' private information
- ❌ Other conduct which could be considered inappropriate

---

## How Can I Contribute?

### 🐛 Reporting Bugs

**Before submitting:**
- Check [existing issues](https://github.com/yourusername/advanced-job-engine/issues)
- Use the latest version
- Test in a clean environment

**Bug report should include:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs. actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version)

**Template:**
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen.

**Environment:**
 - OS: [e.g., Ubuntu 22.04]
 - Python Version: [e.g., 3.9.5]
 - Version: [e.g., 1.0.0]

**Additional context**
Any other context about the problem.
```

### ✨ Suggesting Features

**Feature requests welcome for:**
- New analysis capabilities
- Additional learning resources
- Better automation
- UI/UX improvements
- Integration with other tools

**Template:**
```markdown
**Feature description**
Clear description of the feature.

**Problem it solves**
What user problem does this address?

**Proposed solution**
How should it work?

**Alternatives considered**
What other approaches did you think about?

**Additional context**
Screenshots, mockups, examples.
```

### 📚 Contributing Learning Resources

**High-value contributions:**

1. **Add new skills to resource database**
   ```python
   # In src/learning/resource_db.py
   "your_skill": {
       "study": [
           "Official Documentation",
           "Tutorial Site",
           "Reference Book"
       ],
       "practice": [
           "Practice Platform",
           "Coding Challenges",
           "Project Ideas"
       ],
       "courses": [
           "Course 1 (Platform)",
           "Course 2 (Platform)",
           "Certification Prep"
       ]
   }
   ```

2. **Improve existing resources**
   - Better course recommendations
   - More practice platforms
   - Updated learning paths

3. **Industry-specific templates**
   - Application letters for different fields
   - Networking messages for different industries

### 💻 Contributing Code

**Areas needing help:**
- 🔍 **Parsing**: Better CV/job extraction
- 📊 **Analysis**: Improved matching algorithms
- 🎨 **UI**: Dashboard, visualizations
- 🧪 **Testing**: More test coverage
- 📖 **Documentation**: Guides, examples
- 🌐 **Internationalization**: Multi-language support

### 📖 Improving Documentation

**Needed:**
- Industry-specific guides (finance, tech, healthcare)
- Video tutorials
- Translation to other languages
- More examples and use cases
- API documentation improvements

---

## Development Setup

### Prerequisites

```bash
# Python 3.9+
python --version

# Git
git --version
```

### Setup Steps

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/advanced-job-engine.git
cd advanced-job-engine

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/advanced-job-engine.git

# 4. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 5. Install in development mode
pip install -e ".[dev]"

# Or install from requirements
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 6. Install pre-commit hooks (optional but recommended)
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_cv_parser.py

# Run with verbose output
pytest -v
```

### Code Quality Checks

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/

# Run all checks
pre-commit run --all-files
```

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes
# ... edit files ...

# 3. Test your changes
pytest
python src/python_advanced_job_engine.py  # Manual test

# 4. Commit changes
git add .
git commit -m "feat: add amazing feature"

# 5. Keep your branch updated
git fetch upstream
git rebase upstream/main

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Open Pull Request on GitHub
```

---

## Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Changelog updated (if applicable)

### PR Title Convention

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `style:` Code style (formatting, no logic change)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: add support for LinkedIn job scraping
fix: correct experience calculation in parser
docs: add tutorial for reverse workflow
test: add integration tests for sprint manager
```

### PR Description Template

```markdown
## Description
Clear description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
Describe testing you've done:
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Related Issues
Closes #(issue number)
```

### Review Process

1. **Automated Checks**: CI/CD runs tests
2. **Code Review**: Maintainers review code
3. **Feedback**: Address review comments
4. **Approval**: 1+ maintainer approval required
5. **Merge**: Maintainer merges PR

**Timeline:**
- First review: Within 3 days
- Follow-up reviews: Within 2 days
- Merge: After approval and CI passes

---

## Style Guidelines

### Python Code Style

**Follow PEP 8 with these specifics:**

```python
# Imports: Standard library → Third party → Local
import os
import sys
from pathlib import Path

import pandas as pd
import requests

from src.analyzers import cv_parser
from src.utils import file_readers

# Line length: 88 characters (Black default)

# Function naming: snake_case
def calculate_match_score(cv_data, job_data):
    pass

# Class naming: PascalCase
class AdvancedJobEngine:
    pass

# Constants: UPPER_CASE
MAX_SCORE = 100
DEFAULT_WEIGHTS = {...}

# Private methods: leading underscore
def _internal_helper():
    pass

# Docstrings: Google style
def analyze_job(cv_text: str, job_text: str) -> Dict:
    """
    Analyze job match between CV and job description.
    
    Args:
        cv_text: Full CV text content
        job_text: Full job description text
        
    Returns:
        Dictionary containing analysis results with score,
        gaps, and recommendations.
        
    Raises:
        ValueError: If input text is empty
        
    Example:
        >>> analysis = analyze_job(cv, job)
        >>> print(analysis['score']['total_score'])
        75.5
    """
    pass

# Type hints: Use for function signatures
def process_data(
    items: List[str], 
    threshold: float = 0.5
) -> Tuple[List[str], int]:
    pass
```

### Commit Message Guidelines

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```bash
# Good
git commit -m "feat(parser): add support for PDF extraction"
git commit -m "fix(matcher): correct experience scoring logic"
git commit -m "docs(readme): update installation instructions"

# With body
git commit -m "feat(learning): add AI-powered resource recommendations

Implement machine learning model to suggest personalized
learning resources based on user's learning history and
job requirements. Uses collaborative filtering.

Closes #123"
```

### Documentation Style

**README sections:**
- Clear, concise language
- Code examples that work
- Visual aids (screenshots, diagrams)
- Step-by-step instructions

**Code comments:**
```python
# Good: Explain WHY, not WHAT
# Calculate weighted score to prioritize required skills over preferred
weighted_score = sum(scores[k] * weights[k] for k in scores)

# Bad: States the obvious
# Loop through scores
for score in scores:
    ...
```

**API documentation:**
```python
def create_learning_plan(
    self, 
    analysis: Dict, 
    mode: str = "standard"
) -> Dict:
    """
    Create personalized learning plan based on job analysis.
    
    Generates a structured learning plan with three levels
    (study, practice, courses) and weekly schedules tailored
    to bridge the skill gap identified in the analysis.
    
    Args:
        analysis: Job analysis dictionary from analyze_job_complete()
        mode: Learning mode - "standard" (12 weeks) or 
              "reverse" (16-24 weeks, sprint-based)
              
    Returns:
        Dictionary containing:
            - plan_id: Unique identifier
            - levels: Dict with 'study', 'practice', 'courses' lists
            - weekly_schedule: List of weekly activities
            - milestones: List of milestone definitions
            - estimated_duration: String like "12 weeks"
            
    Example:
        >>> analysis = engine.analyze_job_complete(cv, job)
        >>> plan = engine.create_learning_plan(analysis, "standard")
        >>> print(f"Duration: {plan['estimated_duration']}")
        Duration: 12 weeks
    """
```

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general discussion
- **Discord** (coming soon): Real-time chat
- **Email**: contact@yourproject.com

### Recognition

**Contributors are recognized in:**
- README.md contributors section
- CHANGELOG.md for each release
- Project website (coming soon)

**Special recognition for:**
- 🌟 First-time contributors
- 🏆 Significant features
- 📚 Major documentation improvements
- 🐛 Critical bug fixes

### Becoming a Maintainer

**Path to maintainer status:**
1. Consistent quality contributions
2. Help review PRs
3. Support community members
4. Demonstrate expertise in project areas

**Responsibilities:**
- Review and merge PRs
- Triage issues
- Guide contributors
- Maintain code quality

---

## Areas Needing Contributions

### 🔥 High Priority

1. **Multi-language Support**
   - Translate to Spanish, French, German, Chinese
   - Internationalize UI strings
   - Localized learning resources

2. **Industry Templates**
   - Finance/banking job analysis
   - Healthcare-specific skills
   - Manufacturing/engineering
   - Government/public sector

3. **Enhanced Parsing**
   - Better PDF extraction (preserve formatting)
   - Handle scanned documents (OCR)
   - Parse LinkedIn profiles
   - Extract from Word documents more reliably

4. **Test Coverage**
   - Unit tests for all modules (target: 80%+)
   - Integration tests for workflows
   - Edge case testing

### 💡 Good First Issues

**Beginner-friendly tasks:**
- Add learning resources for popular skills
- Fix typos in documentation
- Add examples to README
- Improve error messages
- Add missing docstrings

**Tag: `good first issue`**

### 🚀 Advanced Contributions

**For experienced developers:**
- Machine learning integration
- Web dashboard (React/Vue)
- Mobile app (React Native/Flutter)
- API service
- Database integration
- LinkedIn/job board scrapers

---

## Development Resources

### Useful Tools

**Code Quality:**
- [Black](https://black.readthedocs.io/): Code formatter
- [Flake8](https://flake8.pycqa.org/): Style checker
- [MyPy](http://mypy-lang.org/): Type checker
- [Pytest](https://pytest.org/): Testing framework

**Documentation:**
- [MkDocs](https://www.mkdocs.org/): Documentation generator
- [Sphinx](https://www.sphinx-doc.org/): API documentation

**CI/CD:**
- GitHub Actions for automation
- Pre-commit hooks for local checks

### Learning Resources

**Python Best Practices:**
- [Real Python](https://realpython.com/)
- [Python Guide](https://docs.python-guide.org/)
- [PEP 8](https://pep8.org/)

**Testing:**
- [Pytest Documentation](https://docs.pytest.org/)
- [Test-Driven Development](https://testdriven.io/)

**Git:**
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

## Questions?

**Need help?**
- 📖 Check [documentation](docs/)
- 💬 Ask in [Discussions](https://github.com/yourusername/advanced-job-engine/discussions)
- 📧 Email: dev@yourproject.com

**Response time:**
- Questions: Within 24-48 hours
- PRs: First review within 3 days
- Issues: Triaged within 2 days

---

## Thank You! 🙏

Every contribution, no matter how small, helps job seekers worldwide. Thank you for being part of this mission!

**Your contributions help:**
- 👔 Job seekers land better roles
- 📈 Career changers transition successfully
- 🎓 Recent graduates get first jobs
- 🌍 People worldwide access quality career tools

---

<div align="center">

**Made with ❤️ by contributors like you**

[Back to README](README.md) | [Code of Conduct](CODE_OF_CONDUCT.md) | [License](LICENSE)

</div>
