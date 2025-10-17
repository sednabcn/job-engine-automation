"""
Module to build improvement strategies based on learning progress.
"""

from typing import Dict


class StrategyBuilder:
    """Constructs improvement strategies for a candidate."""

    def __init__(self):
        pass

    def build_strategy(self, learning_plan: Dict[str, str]) -> str:
        """Build a strategy summary based on a learning plan."""
        strategy = "Follow this learning strategy:\n"
        for skill, resource in learning_plan.items():
            strategy += f"- Learn {skill} using {resource}\n"
        return strategy
