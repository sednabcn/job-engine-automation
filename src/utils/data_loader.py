"""
Data Loader Module
Handles loading and saving JSON data files for the job engine.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading and saving structured data files."""

    def __init__(self, data_dir: str = "job_search_data"):
        """
        Initialize DataLoader.

        Args:
            data_dir: Directory for storing data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_json(self, filename: str, default: Any = None) -> Any:
        """
        Load JSON file.

        Args:
            filename: Name of the JSON file
            default: Default value if file doesn't exist

        Returns:
            Loaded data or default value
        """
        file_path = self.data_dir / filename

        if not file_path.exists():
            logger.info(f"File not found: {filename}. Using default value.")
            return default if default is not None else {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info(f"Loaded {filename}")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filename}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading {filename}: {str(e)}")
            raise

    def save_json(self, filename: str, data: Any, indent: int = 2) -> None:
        """
        Save data to JSON file.

        Args:
            filename: Name of the JSON file
            data: Data to save
            indent: JSON indentation level
        """
        file_path = self.data_dir / filename

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
                logger.info(f"Saved {filename}")
        except Exception as e:
            logger.error(f"Error saving {filename}: {str(e)}")
            raise

    def backup_json(self, filename: str) -> Optional[str]:
        """
        Create a backup of a JSON file.

        Args:
            filename: Name of the JSON file

        Returns:
            Path to backup file or None if original doesn't exist
        """
        file_path = self.data_dir / filename

        if not file_path.exists():
            logger.warning(f"Cannot backup non-existent file: {filename}")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
        backup_path = self.data_dir / "backups" / backup_filename
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            data = self.load_json(filename)
            with open(backup_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Backup created: {backup_filename}")
            return str(backup_path)
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            raise

    def list_files(self, pattern: str = "*.json") -> List[str]:
        """
        List files in data directory.

        Args:
            pattern: File pattern to match

        Returns:
            List of matching filenames
        """
        return [f.name for f in self.data_dir.glob(pattern)]


class MasterSkillsetLoader(DataLoader):
    """Specialized loader for master skillset data."""

    FILENAME = "master_skillset.json"

    def load(self) -> Dict[str, Any]:
        """Load master skillset."""
        # FIXED: Cast the return value to the expected type
        result = self.load_json(
            self.FILENAME, default={"skills": {}, "last_updated": None, "version": "1.0"}
        )
        return cast(Dict[str, Any], result)

    def save(self, skillset: Dict[str, Any]) -> None:
        """Save master skillset."""
        skillset["last_updated"] = datetime.now().isoformat()
        self.save_json(self.FILENAME, skillset)

    def add_skill(self, skill_name: str, skill_data: Dict[str, Any]) -> None:
        """Add or update a skill in the skillset."""
        skillset = self.load()
        skillset["skills"][skill_name] = {
            **skill_data,
            "added_date": skill_data.get("added_date", datetime.now().isoformat()),
            "last_modified": datetime.now().isoformat(),
        }
        self.save(skillset)

    def get_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific skill from the skillset."""
        skillset = self.load()
        # FIXED: Cast the return value to the expected type
        result = skillset["skills"].get(skill_name)
        return cast(Optional[Dict[str, Any]], result)


class JobAnalysisLoader(DataLoader):
    """Specialized loader for analyzed jobs data."""

    FILENAME = "analyzed_jobs.json"

    def load(self) -> List[Dict[str, Any]]:
        """Load analyzed jobs."""
        # FIXED: Cast the return value to the expected type
        result = self.load_json(self.FILENAME, default=[])
        return cast(List[Dict[str, Any]], result)

    def save(self, jobs: List[Dict[str, Any]]) -> None:
        """Save analyzed jobs."""
        self.save_json(self.FILENAME, jobs)

    def add_job(self, job_data: Dict[str, Any]) -> None:
        """Add a new analyzed job."""
        jobs = self.load()
        job_data["analyzed_date"] = datetime.now().isoformat()
        job_data["job_id"] = job_data.get("job_id", f"job_{len(jobs) + 1}")
        jobs.append(job_data)
        self.save(jobs)

    def get_job_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific job by ID."""
        jobs = self.load()
        for job in jobs:
            if job.get("job_id") == job_id:
                return job
        return None

    def get_recent_jobs(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most recent analyzed jobs."""
        jobs = self.load()
        return sorted(jobs, key=lambda x: x.get("analyzed_date", ""), reverse=True)[:limit]


class LearningProgressLoader(DataLoader):
    """Specialized loader for learning progress data."""

    FILENAME = "learning_progress.json"

    def load(self) -> Dict[str, Any]:
        """Load learning progress."""
        # FIXED: Cast the return value to the expected type
        result = self.load_json(
            self.FILENAME, default={"plans": [], "completed_items": [], "current_plan": None}
        )
        return cast(Dict[str, Any], result)

    def save(self, progress: Dict[str, Any]) -> None:
        """Save learning progress."""
        self.save_json(self.FILENAME, progress)

    def add_plan(self, plan: Dict[str, Any]) -> None:
        """Add a new learning plan."""
        progress = self.load()
        plan["created_date"] = datetime.now().isoformat()
        plan["plan_id"] = plan.get("plan_id", f"plan_{len(progress['plans']) + 1}")
        progress["plans"].append(plan)
        progress["current_plan"] = plan["plan_id"]
        self.save(progress)

    def complete_item(self, item_id: str, notes: str = "") -> None:
        """Mark a learning item as completed."""
        progress = self.load()
        progress["completed_items"].append(
            {"item_id": item_id, "completed_date": datetime.now().isoformat(), "notes": notes}
        )
        self.save(progress)


class SprintHistoryLoader(DataLoader):
    """Specialized loader for sprint history data."""

    FILENAME = "sprint_history.json"

    def load(self) -> List[Dict[str, Any]]:
        """Load sprint history."""
        # FIXED: Cast the return value to the expected type
        result = self.load_json(self.FILENAME, default=[])
        return cast(List[Dict[str, Any]], result)

    def save(self, sprints: List[Dict[str, Any]]) -> None:
        """Save sprint history."""
        self.save_json(self.FILENAME, sprints)

    def add_sprint(self, sprint_data: Dict[str, Any]) -> None:
        """Add a new sprint."""
        sprints = self.load()
        sprint_data["created_date"] = datetime.now().isoformat()
        sprint_data["sprint_id"] = sprint_data.get("sprint_id", f"sprint_{len(sprints) + 1}")
        sprints.append(sprint_data)
        self.save(sprints)

    def get_active_sprint(self) -> Optional[Dict[str, Any]]:
        """Get the current active sprint."""
        sprints = self.load()
        for sprint in reversed(sprints):
            if sprint.get("status") == "active":
                return sprint
        return None

    def complete_sprint(self, sprint_id: str, results: Dict[str, Any]) -> None:
        """Mark a sprint as completed."""
        sprints = self.load()
        for sprint in sprints:
            if sprint.get("sprint_id") == sprint_id:
                sprint["status"] = "completed"
                sprint["completed_date"] = datetime.now().isoformat()
                sprint["results"] = results
                break
        self.save(sprints)


class WorkflowStateLoader(DataLoader):
    """Specialized loader for workflow state data."""

    FILENAME = "workflow_state.json"

    def load(self) -> Dict[str, Any]:
        """Load workflow state."""
        # FIXED: Cast the return value to the expected type
        result = self.load_json(
            self.FILENAME,
            default={
                "current_stage": "initial",
                "completed_stages": [],
                "context": {},
                "last_updated": None,
            },
        )
        return cast(Dict[str, Any], result)

    def save(self, state: Dict[str, Any]) -> None:
        """Save workflow state."""
        state["last_updated"] = datetime.now().isoformat()
        self.save_json(self.FILENAME, state)

    def update_stage(self, stage: str, context: Dict[str, Any]) -> None:
        """Update the current workflow stage."""
        state = self.load()
        if state["current_stage"] not in state["completed_stages"]:
            state["completed_stages"].append(state["current_stage"])
        state["current_stage"] = stage
        state["context"].update(context)
        self.save(state)

    def reset(self) -> None:
        """Reset workflow state."""
        self.save(
            {
                "current_stage": "initial",
                "completed_stages": [],
                "context": {},
                "last_updated": datetime.now().isoformat(),
            }
        )


class SkillTestsLoader(DataLoader):
    """Specialized loader for skill tests data."""

    FILENAME = "skill_tests.json"

    def load(self) -> Dict[str, Any]:
        """Load skill tests."""
        # FIXED: Cast the return value to the expected type
        result = self.load_json(self.FILENAME, default={"tests": [], "results": []})
        return cast(Dict[str, Any], result)

    def save(self, tests_data: Dict[str, Any]) -> None:
        """Save skill tests."""
        self.save_json(self.FILENAME, tests_data)

    def add_test(self, test: Dict[str, Any]) -> None:
        """Add a new skill test."""
        tests_data = self.load()
        test["created_date"] = datetime.now().isoformat()
        test["test_id"] = test.get("test_id", f"test_{len(tests_data['tests']) + 1}")
        tests_data["tests"].append(test)
        self.save(tests_data)

    def add_result(self, result: Dict[str, Any]) -> None:
        """Add a test result."""
        tests_data = self.load()
        result["completed_date"] = datetime.now().isoformat()
        tests_data["results"].append(result)
        self.save(tests_data)


# Convenience functions
def get_loader(loader_type: str = "general", data_dir: str = "job_search_data") -> DataLoader:
    """
    Factory function to get appropriate loader.

    Args:
        loader_type: Type of loader (general, skillset, jobs, learning, sprint, workflow, tests)
        data_dir: Data directory path

    Returns:
        Appropriate DataLoader instance
    """
    loaders = {
        "general": DataLoader,
        "skillset": MasterSkillsetLoader,
        "jobs": JobAnalysisLoader,
        "learning": LearningProgressLoader,
        "sprint": SprintHistoryLoader,
        "workflow": WorkflowStateLoader,
        "tests": SkillTestsLoader,
    }

    loader_class = loaders.get(loader_type, DataLoader)
    return loader_class(data_dir)


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example: Load and save skillset
    skillset_loader = MasterSkillsetLoader()
    skillset_loader.add_skill(
        "Python",
        {"level": "advanced", "years_experience": 5, "projects": ["web scraping", "data analysis"]},
    )

    # Example: Load analyzed jobs
    jobs_loader = JobAnalysisLoader()
    recent_jobs = jobs_loader.get_recent_jobs(limit=3)
    print(f"Recent jobs: {len(recent_jobs)}")
