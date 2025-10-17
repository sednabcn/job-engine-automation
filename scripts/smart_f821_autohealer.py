#!/usr/bin/env python3
"""
Smart F821 Auto-Healer
----------------------
Automatically repairs undefined variable errors (F821) by:

1. Fixing underscore mismatches (_var → var)
2. Inserting placeholder definitions (var = None)
3. Adding missing import statements for common modules

Usage:
  flake8 . 2>&1 | grep 'F821' > f821-errors.txt
  python smart_f821_autohealer.py
"""

import keyword
import re
import sys
from collections import defaultdict
from pathlib import Path

# Common built-ins and modules to import if missing
COMMON_MODULES = {
    "os": "import os",
    "sys": "import sys",
    "json": "import json",
    "re": "import re",
    "datetime": "from datetime import datetime",
    "Path": "from pathlib import Path",
    "defaultdict": "from collections import defaultdict",
    "traceback": "import traceback",
}


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
    """Insert 'var_name = None' at correct indentation level with safe bounds checking"""

    # Ensure valid line index
    if error_line < 1 or error_line > len(lines) + 1:
        print(
            f"⚠️  Warning: reported line {error_line} exceeds file length "
            f"({len(lines)}) for '{var_name}'."
        )
        error_line = len(lines) + 1

    # Skip constants or reserved names
    if var_name.isupper() or keyword.iskeyword(var_name):
        return lines

    # Detect indentation scope safely
    indent = 0
    for i in range(min(error_line - 2, len(lines) - 1), -1, -1):
        current_line = lines[i]
        if re.match(r"^\s*def |^\s*class ", current_line):
            indent = len(current_line) - len(current_line.lstrip()) + 4
            break

    placeholder = " " * indent + f"{var_name} = None  # FIX: Define {var_name}\n"
    insertion_point = max(0, min(error_line - 1, len(lines)))
    lines.insert(insertion_point, placeholder)
    return lines


def ensure_import(lines, var_name):
    """Add missing import statement if var_name is a known module/class"""
    if var_name not in COMMON_MODULES:
        return lines, False

    import_stmt = COMMON_MODULES[var_name]
    import_lines = [line for line in lines if line.strip().startswith("import") or "from " in line]
    already_imported = any(var_name in line for line in import_lines)
    if already_imported:
        return lines, False

    insertion_index = 0
    for i, line in enumerate(lines[:10]):
        if (
            line.startswith("#!")
            or line.strip().startswith('"""')
            or line.strip().startswith("'''")
        ):
            insertion_index = i + 1

    lines.insert(insertion_index, import_stmt + "\n")
    return lines, True


def fix_file(filepath, undefined_vars):
    """Fix F821 errors in one file"""
    try:
        lines = Path(filepath).read_text(encoding="utf-8").splitlines(keepends=True)
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False

    modified = False
    vars_to_fix = set()

    # Step 1: Fix underscore mismatches
    for err in undefined_vars:
        var_name = err["var"]
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
        lines = new_lines

    # Step 2: Insert placeholders & imports
    all_text = "".join(lines)
    for err in undefined_vars:
        var_name = err["var"]

        if keyword.iskeyword(var_name) or var_name in dir(__builtins__):
            continue

        new_lines, added_import = ensure_import(lines, var_name)
        if added_import:
            modified = True
            lines = new_lines
            continue

        if not re.search(rf"\b{re.escape(var_name)}\s*=", all_text):
            lines = insert_placeholder_definition(lines, err["line"], var_name)
            modified = True

    # Step 3: Save changes
    if modified:
        backup_file(Path(filepath))
        Path(filepath).write_text("".join(lines), encoding="utf-8")
        return True

    return False


def main():
    print("🧠 Smart F821 Auto-Healer")
    print("=" * 80)

    error_file = Path("f821-errors.txt")
    if not error_file.exists():
        print("❌ No error file found. Run first:")
        print("  flake8 . 2>&1 | grep 'F821' > f821-errors.txt")
        return 1

    errors = extract_f821_errors_from_text(error_file.read_text(encoding="utf-8"))
    if not errors:
        print("✅ No F821 errors found.")
        return 0

    print(f"📂 Found {len(errors)} file(s) with undefined names.")
    print(f"📊 Total errors: {sum(len(v) for v in errors.values())}")

    var_counts = defaultdict(int)
    for file_errors in errors.values():
        for e in file_errors:
            var_counts[e["var"]] += 1

    print("\nTop undefined variables:")
    for name, count in sorted(var_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {name:25s} ({count}x)")

    print("\n🔨 Healing files...\n" + "-" * 80)
    fixed, skipped = 0, 0

    for filepath, file_errors in sorted(errors.items()):
        path = Path(filepath)
        if not path.exists():
            print(f"⚠️  File not found: {filepath}")
            skipped += 1
            continue

        if fix_file(filepath, file_errors):
            print(f"✅ Healed: {filepath} ({len(file_errors)} errors)")
            fixed += 1
        else:
            print(f"⭐️ Skipped: {filepath}")
            skipped += 1

    print("\n📈 Summary")
    print("=" * 80)
    print(f"✅ Fixed/Healed: {fixed} file(s)")
    print(f"⭐️ Skipped: {skipped} file(s)")

    if fixed:
        print("\n✨ Re-run to verify:")
        print("  flake8 . 2>&1 | grep 'F821' > f821-errors.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
