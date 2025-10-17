# 1. Install dependencies
pip install -r requirements-dev.txt

# 2. Create pytest.ini (use the artifact above)

# 3. Update conftest.py (use the comprehensive artifact above)

# 4. Run tests efficiently
make test-unit          # Start here - fast unit tests
make test-fast          # Before commits
make test-cov           # Full coverage check
make test               # Complete suite

# 5. During development
make test-watch         # Auto-rerun on file changes
make test-file FILE=tests/unit/test_matcher.py  # Specific file