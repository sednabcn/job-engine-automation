"""Job Parser Module
Extracts structured information from job description text such as title, company, location,
responsibilities, and qualifications.
"""

import logging
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class JobParser:
    """Parses job description text to extract key details."""

    @staticmethod
    def parse(job_content: str) -> Dict[str, Optional[Any]]:
        """Extracts key information from a job description.

        Args:
            job_content: Text of the job description.

        Returns:
            Dictionary with structured information such as title, company, location, etc.
        """
        if not job_content:
            logger.warning("Empty job description provided to parser.")
            return {
                "title": None,
                "company": None,
                "location": None,
                "responsibilities": [],
                "qualifications": [],
            }

        title = JobParser._extract_field(job_content, r"(?i)position[:\s]+([\w\s\-/,]+)")
        company = JobParser._extract_field(job_content, r"(?i)company[:\s]+([\w\s\-/,]+)")
        location = JobParser._extract_field(job_content, r"(?i)location[:\s]+([\w\s\-/,]+)")

        responsibilities = JobParser._extract_list(job_content, r"(?i)responsibilities|duties")
        qualifications = JobParser._extract_list(job_content, r"(?i)qualifications|requirements")

        return {
            "title": title,
            "company": company,
            "location": location,
            "responsibilities": responsibilities,
            "qualifications": qualifications,
        }

    @staticmethod
    def _extract_field(text: str, pattern: str) -> Optional[str]:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return None

    @staticmethod
    def _extract_list(text: str, section_pattern: str) -> list[str]:
        """Extract bullet or numbered lists following a section header."""
        import re

        section_regex = re.compile(section_pattern + r"[\s\S]*?(?:\n{2,}|$)", re.IGNORECASE)
        match = section_regex.search(text)

        if not match:
            return []

        section_text = match.group(0)
        items = re.findall(r"(?:[-*•]\s+|\d+\.\s+)([A-Za-z0-9,\s\-()]+)", section_text)
        return [item.strip() for item in items if item.strip()]


if __name__ == "__main__":
    sample_job = """Company: OpenAI
Position: Machine Learning Engineer
Location: London

Responsibilities:
- Build scalable ML models
- Collaborate with research and product teams

Qualifications:
- Experience with Python, PyTorch, and TensorFlow
- Strong communication skills
"""

    parsed = JobParser.parse(sample_job)
    print(parsed)
