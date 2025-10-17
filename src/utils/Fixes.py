# ============================================================================
# FIXES FOR helpers.py
# ============================================================================
import json
import logging
import os
import re
import time
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple

_logger = logging.getLogger(__name__)


# Fix 1: extract_keywords function (line 162)
# Add type annotation for word_freq dictionary


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
    words = re.findall(r"\b[a-z]{" + str(min_length) + r",}\b", text.lower())

    # Common stop words to filter out
    stop_words = {
        "the",
        "and",
        "for",
        "are",
        "but",
        "not",
        "you",
        "all",
        "can",
        "her",
        "was",
        "one",
        "our",
        "out",
        "day",
        "get",
        "has",
        "him",
        "his",
        "how",
        "man",
        "new",
        "now",
        "old",
        "see",
        "two",
        "way",
        "who",
        "boy",
        "did",
        "its",
        "let",
        "put",
        "say",
        "she",
        "too",
        "use",
        "with",
        "will",
        "this",
        "that",
        "from",
        "have",
        "they",
        "been",
        "were",
        "what",
        "when",
        "your",
    }

    # Filter stop words and count frequency
    word_freq: Dict[str, int] = {}  # FIX: Added type annotation
    for word in words:
        if word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1

    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # Return top N or all
    keywords = [word for word, _ in sorted_words]
    return keywords[:top_n] if top_n else keywords


# Fix 2: retry_on_error function (line 1393)
# Fix the exception handling to avoid raising None


def retry_on_error(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[type[Exception], ...] = (Exception,),
):
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
            last_exception: Optional[Exception] = None  # FIX: Added type annotation

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        _logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {e}"
                        )
                        raise  # FIX: Raise directly instead of raising last_exception

                    _logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. "
                        f"Retrying in {current_delay}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

            # FIX: This should never be reached, but add safety
            if last_exception is not None:
                raise last_exception
            raise RuntimeError(f"Function {func.__name__} failed without exception")

        return wrapper

    return decorator


# Fix 3: memoize function (lines 1437, 1461-1462)
# Fix cache annotations and cache_clear/cache_info attributes


def memoize(max_size: int = 128):
    """
    Simple memoization decorator with size limit.

    Args:
        max_size: Maximum cache size

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        cache: Dict[str, Any] = {}  # FIX: Added type annotation
        cache_order: List[str] = []

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

        # FIX: Define cache_clear and cache_info properly
        def cache_clear() -> None:
            cache.clear()
            cache_order.clear()

        def cache_info() -> Dict[str, int]:
            return {"size": len(cache), "max_size": max_size}

        # FIX: Assign to wrapper using setattr to avoid type errors
        setattr(wrapper, "cache_clear", cache_clear)
        setattr(wrapper, "cache_info", cache_info)

        return wrapper

    return decorator


# ============================================================================
# FIXES FOR formatters.py
# ============================================================================


def format_skill_summary(skills: List[Dict[str, Any]]) -> str:
    """
    Format a human-readable summary of skills grouped by proficiency level.

    Args:
        skills: List of skill dictionaries.
            Example:
            [
                {"name": "Python", "level": "advanced"},
                {"name": "C++", "level": "intermediate"},
                {"name": "Data Analysis", "level": "advanced"}
            ]

    Returns:
        A formatted multiline string summarizing skills by level.
    """

    if not skills:
        return "No skills available."

    # Group skills by level
    by_level: Dict[str, List[Dict[str, Any]]] = {}

    for skill in skills:
        level = str(skill.get("level", "intermediate")).strip().lower()
        if level not in by_level:
            by_level[level] = []
        by_level[level].append(skill)

    # Sort levels by proficiency importance (optional but clean)
    level_order = ["beginner", "intermediate", "advanced", "expert"]
    ordered_levels = sorted(
        by_level.keys(),
        key=lambda lvl: level_order.index(lvl) if lvl in level_order else len(level_order),
    )

    # Build formatted output
    lines: List[str] = []
    for level in ordered_levels:
        lines.append(f"\n🔹 {level.title()} Skills:")
        level_skills = sorted([s["name"] for s in by_level[level] if "name" in s])
        for name in level_skills:
            lines.append(f"  • {name}")

    # Join all lines
    formatted_summary = "\n".join(lines).strip()

    return formatted_summary


# Add type annotation for by_priority dictionary


def format_learning_plan(plan: Dict[str, Any]) -> str:
    """
    Format a structured learning plan grouped by priority levels.

    Args:
        plan: Learning plan dictionary, expected to include a "tasks" key
              with a list of dict items like:
              {
                  "title": "Learn Python",
                  "priority": "high",
                  "category": "Programming",
                  "deadline": "2025-12-01"
              }

    Returns:
        A formatted, human-readable string summarizing the learning plan.
    """
    # Initialize dictionary grouped by priority
    by_priority: Dict[str, List[Dict[str, Any]]] = {"high": [], "medium": [], "low": []}

    # Safely extract tasks from plan
    tasks = plan.get("tasks", [])
    if not isinstance(tasks, list):
        return "Invalid plan: expected 'tasks' to be a list."

    # Group tasks by priority
    for task in tasks:
        priority = str(task.get("priority", "medium")).lower()
        if priority not in by_priority:
            priority = "medium"  # Default fallback
        by_priority[priority].append(task)

    # Build formatted output
    lines: List[str] = ["Learning Plan Summary", "=" * 24]

    for priority in ["high", "medium", "low"]:
        section_tasks = by_priority.get(priority, [])
        if not section_tasks:
            continue

        lines.append(
            f"\nPriority: {priority.upper()} ({len(section_tasks)} task{'s' if len(section_tasks) != 1 else ''})"
        )
        lines.append("-" * (len(priority) + 15))

        for i, task in enumerate(section_tasks, start=1):
            title = task.get("title", "Untitled task")
            category = task.get("category", "General")
            deadline = task.get("deadline", "No deadline")
            notes = task.get("notes", "")

            lines.append(f"{i}. {title}")
            lines.append(f"   Category : {category}")
            lines.append(f"   Deadline : {deadline}")
            if notes:
                lines.append(f"   Notes    : {notes}")
            lines.append("")  # blank line between tasks

    # Handle empty plan
    if len(lines) <= 2:
        return "No tasks found in the learning plan."

    return "\n".join(lines)


# ============================================================================
# FIXES FOR data_loader.py
# ============================================================================


class MasterSkillsetLoader:
    """
    Loader for master skillset data from a JSON file.

    This class reads and validates a structured skillset definition,
    typically organized by domains, categories, and specific skills.

    Example expected JSON structure:
    {
        "Programming": {
            "languages": ["Python", "C++", "Java"],
            "frameworks": ["Django", "FastAPI"]
        },
        "Data Science": {
            "tools": ["Pandas", "NumPy", "scikit-learn"],
            "concepts": ["Regression", "Clustering"]
        }
    }
    """

    def load_json(self, file_path: str) -> Dict[str, Any]:
        """
        Load and parse JSON file.

        Args:
            file_path: Path to a JSON file

        Returns:
            Parsed dictionary containing the skillset

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If JSON is invalid
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Skillset file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {file_path}: {e}") from e

    def validate_structure(self, data: Dict[str, Any]) -> bool:
        """
        Validate that the loaded data follows the expected structure.

        Args:
            data: The loaded JSON data.

        Returns:
            True if valid, raises ValueError otherwise.
        """
        if not isinstance(data, dict):
            raise ValueError("Skillset must be a dictionary of domains.")

        for domain, content in data.items():
            if not isinstance(content, dict):
                raise ValueError(
                    f"Each domain must map to a dict, got {type(content)} for '{domain}'."
                )

            for category, skills in content.items():
                if not isinstance(skills, list):
                    raise ValueError(
                        f"Category '{category}' in '{domain}' must map to a list of skills, got {type(skills)}."
                    )

        return True

    def load(self, file_path: str) -> Dict[str, Any]:
        """
        Load master skillset data from a JSON file and validate it.

        Args:
            file_path: Path to JSON file.

        Returns:
            Dictionary containing validated skillset data.
        """
        data: Dict[str, Any] = self.load_json(file_path)
        self.validate_structure(data)
        return data


# ============================================================================
# COMPLETE FIXED VERSION OF KEY FUNCTIONS
# ============================================================================

# Here's a complete working version with all fixes applied:


def extract_keywords_fixed(
    text: str, min_length: int = 3, top_n: Optional[int] = None
) -> List[str]:
    """Extract keywords from text with proper type annotations."""
    if not text:
        return []

    words = re.findall(r"\b[a-z]{" + str(min_length) + r",}\b", text.lower())

    stop_words = {
        "the",
        "and",
        "for",
        "are",
        "but",
        "not",
        "you",
        "all",
        "can",
        "her",
        "was",
        "one",
        "our",
        "out",
        "day",
        "get",
        "has",
        "him",
        "his",
        "how",
        "man",
        "new",
        "now",
        "old",
        "see",
        "two",
        "way",
        "who",
        "boy",
        "did",
        "its",
        "let",
        "put",
        "say",
        "she",
        "too",
        "use",
        "with",
        "will",
        "this",
        "that",
        "from",
        "have",
        "they",
        "been",
        "were",
        "what",
        "when",
        "your",
    }

    word_freq: Dict[str, int] = {}
    for word in words:
        if word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1

    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, _ in sorted_words]
    return keywords[:top_n] if top_n else keywords


def retry_on_error_fixed(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[type[Exception], ...] = (Exception,),
):
    """Decorator to retry function on error with exponential backoff."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception: Optional[Exception] = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        _logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {e}"
                        )
                        raise

                    _logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. "
                        f"Retrying in {current_delay}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

            if last_exception is not None:
                raise last_exception
            raise RuntimeError(f"Function {func.__name__} failed without exception")

        return wrapper

    return decorator


def memoize_fixed(max_size: int = 128):
    """Simple memoization decorator with size limit."""

    def decorator(func: Callable) -> Callable:
        cache: Dict[str, Any] = {}
        cache_order: List[str] = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))

            if key in cache:
                return cache[key]

            result = func(*args, **kwargs)
            cache[key] = result
            cache_order.append(key)

            if len(cache) > max_size:
                oldest_key = cache_order.pop(0)
                del cache[oldest_key]

            return result

        def cache_clear() -> None:
            cache.clear()
            cache_order.clear()

        def cache_info() -> Dict[str, int]:
            return {"size": len(cache), "max_size": max_size}

        setattr(wrapper, "cache_clear", cache_clear)
        setattr(wrapper, "cache_info", cache_info)

        return wrapper

    return decorator
