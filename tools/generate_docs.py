#!/usr/bin/env python3
"""
generate_docs.py - Automated documentation generator for the job engine project.

Generates:
- API documentation from docstrings
- Module overview
- Configuration examples
- Usage guides
"""

import argparse
import json
import sys
import traceback
from pathlib import Path
from typing import List


class DocumentationGenerator:
    """Generate documentation from Python source files."""

    def __init__(self, project_root: Path, output_dir: Path):
        self.project_root = Path(project_root)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ======================================================================
    def generate_all(self):
        """Generate all documentation."""
        print("🚀 Starting documentation generation...\n")

        self.generate_api_docs()
        self.generate_module_overview()
        self.generate_configuration_docs()
        self.generate_usage_examples()
        self.generate_index()

        print(f"\n✅ Documentation generated successfully in: {self.output_dir}")

    # ======================================================================
    def generate_api_docs(self):
        """Generate API documentation from source code."""
        print("📚 Generating API documentation...")

        src_dir = self.project_root / "src"
        if not src_dir.exists():
            print(f"⚠️  Source directory not found: {src_dir}")
            return

        api_doc_path = self.output_dir / "api-reference.md"
        with open(api_doc_path, "w", encoding="utf-8") as f:
            f.write("# API Reference\n\n")
            f.write("Complete API documentation for the Advanced Job Engine.\n\n")
            f.write("---\n\n")

            for module_dir in src_dir.iterdir():
                if module_dir.is_dir() and not module_dir.name.startswith("_"):
                    self._document_module_directory(f, module_dir)

        print(f"  ✓ API documentation written to: {api_doc_path}")

    def _document_module_directory(self, file_handle, module_dir: Path):
        """Document all Python files in a module directory."""
        file_handle.write(f"## {module_dir.name.title()} Module\n\n")

        for py_file in sorted(module_dir.glob("*.py")):
            if py_file.name.startswith("_") and py_file.name != "__init__.py":
                continue
            self._document_python_file(file_handle, py_file)

    def _document_python_file(self, file_handle, py_file: Path):
        """Document a single Python file."""
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")
            docstring = self._extract_module_docstring(lines)

            file_handle.write(f"### `{py_file.stem}.py`\n\n")
            if docstring:
                file_handle.write(f"{docstring}\n\n")

            self._extract_classes_and_functions(file_handle, py_file)
            file_handle.write("\n---\n\n")

        except Exception as e:
            print(f"  ⚠️  Error documenting {py_file}: {e}")

    # ======================================================================
    def _extract_module_docstring(self, lines: List[str]) -> str:
        """Extract module-level docstring."""
        docstring_lines = []
        in_docstring = False
        quote_type = None

        for line in lines:
            stripped = line.strip()
            if not in_docstring:
                if stripped.startswith(('"""', "'''")):
                    quote_type = stripped[:3]
                    if stripped.count(quote_type) >= 2:
                        return stripped.strip(quote_type).strip()
                    in_docstring = True
                    docstring_lines.append(stripped.lstrip(quote_type))
            else:
                if quote_type in stripped:
                    docstring_lines.append(stripped.rstrip(quote_type))
                    break
                docstring_lines.append(line)
        return "\n".join(docstring_lines).strip()

    def _extract_classes_and_functions(self, file_handle, py_file: Path):
        """Extract and document classes and functions."""
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            docstring = ""
            for i, line in enumerate(lines):
                stripped = line.strip()

                if stripped.startswith("class "):
                    class_name = stripped.split("(")[0].replace("class ", "").strip(":")
                    file_handle.write(f"#### Class: `{class_name}`\n\n")
                    docstring = self._extract_docstring_from_lines(lines, i + 1)
                    if docstring:
                        file_handle.write(f"{docstring}\n\n")

                elif stripped.startswith("def ") and not stripped.startswith("def _"):
                    func_signature = stripped.replace("def ", "").strip(":")
                    file_handle.write(f"**`{func_signature}`**\n\n")
                    docstring = self._extract_docstring_from_lines(lines, i + 1)
                    if docstring:
                        file_handle.write(f"{docstring}\n\n")

        except Exception as e:
            print(f"  ⚠️  Error extracting classes/functions from {py_file}: {e}")

    def _extract_docstring_from_lines(self, lines: List[str], start_idx: int) -> str:
        """Extract docstring starting from a specific line."""
        docstring_lines = []
        in_docstring = False
        quote_type = None

        for i in range(start_idx, min(start_idx + 50, len(lines))):
            stripped = lines[i].strip()
            if not in_docstring:
                if stripped.startswith(('"""', "'''")):
                    quote_type = stripped[:3]
                    if stripped.count(quote_type) >= 2:
                        return stripped.strip(quote_type).strip()
                    in_docstring = True
                    docstring_lines.append(stripped.lstrip(quote_type))
                elif stripped and not stripped.startswith("#"):
                    break
            else:
                if quote_type in stripped:
                    docstring_lines.append(stripped.rstrip(quote_type))
                    break
                docstring_lines.append(stripped)
        return "\n".join(docstring_lines).strip()

    # ======================================================================
    def generate_module_overview(self):
        """Generate overview of all modules."""
        print("📦 Generating module overview...")

        src_dir = self.project_root / "src"
        if not src_dir.exists():
            print(f"⚠️  Source directory not found: {src_dir}")
            return

        overview_path = self.output_dir / "modules-overview.md"
        with open(overview_path, "w", encoding="utf-8") as f:
            f.write("# Modules Overview\n\n")
            f.write("Overview of all modules in the Advanced Job Engine.\n\n")

            f.write("## Module Structure\n\n```\nsrc/\n")
            for module_dir in sorted(src_dir.iterdir()):
                if module_dir.is_dir() and not module_dir.name.startswith("_"):
                    f.write(f"├── {module_dir.name}/\n")
                    for py_file in sorted(module_dir.glob("*.py")):
                        f.write(f"│   ├── {py_file.name}\n")
            f.write("```\n\n")

            modules_info = {
                "analyzers": "Text parsing and analysis for CVs and job descriptions",
                "learning": "Learning plan generation and resource management",
                "tracking": "Progress tracking and sprint management",
                "generators": "Content generation for reports and materials",
                "utils": "Utility functions for file and data handling",
            }

            for module_name, desc in modules_info.items():
                f.write(f"### {module_name.title()}\n\n{desc}\n\n")

        print(f"  ✓ Module overview written to: {overview_path}")

    # ======================================================================
    def generate_configuration_docs(self):
        """Generate configuration documentation."""
        print("⚙️  Generating configuration documentation...")

        config_doc_path = self.output_dir / "configuration.md"
        with open(config_doc_path, "w", encoding="utf-8") as f:
            f.write("# Configuration Guide\n\n")
            f.write("How to configure the Advanced Job Engine.\n\n")

            f.write("## Environment Variables\n\n")
            f.write("| Variable | Description | Default | Required |\n")
            f.write("|-----------|-------------|----------|----------|\n")
            f.write("| `JOB_ENGINE_DEBUG` | Enable debug mode | `false` | No |\n")
            f.write("| `JOB_ENGINE_OUTPUT_DIR` | Output directory path | `./output` | No |\n")
            f.write(
                "| `JOB_ENGINE_DATA_DIR` | Data directory path | `./job_search_data` | No |\n\n"
            )

            f.write("## Configuration JSON Example\n\n```json\n")
            config_example = {
                "workflow_mode": "reverse",
                "sprint_duration_weeks": 2,
                "quality_gates": {"min_test_score": 70, "min_project_completion": 80},
                "notifications": {"enabled": True, "email": "user@example.com"},
            }
            f.write(json.dumps(config_example, indent=2))
            f.write("\n```\n")

        print(f"  ✓ Configuration docs written to: {config_doc_path}")

    # ======================================================================
    def generate_usage_examples(self):
        """Generate usage examples documentation."""
        print("💡 Generating usage examples...")

        examples_path = self.output_dir / "usage-examples.md"
        with open(examples_path, "w", encoding="utf-8") as f:
            f.write("# Usage Examples\n\n")
            f.write("Practical examples for using the Advanced Job Engine.\n\n")

            f.write("## Basic Usage\n\n```python\n")
            f.write("from src.python_advanced_job_engine import JobEngine\n")
            f.write("engine = JobEngine()\n")
            f.write("result = engine.analyze_job('data/my_cv.pdf', 'data/target_job.pdf')\n")
            f.write("print(result['match_score'])\n```\n\n")

        print(f"  ✓ Usage examples written to: {examples_path}")

    # ======================================================================
    def generate_index(self):
        """Generate documentation index."""
        print("📋 Generating documentation index...")

        index_path = self.output_dir / "index.md"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("# Advanced Job Engine Documentation\n\n")
            f.write("Welcome to the Advanced Job Engine documentation!\n\n")
            f.write("## Quick Links\n")
            f.write("- [API Reference](api-reference.md)\n")
            f.write("- [Configuration Guide](configuration.md)\n")
            f.write("- [Usage Examples](usage-examples.md)\n")
            f.write("- [Modules Overview](modules-overview.md)\n")

        print(f"  ✓ Documentation index written to: {index_path}")


# ======================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Generate documentation for the Advanced Job Engine"
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=".",
        help="Path to project root directory (default: current directory)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="docs",
        help="Output directory for documentation (default: docs/)",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    try:
        project_root = Path(args.project_root).resolve()
        output_dir = Path(args.output_dir).resolve()

        print(f"📁 Project root: {project_root}")
        print(f"📁 Output directory: {output_dir}\n")

        generator = DocumentationGenerator(project_root, output_dir)
        generator.generate_all()

        print("\n✨ Documentation generation complete!")
        print(f"📖 View documentation at: {output_dir}/index.md")

    except Exception as e:
        print(f"\n❌ Error generating documentation: {e}", file=sys.stderr)
        if args.verbose:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
