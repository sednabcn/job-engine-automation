"""Matcher Module
Matches CVs and job descriptions using keyword similarity and scoring mechanisms.
Computes match percentages and highlights aligned or missing terms.
"""

import logging
from typing import Dict, List, Union

logger = logging.getLogger(__name__)


class Matcher:
    """Matches CV and job description content based on keyword overlap."""

    @staticmethod
    def compute_match(cv_content: str, job_content: str) -> Dict[str, Union[float, List[str]]]:
        """Compute similarity score and matched keywords between CV and job description.

        Args:
            cv_content: Text content of the CV.
            job_content: Text content of the job description.

        Returns:
            Dictionary with match score, matched keywords, and missing keywords.
        """
        if not cv_content or not job_content:
            logger.warning("Empty input provided for match computation.")
            return {"score": 0.0, "matched_keywords": [], "missing_keywords": []}

        cv_keywords = Matcher._extract_keywords(cv_content)
        job_keywords = Matcher._extract_keywords(job_content)

        matched_keywords = sorted(list(job_keywords & cv_keywords))
        missing_keywords = sorted(list(job_keywords - cv_keywords))

        score = len(matched_keywords) / len(job_keywords) * 100 if job_keywords else 0.0

        return {
            "score": round(score, 2),
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
        }

    @staticmethod
    def _extract_keywords(text: str) -> set[str]:
        import re

        words = re.findall(r"[a-zA-Z]{3,}", text.lower())
        stopwords = {
            "and",
            "the",
            "for",
            "with",
            "that",
            "this",
            "from",
            "are",
            "was",
            "you",
            "your",
            "have",
            "will",
            "not",
            "but",
            "can",
            "all",
            "our",
            "job",
            "work",
            "team",
            "who",
        }

        return {word for word in words if word not in stopwords}


if __name__ == "__main__":
    cv_text = "Python developer skilled in TensorFlow, SQL, and data analysis."
    job_text = "We seek a Python engineer experienced in TensorFlow, communication, and teamwork."

    result = Matcher.compute_match(cv_text, job_text)
    print(f"Match Score: {result['score']}%")
    print(f"Matched Keywords: {result['matched_keywords']}")
    print(f"Missing Keywords: {result['missing_keywords']}")
