#!/usr/bin/env python3
"""
Smart F821 Auto-Fixer
---------------------
Automatically repairs undefined variable errors (F821) by:
1. Fixing underscore mismatches (_var → var)
2. Inserting placeholder definitions (var = None) when missing

Usage:
  flake8 . 2>&1 | grep 'F821' > f821-errors.txt
  python smart_f821_fixer.py
"""

import re
import sys
from collections import defaultdict
from pathlib import Path


def extract_f821_errors_from_text(error_text):
    """Parse F821 errors from flake8 output text"""
    errors = defaultdict(list)
    for line in error_text.splitlines():
        match = re.match(r"(.+?):(\d+):\d+: F821 undefined name '(.+?)'", line)
        if match:
            filepath, line_num, var_name = match.groups()
            errors[filepath].append({"line": int(line_num), "var": var_name})
    return errors


def backup_file(filepath: Path):
    """Create a .bak backup before modifying"""
    backup_path = filepath.with_suffix(filepath.suffix + ".bak")
    try:
        backup_path.write_text(filepath.read_text(encoding="utf-8"), encoding="utf-8")
        return True
    except Exception as e:
        print(f"⚠️  Could not create backup for {filepath}: {e}")
        return False


def insert_placeholder_definition(lines, error_line, var_name):
    """Insert 'var_name = None' at the appropriate indentation level"""

    # detect current indentation
    for i in range(error_line - 2, -1, -1):
        line = lines[i]
        if re.match(r"^\s*def |^\s*class ", line):
            len(line) - len(line.lstrip()) + 4
            break

    insertion_point = max(0, error_line - 1)
    lines.insert(insertion_point, var_name)
    return lines


def fix_file(filepath, undefined_vars):
    """Fix F821 errors in a file"""
    try:
        lines = Path(filepath).read_text(encoding="utf-8").splitlines(keepends=True)
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False

    modified = False
    vars_to_fix = set()

    # Step 1: detect underscore mismatches (_var → var)
    for error in undefined_vars:
        var_name = error["var"]
        underscore_var = f"_{var_name}"

        if any(re.search(rf"\b{underscore_var}\s*=", line) for line in lines):
            vars_to_fix.add((underscore_var, var_name))

    new_lines = []
    for line in lines:
        new_line = line
        for underscore_var, var_name in vars_to_fix:
            pattern = rf"\b{re.escape(underscore_var)}\b"
            new_line = re.sub(pattern, var_name, new_line)
        new_lines.append(new_line)

    if vars_to_fix:
        modified = True

    # Step 2: handle truly undefined variables (no definition anywhere)
    all_text = "".join(lines)
    for error in undefined_vars:
        var_name = error["var"]
        if not re.search(rf"\b{re.escape(var_name)}\s*=", all_text):
            # Insert placeholder near the error line
            new_lines = insert_placeholder_definition(new_lines, error["line"], var_name)
            modified = True

    # Step 3: write back file
    if modified:
        try:
            backup_file(Path(filepath))
            Path(filepath).write_text("".join(new_lines), encoding="utf-8")
            return True
        except Exception as e:
            print(f"❌ Error writing {filepath}: {e}")
            return False

    return False


def main():
    print("🔧 Smart F821 Undefined Variable Auto-Fixer")
    print("=" * 80)

    error_file = Path("f821-errors.txt")
    if not error_file.exists():
        print(f"❌ Error file not found: {error_file}")
        print("\nRun first:\n  flake8 . 2>&1 | grep 'F821' > f821-errors.txt")
        return 1

    errors = extract_f821_errors_from_text(error_file.read_text(encoding="utf-8"))
    if not errors:
        print("✅ No F821 errors found!")
        return 0

    print(f"📂 Found F821 errors in {len(errors)} file(s)")
    print(f"📊 Total undefined names: {sum(len(v) for v in errors.values())}")

    var_counts = defaultdict(int)
    for file_errors in errors.values():
        for e in file_errors:
            var_counts[e["var"]] += 1

    print("\nTop undefined variables:")
    for name, count in sorted(var_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {name:25s} ({count}x)")

    print("\n🔨 Fixing files...\n" + "-" * 80)

    fixed, skipped = 0, 0
    for filepath, file_errors in sorted(errors.items()):
        path = Path(filepath)
        if not path.exists():
            print(f"⚠️  File not found: {filepath}")
            skipped += 1
            continue

        if fix_file(filepath, file_errors):
            print(f"✅ Fixed: {filepath} ({len(file_errors)} errors)")
            fixed += 1
        else:
            print(f"⏭️  Skipped: {filepath}")
            skipped += 1

    print("\n📈 Summary")
    print("=" * 80)
    print(f"✅ Fixed: {fixed} file(s)")
    print(f"⏭️  Skipped: {skipped} file(s)")

    if fixed:
        print("\n✨ Re-run to verify:")
        print("  flake8 . 2>&1 | grep 'F821' > f821-errors.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
