"""
Helpers Module
Enhanced utility functions and helpers for the job engine.
"""

from typing import Any, Dict, List, Optional, Union, Callable, Tuple
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
import re
import hashlib
import json
import logging
import unicodedata
import time

logger = logging.getLogger(__name__)


# ============================================================================
# TEXT PROCESSING
# ============================================================================

def clean_text(text: str, preserve_newlines: bool = False) -> str:
    """
    Clean and normalize text with enhanced Unicode handling.
    
    Args:
        text: Input text
        preserve_newlines: Keep newline characters
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Normalize Unicode characters (NFD -> NFC)
    text = unicodedata.normalize('NFKC', text)
    
    # Remove null bytes and other control characters
    text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C' or char in '\n\r\t')
    
    if preserve_newlines:
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # Remove extra whitespace but keep newlines
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
    else:
        # Remove all extra whitespace including newlines
        text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,;:!?()\-\'\"@#$%&\n]+', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Input text
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    text = re.sub(r'[<>&\'\";]', '', text)
    
    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()


def extract_keywords(text: str, min_length: int = 3, top_n: Optional[int] = None) -> List[str]:
    """
    Extract keywords from text.
    
    Args:
        text: Input text
        min_length: Minimum keyword length
        top_n: Return top N keywords by frequency
        
    Returns:
        List of keywords
    """
    if not text:
        return []
    
    # Convert to lowercase and split
    words = re.findall(r'\b[a-z]{' + str(min_length) + r',}\b', text.lower())
    
    # Common stop words to filter out
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her',
        'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how',
        'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did',
        'its', 'let', 'put', 'say', 'she', 'too', 'use', 'with', 'will', 'this',
        'that', 'from', 'have', 'they', 'been', 'were', 'what', 'when', 'your'
    }
    
    # Filter stop words and count frequency
    word_freq = {}
    for word in words:
        if word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Return top N or all
    keywords = [word for word, _ in sorted_words]
    return keywords[:top_n] if top_n else keywords


# ============================================================================
# SKILL PROCESSING
# ============================================================================

def normalize_skill_name(skill: str) -> str:
    """
    Enhanced skill name normalization with more variations.
    
    Args:
        skill: Skill name
        
    Returns:
        Normalized skill name
    """
    if not skill:
        return ""
    
    # Convert to lowercase and clean
    skill = skill.lower().strip()
    skill = re.sub(r'[^\w\s.#+\-]', '', skill)
    
    # Comprehensive replacements
    replacements = {
        'javascript': 'js',
        'typescript': 'ts',
        'python3': 'python',
        'python2': 'python',
        'nodejs': 'node.js',
        'node js': 'node.js',
        'react.js': 'react',
        'reactjs': 'react',
        'vue.js': 'vue',
        'vuejs': 'vue',
        'angular.js': 'angular',
        'angularjs': 'angular',
        'c++': 'cpp',
        'c sharp': 'csharp',
        'c#': 'csharp',
        'objective-c': 'objective c',
        'postgresql': 'postgres',
        'mysql': 'sql',
        'mssql': 'sql server',
        'mongodb': 'mongo',
        'amazon web services': 'aws',
        'google cloud platform': 'gcp',
        'microsoft azure': 'azure',
        'kubernetes': 'k8s',
        'continuous integration': 'ci',
        'continuous deployment': 'cd',
        'test driven development': 'tdd',
        'behavior driven development': 'bdd',
    }
    
    return replacements.get(skill, skill)


def extract_years_experience(text: str) -> float:
    """
    Enhanced experience extraction with more patterns.
    
    Args:
        text: Text containing experience duration
        
    Returns:
        Years as float (0 if not found)
    """
    if not text:
        return 0.0
    
    text = text.lower()
    
    # Enhanced patterns
    patterns = [
        (r'(\d+\.?\d*)\+?\s*(?:years?|yrs?)', 1),  # "5 years", "3+ yrs"
        (r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)', 2),  # "3-5 years"
        (r'(\d+)\s*to\s*(\d+)\s*(?:years?|yrs?)', 2),  # "3 to 5 years"
        (r'over\s*(\d+\.?\d*)\s*(?:years?|yrs?)', 1),  # "over 5 years"
        (r'more than\s*(\d+\.?\d*)\s*(?:years?|yrs?)', 1),  # "more than 5 years"
        (r'minimum\s*(?:of\s*)?(\d+\.?\d*)\s*(?:years?|yrs?)', 1),  # "minimum 5 years"
        (r'at least\s*(\d+\.?\d*)\s*(?:years?|yrs?)', 1),  # "at least 5 years"
    ]
    
    for pattern, group_count in patterns:
        match = re.search(pattern, text)
        if match:
            if group_count == 2:
                # Range: take average
                return (float(match.group(1)) + float(match.group(2))) / 2
            else:
                return float(match.group(1))
    
    # Pattern: X months
    month_match = re.search(r'(\d+)\s*(?:months?|mos?)', text)
    if month_match:
        return round(float(month_match.group(1)) / 12, 1)
    
    return 0.0


def calculate_skill_score(
    years_experience: float,
    proficiency: str = "intermediate",
    recency_months: Optional[int] = None
) -> float:
    """
    Enhanced skill score calculation with recency factor.
    
    Args:
        years_experience: Years of experience
        proficiency: Proficiency level
        recency_months: Months since last used (optional)
        
    Returns:
        Score from 0-100
    """
    # Base score from years (logarithmic scale for diminishing returns)
    import math
    if years_experience >= 10:
        base_score = 95
    elif years_experience >= 5:
        base_score = 85
    elif years_experience >= 3:
        base_score = 70
    elif years_experience >= 1:
        base_score = 55
    elif years_experience >= 0.5:
        base_score = 40
    else:
        base_score = 25
    
    # Adjust for proficiency
    proficiency_multipliers = {
        'expert': 1.15,
        'advanced': 1.05,
        'intermediate': 0.90,
        'beginner': 0.75,
        'basic': 0.60,
        'learning': 0.50
    }
    
    multiplier = proficiency_multipliers.get(proficiency.lower(), 0.90)
    score = base_score * multiplier
    
    # Apply recency penalty if provided
    if recency_months is not None:
        if recency_months > 36:  # Over 3 years
            score *= 0.7
        elif recency_months > 24:  # Over 2 years
            score *= 0.8
        elif recency_months > 12:  # Over 1 year
            score *= 0.9
    
    return min(100.0, max(0.0, score))


def fuzzy_match_skills(skill1: str, skill2: str, threshold: float = 0.8) -> bool:
    """
    Enhanced skill matching with better fuzzy logic.
    
    Args:
        skill1: First skill name
        skill2: Second skill name
        threshold: Similarity threshold (0-1)
        
    Returns:
        True if skills match
    """
    s1 = normalize_skill_name(skill1)
    s2 = normalize_skill_name(skill2)
    
    # Exact match
    if s1 == s2:
        return True
    
    # One contains the other (must be significant portion)
    if len(s1) > 2 and len(s2) > 2:
        if s1 in s2 or s2 in s1:
            return True
    
    # Enhanced variations dictionary
    variations = {
        'js': ['javascript', 'ecmascript', 'es6', 'es5'],
        'ts': ['typescript'],
        'py': ['python', 'python3', 'python2'],
        'cpp': ['c++', 'cplusplus'],
        'csharp': ['c#', 'c sharp'],
        'sql': ['mysql', 'postgresql', 'postgres', 'mssql', 'sqlite'],
        'aws': ['amazon web services', 'amazon aws'],
        'gcp': ['google cloud', 'google cloud platform'],
        'azure': ['microsoft azure', 'ms azure'],
        'k8s': ['kubernetes', 'kube'],
        'docker': ['containerization', 'containers'],
        'react': ['reactjs', 'react.js', 'react native'],
        'vue': ['vuejs', 'vue.js'],
        'angular': ['angularjs', 'angular.js'],
        'node': ['nodejs', 'node.js'],
        'ml': ['machine learning', 'machinelearning'],
        'ai': ['artificial intelligence', 'artificialintelligence'],
        'ci': ['continuous integration', 'cicd', 'ci/cd'],
        'cd': ['continuous deployment', 'continuous delivery'],
    }
    
    # Check variations
    for key, values in variations.items():
        if (s1 == key and s2 in values) or (s2 == key and s1 in values):
            return True
        if s1 in values and s2 in values:
            return True
    
    # Levenshtein distance calculation for fuzzy matching
    if len(s1) > 3 and len(s2) > 3:
        distance = levenshtein_distance(s1, s2)
        max_len = max(len(s1), len(s2))
        similarity = 1 - (distance / max_len)
        if similarity >= threshold:
            return True
    
    return False


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate Levenshtein distance between two strings.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Edit distance
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


# ============================================================================
# DATE & TIME UTILITIES
# ============================================================================

def parse_date(date_str: str, fuzzy: bool = True) -> Optional[datetime]:
    """
    Enhanced date parsing with fuzzy matching.
    
    Args:
        date_str: Date string
        fuzzy: Allow fuzzy parsing
        
    Returns:
        Datetime object or None
    """
    if not date_str:
        return None
    
    date_str = date_str.strip()
    
    # Handle relative dates
    relative_patterns = {
        r'\btoday\b': datetime.now(),
        r'\byesterday\b': datetime.now() - timedelta(days=1),
        r'\btomorrow\b': datetime.now() + timedelta(days=1),
    }
    
    for pattern, dt in relative_patterns.items():
        if re.search(pattern, date_str.lower()):
            return dt
    
    # Standard formats
    formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%d-%m-%Y',
        '%d/%m/%Y',
        '%m-%d-%Y',
        '%m/%d/%Y',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%SZ',
        '%d %B %Y',
        '%B %d, %Y',
        '%d %b %Y',
        '%b %d, %Y',
        '%B %Y',
        '%b %Y',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # Try fuzzy parsing for natural language dates
    if fuzzy:
        try:
            # Extract year, month, day with regex
            year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
            month_names = {
                'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
            }
            
            if year_match:
                year = int(year_match.group(0))
                month = 1
                day = 1
                
                # Try to find month
                for month_name, month_num in month_names.items():
                    if month_name in date_str.lower():
                        month = month_num
                        break
                
                # Try to find day
                day_match = re.search(r'\b(\d{1,2})\b', date_str)
                if day_match:
                    day = int(day_match.group(1))
                    if day > 31:
                        day = 1
                
                return datetime(year, month, day)
        except (ValueError, AttributeError):
            pass
    
    return None


def format_date(dt: datetime, format_str: str = '%Y-%m-%d', locale: str = 'en') -> str:
    """
    Enhanced date formatting with locale support.
    
    Args:
        dt: Datetime object
        format_str: Format string
        locale: Locale code (currently only 'en' supported)
        
    Returns:
        Formatted date string
    """
    if not dt:
        return ""
    
    return dt.strftime(format_str)


def calculate_duration(
    start_date: datetime,
    end_date: Optional[datetime] = None,
    unit: str = 'years'
) -> float:
    """
    Enhanced duration calculation with multiple units.
    
    Args:
        start_date: Start date
        end_date: End date (defaults to now)
        unit: Time unit ('years', 'months', 'days', 'hours')
        
    Returns:
        Duration in specified unit
    """
    if not start_date:
        return 0.0
    
    if not end_date:
        end_date = datetime.now()
    
    delta = end_date - start_date
    
    if unit == 'years':
        return delta.days / 365.25
    elif unit == 'months':
        return delta.days / 30.44
    elif unit == 'days':
        return delta.days
    elif unit == 'hours':
        return delta.total_seconds() / 3600
    elif unit == 'minutes':
        return delta.total_seconds() / 60
    elif unit == 'seconds':
        return delta.total_seconds()
    else:
        raise ValueError(f"Invalid unit: {unit}")


def time_ago(dt: datetime, detailed: bool = False) -> str:
    """
    Enhanced human-readable time ago string.
    
    Args:
        dt: Datetime object
        detailed: Include more detailed breakdown
        
    Returns:
        Time ago string
    """
    if not dt:
        return "unknown"
    
    now = datetime.now()
    diff = now - dt
    seconds = diff.total_seconds()
    
    if seconds < 0:
        return "in the future"
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        if detailed:
            remaining_mins = int((seconds % 3600) / 60)
            return f"{hours} hour{'s' if hours != 1 else ''}, {remaining_mins} minute{'s' if remaining_mins != 1 else ''} ago"
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        if detailed:
            remaining_hours = int((seconds % 86400) / 3600)
            return f"{days} day{'s' if days != 1 else ''}, {remaining_hours} hour{'s' if remaining_hours != 1 else ''} ago"
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        if detailed:
            remaining_months = int((seconds % 31536000) / 2592000)
            return f"{years} year{'s' if years != 1 else ''}, {remaining_months} month{'s' if remaining_months != 1 else ''} ago"
        return f"{years} year{'s' if years != 1 else ''} ago"


# ============================================================================
# DATA UTILITIES
# ============================================================================

def generate_id(data: Any, length: int = 12) -> str:
    """
    Enhanced ID generation with custom length.
    
    Args:
        data: Data to hash
        length: ID length (max 32)
        
    Returns:
        Unique ID string
    """
    if isinstance(data, (dict, list)):
        data_str = json.dumps(data, sort_keys=True)
    else:
        data_str = str(data)
    
    hash_obj = hashlib.sha256(data_str.encode())
    return hash_obj.hexdigest()[:min(length, 32)]


def merge_dicts(dict1: Dict, dict2: Dict, deep: bool = True, strategy: str = 'overwrite') -> Dict:
    """
    Enhanced dictionary merging with merge strategies.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        deep: Deep merge nested dicts
        strategy: Merge strategy ('overwrite', 'keep', 'combine')
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result:
            if strategy == 'keep':
                continue  # Keep existing value
            elif strategy == 'combine' and isinstance(result[key], list) and isinstance(value, list):
                result[key] = result[key] + value
            elif deep and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_dicts(result[key], value, deep=True, strategy=strategy)
            else:
                result[key] = value  # Overwrite
        else:
            result[key] = value
    
    return result


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.', max_depth: Optional[int] = None) -> Dict:
    """
    Enhanced dictionary flattening with depth control.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator
        max_depth: Maximum depth to flatten
        
    Returns:
        Flattened dictionary
    """
    items = []
    current_depth = len(parent_key.split(sep)) if parent_key else 0
    
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if max_depth and current_depth >= max_depth:
            items.append((new_key, v))
        elif isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep, max_depth=max_depth).items())
        else:
            items.append((new_key, v))
    
    return dict(items)


def get_nested_value(data: Dict, key_path: str, default: Any = None, sep: str = '.') -> Any:
    """
    Enhanced nested value retrieval with better error handling.
    
    Args:
        data: Dictionary
        key_path: Dot-separated key path
        default: Default value if not found
        sep: Separator character
        
    Returns:
        Value or default
    """
    try:
        keys = key_path.split(sep)
        value = data
        
        for key in keys:
            if isinstance(value, dict):
                value = value[key]
            elif isinstance(value, (list, tuple)) and key.isdigit():
                value = value[int(key)]
            else:
                return default
        
        return value
    except (KeyError, IndexError, TypeError, ValueError):
        return default


def set_nested_value(data: Dict, key_path: str, value: Any, sep: str = '.', create_missing: bool = True) -> bool:
    """
    Enhanced nested value setting with validation.
    
    Args:
        data: Dictionary to modify
        key_path: Dot-separated key path
        value: Value to set
        sep: Separator character
        create_missing: Create missing intermediate keys
        
    Returns:
        True if successful, False otherwise
    """
    try:
        keys = key_path.split(sep)
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                if not create_missing:
                    return False
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        return True
    except (TypeError, AttributeError):
        return False


def chunk_list(lst: List[Any], chunk_size: int, preserve_order: bool = True) -> List[List[Any]]:
    """
    Enhanced list chunking.
    
    Args:
        lst: Input list
        chunk_size: Size of each chunk
        preserve_order: Maintain original order
        
    Returns:
        List of chunks
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")
    
    if preserve_order:
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    else:
        # Distribute items evenly across chunks
        num_chunks = (len(lst) + chunk_size - 1) // chunk_size
        return [lst[i::num_chunks] for i in range(num_chunks)]


# ============================================================================
# FILE UTILITIES
# ============================================================================

def ensure_directory(path: Union[str, Path], mode: int = 0o755) -> Path:
    """
    Enhanced directory creation with permission control.
    
    Args:
        path: Directory path
        mode: Permission mode
        
    Returns:
        Path object
    """
    path = Path(path)
    try:
        path.mkdir(parents=True, exist_ok=True, mode=mode)
        return path
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        raise


def safe_filename(filename: str, max_length: int = 200, replacement: str = '_') -> str:
    """
    Enhanced safe filename generation.
    
    Args:
        filename: Original filename
        max_length: Maximum filename length
        replacement: Replacement character for invalid chars
        
    Returns:
        Safe filename
    """
    # Remove/replace invalid characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    filename = re.sub(invalid_chars, replacement, filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Handle reserved names on Windows
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    name_without_ext = filename.rsplit('.', 1)[0].upper()
    if name_without_ext in reserved_names:
        filename = f"_{filename}"
    
    # Limit length while preserving extension
    if len(filename) > max_length:
        if '.' in filename:
            name, ext = filename.rsplit('.', 1)
            max_name_len = max_length - len(ext) - 1
            filename = f"{name[:max_name_len]}.{ext}"
        else:
            filename = filename[:max_length]
    
    return filename or 'unnamed'


# ============================================================================
# TEXT EXTRACTION
# ============================================================================

def extract_email(text: str, all_matches: bool = False) -> Union[Optional[str], List[str]]:
    """
    Enhanced email extraction.
    
    Args:
        text: Text containing email(s)
        all_matches: Return all matches instead of first
        
    Returns:
        Email address(es) or None
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    if all_matches:
        matches = re.findall(pattern, text)
        return matches if matches else []
    else:
        match = re.search(pattern, text)
        return match.group(0) if match else None


def extract_phone(text: str, all_matches: bool = False) -> Union[Optional[str], List[str]]:
    """
    Enhanced phone number extraction.
    
    Args:
        text: Text containing phone(s)
        all_matches: Return all matches instead of first
        
    Returns:
        Phone number(s) or None
    """
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+?\d{1,3}[-.\s]?\d{2,3}[-.\s]?\d{4}[-.\s]?\d{4}',
    ]
    
    matches = []
    for pattern in patterns:
        found = re.findall(pattern, text)
        matches.extend(found)
    
    if all_matches:
        return matches if matches else []
    else:
        return matches[0] if matches else None


def extract_urls(text: str, unique: bool = True) -> List[str]:
    """
    Enhanced URL extraction.
    
    Args:
        text: Text containing URLs
        unique: Return unique URLs only
        
    Returns:
        List of URLs
    """
    pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    urls = re.findall(pattern, text)
    
    if unique:
        return list(dict.fromkeys(urls))
    return urls
    return urls


# ============================================================================
# FORMATTING & DISPLAY
# ============================================================================

def truncate_text(text: str, max_length: int = 100, suffix: str = '...', word_boundary: bool = True) -> str:
    """
    Enhanced text truncation with word boundary support.
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated
        word_boundary: Truncate at word boundary
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    if word_boundary:
        # Find last space before max_length
        truncate_at = text.rfind(' ', 0, max_length - len(suffix))
        if truncate_at > 0:
            return text[:truncate_at] + suffix
    
    return text[:max_length - len(suffix)] + suffix


def pluralize(count: int, singular: str, plural: Optional[str] = None, include_count: bool = True) -> str:
    """
    Enhanced pluralization.
    
    Args:
        count: Number
        singular: Singular form
        plural: Plural form (defaults to singular + 's')
        include_count: Include count in output
        
    Returns:
        Appropriate form with optional count
    """
    if plural is None:
        # Smart pluralization
        if singular.endswith('y') and singular[-2] not in 'aeiou':
            plural = singular[:-1] + 'ies'
        elif singular.endswith(('s', 'x', 'z', 'ch', 'sh')):
            plural = singular + 'es'
        else:
            plural = singular + 's'
    
    form = singular if count == 1 else plural
    
    if include_count:
        return f"{count} {form}"
    return form


def format_number(num: Union[int, float], decimals: int = 2, thousands_sep: str = ',') -> str:
    """
    Format number with thousands separator.
    
    Args:
        num: Number to format
        decimals: Number of decimal places
        thousands_sep: Thousands separator
        
    Returns:
        Formatted number string
    """
    if isinstance(num, int):
        formatted = f"{num:,}".replace(',', thousands_sep)
    else:
        formatted = f"{num:,.{decimals}f}".replace(',', thousands_sep)
    
    return formatted


def format_bytes(bytes_size: int, precision: int = 2) -> str:
    """
    Format bytes to human-readable size.
    
    Args:
        bytes_size: Size in bytes
        precision: Decimal precision
        
    Returns:
        Formatted size string
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    
    size = float(bytes_size)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.{precision}f} {units[unit_index]}"


def format_duration(seconds: float, verbose: bool = False) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        verbose: Use verbose format
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f} seconds" if verbose else f"{seconds:.1f}s"
    
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f} minutes" if verbose else f"{minutes:.1f}m"
    
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.1f} hours" if verbose else f"{hours:.1f}h"
    
    days = hours / 24
    return f"{days:.1f} days" if verbose else f"{days:.1f}d"


def estimate_reading_time(text: str, words_per_minute: int = 200, include_suffix: bool = True) -> str:
    """
    Enhanced reading time estimation.
    
    Args:
        text: Text to read
        words_per_minute: Reading speed
        include_suffix: Include "min read" suffix
        
    Returns:
        Estimated reading time
    """
    if not text:
        return "0 min read" if include_suffix else "0"
    
    word_count = len(text.split())
    minutes = max(1, int(word_count / words_per_minute))
    
    if include_suffix:
        return f"{minutes} min read"
    return str(minutes)


def create_progress_bar(current: int, total: int, width: int = 50, fill: str = '█', empty: str = '░') -> str:
    """
    Create a text-based progress bar.
    
    Args:
        current: Current progress
        total: Total amount
        width: Bar width in characters
        fill: Fill character
        empty: Empty character
        
    Returns:
        Progress bar string
    """
    if total == 0:
        percentage = 0
    else:
        percentage = (current / total) * 100
    
    filled_width = int(width * current / total) if total > 0 else 0
    bar = fill * filled_width + empty * (width - filled_width)
    
    return f"|{bar}| {percentage:.1f}%"


# ============================================================================
# MATH & CALCULATIONS
# ============================================================================

def percentage_change(old_value: float, new_value: float, precision: int = 2) -> float:
    """
    Enhanced percentage change calculation.
    
    Args:
        old_value: Old value
        new_value: New value
        precision: Decimal precision
        
    Returns:
        Percentage change
    """
    if old_value == 0:
        return 100.0 if new_value > 0 else -100.0 if new_value < 0 else 0.0
    
    change = ((new_value - old_value) / abs(old_value)) * 100
    return round(change, precision)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp value between min and max.
    
    Args:
        value: Input value
        min_value: Minimum value
        max_value: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_value, min(max_value, value))


def normalize(value: float, min_value: float, max_value: float) -> float:
    """
    Normalize value to 0-1 range.
    
    Args:
        value: Input value
        min_value: Minimum of range
        max_value: Maximum of range
        
    Returns:
        Normalized value (0-1)
    """
    if max_value == min_value:
        return 0.5
    
    return (value - min_value) / (max_value - min_value)


def interpolate(start: float, end: float, factor: float) -> float:
    """
    Linear interpolation between two values.
    
    Args:
        start: Start value
        end: End value
        factor: Interpolation factor (0-1)
        
    Returns:
        Interpolated value
    """
    factor = clamp(factor, 0.0, 1.0)
    return start + (end - start) * factor


def weighted_average(values: List[float], weights: Optional[List[float]] = None) -> float:
    """
    Calculate weighted average.
    
    Args:
        values: List of values
        weights: List of weights (defaults to equal weights)
        
    Returns:
        Weighted average
    """
    if not values:
        return 0.0
    
    if weights is None:
        return sum(values) / len(values)
    
    if len(values) != len(weights):
        raise ValueError("Values and weights must have same length")
    
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0
    
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    return weighted_sum / total_weight


def calculate_similarity(list1: List[Any], list2: List[Any]) -> float:
    """
    Calculate Jaccard similarity between two lists.
    
    Args:
        list1: First list
        list2: Second list
        
    Returns:
        Similarity score (0-1)
    """
    set1 = set(list1)
    set2 = set(list2)
    
    if not set1 and not set2:
        return 1.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0


# ============================================================================
# VALIDATION
# ============================================================================

def is_valid_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address
        
    Returns:
        True if valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL string
        
    Returns:
        True if valid
    """
    pattern = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    return bool(re.match(pattern, url))


def is_valid_phone(phone: str, country: str = 'US') -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number
        country: Country code (currently only 'US' supported)
        
    Returns:
        True if valid
    """
    # Remove common separators
    digits = re.sub(r'[-.\s()]+', '', phone)
    
    if country == 'US':
        # US: 10 digits or 11 with country code
        return bool(re.match(r'^\+?1?\d{10}, digits))
    
    # Generic: 7-15 digits
    return bool(re.match(r'^\+?\d{7,15}, digits))


def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
    """
    Validate that start date is before end date.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        True if valid
    """
    return start_date <= end_date


# ============================================================================
# DECORATORS & ERROR HANDLING
# ============================================================================

def retry_on_error(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0, exceptions: Tuple = (Exception,)):
    """
    Decorator to retry function on error with exponential backoff.
    
    Args:
        max_attempts: Maximum retry attempts
        delay: Initial delay between attempts
        backoff: Backoff multiplier
        exceptions: Tuple of exceptions to catch
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}: {e}")
                        raise
                    
                    logger.warning(f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            raise last_exception
        
        return wrapper
    return decorator


def timing_decorator(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to time
        
    Returns:
        Decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        duration = end_time - start_time
        logger.info(f"{func.__name__} took {duration:.3f} seconds")
        
        return result
    
    return wrapper


def memoize(max_size: int = 128):
    """
    Simple memoization decorator with size limit.
    
    Args:
        max_size: Maximum cache size
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        cache_order = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from args and kwargs
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)
            
            # Add to cache
            cache[key] = result
            cache_order.append(key)
            
            # Remove oldest if exceeds max_size
            if len(cache) > max_size:
                oldest_key = cache_order.pop(0)
                del cache[oldest_key]
            
            return result
        
        wrapper.cache_clear = lambda: (cache.clear(), cache_order.clear())
        wrapper.cache_info = lambda: {'size': len(cache), 'max_size': max_size}
        
        return wrapper
    return decorator


def safe_execute(func: Callable, default: Any = None, log_error: bool = True) -> Callable:
    """
    Execute function safely, returning default on error.
    
    Args:
        func: Function to execute
        default: Default return value on error
        log_error: Whether to log errors
        
    Returns:
        Function result or default
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if log_error:
                logger.error(f"Error in {func.__name__}: {e}")
            return default
    
    return wrapper


# ============================================================================
# MISCELLANEOUS
# ============================================================================

def deep_copy(obj: Any) -> Any:
    """
    Create a deep copy of an object.
    
    Args:
        obj: Object to copy
        
    Returns:
        Deep copy of object
    """
    import copy
    return copy.deepcopy(obj)


def get_object_size(obj: Any) -> int:
    """
    Get approximate size of object in bytes.
    
    Args:
        obj: Object to measure
        
    Returns:
        Size in bytes
    """
    import sys
    return sys.getsizeof(obj)


def batch_process(items: List[Any], func: Callable, batch_size: int = 100, show_progress: bool = False) -> List[Any]:
    """
    Process items in batches.
    
    Args:
        items: Items to process
        func: Processing function
        batch_size: Batch size
        show_progress: Show progress indicator
        
    Returns:
        List of results
    """
    results = []
    total_batches = (len(items) + batch_size - 1) // batch_size
    
    for i, batch in enumerate(chunk_list(items, batch_size)):
        batch_results = [func(item) for item in batch]
        results.extend(batch_results)
        
        if show_progress:
            progress = (i + 1) / total_batches * 100
            print(f"Progress: {progress:.1f}% ({i + 1}/{total_batches} batches)", end='\r')
    
    if show_progress:
        print()  # New line after progress
    
    return results


def generate_unique_filename(base_path: Union[str, Path], extension: str = '') -> Path:
    """
    Generate unique filename by appending number if file exists.
    
    Args:
        base_path: Base file path
        extension: File extension (with or without dot)
        
    Returns:
        Unique Path object
    """
    base_path = Path(base_path)
    
    if extension and not extension.startswith('.'):
        extension = f".{extension}"
    
    if not base_path.suffix and extension:
        base_path = base_path.with_suffix(extension)
    
    if not base_path.exists():
        return base_path
    
    # Add counter to filename
    counter = 1
    stem = base_path.stem
    suffix = base_path.suffix
    parent = base_path.parent
    
    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two version strings.
    
    Args:
        version1: First version (e.g., "1.2.3")
        version2: Second version (e.g., "1.2.4")
        
    Returns:
        -1 if version1 < version2, 0 if equal, 1 if version1 > version2
    """
    def parse_version(v: str) -> List[int]:
        return [int(x) for x in v.split('.')]
    
    try:
        v1_parts = parse_version(version1)
        v2_parts = parse_version(version2)
        
        # Pad shorter version with zeros
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))
        
        for p1, p2 in zip(v1_parts, v2_parts):
            if p1 < p2:
                return -1
            elif p1 > p2:
                return 1
        
        return 0
    except (ValueError, AttributeError):
        return 0


if __name__ == "__main__":
    # Example usage and tests
    print("=== Helpers Module Examples ===\n")
    
    # Text processing
    print("1. Text Processing:")
    print(f"   Clean text: {clean_text('Hello    World!  @#)}")
    print(f"   Extract keywords: {extract_keywords('python programming language for data science', top_n=3)}")
    
    # Skill matching
    print("\n2. Skill Matching:")
    print(f"   Normalize: {normalize_skill_name('JavaScript')}")
    print(f"   Match JS/JavaScript: {fuzzy_match_skills('js', 'javascript')}")
    print(f"   Extract experience: {extract_years_experience('5 years of experience')}")
    
    # Date utilities
    print("\n3. Date Utilities:")
    dt = parse_date("2024-01-15")
    if dt:
        print(f"   Parsed date: {format_date(dt)}")
        print(f"   Time ago: {time_ago(dt)}")
    
    # Formatting
    print("\n4. Formatting:")
    print(f"   Pluralize: {pluralize(5, 'item')}")
    print(f"   Format bytes: {format_bytes(1536000)}")
    print(f"   Progress bar: {create_progress_bar(75, 100)}")
    
    # Math
    print("\n5. Math Operations:")
    print(f"   Percentage change: {percentage_change(100, 150)}%")
    print(f"   Weighted average: {weighted_average([80, 90, 70], [0.3, 0.5, 0.2])}")
    
    print("\n=== End Examples ===")
