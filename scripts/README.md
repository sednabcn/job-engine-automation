All three shell scripts are now complete! Here's a quick summary:
1. run_tests.sh
Comprehensive test runner with options for:

Running unit, integration, or all tests
Code coverage reporting
JUnit XML output
Parallel test execution
Verbose/quiet modes
Test markers

Usage examples:
bash./scripts/run_tests.sh                    # Run all tests
./scripts/run_tests.sh -t unit -c         # Unit tests with coverage
./scripts/run_tests.sh -v -c -j           # Verbose, coverage, JUnit
./scripts/run_tests.sh -m slow            # Run tests marked 'slow'
2. clean_data.sh
Smart cleanup tool that can:

Clean generated files safely (default)
Remove cache and temporary files
Optionally clean CV and config files
Dry-run mode to preview deletions
Interactive confirmations

Usage examples:
bash./scripts/clean_data.sh                   # Safe clean
./scripts/clean_data.sh -d                # Dry run
./scripts/clean_data.sh -a                # Clean everything
./scripts/clean_data.sh --no-config       # Clean but keep CV
3. export_results.sh
Export analysis results including:

Complete reports
Learning plans
Application materials (cover letters, emails)
Skill tests and strategies
Optional compression
Multiple format support

Usage examples:
bash./scripts/export_results.sh               # Export latest
./scripts/export_results.sh -j job_001    # Export specific job
./scripts/export_results.sh -a -z         # Export all + compress
./scripts/export_results.sh -f markdown   # Markdown format
Don't forget to make them executable:
bashchmod +x scripts/*.sh