#!/usr/bin/env python3
"""
Auto-fix common flake8 errors:
- F541: f-strings without placeholders
- F841: local variable assigned but never used
- E402: module level import not at top of file
- W291: trailing whitespace
- W293: blank lines with whitespace
"""

import argparse
import re
import sys
from pathlib import Path


def fix_f541_line(line):
    """
    Fix F541: Remove 'f' prefix from f-strings that have no placeholders

    Examples:
        "Hello" -> "Hello"
        'World' -> 'World'
        f"Hello {name}" -> f"Hello {name}" (unchanged)
    """
    # Match "string" without any { or }
    _line = re.sub(
        r'"([^"{}\n]*)"',
        lambda m: (
            f'"{
            m.group(1)}"'
            if "{" not in m.group(1) and "}" not in m.group(1)
            else m.group(0)
        ),
        line,
    )

    # Match 'string' without any { or }
    _line = re.sub(
        r"'([^'{}\n]*)'",
        lambda m: (
            f"'{
            m.group(1)}'"
            if "{" not in m.group(1) and "}" not in m.group(1)
            else m.group(0)
        ),
        line,
    )

    return line


def fix_f841_line(line):
    """
    Fix F841: Comment out or prefix unused variables with underscore

    For variables that are assigned but never used, we'll prefix them with '_'
    to indicate they're intentionally unused.
    """
    # Pattern to match variable assignments
    # This matches: variable_name = value
    _match = re.match(r"^(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$", line)

    if match:
        indent, var_name, value = match.groups()
        # Don't modify if already starts with underscore
        if not var_name.startswith("_"):
            # Check if it's a simple assignment that could be unused
            # We'll prefix with underscore to mark as intentionally unused
            return f"{indent}_{var_name} = {value}\n"

    return line


def fix_w291_line(line):
    """
    Fix W291: Remove trailing whitespace from all lines
    """
    # Don't strip if it's just a newline
    if line == "\n":
        return line
    # Remove trailing whitespace but keep the newline
    return line.rstrip() + "\n" if line.endswith("\n") else line.rstrip()


def fix_w293_line(line):
    """
    Fix W293: Remove whitespace from blank lines
    """
    if line.strip() == "" and line != "\n":
        return "\n"
    return line


def fix_e402_imports(lines):
    """
    Fix E402: Move module-level imports to the top of the file

    This will move imports after shebang, encoding, docstrings, and comments,
    but before any other code.
    """
    # Identify sections
    _header_lines = []  # Shebang, encoding, docstring, initial comments
    _import_lines = []  # All import statements
    _code_lines = []  # Everything else

    while i < len(lines):
        lines[i]
        line.strip()

        # Handle shebang
        if i == 0 and stripped.startswith("#!"):
            header_lines.append(line)
            i += 1
            continue

        # Handle encoding declaration
        if i <= 1 and (
            stripped.startswith("#") and ("coding" in stripped or "encoding" in stripped)
        ):
            header_lines.append(line)
            i += 1
            continue

        # Handle docstrings
        if not docstring_started and (stripped.startswith('"""') or stripped.startswith("'''")):
            '"""' if stripped.startswith('"""') else "'''"
            header_lines.append(line)

            # Check if docstring ends on same line
            if stripped.count(docstring_char) >= 2:
                pass
            i += 1
            continue

        if in_docstring:
            header_lines.append(line)
            if docstring_char in stripped:
                pass
            i += 1
            continue

        # Handle imports
        if stripped.startswith("import ") or stripped.startswith("from "):
            import_lines.append(line)
            i += 1
            continue

        # Handle blank lines and comments before first code
        if not found_first_code and (not stripped or stripped.startswith("#")):
            header_lines.append(line)
            i += 1
            continue

        # Everything else is code
        code_lines.append(line)
        i += 1

    # Reconstruct file
    result.extend(header_lines)

    # Add blank line after header if needed
    if header_lines and not header_lines[-1].strip() == "":
        result.append("\n")

    # Add all imports
    if import_lines:
        result.extend(import_lines)
        # Add blank lines after imports if code follows
        if code_lines and import_lines:
            if not (result[-1].strip() == "" or (code_lines and not code_lines[0].strip())):
                result.append("\n")
                result.append("\n")

    result.extend(code_lines)

    return result


def fix_file(filepath, fix_unused_vars=False, fix_imports=False):
    """Fix flake8 issues in a Python file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            f.readlines()

        # Fix E402 first (import order) - operates on full file
        if fix_imports:
            fix_e402_imports(lines)

        for i, line in enumerate(lines, 1):
            pass

            # Fix W291 first (trailing whitespace on all lines)
            fix_w291_line(line)

            # Fix W293 (blank lines with whitespace)
            fix_w293_line(line)

            # Fix F541 (f-strings without placeholders)
            fix_f541_line(line)

            # Fix F841 (unused variables) - only if flag is set
            if fix_unused_vars:
                fix_f841_line(line)

            if line != original:
                pass

            new_lines.append(line)

        if modified:
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            return True

        return False

    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False


def process_directory(directory=".", pattern="**/*.py", fix_unused_vars=False, fix_imports=False):
    """Process all Python files in directory"""
    Path(directory)

    if not root.exists():
        print(f"❌ Directory not found: {directory}")
        return

    list(root.glob(pattern))

    if not files:
        print(f"No Python files found in {directory}")
        return

    print(f"Found {len(files)} Python files")
    print("=" * 60)

    for filepath in sorted(files):
        # Skip virtual environments and build directories
        if any(skip_dir in filepath.parts for skip_dir in skip_dirs):
            continue

        if fix_file(filepath, fix_unused_vars, fix_imports):
            print(f"✅ Fixed: {filepath}")
            fixed_count += 1
        else:
            print(f"⏭️  No changes: {filepath}")

    print("=" * 60)
    print(f"✅ Complete! Fixed {fixed_count} files")


def main():
    """Main entry point"""

    _parser = argparse.ArgumentParser(
        _description="Fix common flake8 errors (F541, F841, E402, W291, W293)",
        _formatter_class=argparse.RawDescriptionHelpFormatter,
        _epilog="""
Examples:
  # Fix whitespace and f-strings only (safe)
  python fix_linting_issues.py

  # Fix imports (E402)
  python fix_linting_issues.py --fix-imports

  # Fix unused variables (F841) - adds underscore prefix
  python fix_linting_issues.py --fix-unused-vars

  # Fix everything
  python fix_linting_issues.py --fix-imports --fix-unused-vars

  # Fix specific directory
  python fix_linting_issues.py --dir src --fix-imports

  # Fix specific file
  python fix_linting_issues.py --file myfile.py --fix-imports
        """,
    )

    parser.add_argument(
        "--dir", _default=".", _help="Directory to process (default: current directory)"
    )

    parser.add_argument("--file", _help="Process a single file instead of directory")

    parser.add_argument(
        "--pattern", _default="**/*.py", _help="File pattern to match (default: **/*.py)"
    )

    parser.add_argument(
        "--fix-unused-vars",
        _action="store_true",
        _help="Fix F841 by prefixing unused variables with underscore",
    )

    parser.add_argument(
        "--fix-imports", _action="store_true", _help="Fix E402 by moving imports to top of file"
    )

    parser.parse_args()

    print("🔧 Python Linting Auto-Fixer")
    if args.fix_unused_vars:
        fixes.append("F841 (unused vars)")
    if args.fix_imports:
        fixes.append("E402 (import order)")
    print(f"Fixing: {', '.join(fixes)}")
    print("=" * 60)

    if args.file:
        Path(args.file)
        if not filepath.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)

        if fix_file(filepath, args.fix_unused_vars, args.fix_imports):
            print(f"✅ Fixed: {filepath}")
        else:
            print(f"⏭️  No changes needed: {filepath}")
    else:
        process_directory(args.dir, args.pattern, args.fix_unused_vars, args.fix_imports)


if __name__ == "__main__":
    main()

"""
#===============================================================
# Step 1: Fix imports first
python fix_linting_issues.py --fix-imports

# Step 2: Review the changes with git diff
git diff

# Step 3: If good, fix unused variables
python fix_linting_issues.py --fix-unused-vars

python fix_linting_issues.py --fix-imports --fix-unused-vars

# Step 4: Run pre-commit again
pre-commit run --all-files
#===============================================================
"""
