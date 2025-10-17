#!/usr/bin/env python3
"""
validate_data.py - Data validation tool for the job engine

Validates:
- CV files
- Job descriptions
- JSON datasets
- Configuration files
- Generated reports
"""

import argparse
import json
import re
import sys
import traceback
from pathlib import Path
from typing import List


class DataValidator:
    """Validate various data files and formats."""

    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    # ----------------------------------------------------------------------
    def validate_all(self, data_dir: Path) -> bool:
        """Validate all data files in a directory."""
        print("🔍 Starting comprehensive data validation...\n")

        if not data_dir.exists():
            self._add_error(f"Data directory not found: {data_dir}")
            self._print_results()
            return False

        self._validate_cv_files(data_dir)
        self._validate_job_files(data_dir)
        self._validate_json_files(data_dir)
        self._validate_output_files(data_dir)

        self._print_results()

        has_errors = len(self.errors) > 0
        has_warnings = len(self.warnings) > 0

        if self.strict_mode and has_warnings:
            return False

        return not has_errors

    # ----------------------------------------------------------------------
    def _validate_cv_files(self, data_dir: Path):
        print("📄 Validating CV files...")

        cv_files = list(data_dir.glob("*cv*.txt")) + list(data_dir.glob("*cv*.pdf"))
        if not cv_files:
            self._add_warning("No CV files found")
            return

        for cv_file in cv_files:
            if cv_file.suffix == ".txt":
                self._validate_cv_text_file(cv_file)
            elif cv_file.suffix == ".pdf":
                self._validate_pdf_file(cv_file)

    def _validate_cv_text_file(self, cv_file: Path):
        try:
            with open(cv_file, "r", encoding="utf-8") as f:
                content = f.read()

            if len(content) < 200:
                self._add_error(f"{cv_file.name}: CV content too short (< 200 characters)")

            required_patterns = {
                "contact": r"(email|phone|contact)",
                "experience": r"(experience|work history|employment)",
                "skills": r"(skills|technical skills|competencies)",
                "education": r"(education|academic|degree)",
            }

            content_lower = content.lower()
            for section, pattern in required_patterns.items():
                if not re.search(pattern, content_lower):
                    self._add_warning(f"{cv_file.name}: Missing '{section}' section")

            email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
            if not re.search(email_pattern, content):
                self._add_warning(f"{cv_file.name}: No valid email address found")

            phone_pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
            if not re.search(phone_pattern, content):
                self._add_warning(f"{cv_file.name}: No phone number found")

            self._add_info(f"{cv_file.name}: Valid CV file ({len(content)} chars)")
        except Exception as e:
            self._add_error(f"{cv_file.name}: Error reading file - {e}")

    # ----------------------------------------------------------------------
    def _validate_job_files(self, data_dir: Path):
        print("💼 Validating job description files...")

        job_files = list(data_dir.glob("*job*.txt")) + list(data_dir.glob("*job*.pdf"))
        if not job_files:
            self._add_warning("No job description files found")
            return

        for job_file in job_files:
            if job_file.suffix == ".txt":
                self._validate_job_text_file(job_file)
            elif job_file.suffix == ".pdf":
                self._validate_pdf_file(job_file)

    def _validate_job_text_file(self, job_file: Path):
        try:
            with open(job_file, "r", encoding="utf-8") as f:
                content = f.read()

            if len(content) < 300:
                self._add_error(f"{job_file.name}: Job description too short (< 300 chars)")

            required_patterns = {
                "title": r"(job title|position|role)",
                "requirements": r"(requirements|qualifications|required)",
                "responsibilities": r"(responsibilities|duties|will be)",
                "skills": r"(skills|technologies|experience with)",
            }

            content_lower = content.lower()
            for section, pattern in required_patterns.items():
                if not re.search(pattern, content_lower):
                    self._add_warning(f"{job_file.name}: Missing '{section}' section")

            if "company" not in content_lower:
                self._add_warning(f"{job_file.name}: Company not specified")
            if "location" not in content_lower:
                self._add_warning(f"{job_file.name}: Location not specified")

            self._add_info(f"{job_file.name}: Valid job file ({len(content)} chars)")
        except Exception as e:
            self._add_error(f"{job_file.name}: Error reading file - {e}")

    # ----------------------------------------------------------------------
    def _validate_pdf_file(self, pdf_file: Path):
        try:
            file_size = pdf_file.stat().st_size
            if file_size == 0:
                self._add_error(f"{pdf_file.name}: PDF file is empty")
            elif file_size < 1024:
                self._add_warning(f"{pdf_file.name}: Suspiciously small PDF ({file_size} bytes)")
            elif file_size > 10 * 1024 * 1024:
                self._add_warning(f"{pdf_file.name}: Very large PDF ({file_size/1048576:.1f} MB)")
            else:
                self._add_info(f"{pdf_file.name}: Valid PDF ({file_size/1024:.1f} KB)")
        except Exception as e:
            self._add_error(f"{pdf_file.name}: Error checking PDF - {e}")

    # ----------------------------------------------------------------------
    def _validate_json_files(self, data_dir: Path):
        print("📊 Validating JSON data files...")
        json_files = list(data_dir.glob("**/*.json"))
        if not json_files:
            self._add_warning("No JSON files found")
            return

        for jf in json_files:
            self._validate_json_file(jf)

    def _validate_json_file(self, json_file: Path):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self._add_info(f"{json_file.name}: Valid JSON structure ({(len(str(data)))} chars)")
        except json.JSONDecodeError as e:
            self._add_error(f"{json_file.name}: Invalid JSON - {e}")
        except Exception as e:
            self._add_error(f"{json_file.name}: Error validating JSON - {e}")

    # ----------------------------------------------------------------------
    def _validate_output_files(self, data_dir: Path):
        print("📦 Validating output/export files...")
        export_dirs = list(data_dir.glob("export_*"))
        if not export_dirs:
            self._add_info("No export directories found (ok)")
            return

        for export_dir in export_dirs:
            files = list(export_dir.glob("*"))
            self._add_info(f"{export_dir.name}: Contains {len(files)} files")

    # ----------------------------------------------------------------------
    def _add_error(self, message: str):
        self.errors.append(message)

    def _add_warning(self, message: str):
        self.warnings.append(message)

    def _add_info(self, message: str):
        self.info.append(message)

    # ----------------------------------------------------------------------
    def _print_results(self):
        print("\n" + "=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for e in self.errors:
                print(f"  • {e}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  • {w}")

        if self.info:
            print(f"\n✅ INFO ({len(self.info)}):")
            for i in self.info:
                print(f"  • {i}")

        print("\n" + "=" * 70)
        print(
            f"Summary: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} info"
        )
        print("=" * 70)


# ======================================================================
def validate_single_file(file_path: Path, validator: DataValidator) -> bool:
    print(f"🔍 Validating single file: {file_path}")
    if not file_path.exists():
        validator._add_error(f"File not found: {file_path}")
        validator._print_results()
        return False

    if file_path.suffix == ".json":
        validator._validate_json_file(file_path)
    elif file_path.suffix == ".txt":
        if "cv" in file_path.name.lower():
            validator._validate_cv_text_file(file_path)
        elif "job" in file_path.name.lower():
            validator._validate_job_text_file(file_path)
        else:
            validator._add_info(f"{file_path.name}: Generic text file validated")
    elif file_path.suffix == ".pdf":
        validator._validate_pdf_file(file_path)
    else:
        validator._add_warning(f"Unknown file type: {file_path.suffix}")

    validator._print_results()
    return len(validator.errors) == 0


def main():
    parser = argparse.ArgumentParser(description="Validate data files for the Advanced Job Engine")
    parser.add_argument(
        "path", nargs="?", default="job_search_data", help="Path to directory or file"
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--file", action="store_true", help="Validate a single file")
    args = parser.parse_args()

    try:
        validator = DataValidator(strict_mode=args.strict)
        target = Path(args.path)

        success = (
            validate_single_file(target, validator) if args.file else validator.validate_all(target)
        )
        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"\n❌ Validation error: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
