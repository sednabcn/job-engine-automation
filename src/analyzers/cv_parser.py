"""
CV Parser Module
Extracts and structures information from CV/resume text.
"""

import re
from typing import Dict, List, Optional


class CVParser:
    """Parse and extract structured information from CV text."""

    def __init__(self) -> None:
        """Initialize the CV parser."""
        self.skills_keywords = {
            "python",
            "java",
            "javascript",
            "typescript",
            "c++",
            "c#",
            "ruby",
            "go",
            "rust",
            "swift",
            "kotlin",
            "scala",
            "php",
            "r",
            "matlab",
            "django",
            "flask",
            "fastapi",
            "spring",
            "react",
            "angular",
            "vue",
            "node.js",
            "express",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "gcp",
            "sql",
            "postgresql",
            "mysql",
            "mongodb",
            "redis",
            "elasticsearch",
            "git",
            "ci/cd",
            "jenkins",
            "github actions",
            "terraform",
            "ansible",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "data analysis",
            "pandas",
            "numpy",
            "spark",
            "hadoop",
            "kafka",
            "rest api",
            "graphql",
            "microservices",
            "agile",
            "scrum",
            "tdd",
        }

    def parse(self, cv_text: str) -> Dict[str, Optional[object]]:
        """
        Parse CV text and extract structured information.

        Args:
            cv_text: Raw CV text content

        Returns:
            Dictionary containing parsed CV information
        """
        return {
            "name": self._extract_name(cv_text),
            "email": self._extract_email(cv_text),
            "phone": self._extract_phone(cv_text),
            "linkedin": self._extract_linkedin(cv_text),
            "github": self._extract_github(cv_text),
            "skills": self._extract_skills(cv_text),
            "experience": self._extract_experience(cv_text),
            "education": self._extract_education(cv_text),
            "summary": self._extract_summary(cv_text),
            "certifications": self._extract_certifications(cv_text),
        }

    def _extract_name(self, text: str) -> Optional[str]:
        lines = text.strip().split("\n")
        for line in lines[:5]:
            line = line.strip()
            if line and len(line.split()) <= 5 and re.match(r"^[A-Z][a-zA-Z\s\'-]+$", line):
                return line
        return None

    def _extract_email(self, text: str) -> Optional[str]:
        matches = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
        return str(matches[0]) if matches else None

    def _extract_phone(self, text: str) -> Optional[str]:
        patterns = [
            r"\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            r"\+?\d{10,15}",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return str(matches[0])
        return None

    def _extract_linkedin(self, text: str) -> Optional[str]:
        matches = re.findall(
            r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+", text, re.IGNORECASE
        )
        return str(matches[0]) if matches else None

    def _extract_github(self, text: str) -> Optional[str]:
        matches = re.findall(r"(?:https?://)?(?:www\.)?github\.com/[\w-]+", text, re.IGNORECASE)
        return str(matches[0]) if matches else None

    def _extract_skills(self, text: str) -> List[str]:
        text_lower = text.lower()
        found_skills = {skill.title() for skill in self.skills_keywords if skill in text_lower}
        return sorted(found_skills)

    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        section = self._extract_section(
            text, ["experience", "work experience", "employment", "professional experience"]
        )
        if not section:
            return []
        experiences: List[Dict[str, str]] = []
        lines = section.split("\n")
        current_entry: Dict[str, str] = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_entry:
                    experiences.append(current_entry)
                    current_entry = {}
                continue
            year_match = re.search(
                r"(20\d{2})\s*[-–—]\s*(20\d{2}|Present|Current)", line, re.IGNORECASE
            )
            if year_match:
                if current_entry:
                    experiences.append(current_entry)
                current_entry = {
                    "title": line.split(year_match.group(0))[0].strip(),
                    "period": year_match.group(0),
                    "description": "",
                }
            elif current_entry:
                current_entry["description"] += line + " "
        if current_entry:
            experiences.append(current_entry)
        return experiences

    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        section = self._extract_section(text, ["education", "academic"])
        if not section:
            return []
        education: List[Dict[str, str]] = []
        degree_keywords = ["bachelor", "master", "phd", "doctorate", "diploma", "degree"]
        for line in section.split("\n"):
            line = line.strip()
            if any(k in line.lower() for k in degree_keywords):
                education.append({"degree": line})
        return education

    def _extract_summary(self, text: str) -> Optional[str]:
        section = self._extract_section(
            text, ["summary", "professional summary", "profile", "about", "objective"]
        )
        if section:
            paragraphs = [p.strip() for p in section.split("\n\n") if p.strip()]
            return paragraphs[0] if paragraphs else None
        return None

    def _extract_certifications(self, text: str) -> List[str]:
        section = self._extract_section(text, ["certifications", "certificates", "licenses"])
        if not section:
            return []
        return [
            line.strip() for line in section.split("\n") if line.strip() and len(line.strip()) > 5
        ]

    def _extract_section(self, text: str, section_names: List[str]) -> Optional[str]:
        text_lower = text.lower()
        for section_name in section_names:
            pattern = rf"\n\s*{re.escape(section_name)}\s*[:\n]"
            match = re.search(pattern, text_lower)
            if match:
                start_pos = match.end()
                next_section_pattern = r"\n\s*[A-Z][A-Za-z\s]+\s*:\s*\n"
                next_match = re.search(next_section_pattern, text[start_pos:])
                end_pos = start_pos + next_match.start() if next_match else len(text)
                return text[start_pos:end_pos].strip()
        return None
