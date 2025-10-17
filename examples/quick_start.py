#!/usr/bin/env python3
"""
Quick Start Example - Minimal usage
"""

from src.python_advanced_job_engine import AdvancedJobEngine


def main():
    # Initialize
    engine = AdvancedJobEngine()

    # Analyze from files
    analysis = engine.analyze_from_files(
        cv_file="data/my_cv.pdf",
        job_file="data/target_job.pdf",
        job_title="Senior ML Engineer",
        company="TechCorp",
    )

    # Print results
    print(f"Match Score: {analysis['score']['total_score']}%")

    # Create learning plan
    plan = engine.create_learning_plan(analysis)
    print(f"Learning Plan: {plan['estimated_duration']}")

    # Export everything
    result = engine.export_all(analysis["job_id"])
    print(result)


if __name__ == "__main__":
    main()
