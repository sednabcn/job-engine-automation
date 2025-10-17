"""
Unit tests for sprint management
Tests sprint tracking, logging, and completion
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from src.tracking.sprint_manager import SprintManager

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestSprintManager:
    """Test suite for sprint management"""

    @pytest.fixture
    def manager(self):
        """Create a sprint manager instance"""
        return SprintManager()

    @pytest.fixture
    def sample_sprint_data(self):
        """Sample sprint data for testing"""
        return {
            "sprint_number": 1,
            "skills_targeted": ["Docker", "Kubernetes"],
            "project_goal": "Deploy containerized app on K8s cluster",
            "start_date": datetime.now().isoformat(),
            "duration_weeks": 2,
            "daily_logs": [],
            "completed": False,
        }

    def test_start_sprint(self, manager):
        """Test starting a new sprint"""
        skills = ["Docker", "Kubernetes"]
        project_goal = "Deploy containerized app on K8s cluster"

        sprint = manager.start_sprint(skills, project_goal)

        assert sprint["sprint_number"] == 1
        assert sprint["skills_targeted"] == skills
        assert sprint["project_goal"] == project_goal
        assert sprint["completed"] is False
        assert "start_date" in sprint

    def test_log_daily_progress(self, manager, sample_sprint_data):
        """Test logging daily progress"""
        manager.current_sprint = sample_sprint_data

        log_entry = {
            "date": datetime.now().isoformat(),
            "hours_studied": 2.5,
            "topics_covered": ["Docker basics", "Container networking"],
            "challenges": "Understanding volumes",
            "progress_rating": 4,
        }

        manager.log_daily_progress(log_entry)

        assert len(manager.current_sprint["daily_logs"]) == 1
        assert manager.current_sprint["daily_logs"][0]["hours_studied"] == 2.5

    def test_calculate_total_hours(self, manager, sample_sprint_data):
        """Test total hours calculation"""
        sample_sprint_data["daily_logs"] = [
            {"hours_studied": 2.0},
            {"hours_studied": 3.0},
            {"hours_studied": 1.5},
        ]

        total = manager.calculate_total_hours(sample_sprint_data)

        assert total == 6.5

    def test_end_sprint(self, manager, sample_sprint_data):
        """Test ending a sprint"""
        manager.current_sprint = sample_sprint_data

        project_url = "https://github.com/user/k8s-project"
        test_scores = {"Docker": 85, "Kubernetes": 78}

        result = manager.end_sprint(project_url, test_scores)

        assert result["completed"] is True
        assert result["project_url"] == project_url
        assert result["test_scores"] == test_scores
        assert "end_date" in result
        assert "total_hours" in result

    def test_sprint_completion_validation(self, manager, sample_sprint_data):
        """Test sprint completion validation"""
        sample_sprint_data["daily_logs"] = [
            {"hours_studied": 2.0, "date": (datetime.now() - timedelta(days=i)).isoformat()}
            for i in range(14)
        ]

        is_valid = manager.validate_completion(sample_sprint_data)

        assert is_valid is True

    def test_incomplete_sprint_detection(self, manager, sample_sprint_data):
        """Test detection of incomplete sprints"""
        sample_sprint_data["daily_logs"] = [{"hours_studied": 1.0}]  # Only 1 day logged

        is_valid = manager.validate_completion(sample_sprint_data)

        assert is_valid is False

    def test_sprint_progress_percentage(self, manager, sample_sprint_data):
        """Test sprint progress calculation"""
        sample_sprint_data["duration_weeks"] = 2
        sample_sprint_data["daily_logs"] = [
            {"date": (datetime.now() - timedelta(days=i)).isoformat()}
            for i in range(7)  # 7 days out of 14
        ]

        progress = manager.calculate_progress(sample_sprint_data)

        assert progress == 50.0

    def test_consecutive_sprints(self, manager):
        """Test starting consecutive sprints"""
        sprint1 = manager.start_sprint(["Skill1"], "Goal1")
        manager.end_sprint("url1", {"Skill1": 80})

        sprint2 = manager.start_sprint(["Skill2"], "Goal2")

        assert sprint2["sprint_number"] == 2
        assert sprint1["sprint_number"] == 1

    def test_sprint_statistics(self, manager, sample_sprint_data):
        """Test sprint statistics calculation"""
        sample_sprint_data["daily_logs"] = [
            {"hours_studied": 2.0, "progress_rating": 4},
            {"hours_studied": 3.0, "progress_rating": 5},
            {"hours_studied": 2.5, "progress_rating": 3},
        ]

        stats = manager.get_sprint_statistics(sample_sprint_data)

        assert "total_hours" in stats
        assert "average_hours_per_day" in stats
        assert "average_progress_rating" in stats
        assert stats["total_hours"] == 7.5
        assert stats["average_progress_rating"] == 4.0


class TestSprintManagerValidation:
    """Test sprint validation and quality checks"""

    @pytest.fixture
    def manager(self):
        return SprintManager()

    def test_minimum_hours_requirement(self, manager):
        """Test minimum hours requirement for sprint"""
        sprint = {"daily_logs": [{"hours_studied": 0.5}, {"hours_studied": 0.5}]}

        meets_requirement = manager.check_minimum_hours(sprint, minimum=20)

        assert meets_requirement is False

    def test_consistency_check(self, manager):
        """Test checking for consistent daily progress"""
        consistent_sprint = {
            "daily_logs": [
                {"date": (datetime.now() - timedelta(days=i)).isoformat(), "hours_studied": 2.0}
                for i in range(14)
            ]
        }

        is_consistent = manager.check_consistency(consistent_sprint)

        assert is_consistent is True

    def test_gap_detection(self, manager):
        """Test detection of gaps in daily logging"""
        sprint_with_gaps = {
            "start_date": (datetime.now() - timedelta(days=14)).isoformat(),
            "daily_logs": [
                {"date": (datetime.now() - timedelta(days=10)).isoformat()},
                {"date": (datetime.now() - timedelta(days=5)).isoformat()},
                {"date": datetime.now().isoformat()},
            ],
        }

        gaps = manager.detect_gaps(sprint_with_gaps)

        assert len(gaps) > 0

    def test_quality_gate_check(self, manager):
        """Test quality gate checking for sprint completion"""
        sprint = {
            "daily_logs": [{"hours_studied": 2.0} for _ in range(14)],
            "test_scores": {"Skill1": 75, "Skill2": 80},
        }

        quality_gates = {"minimum_hours": 20, "minimum_test_score": 70, "minimum_days": 10}

        passes = manager.check_quality_gates(sprint, quality_gates)

        assert passes is True


class TestSprintManagerReporting:
    """Test sprint reporting and analytics"""

    @pytest.fixture
    def manager(self):
        return SprintManager()

    def test_generate_sprint_report(self, manager):
        """Test sprint report generation"""
        sprint = {
            "sprint_number": 1,
            "skills_targeted": ["Docker"],
            "daily_logs": [{"hours_studied": 2.0} for _ in range(14)],
            "test_scores": {"Docker": 85},
            "completed": True,
        }

        report = manager.generate_report(sprint)

        assert "sprint_number" in report
        assert "total_hours" in report
        assert "completion_status" in report
        assert "performance_summary" in report

    def test_compare_sprints(self, manager):
        """Test comparing multiple sprints"""
        sprint1 = {
            "sprint_number": 1,
            "daily_logs": [{"hours_studied": 2.0} for _ in range(10)],
            "test_scores": {"Skill1": 70},
        }

        sprint2 = {
            "sprint_number": 2,
            "daily_logs": [{"hours_studied": 3.0} for _ in range(12)],
            "test_scores": {"Skill2": 85},
        }

        comparison = manager.compare_sprints([sprint1, sprint2])

        assert "improvement" in comparison
        assert "trends" in comparison

    def test_calculate_velocity(self, manager):
        """Test learning velocity calculation"""
        sprints = [
            {"sprint_number": 1, "skills_mastered": 2, "total_hours": 20},
            {"sprint_number": 2, "skills_mastered": 3, "total_hours": 25},
            {"sprint_number": 3, "skills_mastered": 2, "total_hours": 22},
        ]

        velocity = manager.calculate_velocity(sprints)

        assert "skills_per_sprint" in velocity
        assert "hours_per_skill" in velocity

    def test_predict_completion_date(self, manager):
        """Test completion date prediction"""
        current_progress = {"completed_sprints": 3, "skills_mastered": 7, "target_skills": 15}
        average_velocity = 2.3  # skills per sprint

        prediction = manager.predict_completion(current_progress, average_velocity)

        assert "estimated_sprints_remaining" in prediction
        assert "estimated_completion_date" in prediction


class TestSprintManagerEdgeCases:
    """Test edge cases and error handling"""

    @pytest.fixture
    def manager(self):
        return SprintManager()

    def test_start_sprint_without_ending_previous(self, manager):
        """Test starting new sprint without ending previous one"""
        manager.start_sprint(["Skill1"], "Goal1")

        with pytest.raises(Exception):
            manager.start_sprint(["Skill2"], "Goal2")

    def test_log_progress_without_active_sprint(self, manager):
        """Test logging progress without active sprint"""
        with pytest.raises(Exception):
            manager.log_daily_progress({"hours_studied": 2.0})

    def test_negative_hours(self, manager):
        """Test handling of negative hours"""
        with pytest.raises(ValueError):
            manager.log_daily_progress({"hours_studied": -1.0})

    def test_future_date_logging(self, manager):
        """Test preventing logging for future dates"""
        future_date = (datetime.now() + timedelta(days=1)).isoformat()

        with pytest.raises(ValueError):
            manager.log_daily_progress({"date": future_date, "hours_studied": 2.0})


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
