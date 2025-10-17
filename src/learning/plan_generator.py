"""
Module to generate learning plans for skill gaps.
"""

from typing import Dict, List


class LearningPlanGenerator:
    """Generates personalized learning plans based on skill gaps."""

    def __init__(self):
        pass

    def generate_plan(self, skill_gaps: List[str]) -> Dict[str, str]:
        """Generate a learning plan for given skill gaps.

        Args:
            skill_gaps: List of missing skills.

        Returns:
            Dictionary mapping skill to recommended resource.
        """
        plan = {skill: f"Recommended resource for {skill}" for skill in skill_gaps}
        return plan
