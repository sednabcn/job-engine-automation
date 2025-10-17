"""
Examples Package
----------------
This package exposes all example/demo scripts for the advanced-job-engine project.
You can import individual workflows or automation demos as needed.
"""

from .quick_start import main as quick_start
from .full_workflow import main as full_workflow
from .reverse_workflow import main as reverse_workflow
from .batch_analysis import main as batch_analysis
from .custom_resources import main as custom_resources
from .automation_example import main as automation_example
from .full_roadmap import main as full_roadmap

__all__ = [
    "quick_start",
    "full_workflow",
    "reverse_workflow",
    "batch_analysis",
    "custom_resources",
    "automation_example",
    "full_roadmap",
]
