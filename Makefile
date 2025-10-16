
### Makefile

```makefile
# Makefile for Advanced Job Engine

.PHONY: help install install-dev test lint format clean run docs

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run test suite"
	@echo "  make lint         - Run code linters"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean generated files"
	@echo "  make run          - Run quick analysis"
	@echo "  make docs         - Generate documentation"

install:
	pip install -r requirements.txt
	@echo "✅ Production dependencies installed"

install-dev: install
	pip install -r requirements-dev.txt
	@echo "✅ Development dependencies installed"

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term
	@echo "✅ Tests completed - see htmlcov/index.html for coverage"

lint:
	flake8 src/ tests/
	mypy src/
	@echo "✅ Linting completed"

format:
	black src/ tests/ examples/
	@echo "✅ Code formatted"

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned generated files"

run:
	@bash scripts/run_analysis.sh

docs:
	cd docs && sphinx-build -b html . _build
	@echo "✅ Documentation built - see docs/_build/index.html"

setup:
	@bash scripts/setup_repo.sh

.DEFAULT_GOAL := help
```
