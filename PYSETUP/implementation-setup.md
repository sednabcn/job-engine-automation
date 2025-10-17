# 1. Backup current files
cp tests/conftest.py tests/conftest.py.backup
cp Makefile Makefile.backup

# 2. Replace with enhanced versions
# (Copy the artifacts above)

# 3. Add new config files
# (Copy .flake8 and pyproject.toml artifacts)

# 4. Test the setup
make info          # Check versions
make test-unit     # Quick test
make check         # Full check

# 5. Try new workflows
make test-watch    # Watch mode
make quality       # Format + lint + test
make pre-commit    # Before committing