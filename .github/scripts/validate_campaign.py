#!/usr/bin/env python3
"""
Validate Campaign - GitHub Actions Script
Validates job search campaign setup and requirements before running automation
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Tuple


class CampaignValidator:
    """Validate job search campaign configuration and requirements"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.data_dir = Path("job_search_data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_all(self) -> bool:
        """Run all validation checks"""
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
    
    def validate_directory_structure(self):
        """Validate required directory structure"""
        print("\n📁 Validating Directory Structure...")
        
        required_dirs = [
            "job_search_data",
            "data",
            "docs",
            "src",
            "tests"
        ]
        
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                self.info.append(f"✓ Directory exists: {dir_name}/")
            else:
                self.warnings.append(f"Directory missing: {dir_name}/")
                dir_path.mkdir(parents=True, exist_ok=True)
                self.info.append(f"✓ Created directory: {dir_name}/")
        
        # Check for important files
        important_files = [
            "README.md",
            "requirements.txt",
            ".gitignore"
        ]
        
        for file_name in important_files:
            if Path(file_name).exists():
                self.info.append(f"✓ File exists: {file_name}")
            else:
                self.warnings.append(f"File missing: {file_name}")
    
    def validate_configuration(self):
        """Validate configuration file"""
        print("\n⚙️  Validating Configuration...")
        
        config_path = self.data_dir / "config.json"
        
        if not config_path.exists():
            self.errors.append("Configuration file not found: job_search_data/config.json")
            return
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            self.info.append("✓ Configuration file is valid JSON")
            
            # Validate required sections
            required_sections = ['automation', 'notifications', 'analysis', 'candidate', 'preferences']
            for section in required_sections:
                if section not in config:
                    self.errors.append(f"Missing required config section: {section}")
                else:
                    self.info.append(f"✓ Config section exists: {section}")
            
            # Validate candidate information
            candidate = config.get('candidate', {})
            
            if not candidate.get('name') or candidate.get('name') == 'Your Name':
                self.warnings.append("Candidate name not configured")
            else:
                self.info.append(f"✓ Candidate name: {candidate.get('name')}")
            
            if not candidate.get('email') or '@' not in candidate.get('email', ''):
                self.warnings.append("Valid candidate email not configured")
            else:
                self.info.append(f"✓ Candidate email: {candidate.get('email')}")
            
            if not candidate.get('cv_path'):
                self.errors.append("CV path not configured")
            else:
                self.info.append(f"✓ CV path configured: {candidate.get('cv_path')}")
            
            # Validate automation settings
            automation = config.get('automation', {})
            if automation.get('enabled'):
                if not automation.get('schedule'):
                    self.warnings.append("Automation enabled but no schedule set")
                else:
                    self.info.append(f"✓ Automation schedule: {automation.get('schedule')}")
            
            # Validate notifications
            notifications = config.get('notifications', {})
            if notifications.get('enabled'):
                if not notifications.get('email') and not notifications.get('slack_webhook'):
                    self.warnings.append("Notifications enabled but no contact method configured")
                else:
                    if notifications.get('email'):
                        self.info.append(f"✓ Notification email configured")
                    if notifications.get('slack_webhook'):
                        self.info.append(f"✓ Slack webhook configured")
            
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            self.errors.append(f"Error validating configuration: {e}")
    
    def validate_cv_file(self):
        """Validate CV file exists and is readable"""
        print("\n📄 Validating CV File...")
        
        config_path = self.data_dir / "config.json"
        
        if not config_path.exists():
            return  # Already reported in config validation
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            cv_path = config.get('candidate', {}).get('cv_path')
            
            if not cv_path:
                return  # Already reported in config validation
            
            cv_file = Path(cv_path)
            
            if not cv_file.exists():
                self.errors.append(f"CV file not found: {cv_path}")
                self.info.append(f"💡 Place your CV at: {cv_path}")
            else:
                self.info.append(f"✓ CV file exists: {cv_path}")
                
                # Check file size
                size_mb = cv_file.stat().st_size / (1024 * 1024)
                if size_mb > 10:
                    self.warnings.append(f"CV file is very large: {size_mb:.1f}MB")
                else:
                    self.info.append(f"✓ CV file size: {size_mb:.2f}MB")
                
                # Check file extension
                valid_extensions = ['.pdf', '.docx', '.doc', '.txt']
                if cv_file.suffix.lower() not in valid_extensions:
                    self.warnings.append(f"Unusual CV file extension: {cv_file.suffix}")
                else:
                    self.info.append(f"✓ CV file format: {cv_file.suffix.upper()}")
        
        except Exception as e:
            self.errors.append(f"Error validating CV file: {e}")
    
    def validate_job_files(self):
        """Validate job description files"""
        print("\n💼 Validating Job Description Files...")
        
        data_dir = Path("data")
        
        if not data_dir.exists():
            self.warnings.append("Data directory not found - no job files to analyze")
            return
        
        # Look for job files
        job_patterns = ['*job*.txt', '*job*.pdf', '*position*.txt', '*role*.txt']
        job_files = []
        
        for pattern in job_patterns:
            job_files.extend(data_dir.glob(pattern))
        
        if not job_files:
            self.warnings.append("No job description files found in data/ directory")
            self.info.append("💡 Add job descriptions to data/ directory")
        else:
            self.info.append(f"✓ Found {len(job_files)} job description file(s)")
            for job_file in job_files[:5]:  # Show first 5
                self.info.append(f"  • {job_file.name}")
            
            if len(job_files) > 5:
                self.info.append(f"  ... and {len(job_files) - 5} more")
    
    def validate_dependencies(self):
        """Validate Python dependencies"""
        print("\n📦 Validating Dependencies...")
        
        requirements_file = Path("requirements.txt")
        
        if not requirements_file.exists():
            self.warnings.append("requirements.txt not found")
            return
        
        try:
            with open(requirements_file, 'r') as f:
                requirements = f.read().splitlines()
            
            self.info.append(f"✓ Found {len(requirements)} dependencies in requirements.txt")
            
            # Check if critical packages are listed
            critical_packages = ['pytest', 'pandas', 'numpy']
            
            for package in critical_packages:
                found = any(package in req.lower() for req in requirements)
                if found:
                    self.info.append(f"✓ Critical package listed: {package}")
                else:
                    self.warnings.append(f"Critical package not in requirements: {package}")
        
        except Exception as e:
            self.errors.append(f"Error reading requirements.txt: {e}")
        
        # Try to import critical modules
        try:
            import json
            self.info.append("✓ Python json module available")
        except ImportError:
            self.errors.append("Python json module not available")
        
        try:
            from pathlib import Path
            self.info.append("✓ Python pathlib module available")
        except ImportError:
            self.errors.append("Python pathlib module not available")
    
    def validate_secrets(self):
        """Validate GitHub secrets configuration"""
        print("\n🔐 Validating Secrets...")
        
        # Check for environment variables that should be secrets
        secret_vars = {
            'PYPI_API_TOKEN': 'PyPI publishing',
            'TEST_PYPI_API_TOKEN': 'Test PyPI publishing',
            'NOTIFICATION_EMAIL': 'Email notifications',
            'SLACK_WEBHOOK': 'Slack notifications'
        }
        
        for var_name, purpose in secret_vars.items():
            if os.getenv(var_name):
                self.info.append(f"✓ Secret configured: {var_name} ({purpose})")
            else:
                self.info.append(f"ℹ️  Optional secret not set: {var_name} ({purpose})")
    
    def validate_permissions(self):
        """Validate file permissions"""
        print("\n🔒 Validating Permissions...")
        
        # Check if data directory is writable
        try:
            test_file = self.data_dir / ".permission_test"
            test_file.touch()
            test_file.unlink()
            self.info.append("✓ Data directory is writable")
        except Exception as e:
            self.errors.append(f"Data directory not writable: {e}")
        
        # Check if we can create export directories
        try:
            export_dir = self.data_dir / "test_export"
            export_dir.mkdir(exist_ok=True)
            export_dir.rmdir()
            self.info.append("✓ Can create export directories")
        except Exception as e:
            self.errors.append(f"Cannot create export directories: {e}")
    
    def display_results(self) -> bool:
        """Display validation results"""
        print("\n" + "=" * 70)
        print("📊 VALIDATION RESULTS")
        print("=" * 70)
        
        # Display errors
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        # Display warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        # Display info (only if verbose or no errors/warnings)
        if not self.errors and not self.warnings:
            print(f"\n✅ SUCCESS - All validations passed!")
            if self.info:
                print(f"\nℹ️  DETAILS ({len(self.info)}):")
                for info in self.info:
                    print(f"  {info}")
        
        # Summary
        print("\n" + "-" * 70)
        print(f"Summary: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} info")
        print("=" * 70)
        
        # Provide next steps
        if self.errors:
            print("\n🔧 NEXT STEPS:")
            print("  1. Fix the errors listed above")
            print("  2. Run validation again: python .github/scripts/validate_campaign.py")
            print("  3. Once validation passes, run the campaign")
        elif self.warnings:
            print("\n✅ Campaign can proceed with warnings")
            print("⚠️  Consider addressing warnings for optimal results")
        else:
            print("\n🚀 Campaign is ready to run!")
        
        print()
        
        # Set GitHub Actions output
        if 'GITHUB_OUTPUT' in os.environ:
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write(f"validation_passed={'true' if not self.errors else 'false'}\n")
                f.write(f"errors_count={len(self.errors)}\n")
                f.write(f"warnings_count={len(self.warnings)}\n")
        
        # Return success if no errors
        return len(self.errors) == 0


def main():
    """Main execution"""
    validator = CampaignValidator()
    
    try:
        success = validator.validate_all()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Validation failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
