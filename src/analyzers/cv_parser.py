"""
CV Parser Module
Extracts and structures information from CV/resume text.
"""

import re
from typing import Dict, List, Any, Optional


class CVParser:
    """Parse and extract structured information from CV text."""

    def __init__(self) -> None:
        """Initialize the CV parser."""
        self.skills_keywords = {
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go",
            "rust", "swift", "kotlin", "scala", "php", "r", "matlab",
            "django", "flask", "fastapi", "spring", "react", "angular", "vue",
            "node.js", "express", "docker", "kubernetes", "aws", "azure", "gcp",
            "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
            "git", "ci/cd", "jenkins", "github actions", "terraform", "ansible",
            "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
            "data analysis", "pandas", "numpy", "spark", "hadoop", "kafka",
            "rest api", "graphql", "microservices", "agile", "scrum", "tdd"
        }

    def parse(self, cv_text: str) -> Dict[str, Any]:
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
        """Extract candidate name from CV text."""
        lines = text.strip().split('\n')
        
        # Try to find name after "Name:" label
        for line in lines[:10]:
            if re.match(r'^\s*name\s*:', line, re.IGNORECASE):
                name = re.sub(r'^\s*name\s*:\s*', '', line, flags=re.IGNORECASE).strip()
                if name:
                    return name
        
        # First non-empty line might be the name
        for line in lines[:5]:
            line = line.strip()
            if line and len(line.split()) <= 5:
                # Likely a name if it's short and looks like a name
                if re.match(r'^[A-Z][a-zA-Z\s\'-]+$', line):
                    return line
        
        return None

    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address from CV text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return str(matches[0]) if matches else None

    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from CV text."""
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+?\d{10,15}'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return str(matches[0])
        
        return None

    def _extract_linkedin(self, text: str) -> Optional[str]:
        """Extract LinkedIn profile URL from CV text."""
        linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+'
        matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
        return str(matches[0]) if matches else None

    def _extract_github(self, text: str) -> Optional[str]:
        """Extract GitHub profile URL from CV text."""
        github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w-]+'
        matches = re.findall(github_pattern, text, re.IGNORECASE)
        return str(matches[0]) if matches else None

    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from CV text."""
        text_lower = text.lower()
        found_skills = []
        
        # Look for skills section
        skills_section = self._extract_section(text, ["skills", "technical skills", "expertise"])
        if skills_section:
            text_to_search = skills_section
        else:
            text_to_search = text_lower
        
        # Find matching skills
        for skill in self.skills_keywords:
            if skill in text_to_search:
                found_skills.append(skill.title())
        
        # Remove duplicates and sort
        found_skills = sorted(list(set(found_skills)))
        
        return found_skills

    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience from CV text."""
        experience_section = self._extract_section(
            text, 
            ["experience", "work experience", "employment", "professional experience"]
        )
        
        if not experience_section:
            return []
        
        experiences = []
        
        # Try to find job entries with dates
        # Pattern: company/title with year ranges
        lines = experience_section.split('\n')
        current_entry: Dict[str, Any] = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_entry:
                    experiences.append(current_entry)
                    current_entry = {}
                continue
            
            # Look for year patterns (2020-2023, 2020-Present, etc.)
            year_pattern = r'(20\d{2})\s*[-–—]\s*(20\d{2}|Present|Current)'
            year_match = re.search(year_pattern, line, re.IGNORECASE)
            
            if year_match:
                if current_entry:
                    experiences.append(current_entry)
                current_entry = {
                    "title": line.split(year_match.group(0))[0].strip(),
                    "period": year_match.group(0),
                    "description": ""
                }
            elif current_entry:
                current_entry["description"] += line + " "
        
        if current_entry:
            experiences.append(current_entry)
        
        return experiences

    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information from CV text."""
        education_section = self._extract_section(text, ["education", "academic"])
        
        if not education_section:
            return []
        
        education = []
        lines = education_section.split('\n')
        
        degree_keywords = ["bachelor", "master", "phd", "doctorate", "diploma", "degree"]
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in degree_keywords):
                education.append({"degree": line})
        
        return education

    def _extract_summary(self, text: str) -> Optional[str]:
        """Extract professional summary from CV text."""
        summary_section = self._extract_section(
            text,
            ["summary", "professional summary", "profile", "about", "objective"]
        )
        
        if summary_section:
            # Take first paragraph
            paragraphs = [p.strip() for p in summary_section.split('\n\n') if p.strip()]
            return paragraphs[0] if paragraphs else None
        
        return None

    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications from CV text."""
        cert_section = self._extract_section(
            text,
            ["certifications", "certificates", "licenses"]
        )
        
        if not cert_section:
            return []
        
        certifications = []
        lines = cert_section.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 5:
                certifications.append(line)
        
        return certifications

    def _extract_section(self, text: str, section_names: List[str]) -> Optional[str]:
        """
        Extract a specific section from CV text.

        Args:
            text: CV text content
            section_names: List of possible section header names

        Returns:
            Section content or None if not found
        """
        text_lower = text.lower()
        
        for section_name in section_names:
            # Look for section header (case-insensitive)
            pattern = rf'\n\s*{re.escape(section_name)}\s*[:\n]'
            match = re.search(pattern, text_lower)
            
            if match:
                start_pos = match.end()
                
                # Find the next section header or end of text
                next_section_pattern = r'\n\s*[A-Z][A-Za-z\s]+\s*:\s*\n'
                next_match = re.search(next_section_pattern, text[start_pos:])
                
                if next_match:
                    end_pos = start_pos + next_match.start()
                    return text[start_pos:end_pos].strip()
                else:
                    return text[start_pos:].strip()
        
        return None
