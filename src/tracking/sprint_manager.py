"""
Module to manage sprints and learning cycles.
"""

from typing import Dict, List


class SprintManager:
    """Manages learning sprints."""

    def __init__(self):
        self.sprints: List[Dict[str, str]] = []

    def add_sprint(self, name: str, description: str):
        """Add a new sprint."""
        self.sprints.append({"name": name, "description": description})

    def get_sprints(self) -> List[Dict[str, str]]:
        """Return all sprints."""
        return list(self.sprints)
