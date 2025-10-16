#!/bin/bash
# Run all benchmarks and generate analysis
# Usage: bash benchmarks/run_all_benchmarks.sh [iterations]

set -e  # Exit on error

# Configuration
ITERATIONS=${1:-100}
RESULTS_DIR="benchmarks/results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================================================${NC}"
echo -e "${BLUE}        ADVANCED JOB ENGINE - COMPREHENSIVE BENCHMARK SUITE          ${NC}"
echo -e "${BLUE}=====================================================================${NC}"
echo ""
echo -e "Iterations: ${GREEN}${ITERATIONS}${NC}"
echo -e "Results Directory: ${GREEN}${RESULTS_DIR}${NC}"
echo -e "Timestamp: ${GREEN}${TIMESTAMP}${NC}"
echo ""

# Create results directory if it doesn't exist
mkdir -p "${RESULTS_DIR}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if required modules are installed
echo -e "${YELLOW}Checking dependencies...${NC}"
python3 -c "import sys; sys.path.insert(0, '.'); from src.python_advanced_job_engine import AdvancedJobEngine" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies OK${NC}"
else
    echo -e "${RED}❌ Dependencies missing. Please install:${NC}"
    echo -e "   pip install -r requirements.txt"
    exit 1
fi

# Run Parsing Benchmarks
echo ""
echo -e "${BLUE}=====================================================================${NC}"
echo -e "${YELLOW}Running Parsing Benchmarks...${NC}"
echo -e "${BLUE}=====================================================================${NC}"
python3 benchmarks/benchmark_parsing.py --iterations ${ITERATIONS} --output ${RESULTS_DIR}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Parsing benchmarks completed${NC}"
else
    echo -e "${RED}❌ Parsing benchmarks failed${NC}"
    exit 1
fi

# Run Matching Benchmarks
echo ""
echo -e "${BLUE}=====================================================================${NC}"
echo -e "${YELLOW}Running Matching Benchmarks...${NC}"
echo -e "${BLUE}=====================================================================${NC}"
python3 benchmarks/benchmark_matching.py --iterations ${ITERATIONS} --output ${RESULTS_DIR}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Matching benchmarks completed${NC}"
else
    echo -e "${RED}❌ Matching benchmarks failed${NC}"
    exit 1
fi

# Run Analysis
echo ""
echo -e "${BLUE}=====================================================================${NC}"
echo -e "${YELLOW}Analyzing Results...${NC}"
echo -e "${BLUE}=====================================================================${NC}"
python3 benchmarks/analyze_benchmarks.py --dir ${RESULTS_DIR}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Analysis completed${NC}"
else
    echo -e "${YELLOW}⚠️  Analysis had warnings${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}=====================================================================${NC}"
echo -e "${GREEN}                    BENCHMARK RUN COMPLETED                          ${NC}"
echo -e "${BLUE}=====================================================================${NC}"
echo ""
echo -e "Results saved in: ${GREEN}${RESULTS_DIR}${NC}"
echo ""
echo -e "Latest files:"
ls -lht "${RESULTS_DIR}" | head -n 5
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Review results in ${RESULTS_DIR}/"
echo -e "  2. Compare with previous runs: python3 benchmarks/analyze_benchmarks.py"
echo -e "  3. Check for regressions in the analysis output above"
echo ""
echo -e "${GREEN}✅ All benchmarks completed successfully!${NC}"
