# Makefile for Advanced Job Engine
.PHONY: help install install-dev test test-unit test-integration test-fast lint format clean run

# Variables
PYTHON := python3
PYTEST := pytest
SRC_DIR := src
TEST_DIR := tests

# Colors
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m

.DEFAULT_GOAL := help

help:
	@echo "$(BLUE)Available commands:$(NC)"
	@echo "  $(YELLOW)make install$(NC)          - Install production dependencies"
	@echo "  $(YELLOW)make install-dev$(NC)      - Install development dependencies"
	@echo "  $(YELLOW)make test$(NC)             - Run all tests with coverage"
	@echo "  $(YELLOW)make test-unit$(NC)        - Run only unit tests"
	@echo "  $(YELLOW)make test-integration$(NC) - Run integration tests"
	@echo "  $(YELLOW)make test-fast$(NC)        - Run fast tests only"
	@echo "  $(YELLOW)make test-cov$(NC)         - Generate coverage report"
	@echo "  $(YELLOW)make lint$(NC)             - Run all linters"
	@echo "  $(YELLOW)make format$(NC)           - Format code"
	@echo "  $(YELLOW)make clean$(NC)            - Clean generated files"
	@echo "  $(YELLOW)make run$(NC)              - Run quick analysis"

install:
	@echo "$(GREEN)Installing production dependencies...$(NC)"
	pip install -r requirements.txt
	@echo "$(GREEN)Production dependencies installed$(NC)"

install-dev: install
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	pip install -r requirements-dev.txt
	@echo "$(GREEN)Development dependencies installed$(NC)"

test:
	@echo "$(GREEN)Running all tests with coverage...$(NC)"
	$(PYTEST) $(TEST_DIR)/ -v --cov=$(SRC_DIR) --cov-report=html --cov-report=term
	@echo "$(GREEN)Tests completed$(NC)"

test-unit:
	@echo "$(GREEN)Running unit tests...$(NC)"
	$(PYTEST) $(TEST_DIR)/unit/ -v
	@echo "$(GREEN)Unit tests completed$(NC)"

test-integration:
	@echo "$(GREEN)Running integration tests...$(NC)"
	$(PYTEST) $(TEST_DIR)/integration/ -v
	@echo "$(GREEN)Integration tests completed$(NC)"

test-fast:
	@echo "$(GREEN)Running fast tests...$(NC)"
	$(PYTEST) -m "not slow" -v
	@echo "$(GREEN)Fast tests completed$(NC)"

test-cov:
	@echo "$(GREEN)Generating coverage report...$(NC)"
	$(PYTEST) --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)Coverage report: htmlcov/index.html$(NC)"

lint:
	@echo "$(BLUE)Running linters...$(NC)"
	flake8 $(SRC_DIR)/ $(TEST_DIR)/
	mypy $(SRC_DIR)/
	@echo "$(GREEN)Linting completed$(NC)"

format:
	@echo "$(BLUE)Formatting code...$(NC)"
	black $(SRC_DIR)/ $(TEST_DIR)/ examples/
	@echo "$(GREEN)Code formatted$(NC)"

clean:
	@echo "$(YELLOW)Cleaning generated files...$(NC)"
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)Cleaned$(NC)"

run:
	@bash scripts/run_analysis.sh
