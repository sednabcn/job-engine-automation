#!/usr/bin/env python3
"""
generate_docs.py - Automated documentation generator for the job engine project

This tool generates comprehensive documentation from source code, including:
- API documentation from docstrings
- Module documentation
- Configuration examples
- Usage guides
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
import inspect
import importlib.util


class DocumentationGenerator:
    """Generate documentation from Python source files."""
    
    def __init__(self, project_root: Path, output_dir: Path):
        """
        Initialize the documentation generator.
        
        Args:
            project_root: Root directory of the project
            output_dir: Directory to write documentation files
        """
        self.project_root = Path(project_root)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_all(self):
        """Generate all documentation."""
        print("🚀 Starting documentation generation...")
        
        self.generate_api_docs()
        self.generate_module_overview()
        self.generate_configuration_docs()
        self.generate_usage_examples()
        self.generate_index()
        
        print(f"✅ Documentation generated successfully in: {self.output_dir}")
    
    def generate_api_docs(self):
        """Generate API documentation from source code."""
        print("📚 Generating API documentation...")
        
        src_dir = self.project_root / "src"
        if not src_dir.exists():
            print(f"⚠️  Source directory not found: {src_dir}")
            return
        
        api_doc_path = self.output_dir / "api-reference.md"
        
        with open(api_doc_path, 'w', encoding='utf-8') as f:
            f.write("# API Reference\n\n")
            f.write("Complete API documentation for the Advanced Job Engine.\n\n")
            f.write("---\n\n")
            
            # Process each module
            for module_dir in src_dir.iterdir():
                if module_dir.is_dir() and not module_dir.name.startswith('_'):
                    self._document_module_directory(f, module_dir)
        
        print(f"  ✓ API documentation written to: {api_doc_path}")
    
    def _document_module_directory(self, file_handle, module_dir: Path):
        """Document all Python files in a module directory."""
        file_handle.write(f"## {module_dir.name.title()} Module\n\n")
        
        for py_file in sorted(module_dir.glob("*.py")):
            if py_file.name.startswith('_') and py_file.name != '__init__.py':
                continue
            
            self._document_python_file(file_handle, py_file)
    
    def _document_python_file(self, file_handle, py_file: Path):
        """Document a single Python file."""
        try:
            # Read file content
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract module docstring
            lines = content.split('\n')
            docstring = self._extract_module_docstring(lines)
            
            file_handle.write(f"### `{py_file.stem}.py`\n\n")
            
            if docstring:
                file_handle.write(f"{docstring}\n\n")
            
            # Extract classes and functions
            self._extract_classes_and_functions(file_handle, py_file)
            
            file_handle.write("\n---\n\n")
            
        except Exception as e:
            print(f"  ⚠️  Error documenting {py_file}: {e}")
    
    def _extract_module_docstring(self, lines: List[str]) -> str:
        """Extract module-level docstring."""
        in_docstring = False
        docstring_lines = []
        quote_type = None
        
        for line in lines:
            stripped = line.strip()
            
            if not in_docstring:
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    in_docstring = True
                    quote_type = '"""' if stripped.startswith('"""') else "'''"
                    # Check if docstring ends on same line
                    if stripped.count(quote_type) >= 2:
                        return stripped.strip(quote_type).strip()
                    docstring_lines.append(stripped.lstrip(quote_type))
            else:
                if quote_type in stripped:
                    docstring_lines.append(stripped.rstrip(quote_type))
                    break
                docstring_lines.append(line)
        
        return '\n'.join(docstring_lines).strip()
    
    def _extract_classes_and_functions(self, file_handle, py_file: Path):
        """Extract and document classes and functions."""
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                
                # Detect class definitions
                if stripped.startswith('class '):
                    class_name = stripped.split('(')[0].replace('class ', '').strip(':')
                    file_handle.write(f"#### Class: `{class_name}`\n\n")
                    
                    # Extract class docstring
                    docstring = self._extract_docstring_from_lines(lines, i + 1)
                    if docstring:
                        file_handle.write(f"{docstring}\n\n")
                
                # Detect function/method definitions
                elif stripped.startswith('def ') and not stripped.startswith('def _'):
                    func_signature = stripped.replace('def ', '').strip(':')
                    file_handle.write(f"**`{func_signature}`**\n\n")
                    
                    # Extract function docstring
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
            line = lines[i]
            stripped = line.strip()
            
            if not in_docstring:
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    in_docstring = True
                    quote_type = '"""' if stripped.startswith('"""') else "'''"
                    content = stripped.lstrip(quote_type)
                    # Check if docstring ends on same line
                    if content.count(quote_type) >= 1:
                        return content.rstrip(quote_type).strip()
                    docstring_lines.append(content)
                elif stripped and not stripped.startswith('#'):
                    break
            else:
                if quote_type in stripped:
                    docstring_lines.append(stripped.rstrip(quote_type))
                    break
                docstring_lines.append(line.rstrip())
        
        return '\n'.join(docstring_lines).strip()
    
    def generate_module_overview(self):
        """Generate overview of all modules."""
        print("📦 Generating module overview...")
        
        overview_path = self.output_dir / "modules-overview.md"
        
        src_dir = self.project_root / "src"
        if not src_dir.exists():
            print(f"⚠️  Source directory not found: {src_dir}")
            return
        
        with open(overview_path, 'w', encoding='utf-8') as f:
            f.write("# Modules Overview\n\n")
            f.write("This document provides an overview of all modules in the Advanced Job Engine.\n\n")
            
            f.write("## Module Structure\n\n")
            f.write("```\n")
            f.write("src/\n")
            
            for module_dir in sorted(src_dir.iterdir()):
                if module_dir.is_dir() and not module_dir.name.startswith('_'):
                    f.write(f"├── {module_dir.name}/\n")
                    for py_file in sorted(module_dir.glob("*.py")):
                        f.write(f"│   ├── {py_file.name}\n")
            
            f.write("```\n\n")
            
            f.write("## Module Descriptions\n\n")
            
            modules_info = {
                "analyzers": "Text parsing and analysis for CVs and job descriptions",
                "learning": "Learning plan generation and resource management",
                "tracking": "Progress tracking and sprint management",
                "generators": "Content generation for reports and application materials",
                "utils": "Utility functions for file operations and data handling"
            }
            
            for module_name, description in modules_info.items():
                f.write(f"### {module_name.title()}\n\n")
                f.write(f"{description}\n\n")
        
        print(f"  ✓ Module overview written to: {overview_path}")
    
    def generate_configuration_docs(self):
        """Generate configuration documentation."""
        print("⚙️  Generating configuration documentation...")
        
        config_doc_path = self.output_dir / "configuration.md"
        
        with open(config_doc_path, 'w', encoding='utf-8') as f:
            f.write("# Configuration Guide\n\n")
            f.write("This guide explains how to configure the Advanced Job Engine.\n\n")
            
            f.write("## Environment Variables\n\n")
            f.write("| Variable | Description | Default | Required |\n")
            f.write("|----------|-------------|---------|----------|\n")
            f.write("| `JOB_ENGINE_DEBUG` | Enable debug mode | `false` | No |\n")
            f.write("| `JOB_ENGINE_OUTPUT_DIR` | Output directory path | `./output` | No |\n")
            f.write("| `JOB_ENGINE_DATA_DIR` | Data directory path | `./job_search_data` | No |\n")
            f.write("\n")
            
            f.write("## Configuration Files\n\n")
            f.write("### `.env` File\n\n")
            f.write("Create a `.env` file in the project root:\n\n")
            f.write("```bash\n")
            f.write("JOB_ENGINE_DEBUG=true\n")
            f.write("JOB_ENGINE_OUTPUT_DIR=/path/to/output\n")
            f.write("JOB_ENGINE_DATA_DIR=/path/to/data\n")
            f.write("```\n\n")
            
            f.write("### Configuration JSON\n\n")
            f.write("Example configuration file structure:\n\n")
            f.write("```json\n")
            config_example = {
                "workflow_mode": "reverse",
                "sprint_duration_weeks": 2,
                "quality_gates": {
                    "min_test_score": 70,
                    "min_project_completion": 80
                },
                "notifications": {
                    "enabled": True,
                    "email": "user@example.com"
                }
            }
            f.write(json.dumps(config_example, indent=2))
            f.write("\n```\n\n")
        
        print(f"  ✓ Configuration docs written to: {config_doc_path}")
    
    def generate_usage_examples(self):
        """Generate usage examples documentation."""
        print("💡 Generating usage examples...")
        
        examples_path = self.output_dir / "usage-examples.md"
        
        with open(examples_path, 'w', encoding='utf-8') as f:
            f.write("# Usage Examples\n\n")
            f.write("Practical examples for using the Advanced Job Engine.\n\n")
            
            f.write("## Basic Usage\n\n")
            f.write("```python\n")
            f.write("from src.python_advanced_job_engine import JobEngine\n\n")
            f.write("# Initialize the engine\n")
            f.write("engine = JobEngine()\n\n")
            f.write("# Analyze a job posting\n")
            f.write("result = engine.analyze_job(\n")
            f.write("    cv_path='data/my_cv.pdf',\n")
            f.write("    job_path='data/target_job.pdf'\n")
            f.write(")\n\n")
            f.write("print(f\"Match Score: {result['match_score']}%\")\n")
            f.write("```\n\n")
            
            f.write("## Reverse Mode (Learn Skills First)\n\n")
            f.write("```python\n")
            f.write("# Generate learning plan\n")
            f.write("learning_plan = engine.generate_learning_plan(\n")
            f.write("    skill_gaps=['GraphQL', 'Kubernetes'],\n")
            f.write("    sprint_duration=2\n")
            f.write(")\n\n")
            f.write("# Track progress\n")
            f.write("engine.update_sprint_progress(\n")
            f.write("    sprint_number=1,\n")
            f.write("    completed_tasks=['Complete GraphQL tutorial']\n")
            f.write(")\n")
            f.write("```\n\n")
            
            f.write("## Batch Analysis\n\n")
            f.write("```python\n")
            f.write("# Analyze multiple job postings\n")
            f.write("job_files = ['job1.pdf', 'job2.pdf', 'job3.pdf']\n")
            f.write("results = []\n\n")
            f.write("for job_file in job_files:\n")
            f.write("    result = engine.analyze_job(\n")
            f.write("        cv_path='data/my_cv.pdf',\n")
            f.write("        job_path=f'data/{job_file}'\n")
            f.write("    )\n")
            f.write("    results.append(result)\n\n")
            f.write("# Sort by match score\n")
            f.write("sorted_results = sorted(results, key=lambda x: x['match_score'], reverse=True)\n")
            f.write("```\n\n")
        
        print(f"  ✓ Usage examples written to: {examples_path}")
    
    def generate_index(self):
        """Generate documentation index/table of contents."""
        print("📋 Generating documentation index...")
        
        index_path = self.output_dir / "index.md"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# Advanced Job Engine Documentation\n\n")
            f.write("Welcome to the Advanced Job Engine documentation!\n\n")
            
            f.write("## Quick Links\n\n")
            f.write("- [Getting Started](getting-started.md)\n")
            f.write("- [User Guide](user-guide.md)\n")
            f.write("- [API Reference](api-reference.md)\n")
            f.write("- [Configuration Guide](configuration.md)\n")
            f.write("- [Usage Examples](usage-examples.md)\n")
            f.write("- [Modules Overview](modules-overview.md)\n\n")
            
            f.write("## About\n\n")
            f.write("The Advanced Job Engine is a comprehensive tool for job search automation, ")
            f.write("skill gap analysis, and career development planning.\n\n")
            
            f.write("## Features\n\n")
            f.write("- 📊 CV and job description analysis\n")
            f.write("- 🎯 Skill gap identification\n")
            f.write("- 📚 Learning plan generation\n")
            f.write("- 🏃 Sprint-based progress tracking\n")
            f.write("- ✅ Quality gate checking\n")
            f.write("- 📝 Application material generation\n")
            f.write("- 🤖 GitHub Actions automation\n\n")
            
            f.write("## Documentation Sections\n\n")
            
            docs = [
                ("API Reference", "Complete API documentation with all classes and functions"),
                ("Configuration Guide", "How to configure the job engine"),
                ("Usage Examples", "Practical examples and code snippets"),
                ("Modules Overview", "Overview of all modules and their purposes")
            ]
            
            for title, desc in docs:
                f.write(f"### {title}\n\n")
                f.write(f"{desc}\n\n")
        
        print(f"  ✓ Documentation index written to: {index_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate documentation for the Advanced Job Engine"
    )
    parser.add_argument(
        '--project-root',
        type=str,
        default='.',
        help='Path to project root directory (default: current directory)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='docs',
        help='Output directory for documentation (default: docs/)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    try:
        project_root = Path(args.project_root).resolve()
        output_dir = project_root / args.output_dir
        
        print(f"📁 Project root: {project_root}")
        print(f"📁 Output directory: {output_dir}\n")
        
        generator = DocumentationGenerator(project_root, output_dir)
        generator.generate_all()
        
        print("\n✨ Documentation generation complete!")
        print(f"📖 View documentation at: {output_dir}/index.md")
        
    except Exception as e:
        print(f"\n❌ Error generating documentation: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
