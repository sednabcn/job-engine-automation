"""
Module to generate skill tests.
"""

from typing import Dict, List


class SkillTestGenerator:
    """Generates simple tests for candidate skills."""

    def __init__(self):
        pass

    def generate_test(self, skills: List[str]) -> Dict[str, str]:
        """Generate a simple test question per skill."""
        return {skill: f"Question to test {skill}" for skill in skills}
