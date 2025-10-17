#!/usr/bin/env python3
"""
Analyze and fix F821 errors (undefined names)

This script identifies patterns in F821 errors and can auto-fix some common cases:
1. Variables with underscore prefix (F841) that should not have underscore
2. Missing variable definitions that can be inferred from context
"""

import re
import sys
from collections import defaultdict
from pathlib import Path


def parse_flake8_output(flake8_file):
    """Parse flake8 output to extract F821 errors"""
    errors = defaultdict(list)

    with open(flake8_file, "r") as f:
        for line in f:
            # Match: filename:line:col: F821 undefined name 'varname'
            match = re.match(r"(.+?):(\d+):\d+: F821 undefined name '(.+?)'", line)
            if match:
                filepath, line_num, var_name = match.groups()
                errors[filepath].append(
                    {"line": int(line_num), "var": var_name, "full_line": line.strip()}
                )

    return errors


def analyze_undefined_variables(filepath, undefined_vars):
    """Analyze file to find patterns and suggest fixes"""
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except BaseException:
        return []

    suggestions = []

    for error in undefined_vars:
        line_num = error["line"]
        var_name = error["var"]

        if line_num > len(lines):
            continue

        lines[line_num - 1]

        # Pattern 1: Variable used but defined with underscore prefix
        underscore_var = f"_{var_name}"
        for i in range(max(0, line_num - 20), min(len(lines), line_num + 5)):
            if underscore_var in lines[i] and "=" in lines[i]:
                suggestions.append(
                    {
                        "type": "remove_underscore",
                        "line": line_num,
                        "var": var_name,
                        "underscore_var": underscore_var,
                        "def_line": i + 1,
                        "fix": f"Remove underscore from variable definition at line {i + 1}",
                    }
                )
                break

        # Pattern 2: Variable assigned but marked with F841 (unused)
        # Look backwards for assignment with underscore
        for i in range(line_num - 1, max(0, line_num - 30), -1):
            prev_line = lines[i]
            # Check if this line has _varname = something
            if re.match(rf"\s*_{var_name}\s*=", prev_line):
                suggestions.append(
                    {
                        "type": "remove_underscore_assignment",
                        "line": line_num,
                        "var": var_name,
                        "def_line": i + 1,
                        "fix": f"Change _{var_name} to {var_name} at line {i + 1}",
                    }
                )
                break

    return suggestions


def fix_underscore_variables(filepath, suggestions):
    """Fix variables that have underscore prefix but are actually used"""
    try:
        with open(filepath, "r") as f:
            content = f.read()
            f.readlines()
    except BaseException:
        return False

    modified = False

    # Group by type
    remove_underscore = [
        s for s in suggestions if s["type"] in ["remove_underscore", "remove_underscore_assignment"]
    ]

    if not remove_underscore:
        return False

    # Get unique variable pairs to fix
    vars_to_fix = {}
    for sugg in remove_underscore:
        var_name = sugg["var"]
        underscore_var = f"_{var_name}"
        vars_to_fix[underscore_var] = var_name

    # Replace all occurrences
    new_content = content
    for underscore_var, var_name in vars_to_fix.items():
        # Use word boundaries to avoid partial matches
        pattern = rf"\b{re.escape(underscore_var)}\b"
        new_content = re.sub(pattern, var_name, new_content)

    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)
        modified = True

    return modified


def generate_report(errors, suggestions_by_file):
    """Generate a detailed report of F821 errors"""
    total_errors = sum(len(errs) for errs in errors.values())
    total_fixable = sum(len(suggs) for suggs in suggestions_by_file.values())

    print("\n" + "=" * 80)
    print("F821 UNDEFINED VARIABLE ANALYSIS")
    print("=" * 80)
    print(f"\nTotal F821 errors: {total_errors}")
    print(f"Auto-fixable: {total_fixable}")
    print(f"Manual review needed: {total_errors - total_fixable}")

    # Most common undefined variables
    var_counts = defaultdict(int)
    for file_errors in errors.values():
        for error in file_errors:
            var_counts[error["var"]] += 1

    print("\n" + "-" * 80)
    print("Most Common Undefined Variables:")
    print("-" * 80)
    for var, count in sorted(var_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {var:30s} {count:3d} occurrences")

    # Files with most errors
    print("\n" + "-" * 80)
    print("Files with Most Errors:")
    print("-" * 80)
    for filepath, file_errors in sorted(errors.items(), key=lambda x: -len(x[1]))[:10]:
        fixable = len(suggestions_by_file.get(filepath, []))
        print(f"  {filepath:60s} {len(file_errors):3d} errors ({fixable} fixable)")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze and fix F821 undefined variable errors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # First, save flake8 output to a file:
  flake8 . > flake8_errors.txt

  # Analyze the errors:
  python fix_f821.py --analyze flake8_errors.txt

  # Fix underscore prefix issues:
  python fix_f821.py --fix flake8_errors.txt

  # Fix specific file:
  python fix_f821.py --fix flake8_errors.txt --file src/myfile.py
        """,
    )

    parser.add_argument(
        "flake8_output",
        help="Path to flake8 output file (redirect flake8 output: flake8 . > errors.txt)",
    )

    parser.add_argument(
        "--analyze", action="store_true", help="Only analyze and report, do not fix"
    )

    parser.add_argument("--fix", action="store_true", help="Attempt to auto-fix issues")

    parser.add_argument("--file", help="Only process this specific file")

    args = parser.parse_args()

    if not Path(args.flake8_output).exists():
        print(f"Error: File not found: {args.flake8_output}")
        print("\nPlease run: flake8 . > flake8_errors.txt")
        sys.exit(1)

    print("🔍 Parsing F821 errors...")
    errors = parse_flake8_output(args.flake8_output)

    if not errors:
        print("✅ No F821 errors found!")
        return

    print(f"Found F821 errors in {len(errors)} files")

    print("\n🔬 Analyzing patterns...")
    suggestions_by_file = {}
    for filepath, file_errors in errors.items():
        if args.file and filepath != args.file:
            continue
        suggestions = analyze_undefined_variables(filepath, file_errors)
        if suggestions:
            suggestions_by_file[filepath] = suggestions

    # Generate report
    generate_report(errors, suggestions_by_file)

    if args.analyze:
        print("\n" + "=" * 80)
        print("DETAILED SUGGESTIONS:")
        print("=" * 80)
        for filepath, suggestions in suggestions_by_file.items():
            if suggestions:
                print(f"\n{filepath}:")
                for sugg in suggestions:
                    print(f"  Line {sugg['line']}: {sugg['fix']}")
        return

    if args.fix:
        print("\n" + "=" * 80)
        print("FIXING FILES:")
        print("=" * 80)
        fixed_count = 0
        for filepath, suggestions in suggestions_by_file.items():
            if fix_underscore_variables(filepath, suggestions):
                print(f"✅ Fixed: {filepath}")
                fixed_count += 1
            else:
                print(f"⏭️  No changes: {filepath}")

        print("\n" + "=" * 80)
        print(f"✅ Fixed {fixed_count} files")
        print("\n⚠️  IMPORTANT: Many F821 errors require manual review!")
        print("These are logic errors where variables are used but never defined.")
        print("You need to:")
        print("  1. Define the missing variables")
        print("  2. Import missing modules")
        print("  3. Fix variable names")
        print("  4. Remove unused code")
        return

    print("\n" + "=" * 80)
    print("Use --fix to attempt auto-fixes, or --analyze for detailed report")
    print("=" * 80)


if __name__ == "__main__":
    main()

"""
#=====================================================
🎯 How to Use This Tool
Step 1: Save flake8 errors to a file:

flake8 . 2>&1 | grep F821 > f821_errors.txt

Step 2: Analyze the errors:

python fix_f821.py f821_errors.txt --analyze

Step 3: Fix what can be auto-fixed:

python fix_f821.py f821_errors.txt --fix
#===================================================
"""
