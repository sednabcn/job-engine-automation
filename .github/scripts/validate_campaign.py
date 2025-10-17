#!/usr/bin/env python3
"""
Validate Campaign - GitHub Actions Script
Validates job search campaign setup and requirements before running automation.
"""

import json
import os
import sys
import traceback
from pathlib import Path


class CampaignValidator:
    """Validate job search campaign configuration and requirements."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.data_dir = Path("job_search_data")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    # ============================================================
    # MASTER VALIDATION CALL
    # ============================================================
    def validate_all(self) -> bool:
        """Run all validation checks."""
        print("🔍 Validating Job Search Campaign Setup...")
        print("=" * 70)

        self.validate_directory_structure()
        self.validate_configuration()
        self.validate_cv_file()
        self.validate_job_files()
        self.validate_dependencies()
        self.validate_secrets()
        self.validate_permissions()

        return self.display_results()

    # ============================================================
    # VALIDATION METHODS
    # ============================================================
    def validate_directory_structure(self):
        """Validate required directory structure."""
        print("\n📁 Validating Directory Structure...")

        required_dirs = [
            "job_search_data",
            "data",
            ".github/scripts",
            ".github/workflows",
        ]

        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                self.info.append(f"✓ Directory exists: {dir_name}/")
            else:
                self.warnings.append(f"Directory missing: {dir_name}/")
                dir_path.mkdir(parents=True, exist_ok=True)
                self.info.append(f"✓ Created directory: {dir_name}/")

        important_files = [
            "README.md",
            "requirements.txt",
            ".gitignore",
            "setup.py",
        ]

        for file_name in important_files:
            file_path = Path(file_name)
            if file_path.exists():
                self.info.append(f"✓ File exists: {file_name}")
            else:
                self.warnings.append(f"File missing: {file_name}")

    def validate_configuration(self):
        """Validate configuration file."""
        print("\n⚙️  Validating Configuration...")

        config_path = self.data_dir / "config.json"
        if not config_path.exists():
            self.errors.append("Configuration file not found: job_search_data/config.json")
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            self.info.append("✓ Configuration file is valid JSON")

            required_sections = [
                "automation",
                "notifications",
                "analysis",
                "candidate",
                "preferences",
            ]

            for section in required_sections:
                if section not in config:
                    self.errors.append(f"Missing required config section: {section}")
                else:
                    self.info.append(f"✓ Config section exists: {section}")

            candidate = config.get("candidate", {})
            if not candidate.get("name") or candidate.get("name") == "Your Name":
                self.warnings.append("Candidate name not configured")
            else:
                self.info.append(f"✓ Candidate name: {candidate.get('name')}")

            if not candidate.get("email") or "@" not in candidate.get("email", ""):
                self.warnings.append("Valid candidate email not configured")
            else:
                self.info.append(f"✓ Candidate email: {candidate.get('email')}")

            if not candidate.get("cv_path"):
                self.errors.append("CV path not configured")
            else:
                self.info.append(f"✓ CV path configured: {candidate.get('cv_path')}")

            automation = config.get("automation", {})
            if automation.get("enabled"):
                schedule = automation.get("schedule")
                if not schedule:
                    self.warnings.append("Automation enabled but no schedule set")
                else:
                    self.info.append(f"✓ Automation schedule: {schedule}")

            notifications = config.get("notifications", {})
            if notifications.get("enabled"):
                email = notifications.get("email")
                slack = notifications.get("slack_webhook")
                if not email and not slack:
                    self.warnings.append("Notifications enabled but no contact method configured")
                else:
                    if email:
                        self.info.append("✓ Notification email configured")
                    if slack:
                        self.info.append("✓ Slack webhook configured")

        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            self.errors.append(f"Error validating configuration: {e}")

    def validate_cv_file(self):
        """Validate CV file exists and is readable."""
        print("\n📄 Validating CV File...")

        config_path = self.data_dir / "config.json"
        if not config_path.exists():
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            candidate = config.get("candidate", {})
            cv_path = candidate.get("cv_path", "")
            if not cv_path:
                return

            cv_file = Path(cv_path)
            if not cv_file.exists():
                self.errors.append(f"CV file not found: {cv_path}")
                self.info.append(f"💡 Place your CV at: {cv_path}")
                return

            self.info.append(f"✓ CV file exists: {cv_path}")

            size_mb = cv_file.stat().st_size / (1024 * 1024)
            if size_mb > 10:
                self.warnings.append(f"CV file is very large: {size_mb:.1f}MB")
            else:
                self.info.append(f"✓ CV file size: {size_mb:.2f}MB")

            valid_extensions = [".pdf", ".docx", ".txt"]
            ext = cv_file.suffix.lower()
            if ext not in valid_extensions:
                self.warnings.append(f"Unusual CV file extension: {ext}")
            else:
                self.info.append(f"✓ CV file format: {ext.upper()}")

        except Exception as e:
            self.errors.append(f"Error validating CV file: {e}")

    def validate_job_files(self):
        """Validate job description files."""
        print("\n💼 Validating Job Description Files...")

        data_dir = Path("data")
        if not data_dir.exists():
            self.warnings.append("Data directory not found - no job files to analyze")
            return

        job_patterns = ["*.txt", "*.pdf", "*.docx"]
        job_files = []
        for pattern in job_patterns:
            job_files.extend(list(data_dir.glob(pattern)))

        if not job_files:
            self.warnings.append("No job description files found in data/ directory")
            self.info.append("💡 Add job descriptions to data/ directory")
            return

        self.info.append(f"✓ Found {len(job_files)} job description file(s)")
        for job_file in job_files[:5]:
            self.info.append(f"  • {job_file.name}")
        if len(job_files) > 5:
            self.info.append(f"  ... and {len(job_files) - 5} more")

    def validate_dependencies(self):
        """Validate Python dependencies."""
        print("\n📦 Validating Dependencies...")

        requirements_file = Path("requirements.txt")
        if not requirements_file.exists():
            self.warnings.append("requirements.txt not found")
            return

        try:
            with open(requirements_file, "r", encoding="utf-8") as f:
                requirements = f.read().splitlines()

            self.info.append(f"✓ Found {len(requirements)} dependencies in requirements.txt")

            critical_packages = ["anthropic", "python-dotenv"]
            for package in critical_packages:
                found = any(package in req.lower() for req in requirements)
                if found:
                    self.info.append(f"✓ Critical package listed: {package}")
                else:
                    self.warnings.append(f"Critical package not in requirements: {package}")

        except Exception as e:
            self.errors.append(f"Error reading requirements.txt: {e}")

        # Check standard library modules
        try:
            import json  # noqa: F401

            self.info.append("✓ Python json module available")
        except ImportError:
            self.errors.append("Python json module not available")

        try:
            from pathlib import Path  # noqa: F401

            self.info.append("✓ Python pathlib module available")
        except ImportError:
            self.errors.append("Python pathlib module not available")

    def validate_secrets(self):
        """Validate GitHub secrets configuration."""
        print("\n🔐 Validating Secrets...")

        secret_vars = {
            "PYPI_API_TOKEN": "PyPI publishing",
            "TEST_PYPI_API_TOKEN": "Test PyPI publishing",
            "NOTIFICATION_EMAIL": "Email notifications",
            "SLACK_WEBHOOK": "Slack notifications",
        }

        for var_name, purpose in secret_vars.items():
            value = os.getenv(var_name)
            if value:
                self.info.append(f"✓ Secret configured: {var_name} ({purpose})")
            else:
                self.info.append(f"ℹ️  Optional secret not set: {var_name} ({purpose})")

    def validate_permissions(self):
        """Validate file permissions."""
        print("\n🔒 Validating Permissions...")

        try:
            test_file = self.data_dir / ".permission_test"
            test_file.touch()
            test_file.unlink()
            self.info.append("✓ Data directory is writable")
        except Exception as e:
            self.errors.append(f"Data directory not writable: {e}")

        try:
            export_dir = self.data_dir / "test_export"
            export_dir.mkdir(exist_ok=True)
            export_dir.rmdir()
            self.info.append("✓ Can create export directories")
        except Exception as e:
            self.errors.append(f"Cannot create export directories: {e}")

    # ============================================================
    # RESULTS DISPLAY
    # ============================================================
    def display_results(self) -> bool:
        """Display validation results."""
        print("\n" + "=" * 70)
        print("📊 VALIDATION RESULTS")
        print("=" * 70)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for e in self.errors:
                print(f"  • {e}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  • {w}")

        if not self.errors and not self.warnings:
            print("\n✅ SUCCESS - All validations passed!")
            for info in self.info:
                print(f"  {info}")

        print("\n" + "-" * 70)
        print(
            f"Summary: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} info"
        )
        print("=" * 70)

        if self.errors:
            print("\n🔧 NEXT STEPS:")
            print("  1. Fix the errors listed above")
            print("  2. Run validation again: python .github/scripts/validate_campaign.py")
        elif self.warnings:
            print("\n✅ Campaign can proceed with warnings")
        else:
            print("\n🚀 Campaign is ready to run!")

        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
                f.write(f"validation_passed={'true' if not self.errors else 'false'}\n")
                f.write(f"errors_count={len(self.errors)}\n")
                f.write(f"warnings_count={len(self.warnings)}\n")

        return len(self.errors) == 0


# ============================================================
# MAIN ENTRY
# ============================================================
def main():
    """Main execution entrypoint."""
    validator = CampaignValidator()
    try:
        success = validator.validate_all()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Validation failed with exception: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
