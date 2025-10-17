"""
Learning Plan Demo
-----------------
Generates a personalized learning plan based on missing skills
from CV vs. Job Description.
"""

from src.analyzers import cv_parser, gap_analyzer
from src.learning import plan_generator, strategy_builder
from src.utils import file_readers


def main():
    # Load sample CV and job description
    cv_text = file_readers.read_text_file("tests/fixtures/sample_cv.txt")
    job_text = file_readers.read_text_file("tests/fixtures/sample_job.txt")

    # Parse CV
    parser = cv_parser.CVParser()
    cv_data = parser.parse(cv_text)

    # Compute skill gaps
    gaps = gap_analyzer.analyze(cv_data, job_text)
    missing_skills = gaps.get("missing_keywords", [])

    if not missing_skills:
        print("No skill gaps detected. Candidate is a perfect match!")
        return

    # Generate learning plan
    plan = plan_generator.LearningPlanGenerator(missing_skills).generate_plan()

    # Generate improvement strategy
    strategy = strategy_builder.StrategyBuilder(plan).build_strategy()

    # Print learning plan and strategy
    print("Missing Skills:", missing_skills)
    print("\nRecommended Learning Plan:")
    for step in plan:
        print("-", step)

    print("\nSuggested Improvement Strategy:")
    for s in strategy:
        print("-", s)


if __name__ == "__main__":
    main()
