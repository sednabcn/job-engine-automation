"""Gap Analyzer Module
Analyzes gaps or mismatches between CV content and job description content.
Ensures compatibility and identifies missing skills, keywords, or experience areas.
"""

import logging
from typing import Dict, List, Set

logger = logging.getLogger(__name__)


class GapAnalyzer:
    """Compares CV and job description text to identify skill and keyword gaps."""

    @staticmethod
    def analyze(cv_content: str, job_content: str) -> Dict[str, List[str]]:
        """Analyze the difference in keywords between CV and job description.

        Args:
            cv_content: Text content of the CV.
            job_content: Text content of the job description.

        Returns:
            Dictionary containing missing skills and overlapping keywords.
        """
        if not cv_content or not job_content:
            logger.warning("Empty content detected for analysis.")
            return {"missing_keywords": [], "matched_keywords": []}

        cv_words = GapAnalyzer._extract_keywords(cv_content)
        job_words = GapAnalyzer._extract_keywords(job_content)

        missing_keywords = sorted(list(job_words - cv_words))
        matched_keywords = sorted(list(job_words & cv_words))

        return {
            "missing_keywords": missing_keywords,
            "matched_keywords": matched_keywords,
        }

    @staticmethod
    def _extract_keywords(text: str) -> Set[str]:
        """Extract meaningful keywords from text.

        Converts text to lowercase, splits on non-alphabetic characters,
        and filters out short or common words.
        """
        import re

        words = re.findall(r"[a-zA-Z]{3,}", text.lower())

        stopwords = {
            "and", "the", "for", "with", "that", "this", "from", "are", "was", "you", "your",
            "have", "will", "not", "but", "can", "all", "our", "job", "work", "team", "who",
        }

        keywords = {word for word in words if word not in stopwords}
        return keywords


if __name__ == "__main__":
    # Example usage
    cv_text = "Experienced data scientist skilled in Python, SQL, and machine learning."
    job_text = "Looking for a Python developer with SQL, TensorFlow, and communication skills."

    result = GapAnalyzer.analyze(cv_text, job_text)
    print("Missing Keywords:", result["missing_keywords"])
    print("Matched Keywords:", result["matched_keywords"])
