"""
Reverse Workflow Demo
--------------------
Demonstrates the reverse mode: starting from a target job description,
analyzing skill gaps, generating a learning plan, and preparing actionable outputs.
"""

from src.analyzers import cv_parser, gap_analyzer
from src.learning import plan_generator, strategy_builder, test_generator
from src.tracking import progress_tracker, sprint_manager, state_manager
from src.utils import file_readers


def main():
    # Load candidate CV and target job description
    cv_text = file_readers.read_text_file("data/my_cv.pdf")
    job_text = file_readers.read_text_file("data/target_job.pdf")

    # Parse CV
    parser = cv_parser.CVParser()
    cv_data = parser.parse(cv_text)

    # Compute skill gaps
    gap = gap_analyzer.GapAnalyzer()
    gaps = gap.compute_gaps(cv_data.get("skills", []), job_text)
    print("\n--- Identified Skill Gaps ---")
    print(gaps)

    # Generate learning plan
    plan = plan_generator.LearningPlanGenerator()
    learning_plan = plan.generate_plan(gaps)
    print("\n--- Generated Learning Plan ---")
    for step in learning_plan:
        print(step)

    # Generate improvement strategy
    strategy = strategy_builder.StrategyBuilder()
    strategy_actions = strategy.build_strategy(gaps)
    print("\n--- Recommended Improvement Strategy ---")
    for action in strategy_actions:
        print(action)

    # Generate skill tests
    tests = test_generator.SkillTestGenerator()
    skill_tests = tests.generate_tests(gaps)
    print("\n--- Generated Skill Tests ---")
    for test in skill_tests:
        print(test)

    # Optionally track progress
    sprint = sprint_manager.SprintManager("Reverse Workflow Sprint", duration_days=14)
    progress_tracker.ProgressTracker(sprint)
    state = state_manager.StateManager()
    state.save_progress({"learning_plan": learning_plan, "strategy": strategy_actions})
    print("\nProgress state saved.")


if __name__ == "__main__":
    main()
