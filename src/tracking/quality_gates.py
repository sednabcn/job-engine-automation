"""
Module to check quality gates for learning milestones.
"""

from typing import Dict


class QualityGates:
    """Checks if certain criteria/milestones are met."""

    def __init__(self):
        self.gates: Dict[str, float] = {}

    def set_gate(self, milestone: str, threshold: float):
        """Set a completion threshold for a milestone."""
        self.gates[milestone] = threshold

    def check_gate(self, milestone: str, progress: float) -> bool:
        """Check if milestone is achieved."""
        threshold = self.gates.get(milestone, 100.0)
        return progress >= threshold
