"""
Advanced Job Engine - main package
"""

# Optional: import key submodules for top-level access
from .analyzers import cv_parser, gap_analyzer, job_parser, matcher
from .generators import letter_generator, report_generator, template_engine
from .learning import plan_generator, resource_db, strategy_builder, test_generator
from .tracking import progress_tracker, quality_gates, sprint_manager, state_manager
from .utils import data_loader, file_readers, formatters, helpers, validators

__all__ = [
    "gap_analyzer",
    "matcher",
    "cv_parser",
    "job_parser",
    "plan_generator",
    "resource_db",
    "test_generator",
    "strategy_builder",
    "sprint_manager",
    "quality_gates",
    "progress_tracker",
    "state_manager",
    "letter_generator",
    "report_generator",
    "template_engine",
    "file_readers",
    "data_loader",
    "validators",
    "formatters",
    "helpers",
]
