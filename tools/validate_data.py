#!/usr/bin/env python3
"""
validate_data.py - Data validation tool for the job engine

This tool validates:
- CV files and format
- Job description files and format
- JSON data files and schema
- Configuration files
- Generated reports and outputs
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re


class DataValidator:
    """Validate various data files and formats."""
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize the data validator.
        
        Args:
            strict_mode: If True, treat warnings as errors
        """
        self.strict_mode = strict_mode
        self.errors = []
        self.warnings = []
        self.info = []
    
    def validate_all(self, data_dir: Path) -> bool:
        """
        Validate all data files in a directory.
        
        Args:
            data_dir: Directory containing data files
            
        Returns:
            True if validation passes, False otherwise
        """
        print("🔍 Starting comprehensive data validation...\n")
        
        data_dir = Path(data_dir)
        
        if not data_dir.exists():
            self._add_error(f"Data directory not found: {data_dir}")
            return False
        
        # Validate different file types
        self._validate_cv_files(data_dir)
        self._validate_job_files(data_dir)
        self._validate_json_files(data_dir)
        self._validate_output_files(data_dir)
        
        # Print results
        self._print_results()
        
        # Determine if validation passed
        has_errors = len(self.errors) > 0
        has_warnings = len(self.warnings) > 0
        
        if self.strict_mode and has_warnings:
            return False
        
        return not has_errors
    
    def _validate_cv_files(self, data_dir: Path):
        """Validate CV files."""
        print("📄 Validating CV files...")
        
        cv_files = list(data_dir.glob("*cv*.txt")) + list(data_dir.glob("*cv*.pdf"))
        
        if not cv_files:
            self._add_warning("No CV files found")
            return
        
        for cv_file in cv_files:
            if cv_file.suffix == '.txt':
                self._validate_cv_text_file(cv_file)
            elif cv_file.suffix == '.pdf':
                self._validate_pdf_file(cv_file)
    
    def _validate_cv_text_file(self, cv_file: Path):
        """Validate CV text file content."""
        try:
            with open(cv_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check minimum length
            if len(content) < 200:
                self._add_error(f"{cv_file.name}: CV content too short (< 200 characters)")
            
            # Check for required sections (flexible matching)
            required_patterns = {
                'contact': r'(email|phone|contact)',
                'experience': r'(experience|work history|employment)',
                'skills': r'(skills|technical skills|competencies)',
                'education': r'(education|academic|degree)'
            }
            
            content_lower = content.lower()
            
            for section, pattern in required_patterns.items():
                if not re.search(pattern, content_lower):
                    self._add_warning(f"{cv_file.name}: Missing '{section}' section")
            
            # Check for email format
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not re.search(email_pattern, content):
                self._add_warning(f"{cv_file.name}: No valid email address found")
            
            # Check for phone number
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            if not re.search(phone_pattern, content):
                self._add_warning(f"{cv_file.name}: No phone number found")
            
            self._add_info(f"{cv_file.name}: Valid CV file ({len(content)} characters)")
            
        except Exception as e:
            self._add_error(f"{cv_file.name}: Error reading file - {str(e)}")
    
    def _validate_job_files(self, data_dir: Path):
        """Validate job description files."""
        print("💼 Validating job description files...")
        
        job_files = list(data_dir.glob("*job*.txt")) + list(data_dir.glob("*job*.pdf"))
        
        if not job_files:
            self._add_warning("No job description files found")
            return
        
        for job_file in job_files:
            if job_file.suffix == '.txt':
                self._validate_job_text_file(job_file)
            elif job_file.suffix == '.pdf':
                self._validate_pdf_file(job_file)
    
    def _validate_job_text_file(self, job_file: Path):
        """Validate job description text file content."""
        try:
            with open(job_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check minimum length
            if len(content) < 300:
                self._add_error(f"{job_file.name}: Job description too short (< 300 characters)")
            
            # Check for required sections
            required_patterns = {
                'title': r'(job title|position|role)',
                'requirements': r'(requirements|qualifications|required)',
                'responsibilities': r'(responsibilities|duties|will be)',
                'skills': r'(skills|technologies|experience with)'
            }
            
            content_lower = content.lower()
            
            for section, pattern in required_patterns.items():
                if not re.search(pattern, content_lower):
                    self._add_warning(f"{job_file.name}: Missing '{section}' section")
            
            # Check for company name
            if not re.search(r'company:', content_lower):
                self._add_warning(f"{job_file.name}: Company name not clearly specified")
            
            # Check for location
            if not re.search(r'location:', content_lower):
                self._add_warning(f"{job_file.name}: Location not specified")
            
            self._add_info(f"{job_file.name}: Valid job description ({len(content)} characters)")
            
        except Exception as e:
            self._add_error(f"{job_file.name}: Error reading file - {str(e)}")
    
    def _validate_pdf_file(self, pdf_file: Path):
        """Validate PDF file exists and has reasonable size."""
        try:
            file_size = pdf_file.stat().st_size
            
            if file_size == 0:
                self._add_error(f"{pdf_file.name}: PDF file is empty")
            elif file_size < 1024:  # Less than 1KB
                self._add_warning(f"{pdf_file.name}: PDF file suspiciously small ({file_size} bytes)")
            elif file_size > 10 * 1024 * 1024:  # More than 10MB
                self._add_warning(f"{pdf_file.name}: PDF file very large ({file_size / (1024*1024):.1f} MB)")
            else:
                self._add_info(f"{pdf_file.name}: Valid PDF file ({file_size / 1024:.1f} KB)")
            
        except Exception as e:
            self._add_error(f"{pdf_file.name}: Error checking PDF - {str(e)}")
    
    def _validate_json_files(self, data_dir: Path):
        """Validate JSON data files."""
        print("📊 Validating JSON data files...")
        
        json_files = list(data_dir.glob("**/*.json"))
        
        if not json_files:
            self._add_warning("No JSON files found")
            return
        
        for json_file in json_files:
            self._validate_json_file(json_file)
    
    def _validate_json_file(self, json_file: Path):
        """Validate individual JSON file."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate based on file name/type
            if 'master_skillset' in json_file.name or 'skillset' in json_file.name:
                self._validate_skillset_json(json_file, data)
            
            elif 'analyzed_jobs' in json_file.name or 'analysis' in json_file.name:
                self._validate_analysis_json(json_file, data)
            
            elif 'learning' in json_file.name or 'plan' in json_file.name:
                self._validate_learning_json(json_file, data)
            
            elif 'sprint' in json_file.name:
                self._validate_sprint_json(json_file, data)
            
            else:
                self._add_info(f"{json_file.name}: Valid JSON file")
            
        except json.JSONDecodeError as e:
            self._add_error(f"{json_file.name}: Invalid JSON - {str(e)}")
        except Exception as e:
            self._add_error(f"{json_file.name}: Error validating JSON - {str(e)}")
    
    def _validate_skillset_json(self, file_path: Path, data: Dict[str, Any]):
        """Validate skillset JSON structure."""
        required_fields = ['technical_skills']
        
        for field in required_fields:
            if field not in data:
                self._add_error(f"{file_path.name}: Missing required field '{field}'")
        
        if 'technical_skills' in data:
            tech_skills = data['technical_skills']
            
            expected_categories = ['programming_languages', 'frameworks', 'databases', 'cloud_devops']
            for category in expected_categories:
                if category not in tech_skills:
                    self._add_warning(f"{file_path.name}: Missing skill category '{category}'")
        
        self._add_info(f"{file_path.name}: Valid skillset JSON")
    
    def _validate_analysis_json(self, file_path: Path, data: Dict[str, Any]):
        """Validate analysis JSON structure."""
        if isinstance(data, list):
            for item in data:
                self._validate_single_analysis(file_path, item)
        elif isinstance(data, dict):
            self._validate_single_analysis(file_path, data)
        
        self._add_info(f"{file_path.name}: Valid analysis JSON")
    
    def _validate_single_analysis(self, file_path: Path, analysis: Dict[str, Any]):
        """Validate single job analysis structure."""
        required_fields = ['job_id', 'match_score']
        
        for field in required_fields:
            if field not in analysis:
                self._add_error(f"{file_path.name}: Missing required field '{field}' in analysis")
        
        if 'match_score' in analysis:
            score = analysis['match_score']
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                self._add_error(f"{file_path.name}: Invalid match_score value: {score}")
    
    def _validate_learning_json(self, file_path: Path, data: Dict[str, Any]):
        """Validate learning plan JSON structure."""
        expected_fields = ['skills_in_progress', 'completed_skills', 'planned_skills']
        
        for field in expected_fields:
            if field not in data:
                self._add_warning(f"{file_path.name}: Missing field '{field}'")
        
        self._add_info(f"{file_path.name}: Valid learning plan JSON")
    
    def _validate_sprint_json(self, file_path: Path, data: Dict[str, Any]):
        """Validate sprint JSON structure."""
        if isinstance(data, list):
            for sprint in data:
                self._validate_single_sprint(file_path, sprint)
        elif isinstance(data, dict):
            self._validate_single_sprint(file_path, data)
        
        self._add_info(f"{file_path.name}: Valid sprint JSON")
    
    def _validate_single_sprint(self, file_path: Path, sprint: Dict[str, Any]):
        """Validate single sprint structure."""
        required_fields = ['sprint_number', 'start_date', 'end_date', 'goals']
        
        for field in required_fields:
            if field not in sprint:
                self._add_error(f"{file_path.name}: Missing required field '{field}' in sprint")
        
        # Validate dates
        if 'start_date' in sprint and 'end_date' in sprint:
            try:
                start = datetime.fromisoformat(sprint['start_date'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(sprint['end_date'].replace('Z', '+00:00'))
                
                if end <= start:
                    self._add_error(f"{file_path.name}: Sprint end_date must be after start_date")
            except ValueError:
                self._add_error(f"{file_path.name}: Invalid date format in sprint")
    
    def _validate_output_files(self, data_dir: Path):
        """Validate output/export files."""
        print("📦 Validating output files...")
        
        export_dirs = list(data_dir.glob("export_*"))
        
        if not export_dirs:
            self._add_info("No export directories found (this is okay)")
            return
        
        for export_dir in export_dirs:
            self._validate_export_directory(export_dir)
    
    def _validate_export_directory(self, export_dir: Path):
        """Validate export directory contents."""
        expected_files = [
            'complete_report.txt',
            'learning_plan.json',
            'improvement_strategy.json'
        ]
        
        for expected_file in expected_files:
            file_path = export_dir / expected_file
            if not file_path.exists():
                self._add_warning(f"{export_dir.name}: Missing expected file '{expected_file}'")
        
        # Count actual files
        actual_files = list(export_dir.glob("*"))
        self._add_info(f"{export_dir.name}: Contains {len(actual_files)} files")
    
    def _add_error(self, message: str):
        """Add an error message."""
        self.errors.append(message)
    
    def _add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)
    
    def _add_info(self, message: str):
        """Add an info message."""
        self.info.append(message)
    
    def _print_results(self):
        """Print validation results."""
        print("\n" + "=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.info:
            print(f"\n✅ INFO ({len(self.info)}):")
            for info_msg in self.info:
                print(f"  • {info_msg}")
        
        print("\n" + "=" * 70)
        print(f"Summary: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} info")
        print("=" * 70)
        
        if not self.errors and not self.warnings:
            print("\n🎉 All validations passed!")
        elif not self.errors:
            print("\n✓ Validation passed with warnings")
        else:
            print("\n✗ Validation failed")


def validate_single_file(file_path: Path, validator: DataValidator) -> bool:
    """Validate a single file."""
    print(f"🔍 Validating: {file_path}\n")
    
    if not file_path.exists():
        validator._add_error(f"File not found: {file_path}")
        validator._print_results()
        return False
    
    if file_path.suffix == '.json':
        validator._validate_json_file(file_path)
    elif file_path.suffix == '.txt':
        if 'cv' in file_path.name.lower():
            validator._validate_cv_text_file(file_path)
        elif 'job' in file_path.name.lower():
            validator._validate_job_text_file(file_path)
        else:
            validator._add_info(f"{file_path.name}: Text file validated")
    elif file_path.suffix == '.pdf':
        validator._validate_pdf_file(file_path)
    else:
        validator._add_warning(f"Unknown file type: {file_path.suffix}")
    
    validator._print_results()
    return len(validator.errors) == 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate data files for the Advanced Job Engine"
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='job_search_data',
        help='Path to data directory or specific file (default: job_search_data/)'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )
    
    parser.add_argument(
        '--file',
        action='store_true',
        help='Validate a single file instead of a directory'
    )
    
    args = parser.parse_args()
    
    try:
        validator = DataValidator(strict_mode=args.strict)
        
        path = Path(args.path)
        
        if args.file:
            success = validate_single_file(path, validator)
        else:
            success = validator.validate_all(path)
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"\n❌ Validation error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
