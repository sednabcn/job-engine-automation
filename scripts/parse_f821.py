#!/usr/bin/env python3
"""
Parse F821 errors from flake8 output and create a summary table grouped by file.
"""

import re
from collections import defaultdict


def parse_f821_errors(error_text):
    """
    Parse F821 errors from flake8 output text.

    Returns:
        dict: Dictionary with filename as key and list of (line_num, undefined_name) tuples
    """
    errors_by_file = defaultdict(list)

    # Pattern to match F821 errors
    # Format: filename:line:col: F821 undefined name 'variable_name'
    pattern = (
        r"\[1m(.+?)\[m\[36m:\[m(\d+)\[36m:\[m\d+\[36m:\[m \[1m\[31mF821\[m undefined name \'(.+?)\'"
    )

    matches = re.findall(pattern, error_text)

    for filename, line_num, var_name in matches:
        errors_by_file[filename].append((int(line_num), var_name))

    return errors_by_file


def create_summary_table(errors_by_file):
    """
    Create a formatted summary table of errors by file.

    Args:
        errors_by_file: Dictionary with filename and list of errors

    Returns:
        str: Formatted table as string
    """
    lines = []
    lines.append("=" * 100)
    lines.append(f"{'FILENAME':<60} {'ERROR COUNT':>12} {'UNDEFINED NAMES':<25}")
    lines.append("=" * 100)

    # Sort by error count (descending) then by filename
    sorted_files = sorted(errors_by_file.items(), key=lambda x: (-len(x[1]), x[0]))

    total_errors = 0

    for filename, errors in sorted_files:
        error_count = len(errors)
        total_errors += error_count

        # Get unique undefined names (first 5)
        unique_names = list(set(name for _, name in errors))[:5]
        names_str = ", ".join(unique_names)
        if len(unique_names) < len(set(name for _, name in errors)):
            names_str += ", ..."

        lines.append(f"{filename:<60} {error_count:>12} {names_str:<25}")

    lines.append("=" * 100)
    lines.append(f"{'TOTAL FILES:':<60} {len(errors_by_file):>12}")
    lines.append(f"{'TOTAL ERRORS:':<60} {total_errors:>12}")
    lines.append("=" * 100)

    return "\n".join(lines)


def create_detailed_report(errors_by_file):
    """
    Create a detailed report showing all errors for each file.

    Args:
        errors_by_file: Dictionary with filename and list of errors

    Returns:
        str: Detailed report as string
    """
    lines = []
    lines.append("\n" + "=" * 100)
    lines.append("DETAILED ERROR REPORT")
    lines.append("=" * 100 + "\n")

    sorted_files = sorted(errors_by_file.items(), key=lambda x: (-len(x[1]), x[0]))

    for filename, errors in sorted_files:
        lines.append(f"\n{filename}")
        lines.append("-" * 100)
        lines.append(f"Total errors: {len(errors)}")
        lines.append("")

        # Sort errors by line number
        sorted_errors = sorted(errors, key=lambda x: x[0])

        # Group by undefined name
        name_groups = defaultdict(list)
        for line_num, var_name in sorted_errors:
            name_groups[var_name].append(line_num)

        # Show grouped by variable name
        for var_name, line_nums in sorted(name_groups.items()):
            line_str = ", ".join(str(ln) for ln in sorted(line_nums)[:10])
            if len(line_nums) > 10:
                line_str += f" ... (+{len(line_nums) - 10} more)"
            lines.append(f"  '{var_name}': lines {line_str}")

        lines.append("")

    return "\n".join(lines)


def main():
    # Read the error file
    error_file = "f821-errors.txt"

    try:
        with open(error_file, "r", encoding="utf-8") as f:
            error_text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{error_file}' not found.")
        print("Please ensure the file is in the current directory.")
        return

    # Parse errors
    errors_by_file = parse_f821_errors(error_text)

    if not errors_by_file:
        print("No F821 errors found in the file.")
        return

    # Create and display summary table
    summary = create_summary_table(errors_by_file)
    print(summary)

    # Create detailed report
    detailed = create_detailed_report(errors_by_file)

    # Save to output file
    output_file = "f821-errors-summary.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)
        f.write("\n\n")
        f.write(detailed)

    print(f"\nDetailed report saved to: {output_file}")

    # Print top 10 most problematic files
    print("\n" + "=" * 100)
    print("TOP 10 FILES WITH MOST ERRORS:")
    print("=" * 100)
    sorted_files = sorted(errors_by_file.items(), key=lambda x: -len(x[1]))
    for filename, errors in sorted_files[:10]:
        print(f"{len(errors):>4} errors - {filename}")


if __name__ == "__main__":
    main()


"""
#==============================================================
I've created a Python script that will parse your F821 errors file and generate a comprehensive table grouped by filename. The script will:

Parse the F821 errors from the flake8 output format
Create a summary table showing:

Filename
Error count per file
Sample of undefined variable names
Total files and errors


Generate a detailed report with:

All errors grouped by file
Variable names grouped with their line numbers
Sorted by error count (descending)


Display top 10 most problematic files in the console
Save the complete report to f821-errors-summary.txt

To use it:

Save the script as parse_f821_errors.py
Make sure your f821-errors.txt file is in the same directory
Run: python parse_f821_errors.py

The script will display a summary table in the console and save a detailed report to a file. This will help you quickly identify which files have the most undefined name errors and what variables need to be fixed.RetryClaude can make mistakes. Please double-check responses.
#==========================================================
"""
