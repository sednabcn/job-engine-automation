# Pytest Organization Guide

## Directory Structure Strategy

```
tests/
├── conftest.py                 # Shared fixtures (already created)
│
├── unit/                       # Fast, isolated tests
│   ├── test_cv_parser.py      # CV parsing logic
│   ├── test_job_parser.py     # Job parsing logic
│   ├── test_matcher.py        # Matching algorithm
│   ├── test_gap_analyzer.py   # Gap analysis
│   ├── test_plan_generator.py # Learning plan generation
│   ├── test_sprint_manager.py # Sprint management
│   ├── test_report_generator.py # Report generation
│   └── test_file_readers.py   # File I/O utilities
│
├── integration/                # Multi-component tests
│   ├── test_full_workflow.py  # Complete analysis workflow
│   ├── test_reverse_workflow.py # Reverse mode workflow
│   ├── test_data_persistence.py # State management
│   └── test_learning_system.py # Learning plan → tracking
│
├── fixtures/                   # Test data files
│   ├── sample_cv.txt
│   ├── sample_job.txt
│   └── sample_data.json
│
└── mocks/                      # Mock objects
    └── mock_data.py
```

## Test Naming Convention

### Files
- `test_<module_name>.py` - e.g., `test_cv_parser.py`
- Group related tests in same file

### Classes (Optional)
- `Test<FeatureName>` - e.g., `TestCVParser`
- Use for grouping related test methods

### Functions
- `test_<what_it_tests>` - descriptive names
- Examples:
  - `test_parse_cv_extracts_skills`
  - `test_matcher_calculates_score_correctly`
  - `test_invalid_input_raises_error`

## Test Structure Pattern

```python
# AAA Pattern: Arrange, Act, Assert

def test_feature_name(fixture1, fixture2):
    """Brief description of what's being tested"""
    # Arrange - Set up test data
    input_data = {"key": "value"}
    
    # Act - Execute the code being tested
    result = function_under_test(input_data)
    
    # Assert - Verify the results
    assert result == expected_value
    assert "key" in result
```

## Efficient Test Running Workflow

### 1. Development (Fast Feedback)
```bash
# Run only fast unit tests
make test-unit

# Or specific module you're working on
make test-file FILE=tests/unit/test_matcher.py

# Watch mode (auto-rerun on changes)
make test-watch
```

### 2. Before Commit (Quick Check)
```bash
# Run fast tests + smoke tests
make test-fast
make test-smoke
```

### 3. Before Push (Comprehensive)
```bash
# Run all tests with coverage
make test-cov
```

### 4. CI/CD (Full Suite)
```bash
# Run everything including slow tests
make test
```

## Marking Tests for Efficiency

```python
import pytest

# Mark slow tests
@pytest.mark.slow
def test_large_file_processing():
    """This test takes >5 seconds"""
    pass

# Mark by module
@pytest.mark.cv_parser
def test_cv_parsing():
    pass

# Mark smoke tests (critical paths)
@pytest.mark.smoke
def test_basic_workflow_works():
    """Ensure core functionality works"""
    pass

# Combine markers
@pytest.mark.integration
@pytest.mark.slow
def test_full_workflow():
    pass
```

## Parametrized Tests (DRY Principle)

```python
@pytest.mark.parametrize("input_val,expected", [
    ("Python", True),
    ("Java", True),
    ("", False),
    (None, False),
])
def test_skill_validation(input_val, expected):
    assert validate_skill(input_val) == expected
```

## Fixture Scopes for Performance

```python
# Function scope (default) - new instance per test
@pytest.fixture
def temp_file():
    return create_temp_file()

# Class scope - shared across test class
@pytest.fixture(scope="class")
def database_connection():
    return connect_to_db()

# Module scope - shared across test file
@pytest.fixture(scope="module")
def expensive_resource():
    return load_large_dataset()

# Session scope - shared across all tests
@pytest.fixture(scope="session")
def config():
    return load_config()
```

## Coverage Strategy

### Aim for 80%+ coverage, but focus on:
1. **Critical paths** - Core functionality
2. **Complex logic** - Algorithms, calculations
3. **Edge cases** - Error handling, boundaries
4. **Public APIs** - User-facing functions

### Don't obsess over:
- Simple getters/setters
- `__repr__` methods
- Import statements
- Configuration files

## Test Data Management

### Use fixtures directory for:
- Sample CV files
- Sample job descriptions
- Reference data

### Use mock data for:
- API responses
- Database records
- Complex objects

```python
# Good: Use fixture file
def test_cv_parsing(sample_cv_text):
    result = parse_cv(sample_cv_text)
    assert result["name"]

# Better: Use mock for dynamic data
def test_matching(mock_cv_data, mock_job_data):
    score = calculate_match(mock_cv_data, mock_job_data)
    assert 0 <= score <= 100
```

## Common Pytest Commands

```bash
# Basic runs
pytest                           # Run all tests
pytest tests/unit/              # Run specific directory
pytest tests/unit/test_matcher.py  # Run specific file
pytest tests/unit/test_matcher.py::test_calculate_score  # Run specific test

# With markers
pytest -m unit                  # Run unit tests only
pytest -m "not slow"           # Skip slow tests
pytest -m "cv_parser or job_parser"  # Run specific modules

# Output control
pytest -v                       # Verbose
pytest -vv                      # More verbose
pytest -q                       # Quiet
pytest -s                       # Show print statements
pytest --tb=short              # Shorter tracebacks

# Debugging
pytest --pdb                    # Drop into debugger on failure
pytest -x                       # Stop on first failure
pytest --lf                     # Run last failed
pytest --ff                     # Run failed first, then others

# Coverage
pytest --cov=src               # Show coverage
pytest --cov-report=html       # HTML report
pytest --cov-report=term-missing  # Show missing lines

# Performance
pytest -n auto                 # Parallel execution (needs pytest-xdist)
pytest --durations=10          # Show 10 slowest tests
```

## Tips for Efficient Testing

1. **Keep unit tests fast** (<100ms each)
2. **Use markers** to organize and filter tests
3. **Run incrementally** during development
4. **Use fixtures** to avoid repetition
5. **Mock external dependencies** (APIs, databases)
6. **Parametrize** similar test cases
7. **Test behavior, not implementation**
8. **Write descriptive test names**
9. **One assertion per test** (generally)
10. **Clean up after tests** (use fixtures with cleanup)

## Quick Reference Card

| Goal | Command |
|------|---------|
| Fast feedback   | `make test-unit`    |
| Specific module | `make test-matcher` |
| Watch mode      | `make test-watch`   |
| Coverage        | `make test-cov`     |
| Before commit   | `make test-fast`    |
| Full suite      | `make test`         |
| Debug           | `make test-debug`   |
| Re-run failures | `make test-failed`  |