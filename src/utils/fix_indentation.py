#!/usr/bin/env python3
"""
Automatic indentation fixer for python_advanced_job_engine.py
This will fix all indentation issues in one go.
"""

import re
import sys


def fix_file_indentation(input_path, output_path=None):
    """Fix indentation issues in the Python file"""

    if output_path is None:
        output_path = input_path

    print(f"📖 Reading: {input_path}")

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {input_path}")
        sys.exit(1)

    print(f"   Lines read: {len(lines)}")

    # Step 1: Replace all tabs with 4 spaces
    lines = [line.replace("\t", "    ") for line in lines]
    print("✅ Step 1: Converted tabs to spaces")

    # Step 2: Fix the specific problematic methods
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Track if we're in a class
        if re.match(r"^class \w+", line):
            fixed_lines.append(line)
            i += 1
            continue

        # Check for methods that should be at class level (4 spaces)
        # but are indented to 8 spaces (nested incorrectly)
        method_match = re.match(
            r"^(\s+)def (end_sprint|check_quality_gates|stage_positioning|display_progress_dashboard)\(",
            line,
        )

        if method_match:
            current_indent = len(method_match.group(1))
            if current_indent > 4:
                # This method is over-indented, fix it to 4 spaces
                method_name = method_match.group(2)
                print(f"   Fixing: {method_name} (was {current_indent} spaces, now 4)")

                # Fix this line
                fixed_line = "    " + line.lstrip()
                fixed_lines.append(fixed_line)
                i += 1

                # Fix all subsequent lines until we hit another method definition at <= 4 spaces
                while i < len(lines):
                    next_line = lines[i]

                    # Check if we've reached another method or end of indented block
                    if re.match(r"^    def \w+", next_line) and not re.match(
                        r"^        ", next_line
                    ):
                        # Found next method at correct level
                        break
                    elif re.match(r"^class \w+", next_line):
                        # Found next class
                        break
                    elif re.match(r"^def \w+", next_line):
                        # Found module-level function
                        break
                    elif next_line.strip() == "":
                        # Empty line
                        fixed_lines.append(next_line)
                        i += 1
                    elif next_line.startswith("        "):
                        # Line belonging to the method we're fixing - reduce indent by 4
                        fixed_lines.append(next_line[4:])
                        i += 1
                    else:
                        # Line at wrong indent, just add it
                        fixed_lines.append(next_line)
                        i += 1
                continue

        # Check for main() function - should be at module level (0 spaces)
        main_match = re.match(r"^(\s+)def main\(\):", line)
        if main_match:
            current_indent = len(main_match.group(1))
            if current_indent > 0:
                print(f"   Fixing: main() function (was {current_indent} spaces, now 0)")
                fixed_lines.append("def main():\n")
                i += 1

                # Fix all lines in main() function
                while i < len(lines):
                    next_line = lines[i]

                    if re.match(r"^if __name__", next_line):
                        # Reached the if __name__ block
                        break
                    elif next_line.strip() == "":
                        fixed_lines.append(next_line)
                        i += 1
                    elif next_line.startswith("    "):
                        # Content of main() - should stay at 4 spaces
                        fixed_lines.append(next_line[current_indent:])
                        fixed_lines[-1] = "    " + fixed_lines[-1].lstrip()
                        i += 1
                    else:
                        fixed_lines.append(next_line)
                        i += 1
                continue

        # Normal line - just add it
        fixed_lines.append(line)
        i += 1

    print("✅ Step 2: Fixed method indentation")

    # Step 3: Write output
    print(f"💾 Writing: {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)

    print(f"✅ Done! Fixed {len(fixed_lines)} lines")
    print(f"\n🧪 Test with: python -m py_compile {output_path}")
    print(f"🧪 Then run: python3 {output_path}")

    return True


if __name__ == "__main__":

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "src/python_advanced_job_engine.py"

    # Create backup first
    backup_file = input_file + ".backup"
    print(f"📦 Creating backup: {backup_file}")
    try:
        with open(input_file, "r") as f:
            content = f.read()
        with open(backup_file, "w") as f:
            f.write(content)
        print("✅ Backup created")
    except Exception as e:
        print(f"⚠️  Could not create backup: {e}")

    # Fix the file
    print("\n" + "=" * 60)
    fix_file_indentation(input_file, input_file)
    print("=" * 60)

    print(f"\n✅ Original file updated: {input_file}")
    print(f"📦 Backup saved as: {backup_file}")
    print("\nIf something went wrong, restore with:")
    print(f"   cp {backup_file} {input_file}")
