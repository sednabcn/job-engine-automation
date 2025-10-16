#!/bin/bash
# clean_data.sh - Clean generated data and temporary files

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
DRY_RUN=false
FORCE=false
KEEP_CONFIG=true
KEEP_CV=true
INTERACTIVE=true

# Usage function
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Clean generated data and temporary files from the Advanced Job Engine.

OPTIONS:
    -a, --all              Clean everything (including CV and config)
    -d, --dry-run          Show what would be deleted without actually deleting
    -f, --force            Skip confirmation prompts
    -y, --yes              Non-interactive mode (auto-confirm)
    --no-config            Also delete configuration files
    --no-cv                Also delete CV files
    -h, --help             Show this help message

WHAT GETS CLEANED:
    Default (safe):
        - Generated JSON files (analyzed_jobs, learning_progress, etc.)
        - Export directories
        - Temporary files
        - Cache files
        - Log files
        - __pycache__ directories
        - .pyc files
    
    With --all:
        - Everything above
        - CV files
        - Configuration files
        - All data directories

EXAMPLES:
    $0                     # Safe clean (keep CV and config)
    $0 -d                  # Dry run (show what would be deleted)
    $0 -f                  # Force clean without confirmation
    $0 -a                  # Clean everything
    $0 --no-config         # Clean but keep CV, delete config

EOF
    exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--all)
            KEEP_CONFIG=false
            KEEP_CV=false
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -y|--yes)
            INTERACTIVE=false
            shift
            ;;
        --no-config)
            KEEP_CONFIG=false
            shift
            ;;
        --no-cv)
            KEEP_CV=false
            shift
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
    echo -e "${BLUE}  Clean Job Engine Data${NC}"
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

# Print warning
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Confirm action
confirm() {
    if [ "$INTERACTIVE" = false ] || [ "$FORCE" = true ]; then
        return 0
    fi
    
    local message="$1"
    read -p "$message (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# Remove file or directory
remove_item() {
    local item="$1"
    local description="$2"
    
    if [ -e "$item" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "  [DRY RUN] Would delete: $item"
        else
            rm -rf "$item"
            print_success "Deleted: $description"
        fi
    fi
}

# Clean generated JSON files
clean_generated_json() {
    print_section "Cleaning generated JSON files"
    
    cd "$PROJECT_ROOT"
    
    local json_files=(
        "job_search_data/analyzed_jobs.json"
        "job_search_data/learning_progress.json"
        "job_search_data/sprint_history.json"
        "job_search_data/skill_tests.json"
        "job_search_data/workflow_state.json"
        "job_search_data/master_skillset.json"
    )
    
    for file in "${json_files[@]}"; do
        remove_item "$file" "$(basename "$file")"
    done
}

# Clean export directories
clean_exports() {
    print_section "Cleaning export directories"
    
    cd "$PROJECT_ROOT"
    
    local export_count=0
    for dir in job_search_data/export_*; do
        if [ -d "$dir" ]; then
            remove_item "$dir" "$(basename "$dir")"
            ((export_count++))
        fi
    done
    
    if [ $export_count -eq 0 ]; then
        echo "  No export directories found"
    else
        print_success "Cleaned $export_count export directories"
    fi
}

# Clean temporary files
clean_temp_files() {
    print_section "Cleaning temporary files"
    
    cd "$PROJECT_ROOT"
    
    # Remove temp directories
    remove_item "tmp" "tmp directory"
    remove_item "temp" "temp directory"
    remove_item ".tmp" ".tmp directory"
    
    # Remove backup files
    find . -type f -name "*.bak" -delete 2>/dev/null || true
    find . -type f -name "*~" -delete 2>/dev/null || true
    
    print_success "Temporary files cleaned"
}

# Clean cache files
clean_cache() {
    print_section "Cleaning cache files"
    
    cd "$PROJECT_ROOT"
    
    # Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    
    # Pytest cache
    remove_item ".pytest_cache" ".pytest_cache"
    
    # Coverage cache
    remove_item ".coverage" ".coverage"
    remove_item "htmlcov" "htmlcov"
    
    # MyPy cache
    remove_item ".mypy_cache" ".mypy_cache"
    
    print_success "Cache files cleaned"
}

# Clean log files
clean_logs() {
    print_section "Cleaning log files"
    
    cd "$PROJECT_ROOT"
    
    find . -type f -name "*.log" -delete 2>/dev/null || true
    remove_item "logs" "logs directory"
    
    print_success "Log files cleaned"
}

# Clean test results
clean_test_results() {
    print_section "Cleaning test results"
    
    cd "$PROJECT_ROOT"
    
    remove_item "test_results" "test_results directory"
    remove_item ".tox" ".tox directory"
    
    print_success "Test results cleaned"
}

# Clean CV files
clean_cv_files() {
    if [ "$KEEP_CV" = true ]; then
        return
    fi
    
    print_section "Cleaning CV files"
    
    cd "$PROJECT_ROOT"
    
    if confirm "Are you sure you want to delete CV files?"; then
        remove_item "data/my_cv.pdf" "CV (PDF)"
        remove_item "data/my_cv.txt" "CV (TXT)"
        remove_item "data/my_cv.docx" "CV (DOCX)"
        print_success "CV files cleaned"
    else
        print_warning "Skipped CV files"
    fi
}

# Clean configuration files
clean_config_files() {
    if [ "$KEEP_CONFIG" = true ]; then
        return
    fi
    
    print_section "Cleaning configuration files"
    
    cd "$PROJECT_ROOT"
    
    if confirm "Are you sure you want to delete configuration files?"; then
        remove_item ".env" ".env file"
        remove_item "config.json" "config.json"
        print_success "Configuration files cleaned"
    else
        print_warning "Skipped configuration files"
    fi
}

# Clean all data directories
clean_all_data() {
    if [ "$KEEP_CV" = true ] && [ "$KEEP_CONFIG" = true ]; then
        return
    fi
    
    print_section "Cleaning all data"
    
    cd "$PROJECT_ROOT"
    
    if confirm "Are you sure you want to delete ALL data directories?"; then
        remove_item "job_search_data" "job_search_data directory"
        remove_item "data" "data directory"
        print_success "All data directories cleaned"
    else
        print_warning "Skipped data directories"
    fi
}

# Show summary
show_summary() {
    echo ""
    print_section "Summary"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN MODE - No files were actually deleted"
    else
        print_success "Cleanup complete!"
    fi
    
    echo ""
    echo "Settings used:"
    echo "  Keep CV files: $KEEP_CV"
    echo "  Keep config files: $KEEP_CONFIG"
    echo "  Dry run: $DRY_RUN"
    echo "  Force: $FORCE"
    echo "  Interactive: $INTERACTIVE"
}

# Main execution
main() {
    print_header
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN MODE - No files will be deleted"
        echo ""
    fi
    
    # Always safe to clean
    clean_generated_json
    clean_exports
    clean_temp_files
    clean_cache
    clean_logs
    clean_test_results
    
    # Conditional cleaning
    clean_cv_files
    clean_config_files
    
    # Show summary
    show_summary
    
    echo ""
    print_success "Done!"
}

# Run main function
main
