"""
Progress Tracking Demo
---------------------
Demonstrates sprint management, progress tracking,
and state persistence for a candidate’s learning plan.
"""

from src.tracking import sprint_manager, progress_tracker, state_manager

def main():
    # Initialize Sprint Manager
    sprint = sprint_manager.SprintManager(sprint_name="October Sprint", duration_days=14)

    # Add sample tasks
    sprint.add_task("Complete Python advanced course")
    sprint.add_task("Build a portfolio project")
    sprint.add_task("Learn TensorFlow basics")

    # Track progress
    tracker = progress_tracker.ProgressTracker(sprint)
    tracker.mark_task_complete("Complete Python advanced course")

    # Save state
    state = state_manager.StateManager()
    state.save_progress(tracker.get_status())

    # Print progress summary
    print("Sprint Name:", sprint.sprint_name)
    print("Tasks Completed:", tracker.completed_tasks)
    print("Tasks Pending:", tracker.pending_tasks)
    print("Saved State:", state.load_progress())

if __name__ == "__main__":
    main()
