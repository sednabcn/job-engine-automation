#!/usr/bin/env python3
"""
Full Workflow Example - Complete process demonstration
"""

from src.python_advanced_job_engine import AdvancedJobEngine


def main():
    # Initialize engine
    engine = AdvancedJobEngine()

    # Step 1: Analyze job
    print("Step 1: Analyzing job posting...")
    analysis = engine.analyze_from_files(cv_file="data/my_cv.pdf", job_file="data/target_job.pdf")

    # Step 2: Review match score
    print(f"Match Score: {analysis['score']['total_score']}%")

    # Step 3: Create application strategy
    engine.create_application_strategy(analysis)
    strategy = engine.create_application_strategy(analysis)
    print(f"Strategy: {strategy['approach']}")

    # Step 4: Generate skill tests
    print("\nStep 4: Generating skill tests...")
    tests = engine.generate_skill_tests(analysis["gaps"]["missing_required_skills"])
    print(f"Created {len(tests)} skill assessment tests")

    # Step 5: Update master skillset
    new_skills = engine.update_skillset_from_analysis(analysis)
    print(f"Updated skillset with {len(new_skills)} new skills")

    # Step 6: Generate cover letter variations
    print("\nStep 6: Generating application materials...")
    letters = engine.generate_cover_letter_variations(analysis, count=3)
    print(f"Generated {len(letters)} cover letter variations")

    # Step 7: Export everything
    print("\nStep 7: Exporting results...")
    result = engine.export_all(analysis["job_id"])
    print(result)


if __name__ == "__main__":
    main()
