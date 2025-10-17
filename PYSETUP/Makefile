# Makefile for Advanced Job Engine
# =================================

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := pytest
BLACK := black
FLAKE8 := flake8
MYPY := mypy
ISORT := isort

# Directories
SRC_DIR := src
TEST_DIR := tests
DOCS_DIR := docs
SCRIPTS_DIR := scripts

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
RED := \033[0;31m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

# =================================
# HELP
# =================================

.PHONY: help
help:
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(BLUE)  Advanced Job Engine - Makefile Commands$(NC)"
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo ""
	@echo "$(GREEN)📦 Installation:$(NC)"
	@echo "  $(YELLOW)make install$(NC)          - Install production dependencies"
	@echo "  $(YELLOW)make install-dev$(NC)      - Install development dependencies"
	@echo "  $(YELLOW)make setup$(NC)            - Complete project setup"
	@echo ""
	@echo "$(GREEN)🧪 Testing:$(NC)"
	@echo "  $(YELLOW)make test$(NC)             - Run all tests with coverage"
	@echo "  $(YELLOW)make test-unit$(NC)        - Run only unit tests (fast)"
	@echo "  $(YELLOW)make test-integration$(NC) - Run integration tests"
	@echo "  $(YELLOW)make test-fast$(NC)        - Run fast tests only"
	@echo "  $(YELLOW)make test-slow$(NC)        - Run slow tests only"
	@echo "  $(YELLOW)make test-watch$(NC)       - Run tests in watch mode"
	@echo "  $(YELLOW)make test-debug$(NC)       - Run tests with debugger"
	@echo "  $(YELLOW)make test-failed$(NC)      - Re-run only failed tests"
	@echo "  $(YELLOW)make test-cov$(NC)         - Generate coverage report"
	@echo ""
	@echo "$(GREEN)🔍 Code Quality:$(NC)"
	@echo "  $(YELLOW)make lint$(NC)             - Run all linters"
	@echo "  $(YELLOW)make lint-flake8$(NC)      - Run flake8"
	@echo "  $(YELLOW)make lint-mypy$(NC)        - Run mypy type checker"
	@echo "  $(YELLOW)make format$(NC)           - Format code with black & isort"
	@echo "  $(YELLOW)make format-check$(NC)     - Check formatting without changes"
	@echo "  $(YELLOW)make quality$(NC)          - Run format + lint + test"
	@echo ""
	@echo "$(GREEN)🧹 Cleanup:$(NC)"
	@echo "  $(YELLOW)make clean$(NC)            - Clean all generated files"
	@echo "  $(YELLOW)make clean-test$(NC)       - Clean test artifacts"
	@echo "  $(YELLOW)make clean-build$(NC)      - Clean build artifacts"
	@echo "  $(YELLOW)make clean-pyc$(NC)        - Clean Python cache files"
	@echo ""
	@echo "$(GREEN)📚 Documentation:$(NC)"
	@echo "  $(YELLOW)make docs$(NC)             - Generate documentation"
	@echo "  $(YELLOW)make docs-serve$(NC)       - Serve docs locally"
	@echo ""
	@echo "$(GREEN)🚀 Running:$(NC)"
	@echo "  $(YELLOW)make run$(NC)              - Run quick analysis"
	@echo "  $(YELLOW)make demo$(NC)             - Run demo workflow"
	@echo ""
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"

# =================================
# INSTALLATION
# =================================

.PHONY: install
install:
	@echo "$(GREEN)📦 Installing production dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Production dependencies installed$(NC)"

.PHONY: install-dev
install-dev: install
	@echo "$(GREEN)📦 Installing development dependencies...$(NC)"
	$(PIP) install -r requirements-dev.txt
	@echo "$(GREEN)✅ Development dependencies installed$(NC)"

.PHONY: setup
setup:
	@echo "$(GREEN)🚀 Setting up project...$(NC)"
	@bash $(SCRIPTS_DIR)/setup_repo.sh
	@$(MAKE) install-dev
	@echo "$(GREEN)✅ Project setup complete$(NC)"

# =================================
# TESTING
# =================================

.PHONY: test
test:
	@echo "$(GREEN)🧪 Running all tests with coverage...$(NC)"
	$(PYTEST) $(TEST_DIR)/ -v --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)✅ Tests completed - see htmlcov/index.html for coverage$(NC)"

.PHONY: test-unit
test-unit:
	@echo "$(GREEN)🧪 Running unit tests...$(NC)"
	$(PYTEST) $(TEST_DIR)/unit/ -v
	@echo "$(GREEN)✅ Unit tests completed$(NC)"

.PHONY: test-integration
test-integration:
	@echo "$(GREEN)🧪 Running integration tests...$(NC)"
	$(PYTEST) $(TEST_DIR)/integration/ -v
	@echo "$(GREEN)✅ Integration tests completed$(NC)"

.PHONY: test-fast
test-fast:
	@echo "$(GREEN)🧪 Running fast tests...$(NC)"
	$(PYTEST) -m "not slow" -v
	@echo "$(GREEN)✅ Fast tests completed$(NC)"

.PHONY: test-slow
test-slow:
	@echo "$(YELLOW)🧪 Running slow tests...$(NC)"
	$(PYTEST) -m "slow" -v
	@echo "$(GREEN)✅ Slow tests completed$(NC)"

.PHONY: test-watch
test-watch:
	@echo "$(GREEN)🧪 Running tests in watch mode...$(NC)"
	@which ptw > /dev/null || (echo "$(RED)❌ pytest-watch not installed. Run: pip install pytest-watch$(NC)" && exit 1)
	ptw -- -v

.PHONY: test-debug
test-debug:
	@echo "$(YELLOW)🧪 Running tests in debug mode...$(NC)"
	$(PYTEST) -vv --pdb

.PHONY: test-failed
test-failed:
	@echo "$(YELLOW)🧪 Re-running failed tests...$(NC)"
	$(PYTEST) --lf -v

.PHONY: test-cov
test-cov:
	@echo "$(GREEN)🧪 Generating coverage report...$(NC)"
	$(PYTEST) --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing --cov-report=xml
	@echo "$(GREEN)✅ Coverage report generated: htmlcov/index.html$(NC)"

.PHONY: test-smoke
test-smoke:
	@echo "$(GREEN)🧪 Running smoke tests...$(NC)"
	$(PYTEST) -m smoke -v
	@echo "$(GREEN)✅ Smoke tests completed$(NC)"

.PHONY: test-parallel
test-parallel:
	@echo "$(GREEN)🧪 Running tests in parallel...$(NC)"
	$(PYTEST) -n auto
	@echo "$(GREEN)✅ Parallel tests completed$(NC)"

# Test by module
.PHONY: test-cv
test-cv:
	@echo "$(GREEN)🧪 Running CV parser tests...$(NC)"
	$(PYTEST) -m cv_parser -v

.PHONY: test-matcher
test-matcher:
	@echo "$(GREEN)🧪 Running matcher tests...$(NC)"
	$(PYTEST) -m matcher -v

.PHONY: test-learning
test-learning:
	@echo "$(GREEN)🧪 Running learning tests...$(NC)"
	$(PYTEST) -m learning -v

# =================================
# CODE QUALITY
# =================================

.PHONY: lint
lint: lint-flake8 lint-mypy
	@echo "$(GREEN)✅ All linting completed$(NC)"

.PHONY: lint-flake8
lint-flake8:
	@echo "$(BLUE)🔍 Running flake8...$(NC)"
	$(FLAKE8) $(SRC_DIR)/ $(TEST_DIR)/ --count --statistics
	@echo "$(GREEN)✅ flake8 passed$(NC)"

.PHONY: lint-mypy
lint-mypy:
	@echo "$(BLUE)🔍 Running mypy...$(NC)"
	$(MYPY) $(SRC_DIR)/
	@echo "$(GREEN)✅ mypy passed$(NC)"

.PHONY: format
format:
	@echo "$(BLUE)✨ Formatting code with black...$(NC)"
	$(BLACK) $(SRC_DIR)/ $(TEST_DIR)/ examples/
	@echo "$(BLUE)✨ Sorting imports with isort...$(NC)"
	$(ISORT) $(SRC_DIR)/ $(TEST_DIR)/ examples/
	@echo "$(GREEN)✅ Code formatted$(NC)"

.PHONY: format-check
format-check:
	@echo "$(BLUE)🔍 Checking code formatting...$(NC)"
	$(BLACK) --check $(SRC_DIR)/ $(TEST_DIR)/ examples/
	$(ISORT) --check-only $(SRC_DIR)/ $(TEST_DIR)/ examples/
	@echo "$(GREEN)✅ Format check passed$(NC)"

.PHONY: quality
quality: format lint test-fast
	@echo "$(GREEN)✅ All quality checks passed$(NC)"

# =================================
# CLEANUP
# =================================

.PHONY: clean
clean: clean-build clean-pyc clean-test
	@echo "$(GREEN)✅ All artifacts cleaned$(NC)"

.PHONY: clean-build
clean-build:
	@echo "$(YELLOW)🧹 Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +
	@echo "$(GREEN)✅ Build artifacts cleaned$(NC)"

.PHONY: clean-pyc
clean-pyc:
	@echo "$(YELLOW)🧹 Cleaning Python cache files...$(NC)"
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '*.pyc' -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Python cache cleaned$(NC)"

.PHONY: clean-test
clean-test:
	@echo "$(YELLOW)🧹 Cleaning test artifacts...$(NC)"
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/
	rm -rf junit.xml
	rm -rf coverage.xml
	@echo "$(GREEN)✅ Test artifacts cleaned$(NC)"

.PHONY: clean-docs
clean-docs:
	@echo "$(YELLOW)🧹 Cleaning documentation...$(NC)"
	rm -rf $(DOCS_DIR)/_build/
	@echo "$(GREEN)✅ Documentation cleaned$(NC)"

# =================================
# DOCUMENTATION
# =================================

.PHONY: docs
docs:
	@echo "$(BLUE)📚 Generating documentation...$(NC)"
	@if [ -f $(DOCS_DIR)/conf.py ]; then \
		cd $(DOCS_DIR) && sphinx-build -b html . _build; \
		echo "$(GREEN)✅ Documentation built - see $(DOCS_DIR)/_build/index.html$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  Sphinx not configured. Creating basic docs...$(NC)"; \
		mkdir -p $(DOCS_DIR)/_build; \
		echo "<h1>Documentation coming soon</h1>" > $(DOCS_DIR)/_build/index.html; \
	fi

.PHONY: docs-serve
docs-serve: docs
	@echo "$(BLUE)📚 Serving documentation on http://localhost:8000...$(NC)"
	@cd $(DOCS_DIR)/_build && $(PYTHON) -m http.server 8000

# =================================
# RUNNING
# =================================

.PHONY: run
run:
	@echo "$(GREEN)🚀 Running quick analysis...$(NC)"
	@if [ -f $(SCRIPTS_DIR)/run_analysis.sh ]; then \
		bash $(SCRIPTS_DIR)/run_analysis.sh; \
	else \
		$(PYTHON) $(SRC_DIR)/python_advanced_job_engine.py; \
	fi

.PHONY: demo
demo:
	@echo "$(GREEN)🚀 Running demo workflow...$(NC)"
	@if [ -f examples/quick_start.py ]; then \
		$(PYTHON) examples/quick_start.py; \
	else \
		echo "$(YELLOW)⚠️  Demo file not found$(NC)"; \
	fi

# =================================
# DEVELOPMENT HELPERS
# =================================

.PHONY: shell
shell:
	@echo "$(BLUE)🐚 Starting Python shell with project context...$(NC)"
	$(PYTHON) -i -c "import sys; sys.path.insert(0, 'src'); print('Project modules available for import')"

.PHONY: check
check: format-check lint test-fast
	@echo "$(GREEN)✅ Pre-commit checks passed$(NC)"

.PHONY: pre-commit
pre-commit: check
	@echo "$(GREEN)✅ Ready to commit$(NC)"

.PHONY: pre-push
pre-push: quality test
	@echo "$(GREEN)✅ Ready to push$(NC)"

# =================================
# CI/CD
# =================================

.PHONY: ci
ci: install-dev format-check lint test-cov
	@echo "$(GREEN)✅ CI pipeline completed$(NC)"

.PHONY: test-ci
test-ci:
	@echo "$(GREEN)🧪 Running tests for CI...$(NC)"
	$(PYTEST) --junitxml=junit.xml --cov=$(SRC_DIR) --cov-report=xml --cov-report=term
	@echo "$(GREEN)✅ CI tests completed$(NC)"

# =================================
# PACKAGE MANAGEMENT
# =================================

.PHONY: requirements
requirements:
	@echo "$(BLUE)📝 Generating requirements files...$(NC)"
	$(PIP) freeze > requirements.txt
	@echo "$(GREEN)✅ Requirements updated$(NC)"

.PHONY: update-deps
update-deps:
	@echo "$(BLUE)📦 Updating dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements.txt
	$(PIP) install --upgrade -r requirements-dev.txt
	@echo "$(GREEN)✅ Dependencies updated$(NC)"

# =================================
# PROJECT INFO
# =================================

.PHONY: info
info:
	@echo "$(BLUE)ℹ️  Project Information$(NC)"
	@echo "Python: $($(PYTHON) --version)"
	@echo "Pip: $($(PIP) --version | cut -d' ' -f2)"
	@echo "Pytest: $($(PYTEST) --version 2>/dev/null || echo 'not installed')"
	@echo "Black: $($(BLACK) --version 2>/dev/null || echo 'not installed')"
	@echo "Mypy: $($(MYPY) --version 2>/dev/null || echo 'not installed')"
	@echo "Project root: $(pwd)"

.PHONY: stats
stats:
	@echo "$(BLUE)📊 Project Statistics$(NC)"
	@echo "Python files: $(find $(SRC_DIR) -name '*.py' | wc -l)"
	@echo "Test files: $(find $(TEST_DIR) -name 'test_*.py' | wc -l)"
	@echo "Lines of code: $(find $(SRC_DIR) -name '*.py' -exec wc -l {} + | tail -1 | awk '{print $1}')"
	@echo "Lines of tests: $(find $(TEST_DIR) -name '*.py' -exec wc -l {} + | tail -1 | awk '{print $1}')"

# =================================
# DOCKER (if applicable)
# =================================

.PHONY: docker-build
docker-build:
	@echo "$(BLUE)🐳 Building Docker image...$(NC)"
	docker build -t advanced-job-engine .
	@echo "$(GREEN)✅ Docker image built$(NC)"

.PHONY: docker-run
docker-run:
	@echo "$(BLUE)🐳 Running Docker container...$(NC)"
	docker run -it --rm advanced-job-engine

# =================================
# ALIASES
# =================================

.PHONY: t
t: test-unit

.PHONY: tf
tf: test-fast

.PHONY: tc
tc: test-cov

.PHONY: l
l: lint

.PHONY: f
f: format

.PHONY: c
c: clean
