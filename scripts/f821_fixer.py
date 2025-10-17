#!/usr/bin/env python3
"""
Comprehensive F821 Error Fixer

Fixes undefined variable errors by:
1. Removing underscore prefixes from variables that are actually used
2. Finding and fixing variable definition/usage mismatches
3. Handling assignment expressions that assign to _var but use var
"""

import re
import sys
from collections import defaultdict
from pathlib import Path


def extract_f821_errors_from_text(error_text):
    """Parse F821 errors from flake8 output text"""
    errors = defaultdict(list)

    for line in error_text.split("\n"):
        # Match: filename:line:col: F821 undefined name 'varname'
        match = re.match(r"(.+?):(\d+):\d+: F821 undefined name '(.+?)'", line)
        if match:
            filepath, line_num, var_name = match.groups()
            errors[filepath].append({"line": int(line_num), "var": var_name})

    return errors


def fix_file(filepath, undefined_vars):
    """Fix F821 errors in a file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False

    modified = False
    vars_to_fix = set()

    # Find all undefined variables that have underscore-prefixed definitions
    for error in undefined_vars:
        var_name = error["var"]
        underscore_var = f"_{var_name}"

        # Search entire file for underscore definition
        for line in lines:
            # Check if _var is assigned
            if re.search(rf"\b{re.escape(underscore_var)}\s*=", line):
                vars_to_fix.add((underscore_var, var_name))
                break

    if not vars_to_fix:
        return False

    # Replace underscore variables with non-underscore versions
    new_lines = []
    for line in lines:
        new_line = line
        for underscore_var, var_name in vars_to_fix:
            # Replace _var with var, using word boundaries
            pattern = rf"\b{re.escape(underscore_var)}\b"
            new_line = re.sub(pattern, var_name, new_line)

        new_lines.append(new_line)
        if new_line != line:
            modified = True

    if modified:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            return True
        except Exception as e:
            print(f"❌ Error writing {filepath}: {e}")
            return False

    return False


def main():
    print("🔧 F821 Undefined Variable Fixer")
    print("=" * 80)

    # Read the error file content
    error_file = Path("f821-errors.txt")

    if not error_file.exists():
        print(f"❌ Error file not found: {error_file}")
        print("\nPlease create it by running:")
        print("  flake8 . 2>&1 | grep 'F821' > f821-errors.txt")
        return 1

    with open(error_file, "r") as f:
        error_text = f.read()

    print(f"📄 Reading errors from {error_file}")
    errors = extract_f821_errors_from_text(error_text)

    if not errors:
        print("✅ No F821 errors found!")
        return 0

    print(f"Found F821 errors in {len(errors)} files")
    print(f"Total errors: {sum(len(v) for v in errors.values())}")

    # Statistics
    var_counts = defaultdict(int)
    for file_errors in errors.values():
        for error in file_errors:
            var_counts[error["var"]] += 1

    print("\n📊 Top 10 most common undefined variables:")
    for var, count in sorted(var_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {var:30s} ({count} times)")

    print("\n" + "=" * 80)
    print("🔨 Fixing files...")
    print("=" * 80)

    fixed_files = 0
    skipped_files = 0

    for filepath, file_errors in sorted(errors.items()):
        if not Path(filepath).exists():
            print(f"⚠️  File not found: {filepath}")
            skipped_files += 1
            continue

        if fix_file(filepath, file_errors):
            print(f"✅ Fixed: {filepath} ({len(file_errors)} errors)")
            fixed_files += 1
        else:
            print(f"⏭️  Skipped: {filepath} (no underscore pattern found)")
            skipped_files += 1

    print("\n" + "=" * 80)
    print("📈 Summary:")
    print("=" * 80)
    print(f"✅ Fixed: {fixed_files} files")
    print(f"⏭️  Skipped: {skipped_files} files")

    if fixed_files > 0:
        print("\n✨ Success! Re-run flake8 to check remaining errors:")
        print("   flake8 . 2>&1 | grep 'F821' > f821-errors.txt")

    if skipped_files > 0:
        print("\n⚠️  Some errors require manual fixes:")
        print("   - Missing imports")
        print("   - Typos in variable names")
        print("   - Logic errors where variables are never defined")
        print("   - Variables from deleted code still being referenced")

    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
# Save the script
python f821_fixer.py > fix_output.txt

# Check results
cat fix_output.txt

# Re-run flake8 to see what's left
flake8 . 2>&1 | grep 'F821' | wc -l
"""
