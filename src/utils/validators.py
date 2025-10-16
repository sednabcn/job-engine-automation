"""
Validators Module
Input validation functions for the job engine.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class Validator:
    """Base validator class with common validation methods."""
    
    @staticmethod
    def validate_not_empty(value: str, field_name: str = "Field") -> None:
        """
        Validate that a string is not empty.
        
        Args:
            value: String to validate
            field_name: Name of the field for error messages
            
        Raises:
            ValidationError: If value is empty
        """
        if not value or not value.strip():
            raise ValidationError(f"{field_name} cannot be empty")
    
    @staticmethod
    def validate_type(value: Any, expected_type: type, field_name: str = "Field") -> None:
        """
        Validate value type.
        
        Args:
            value: Value to validate
            expected_type: Expected type
            field_name: Name of the field for error messages
            
        Raises:
            ValidationError: If type doesn't match
        """
        if not isinstance(value, expected_type):
            raise ValidationError(
                f"{field_name} must be of type {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
    
    @staticmethod
    def validate_range(value: float, min_val: float, max_val: float, 
                      field_name: str = "Field") -> None:
        """
        Validate that a number is within a range.
        
        Args:
            value: Number to validate
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)
            field_name: Name of the field for error messages
            
        Raises:
            ValidationError: If value is out of range
        """
        if not (min_val <= value <= max_val):
            raise ValidationError(
                f"{field_name} must be between {min_val} and {max_val}, got {value}"
            )
    
    @staticmethod
    def validate_choices(value: Any, choices: List[Any], field_name: str = "Field") -> None:
        """
        Validate that a value is in a list of choices.
        
        Args:
            value: Value to validate
            choices: List of valid choices
            field_name: Name of the field for error messages
            
        Raises:
            ValidationError: If value is not in choices
        """
        if value not in choices:
            raise ValidationError(
                f"{field_name} must be one of {choices}, got {value}"
            )


class FileValidator(Validator):
    """Validator for file-related inputs."""
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt', '.json'}
    MAX_FILE_SIZE_MB = 10
    
    @staticmethod
    def validate_file_exists(file_path: str) -> None:
        """
        Validate that a file exists.
        
        Args:
            file_path: Path to file
            
        Raises:
            ValidationError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise ValidationError(f"File not found: {file_path}")
        if not path.is_file():
            raise ValidationError(f"Path is not a file: {file_path}")
    
    @staticmethod
    def validate_file_extension(file_path: str, 
                               allowed_extensions: Optional[List[str]] = None) -> None:
        """
        Validate file extension.
        
        Args:
            file_path: Path to file
            allowed_extensions: List of allowed extensions (default: SUPPORTED_EXTENSIONS)
            
        Raises:
            ValidationError: If extension is not allowed
        """
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if allowed_extensions is None:
            allowed_extensions = FileValidator.SUPPORTED_EXTENSIONS
        else:
            allowed_extensions = {ext.lower() for ext in allowed_extensions}
        
        if extension not in allowed_extensions:
            raise ValidationError(
                f"Unsupported file extension: {extension}. "
                f"Allowed: {', '.join(allowed_extensions)}"
            )
    
    @staticmethod
    def validate_file_size(file_path: str, max_size_mb: Optional[float] = None) -> None:
        """
        Validate file size.
        
        Args:
            file_path: Path to file
            max_size_mb: Maximum size in MB (default: MAX_FILE_SIZE_MB)
            
        Raises:
            ValidationError: If file is too large
        """
        if max_size_mb is None:
            max_size_mb = FileValidator.MAX_FILE_SIZE_MB
        
        path = Path(file_path)
        size_mb = path.stat().st_size / (1024 * 1024)
        
        if size_mb > max_size_mb:
            raise ValidationError(
                f"File too large: {size_mb:.2f}MB (max: {max_size_mb}MB)"
            )
    
    @staticmethod
    def validate_file(file_path: str, 
                     allowed_extensions: Optional[List[str]] = None,
                     max_size_mb: Optional[float] = None) -> None:
        """
        Perform all file validations.
        
        Args:
            file_path: Path to file
            allowed_extensions: List of allowed extensions
            max_size_mb: Maximum size in MB
            
        Raises:
            ValidationError: If any validation fails
        """
        FileValidator.validate_file_exists(file_path)
        FileValidator.validate_file_extension(file_path, allowed_extensions)
        FileValidator.validate_file_size(file_path, max_size_mb)


class SkillValidator(Validator):
    """Validator for skill-related inputs."""
    
    VALID_SKILL_LEVELS = ['beginner', 'intermediate', 'advanced', 'expert']
    
    @staticmethod
    def validate_skill_name(skill_name: str) -> None:
        """
        Validate skill name.
        
        Args:
            skill_name: Name of the skill
            
        Raises:
            ValidationError: If skill name is invalid
        """
        Validator.validate_not_empty(skill_name, "Skill name")
        
        if len(skill_name) < 2:
            raise ValidationError("Skill name must be at least 2 characters")
        
        if len(skill_name) > 100:
            raise ValidationError("Skill name must not exceed 100 characters")
    
    @staticmethod
    def validate_skill_level(level: str) -> None:
        """
        Validate skill level.
        
        Args:
            level: Skill level
            
        Raises:
            ValidationError: If skill level is invalid
        """
        Validator.validate_choices(
            level.lower(), 
            SkillValidator.VALID_SKILL_LEVELS, 
            "Skill level"
        )
    
    @staticmethod
    def validate_years_experience(years: float) -> None:
        """
        Validate years of experience.
        
        Args:
            years: Years of experience
            
        Raises:
            ValidationError: If years is invalid
        """
        Validator.validate_type(years, (int, float), "Years of experience")
        Validator.validate_range(years, 0, 50, "Years of experience")
    
    @staticmethod
    def validate_skill_score(score: float) -> None:
        """
        Validate skill match score.
        
        Args:
            score: Match score
            
        Raises:
            ValidationError: If score is invalid
        """
        Validator.validate_type(score, (int, float), "Skill score")
        Validator.validate_range(score, 0, 100, "Skill score")


class JobValidator(Validator):
    """Validator for job-related inputs."""
    
    @staticmethod
    def validate_job_title(title: str) -> None:
        """
        Validate job title.
        
        Args:
            title: Job title
            
        Raises:
            ValidationError: If job title is invalid
        """
        Validator.validate_not_empty(title, "Job title")
        
        if len(title) < 3:
            raise ValidationError("Job title must be at least 3 characters")
        
        if len(title) > 200:
            raise ValidationError("Job title must not exceed 200 characters")
    
    @staticmethod
    def validate_company_name(company: str) -> None:
        """
        Validate company name.
        
        Args:
            company: Company name
            
        Raises:
            ValidationError: If company name is invalid
        """
        Validator.validate_not_empty(company, "Company name")
        
        if len(company) < 2:
            raise ValidationError("Company name must be at least 2 characters")
    
    @staticmethod
    def validate_job_description(description: str) -> None:
        """
        Validate job description.
        
        Args:
            description: Job description text
            
        Raises:
            ValidationError: If job description is invalid
        """
        Validator.validate_not_empty(description, "Job description")
        
        word_count = len(description.split())
        if word_count < 50:
            raise ValidationError(
                f"Job description too short: {word_count} words (minimum: 50)"
            )


class ConfigValidator(Validator):
    """Validator for configuration inputs."""
    
    @staticmethod
    def validate_email(email: str) -> None:
        """
        Validate email address.
        
        Args:
            email: Email address
            
        Raises:
            ValidationError: If email is invalid
        """
        Validator.validate_not_empty(email, "Email")
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        if not re.match(pattern, email):
            raise ValidationError(f"Invalid email address: {email}")
    
    @staticmethod
    def validate_url(url: str, field_name: str = "URL") -> None:
        """
        Validate URL.
        
        Args:
            url: URL to validate
            field_name: Name of the field for error messages
            
        Raises:
            ValidationError: If URL is invalid
        """
        Validator.validate_not_empty(url, field_name)
        
        pattern = r'^https?://[^\s/$.?#].[^\s]*'
        if not re.match(pattern, url, re.IGNORECASE):
            raise ValidationError(f"Invalid {field_name}: {url}")
    
    @staticmethod
    def validate_phone(phone: str) -> None:
        """
        Validate phone number.
        
        Args:
            phone: Phone number
            
        Raises:
            ValidationError: If phone is invalid
        """
        Validator.validate_not_empty(phone, "Phone number")
        
        # Remove common separators
        cleaned = re.sub(r'[-.\s()]', '', phone)
        
        if not cleaned.isdigit():
            raise ValidationError("Phone number must contain only digits and separators")
        
        if len(cleaned) < 10 or len(cleaned) > 15:
            raise ValidationError(
                f"Phone number must be 10-15 digits, got {len(cleaned)}"
            )
    
    @staticmethod
    def validate_date(date_str: str, format: str = "%Y-%m-%d") -> None:
        """
        Validate date string.
        
        Args:
            date_str: Date string
            format: Expected date format
            
        Raises:
            ValidationError: If date is invalid
        """
        try:
            datetime.strptime(date_str, format)
        except ValueError:
            raise ValidationError(
                f"Invalid date format: {date_str} (expected: {format})"
            )


class SprintValidator(Validator):
    """Validator for sprint-related inputs."""
    
    @staticmethod
    def validate_sprint_duration(duration: int) -> None:
        """
        Validate sprint duration in days.
        
        Args:
            duration: Duration in days
            
        Raises:
            ValidationError: If duration is invalid
        """
        Validator.validate_type(duration, int, "Sprint duration")
        Validator.validate_range(duration, 1, 90, "Sprint duration")
    
    @staticmethod
    def validate_sprint_goals(goals: List[str]) -> None:
        """
        Validate sprint goals.
        
        Args:
            goals: List of goals
            
        Raises:
            ValidationError: If goals are invalid
        """
        Validator.validate_type(goals, list, "Sprint goals")
        
        if not goals:
            raise ValidationError("Sprint must have at least one goal")
        
        if len(goals) > 10:
            raise ValidationError("Sprint cannot have more than 10 goals")
        
        for i, goal in enumerate(goals):
            if not isinstance(goal, str):
                raise ValidationError(f"Goal {i+1} must be a string")
            if not goal.strip():
                raise ValidationError(f"Goal {i+1} cannot be empty")


class LearningPlanValidator(Validator):
    """Validator for learning plan inputs."""
    
    @staticmethod
    def validate_learning_item(item: Dict[str, Any]) -> None:
        """
        Validate a learning plan item.
        
        Args:
            item: Learning item dictionary
            
        Raises:
            ValidationError: If item is invalid
        """
        required_fields = ['title', 'type', 'estimated_hours']
        
        for field in required_fields:
            if field not in item:
                raise ValidationError(f"Learning item missing required field: {field}")
        
        # Validate title
        Validator.validate_not_empty(item['title'], "Learning item title")
        
        # Validate type
        valid_types = ['course', 'book', 'tutorial', 'project', 'practice', 'certification']
        Validator.validate_choices(item['type'], valid_types, "Learning item type")
        
        # Validate estimated hours
        Validator.validate_type(item['estimated_hours'], (int, float), "Estimated hours")
        Validator.validate_range(item['estimated_hours'], 0.5, 1000, "Estimated hours")
    
    @staticmethod
    def validate_learning_plan(plan: Dict[str, Any]) -> None:
        """
        Validate a complete learning plan.
        
        Args:
            plan: Learning plan dictionary
            
        Raises:
            ValidationError: If plan is invalid
        """
        required_fields = ['title', 'items']
        
        for field in required_fields:
            if field not in plan:
                raise ValidationError(f"Learning plan missing required field: {field}")
        
        # Validate title
        Validator.validate_not_empty(plan['title'], "Learning plan title")
        
        # Validate items
        Validator.validate_type(plan['items'], list, "Learning plan items")
        
        if not plan['items']:
            raise ValidationError("Learning plan must have at least one item")
        
        for item in plan['items']:
            LearningPlanValidator.validate_learning_item(item)


def validate_cv_data(cv_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate CV data structure.
    
    Args:
        cv_data: CV data dictionary
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required fields
    required_fields = ['content', 'file_info']
    for field in required_fields:
        if field not in cv_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate content
    if 'content' in cv_data:
        try:
            Validator.validate_not_empty(cv_data['content'], "CV content")
            word_count = len(cv_data['content'].split())
            if word_count < 100:
                errors.append(f"CV too short: {word_count} words (minimum: 100)")
        except ValidationError as e:
            errors.append(str(e))
    
    return len(errors) == 0, errors


def validate_job_data(job_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate job data structure.
    
    Args:
        job_data: Job data dictionary
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required fields
    required_fields = ['content']
    for field in required_fields:
        if field not in job_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate content
    if 'content' in job_data:
        try:
            JobValidator.validate_job_description(job_data['content'])
        except ValidationError as e:
            errors.append(str(e))
    
    return len(errors) == 0, errors


def validate_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate configuration data.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Validate email if present
    if 'email' in config and config['email']:
        try:
            ConfigValidator.validate_email(config['email'])
        except ValidationError as e:
            errors.append(str(e))
    
    # Validate URLs if present
    url_fields = ['linkedin_url', 'github_url', 'portfolio_url']
    for field in url_fields:
        if field in config and config[field]:
            try:
                ConfigValidator.validate_url(config[field], field)
            except ValidationError as e:
                errors.append(str(e))
    
    return len(errors) == 0, errors


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example: Validate file
    try:
        FileValidator.validate_file("data/my_cv.pdf", ['.pdf'])
        print("✓ File validation passed")
    except ValidationError as e:
        print(f"✗ File validation failed: {e}")
    
    # Example: Validate email
    try:
        ConfigValidator.validate_email("user@example.com")
        print("✓ Email validation passed")
    except ValidationError as e:
        print(f"✗ Email validation failed: {e}")
    
    # Example: Validate skill
    try:
        SkillValidator.validate_skill_name("Python Programming")
        SkillValidator.validate_skill_level("advanced")
        SkillValidator.validate_years_experience(5)
        print("✓ Skill validation passed")
    except ValidationError as e:
        print(f"✗ Skill validation failed: {e}")
