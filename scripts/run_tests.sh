#!/bin/bash
# run_tests.sh - Comprehensive test runner for the Advanced Job Engine

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default values
TEST_TYPE="all"
VERBOSE=false
COVERAGE=false
JUNIT=false
PARALLEL=false

# Usage function
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Run tests for the Advanced Job Engine project.

OPTIONS:
    -t, --type TYPE        Test type: all, unit, integration, specific (default: all)
    -v, --verbose          Enable verbose output
    -c, --coverage         Generate coverage report
    -j, --junit            Generate JUnit XML report
    -p, --parallel         Run tests in parallel
    -f, --file FILE        Run specific test file
    -m, --marker MARKER    Run tests with specific marker
    -h, --help             Show this help message

EXAMPLES:
    $0                              # Run all tests
    $0 -t unit                      # Run only unit tests
    $0 -t unit -c                   # Run unit tests with coverage
    $0 -f test_cv_parser.py         # Run specific test file
    $0 -m slow                      # Run tests marked as 'slow'
    $0 -v -c -j                     # Verbose, coverage, JUnit output

EOF
    exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            TEST_TYPE="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -j|--junit)
            JUNIT=true
            shift
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        -f|--file)
            TEST_FILE="$2"
            shift 2
            ;;
        -m|--marker)
            MARKER="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Print header
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Advanced Job Engine Tests${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
}

# Print section
print_section() {
    echo -e "${YELLOW}>>> $1${NC}"
}

# Print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    print_success "Python 3 found: $(python3 --version)"
}

# Check if pytest is installed
check_pytest() {
    if ! python3 -c "import pytest" 2>/dev/null; then
        print_error "pytest is not installed"
        echo "Installing pytest..."
        pip install pytest pytest-cov pytest-xdist
    fi
    print_success "pytest found: $(python3 -m pytest --version | head -n 1)"
}

# Create necessary directories
setup_directories() {
    mkdir -p "$PROJECT_ROOT/test_results"
    mkdir -p "$PROJECT_ROOT/htmlcov"
    mkdir -p "$PROJECT_ROOT/.pytest_cache"
}

# Build pytest command
build_pytest_command() {
    local cmd="python3 -m pytest"
    
    # Add test path based on type
    case $TEST_TYPE in
        unit)
            cmd="$cmd tests/unit"
            ;;
        integration)
            cmd="$cmd tests/integration"
            ;;
        specific)
            if [ -n "$TEST_FILE" ]; then
                cmd="$cmd tests/**/$TEST_FILE"
            else
                print_error "Please specify a test file with -f/--file"
                exit 1
            fi
            ;;
        all)
            cmd="$cmd tests/"
            ;;
        *)
            print_error "Unknown test type: $TEST_TYPE"
            exit 1
            ;;
    esac
    
    # Add verbose flag
    if [ "$VERBOSE" = true ]; then
        cmd="$cmd -v"
    else
        cmd="$cmd -q"
    fi
    
    # Add coverage
    if [ "$COVERAGE" = true ]; then
        cmd="$cmd --cov=src --cov-report=html --cov-report=term"
    fi
    
    # Add JUnit XML
    if [ "$JUNIT" = true ]; then
        cmd="$cmd --junit-xml=test_results/junit.xml"
    fi
    
    # Add parallel execution
    if [ "$PARALLEL" = true ]; then
        cmd="$cmd -n auto"
    fi
    
    # Add marker
    if [ -n "$MARKER" ]; then
        cmd="$cmd -m $MARKER"
    fi
    
    echo "$cmd"
}

# Run tests
run_tests() {
    local pytest_cmd=$(build_pytest_command)
    
    print_section "Running tests..."
    echo "Command: $pytest_cmd"
    echo ""
    
    cd "$PROJECT_ROOT"
    
    if eval "$pytest_cmd"; then
        print_success "All tests passed!"
        return 0
    else
        print_error "Some tests failed!"
        return 1
    fi
}

# Generate coverage report
show_coverage_report() {
    if [ "$COVERAGE" = true ]; then
        echo ""
        print_section "Coverage Report"
        
        if [ -f "$PROJECT_ROOT/htmlcov/index.html" ]; then
            print_success "HTML coverage report generated: htmlcov/index.html"
            
            # Try to open in browser (optional)
            if command -v xdg-open &> /dev/null; then
                echo "Opening coverage report in browser..."
                xdg-open "$PROJECT_ROOT/htmlcov/index.html" 2>/dev/null || true
            fi
        fi
    fi
}

# Show test summary
show_summary() {
    echo ""
    print_section "Test Summary"
    
    echo "Test type: $TEST_TYPE"
    echo "Verbose: $VERBOSE"
    echo "Coverage: $COVERAGE"
    echo "JUnit XML: $JUNIT"
    echo "Parallel: $PARALLEL"
    
    if [ -n "$MARKER" ]; then
        echo "Marker: $MARKER"
    fi
    
    if [ -n "$TEST_FILE" ]; then
        echo "Test file: $TEST_FILE"
    fi
    
    echo ""
    
    if [ -f "$PROJECT_ROOT/test_results/junit.xml" ]; then
        print_success "JUnit XML report: test_results/junit.xml"
    fi
}

# Cleanup function
cleanup() {
    print_section "Cleaning up..."
    
    # Remove __pycache__ directories
    find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    
    # Remove .pyc files
    find "$PROJECT_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
    
    print_success "Cleanup complete"
}

# Main execution
main() {
    print_header
    
    # Pre-flight checks
    print_section "Pre-flight checks"
    check_python
    check_pytest
    setup_directories
    echo ""
    
    # Run tests
    if run_tests; then
        TEST_RESULT=0
    else
        TEST_RESULT=1
    fi
    
    # Post-test actions
    show_coverage_report
    show_summary
    
    # Cleanup
    if [ "$VERBOSE" = false ]; then
        cleanup
    fi
    
    echo ""
    if [ $TEST_RESULT -eq 0 ]; then
        print_success "Test run completed successfully!"
    else
        print_error "Test run failed!"
    fi
    
    exit $TEST_RESULT
}

# Run main function
main
