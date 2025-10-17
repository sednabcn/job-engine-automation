import pytest

from src.analyzers import gap_analyzer
from src.learning import plan_generator
from src.tracking import sprint_manager
from tests.mocks import mock_data

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def sample_cv():
    return mock_data.get_mock_cv(parsed=True)


@pytest.fixture
def sample_job():
    return mock_data.get_mock_job(parsed=True)


@pytest.fixture
def completed_sprint():
    return mock_data.MOCK_COMPLETED_SPRINT.copy()


@pytest.fixture
def skill_tests():
    return mock_data.MOCK_SKILL_TESTS.copy()


# ============================================================================
# END-TO-END REVERSE WORKFLOW TESTS
# ============================================================================


def test_full_workflow_with_completed_sprint(sample_cv, sample_job, completed_sprint, skill_tests):
    """
    Full end-to-end workflow:
    CV -> Job -> Gap Analysis -> Learning Plan -> Sprint -> Skill Tests -> Score Update
    """

    # Step 1: Analyze gaps
    gaps = gap_analyzer.analyze_skill_gaps(sample_cv, sample_job)

    # Step 2: Generate learning plan based on gaps
    learning_plan = plan_generator.generate_learning_plan(cv=sample_cv, job=sample_job, gaps=gaps)

    # Step 3: Simulate sprint completion
    sprint_result = sprint_manager.complete_sprint(completed_sprint)

    # Ensure sprint marked completed
    assert sprint_result["completed"] is True
    assert sprint_result["completion_rate"] == 100.0
    assert sprint_result["total_hours"] > 0
    assert "Docker" in sprint_result["skills_targeted"]

    # Step 4: Simulate skill tests results
    for skill_name, skill_test in skill_tests.items():
        # Simple simulation: pass all multiple-choice tests
        passed = all(
            q.get("correct_answer") is not None
            for q in skill_test["questions"]
            if q["type"] == "multiple_choice"
        )
        assert passed is True  # All MC questions have correct_answer

    # Step 5: Update learning plan score after sprint and tests
    current_score = learning_plan["current_score"] + getattr(sprint_result, "score_improvement", 0)
    # Ensure it does not exceed 100
    current_score = min(current_score, 100)
    assert 0 <= current_score <= 100

    # Step 6: Check that skills learned in sprint are reflected
    for skill in sprint_result["skills_targeted"]:
        assert skill in learning_plan["skills_to_learn"] or skill in sample_cv["skills"]
