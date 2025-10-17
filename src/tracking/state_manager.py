"""
Module to manage persistent state for learning and tracking.
"""

from typing import Any, Dict


class StateManager:
    """Stores and retrieves persistent state."""

    def __init__(self):
        self.state: Dict[str, Any] = {}

    def set_state(self, key: str, value: Any):
        """Set a state value."""
        self.state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a state value."""
        return self.state.get(key, default)

    def get_all_state(self) -> Dict[str, Any]:
        """Return all stored state."""
        return dict(self.state)
