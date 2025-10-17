"""
Module managing the learning resources database.
"""

from typing import Dict, List


class LearningResourceDB:
    """Database of learning resources."""

    def __init__(self):
        self.resources: Dict[str, List[str]] = {}

    def add_resource(self, skill: str, resource: str):
        """Add a resource for a specific skill."""
        if skill not in self.resources:
            self.resources[skill] = []
        self.resources[skill].append(resource)

    def get_resources(self, skill: str) -> List[str]:
        """Retrieve resources for a skill."""
        return self.resources.get(skill, [])
