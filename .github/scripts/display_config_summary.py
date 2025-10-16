#!/usr/bin/env python3
"""
Configuration Summary Display Script
Displays job engine configuration in a clean, organized format with validation.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class ConfigValidator:
    """Validates configuration and identifies issues."""
    
    def __init__(self):
        self.warnings: List[str] = []
        self.errors: List[str] = []
    
    def validate(self, config: Dict[str, Any]) -> bool:
        """Validate configuration and collect issues."""
        self.warnings.clear()
        self.errors.clear()
        
        # Validate automation settings
        self._validate_automation(config.get('automation', {}))
        
        # Validate notifications
        self._validate_notifications(config.get('notifications', {}))
        
        # Validate candidate info
        self._validate_candidate(config.get('candidate', {}))
        
        # Validate job preferences
        self._validate_job_preferences(config.get('job_preferences', {}))
        
        # Validate analysis settings
        self._validate_analysis(config.get('analysis', {}))
        
        return len(self.errors) == 0
    
    def _validate_automation(self, automation: Dict[str, Any]):
        """Validate automation settings."""
        if not automation:
            self.warnings.append("Automation settings not configured")
            return
        
        if automation.get('enabled') and not automation.get('schedule'):
            self.warnings.append("Automation enabled but no schedule set")
        
        auto_apply = automation.get('auto_apply', {})
        if auto_apply.get('enabled'):
            if auto_apply.get('min_match_score', 0) < 60:
                self.warnings.append("Auto-apply minimum match score is quite low (<60%)")
    
    def _validate_notifications(self, notifications: Dict[str, Any]):
        """Validate notification settings."""
        if not notifications:
            self.warnings.append("Notification settings not configured")
            return
        
        email = notifications.get('email', {})
        if email.get('enabled'):
            if not email.get('recipient'):
                self.errors.append("Email notifications enabled but no recipient specified")
            if not email.get('smtp_host'):
                self.errors.append("Email notifications enabled but no SMTP host configured")
        
        slack = notifications.get('slack', {})
        if slack.get('enabled') and not slack.get('webhook_url'):
            self.errors.append("Slack notifications enabled but no webhook URL configured")
    
    def _validate_candidate(self, candidate: Dict[str, Any]):
        """Validate candidate information."""
        if not candidate:
            self.warnings.append("Candidate information not configured")
            return
        
        required_fields = ['name', 'email']
        for field in required_fields:
            if not candidate.get(field):
                self.warnings.append(f"Candidate {field} not specified")
        
        if candidate.get('email') and '@' not in candidate['email']:
            self.errors.append("Invalid email format")
    
    def _validate_job_preferences(self, prefs: Dict[str, Any]):
        """Validate job preferences."""
        if not prefs:
            self.warnings.append("Job preferences not configured")
            return
        
        if not prefs.get('target_roles'):
            self.warnings.append("No target roles specified")
        
        if not prefs.get('preferred_locations'):
            self.warnings.append("No preferred locations specified")
        
        salary = prefs.get('salary_range', {})
        if salary.get('min') and salary.get('max'):
            if salary['min'] > salary['max']:
                self.errors.append("Minimum salary is greater than maximum salary")
    
    def _validate_analysis(self, analysis: Dict[str, Any]):
        """Validate analysis settings."""
        if not analysis:
            self.warnings.append("Analysis settings not configured")
            return
        
        weights = analysis.get('scoring_weights', {})
        if weights:
            total = sum(weights.values())
            if abs(total - 1.0) > 0.01:
                self.warnings.append(f"Scoring weights sum to {total:.2f}, should sum to 1.0")


class ConfigDisplay:
    """Displays configuration in a formatted, organized way."""
    
    # ANSI color codes
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    def __init__(self, config: Dict[str, Any], validator: ConfigValidator):
        self.config = config
        self.validator = validator
    
    def display(self):
        """Display complete configuration summary."""
        self._print_header()
        self._print_automation_settings()
        self._print_notification_settings()
        self._print_candidate_info()
        self._print_job_preferences()
        self._print_analysis_settings()
        self._print_validation_results()
        self._print_footer()
    
    def _print_header(self):
        """Print header section."""
        print(f"\n{self.HEADER}{self.BOLD}╔═══════════════════════════════════════════════════════════╗{self.END}")
        print(f"{self.HEADER}{self.BOLD}║     JOB ENGINE CONFIGURATION SUMMARY                      ║{self.END}")
        print(f"{self.HEADER}{self.BOLD}╚═══════════════════════════════════════════════════════════╝{self.END}\n")
        print(f"{self.CYAN}Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{self.END}\n")
    
    def _print_section_header(self, title: str):
        """Print section header."""
        print(f"\n{self.BLUE}{self.BOLD}━━━ {title} ━━━{self.END}")
    
    def _print_automation_settings(self):
        """Display automation settings."""
        self._print_section_header("⚙️  AUTOMATION SETTINGS")
        automation = self.config.get('automation', {})
        
        if not automation:
            print(f"{self.YELLOW}  ⚠ Not configured{self.END}")
            return
        
        enabled = automation.get('enabled', False)
        status = f"{self.GREEN}✓ Enabled{self.END}" if enabled else f"{self.RED}✗ Disabled{self.END}"
        print(f"  Status: {status}")
        
        if automation.get('schedule'):
            print(f"  Schedule: {automation['schedule']}")
        
        # Auto-apply settings
        auto_apply = automation.get('auto_apply', {})
        if auto_apply:
            print(f"\n  {self.BOLD}Auto-Apply:{self.END}")
            print(f"    Enabled: {self._format_bool(auto_apply.get('enabled', False))}")
            print(f"    Min Match Score: {auto_apply.get('min_match_score', 'N/A')}%")
            print(f"    Max Applications/Day: {auto_apply.get('max_applications_per_day', 'N/A')}")
        
        # Workflow settings
        workflow = automation.get('workflow', {})
        if workflow:
            print(f"\n  {self.BOLD}Workflow:{self.END}")
            print(f"    Auto-generate documents: {self._format_bool(workflow.get('auto_generate_documents', False))}")
            print(f"    Auto-create sprints: {self._format_bool(workflow.get('auto_create_sprints', False))}")
            print(f"    Auto-track progress: {self._format_bool(workflow.get('auto_track_progress', False))}")
    
    def _print_notification_settings(self):
        """Display notification settings."""
        self._print_section_header("🔔 NOTIFICATION SETTINGS")
        notifications = self.config.get('notifications', {})
        
        if not notifications:
            print(f"{self.YELLOW}  ⚠ Not configured{self.END}")
            return
        
        # Email notifications
        email = notifications.get('email', {})
        print(f"  {self.BOLD}Email:{self.END}")
        print(f"    Enabled: {self._format_bool(email.get('enabled', False))}")
        if email.get('enabled'):
            print(f"    Recipient: {email.get('recipient', 'N/A')}")
            print(f"    SMTP Host: {email.get('smtp_host', 'N/A')}")
            print(f"    SMTP Port: {email.get('smtp_port', 'N/A')}")
        
        # Slack notifications
        slack = notifications.get('slack', {})
        print(f"\n  {self.BOLD}Slack:{self.END}")
        print(f"    Enabled: {self._format_bool(slack.get('enabled', False))}")
        if slack.get('enabled'):
            webhook = slack.get('webhook_url', '')
            masked = f"{webhook[:20]}..." if len(webhook) > 20 else webhook
            print(f"    Webhook: {masked}")
        
        # Notification events
        events = notifications.get('notify_on', [])
        if events:
            print(f"\n  {self.BOLD}Notify On:{self.END}")
            for event in events:
                print(f"    • {event}")
    
    def _print_candidate_info(self):
        """Display candidate information."""
        self._print_section_header("👤 CANDIDATE INFORMATION")
        candidate = self.config.get('candidate', {})
        
        if not candidate:
            print(f"{self.YELLOW}  ⚠ Not configured{self.END}")
            return
        
        print(f"  Name: {candidate.get('name', 'N/A')}")
        print(f"  Email: {candidate.get('email', 'N/A')}")
        print(f"  Phone: {candidate.get('phone', 'N/A')}")
        print(f"  LinkedIn: {candidate.get('linkedin', 'N/A')}")
        print(f"  GitHub: {candidate.get('github', 'N/A')}")
        print(f"  Portfolio: {candidate.get('portfolio', 'N/A')}")
        
        if candidate.get('current_title'):
            print(f"  Current Title: {candidate['current_title']}")
        
        if candidate.get('years_experience'):
            print(f"  Years Experience: {candidate['years_experience']}")
    
    def _print_job_preferences(self):
        """Display job preferences."""
        self._print_section_header("🎯 JOB PREFERENCES")
        prefs = self.config.get('job_preferences', {})
        
        if not prefs:
            print(f"{self.YELLOW}  ⚠ Not configured{self.END}")
            return
        
        # Target roles
        roles = prefs.get('target_roles', [])
        if roles:
            print(f"  {self.BOLD}Target Roles:{self.END}")
            for role in roles:
                print(f"    • {role}")
        
        # Preferred locations
        locations = prefs.get('preferred_locations', [])
        if locations:
            print(f"\n  {self.BOLD}Preferred Locations:{self.END}")
            for loc in locations:
                print(f"    • {loc}")
        
        # Work settings
        print(f"\n  {self.BOLD}Work Settings:{self.END}")
        print(f"    Remote OK: {self._format_bool(prefs.get('remote_ok', False))}")
        print(f"    Hybrid OK: {self._format_bool(prefs.get('hybrid_ok', False))}")
        print(f"    Relocation OK: {self._format_bool(prefs.get('willing_to_relocate', False))}")
        
        # Employment type
        emp_types = prefs.get('employment_type', [])
        if emp_types:
            print(f"    Employment Types: {', '.join(emp_types)}")
        
        # Salary range
        salary = prefs.get('salary_range', {})
        if salary:
            print(f"\n  {self.BOLD}Salary Range:{self.END}")
            print(f"    Min: ${salary.get('min', 'N/A'):,}" if salary.get('min') else "    Min: N/A")
            print(f"    Max: ${salary.get('max', 'N/A'):,}" if salary.get('max') else "    Max: N/A")
            print(f"    Currency: {salary.get('currency', 'N/A')}")
        
        # Deal breakers
        deal_breakers = prefs.get('deal_breakers', [])
        if deal_breakers:
            print(f"\n  {self.BOLD}Deal Breakers:{self.END}")
            for item in deal_breakers:
                print(f"    ✗ {item}")
    
    def _print_analysis_settings(self):
        """Display analysis settings."""
        self._print_section_header("📊 ANALYSIS SETTINGS")
        analysis = self.config.get('analysis', {})
        
        if not analysis:
            print(f"{self.YELLOW}  ⚠ Not configured{self.END}")
            return
        
        # Scoring weights
        weights = analysis.get('scoring_weights', {})
        if weights:
            print(f"  {self.BOLD}Scoring Weights:{self.END}")
            for key, value in weights.items():
                percentage = value * 100
                bar = self._create_bar(value, 20)
                print(f"    {key.replace('_', ' ').title()}: {bar} {percentage:.0f}%")
        
        # Thresholds
        print(f"\n  {self.BOLD}Thresholds:{self.END}")
        print(f"    Strong Match: {analysis.get('strong_match_threshold', 'N/A')}%")
        print(f"    Weak Match: {analysis.get('weak_match_threshold', 'N/A')}%")
        
        # Sprint settings
        sprint = analysis.get('sprint_settings', {})
        if sprint:
            print(f"\n  {self.BOLD}Sprint Settings:{self.END}")
            print(f"    Default Duration: {sprint.get('default_duration_weeks', 'N/A')} weeks")
            print(f"    Default Capacity: {sprint.get('default_capacity_hours', 'N/A')} hours/week")
    
    def _print_validation_results(self):
        """Display validation warnings and errors."""
        if not self.validator.warnings and not self.validator.errors:
            print(f"\n{self.GREEN}{self.BOLD}✓ Configuration is valid{self.END}")
            return
        
        if self.validator.warnings:
            self._print_section_header("⚠️  WARNINGS")
            for warning in self.validator.warnings:
                print(f"  {self.YELLOW}⚠{self.END} {warning}")
        
        if self.validator.errors:
            self._print_section_header("❌ ERRORS")
            for error in self.validator.errors:
                print(f"  {self.RED}✗{self.END} {error}")
    
    def _print_footer(self):
        """Print footer section."""
        print(f"\n{self.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{self.END}\n")
    
    def _format_bool(self, value: bool) -> str:
        """Format boolean value with color."""
        return f"{self.GREEN}Yes{self.END}" if value else f"{self.RED}No{self.END}"
    
    def _create_bar(self, value: float, width: int = 20) -> str:
        """Create a visual bar for numeric values."""
        filled = int(value * width)
        bar = '█' * filled + '░' * (width - filled)
        return f"{self.CYAN}{bar}{self.END}"


def create_default_config() -> Dict[str, Any]:
    """Create a default configuration template."""
    return {
        "automation": {
            "enabled": False,
            "schedule": "0 9 * * 1-5",
            "auto_apply": {
                "enabled": False,
                "min_match_score": 75,
                "max_applications_per_day": 5
            },
            "workflow": {
                "auto_generate_documents": False,
                "auto_create_sprints": False,
                "auto_track_progress": True
            }
        },
        "notifications": {
            "email": {
                "enabled": False,
                "recipient": "",
                "smtp_host": "",
                "smtp_port": 587
            },
            "slack": {
                "enabled": False,
                "webhook_url": ""
            },
            "notify_on": ["high_match_found", "application_submitted", "sprint_completed"]
        },
        "candidate": {
            "name": "",
            "email": "",
            "phone": "",
            "linkedin": "",
            "github": "",
            "portfolio": ""
        },
        "job_preferences": {
            "target_roles": [],
            "preferred_locations": [],
            "remote_ok": True,
            "hybrid_ok": True,
            "willing_to_relocate": False,
            "employment_type": ["full-time"],
            "salary_range": {
                "min": None,
                "max": None,
                "currency": "USD"
            },
            "deal_breakers": []
        },
        "analysis": {
            "scoring_weights": {
                "skills_match": 0.4,
                "experience_match": 0.25,
                "education_match": 0.15,
                "culture_fit": 0.2
            },
            "strong_match_threshold": 75,
            "weak_match_threshold": 50,
            "sprint_settings": {
                "default_duration_weeks": 2,
                "default_capacity_hours": 10
            }
        }
    }


def main():
    """Main execution function."""
    # Determine config file path
    config_path = Path("config.json")
    
    # Check for custom path from command line
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    
    # Load or create configuration
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"Loaded configuration from: {config_path}")
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}")
            sys.exit(1)
    else:
        print(f"Configuration file not found at: {config_path}")
        print("Creating default configuration...")
        config = create_default_config()
        
        # Save default config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Default configuration saved to: {config_path}")
    
    # Validate configuration
    validator = ConfigValidator()
    is_valid = validator.validate(config)
    
    # Display configuration
    display = ConfigDisplay(config, validator)
    display.display()
    
    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()

"""
Key Features:

Configuration Loading & Validation

Loads config from config.json or custom path
Creates default config if missing
Validates all settings with detailed checks


Organized Display Sections

⚙️ Automation Settings (enabled/disabled, schedule, auto-apply rules)
🔔 Notification Settings (email, Slack, notification events)
👤 Candidate Information (name, contact details, experience)
🎯 Job Preferences (roles, locations, salary, deal breakers)
📊 Analysis Settings (scoring weights with visual bars, thresholds)


Validation System

Checks for missing required fields
Validates email formats, salary ranges, scoring weights
Identifies configuration inconsistencies
Separates warnings and errors


Clean Formatted Output

Color-coded sections (headers, warnings, errors, success)
Visual progress bars for scoring weights
Boolean values displayed as Yes/No with colors
Formatted currency and percentage values
Clean sectioned layout with Unicode characters


Smart Features

Masks sensitive data (webhook URLs)
Handles missing sections gracefully
Provides helpful warnings
Exit codes (0 for valid, 1 for errors)
Command-line config path support



Usage:
bashpython display_config_summary.py
python display_config_summary.py path/to/custom/config.jsonRetryClaude does not have the ability to run the code it generates yet.Claude can make mistakes. Please double-check responses. Sonnet 4.5
"""
