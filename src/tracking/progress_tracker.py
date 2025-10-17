"""
Module to track candidate's learning progress.
"""

from typing import Dict


class ProgressTracker:
    """Tracks learning progress for skills."""

    def __init__(self):
        self.progress: Dict[str, float] = {}

    def update_progress(self, skill: str, completion: float):
        """Update the progress for a given skill (0-100%)."""
        self.progress[skill] = max(0.0, min(100.0, completion))

    def get_progress(self, skill: str) -> float:
        """Get current progress of a skill."""
        return self.progress.get(skill, 0.0)

    def get_all_progress(self) -> Dict[str, float]:
        """Return progress for all tracked skills."""
        return dict(self.progress)
