#!/usr/bin/env python3
"""
Automation Example - GitHub Actions Integration
Demonstrates how to use the Advanced Job Engine with GitHub Actions automation
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml


class GitHubActionsAutomation:
    """Automate job analysis workflow with GitHub Actions"""

    def __init__(self, workspace_path: str = None):
        self.workspace = Path(workspace_path or os.getenv("GITHUB_WORKSPACE", "."))
        self.output_dir = self.workspace / "job_search_data" / "automation_runs"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_automated_analysis(
        self, cv_path: str, job_path: str, config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Run complete automated analysis

        Args:
            cv_path: Path to CV file
            job_path: Path to job description
            config: Configuration options

        Returns:
            Analysis results dictionary
        """
        print("🤖 Starting Automated Job Analysis...")
        print(f"📄 CV: {cv_path}")
        print(f"💼 Job: {job_path}")

        config = config or {}

        # Load files
        cv_data = self._load_file(cv_path)
        job_data = self._load_file(job_path)

        # Parse and analyze
        candidate = self._parse_cv(cv_data)
        job_desc = self._parse_job(job_data)

        # Calculate match
        match_results = self._calculate_match(candidate, job_desc)

        # Generate outputs
        report = self._generate_report(match_results)
        learning_plan = self._generate_learning_plan(match_results)
        application_materials = self._generate_application_materials(match_results)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = f"run_{timestamp}"

        results = {
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "match_score": match_results["overall_score"],
            "recommendation": match_results["recommendation"],
            "report_path": str(self.output_dir / f"{run_id}_report.md"),
            "learning_plan_path": str(self.output_dir / f"{run_id}_learning_plan.json"),
            "cover_letter_path": str(self.output_dir / f"{run_id}_cover_letter.txt"),
        }

        # Save all outputs
        self._save_output(results["report_path"], report)
        self._save_output(results["learning_plan_path"], json.dumps(learning_plan, indent=2))
        self._save_output(results["cover_letter_path"], application_materials["cover_letter"])

        # Set GitHub Actions outputs
        self._set_github_output("match_score", match_results["overall_score"])
        self._set_github_output("recommendation", match_results["recommendation"])
        self._set_github_output("report_path", results["report_path"])

        print("\n✅ Analysis Complete!")
        print(f"📊 Match Score: {match_results['overall_score']}%")
        print(f"💡 Recommendation: {match_results['recommendation']}")
        print(f"📁 Results saved to: {self.output_dir / run_id}")

        return results

    def schedule_analysis(self, cron_schedule: str = "0 9 * * 1"):
        """
        Generate GitHub Actions workflow for scheduled analysis

        Args:
            cron_schedule: Cron expression (default: Monday 9am)
        """
        workflow = {
            "name": "Scheduled Job Analysis",
            "on": {"schedule": [{"cron": cron_schedule}], "workflow_dispatch": {}},
            "jobs": {
                "analyze": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v3"},
                        {
                            "name": "Set up Python",
                            "uses": "actions/setup-python@v4",
                            "with": {"python-version": "3.9"},
                        },
                        {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
                        {"name": "Run analysis", "run": "python examples/automation_example.py"},
                        {
                            "name": "Upload results",
                            "uses": "actions/upload-artifact@v3",
                            "with": {
                                "name": "analysis-results",
                                "path": "job_search_data/automation_runs/",
                            },
                        },
                        {
                            "name": "Send notification",
                            "run": "python scripts/send_notification.py",
                            "env": {
                                "EMAIL": "${{ secrets.EMAIL }}",
                                "MATCH_SCORE": "${{ steps.analysis.outputs.match_score }}",
                            },
                        },
                    ],
                }
            },
        }

        workflow_path = self.workspace / ".github" / "workflows" / "scheduled-analysis.yml"
        workflow_path.parent.mkdir(parents=True, exist_ok=True)

        with open(workflow_path, "w") as f:
            yaml.dump(workflow, f, default_flow_style=False)

        print(f"✅ Workflow created: {workflow_path}")
        return workflow_path

    def setup_notifications(self, email: str = None, slack_webhook: str = None):
        """Configure notification settings"""
        config = {
            "notifications": {
                "enabled": True,
                "email": email or os.getenv("NOTIFICATION_EMAIL"),
                "slack_webhook": slack_webhook or os.getenv("SLACK_WEBHOOK"),
                "notify_on": ["high_match", "new_opportunities", "learning_milestone"],
            }
        }

        config_path = self.workspace / "job_search_data" / "notification_config.json"
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"✅ Notifications configured: {config_path}")
        return config

    def batch_analyze_jobs(self, jobs_dir: str, cv_path: str) -> List[Dict[str, Any]]:
        """
        Analyze multiple job postings in batch

        Args:
            jobs_dir: Directory containing job description files
            cv_path: Path to CV file

        Returns:
            List of analysis results sorted by match score
        """
        print("📄 Starting batch analysis...")

        jobs_path = Path(jobs_dir)
        job_files = list(jobs_path.glob("*.txt")) + list(jobs_path.glob("*.pdf"))

        results = []
        for i, job_file in enumerate(job_files, 1):
            print(f"\n📋 Analyzing job {i}/{len(job_files)}: {job_file.name}")

            try:
                result = self.run_automated_analysis(cv_path, str(job_file))
                result["job_file"] = job_file.name
                results.append(result)
            except Exception as e:
                print(f"❌ Error analyzing {job_file.name}: {e}")
                continue

        # Sort by match score
        results.sort(key=lambda x: x["match_score"], reverse=True)

        # Save summary
        summary_path = self.output_dir / "batch_summary.json"
        with open(summary_path, "w") as f:
            json.dump(results, f, indent=2)

        print("\n✅ Batch analysis complete!")
        print(f"📊 Analyzed {len(results)} jobs")
        print(f"🥇 Top match: {results[0]['job_file']} ({results[0]['match_score']}%)")

        return results

    def _load_file(self, path: str) -> str:
        """Load file content"""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _parse_cv(self, cv_text: str) -> Dict[str, Any]:
        """Parse CV (simplified for example)"""
        return {
            "name": "Alex Johnson",
            "experience_years": 8.3,
            "skills": ["Python", "Kubernetes", "AWS", "Docker", "PostgreSQL"],
            "certifications": ["AWS SA", "CKA", "Docker"],
        }

    def _parse_job(self, job_text: str) -> Dict[str, Any]:
        """Parse job description (simplified for example)"""
        return {
            "title": "Staff Backend Engineer",
            "company": "CloudNative Systems",
            "required_skills": ["Python", "Go", "Kubernetes", "AWS"],
            "experience_required": 8,
        }

    def _calculate_match(self, candidate: Dict, job: Dict) -> Dict[str, Any]:
        """Calculate match score (simplified for example)"""
        # Simplified matching logic
        required_skills = set(job["required_skills"])
        candidate_skills = set(candidate["skills"])

        matched_skills = required_skills & candidate_skills
        skill_coverage = len(matched_skills) / len(required_skills) * 100

        overall_score = min(skill_coverage, 100)

        if overall_score >= 85:
            recommendation = "Excellent Match - Apply Now"
        elif overall_score >= 70:
            recommendation = "Good Match - Apply with Confidence"
        else:
            recommendation = "Fair Match - Consider Upskilling"

        return {
            "overall_score": round(overall_score, 1),
            "recommendation": recommendation,
            "matched_skills": list(matched_skills),
            "missing_skills": list(required_skills - candidate_skills),
            "candidate": candidate,
            "job": job,
        }

    def _generate_report(self, match_results: Dict) -> str:
        """Generate markdown report"""
        report = f"""# Job Analysis Report

## Match Score: {match_results['overall_score']}%

**Recommendation:** {match_results['recommendation']}

### Matched Skills
{chr(10).join(f"- {skill}" for skill in match_results['matched_skills'])}

### Skills to Develop
{chr(10).join(f"- {skill}" for skill in match_results['missing_skills'])}

### Next Steps
1. Review the learning plan
2. Update your resume
3. Prepare application materials
4. Apply with confidence

---
*Generated by Advanced Job Engine - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return report

    def _generate_learning_plan(self, match_results: Dict) -> Dict[str, Any]:
        """Generate learning plan"""
        return {
            "missing_skills": match_results["missing_skills"],
            "sprints": [
                {
                    "sprint": 1,
                    "duration_weeks": 2,
                    "skills": (
                        match_results["missing_skills"][:2]
                        if match_results["missing_skills"]
                        else []
                    ),
                    "hours": 40,
                }
            ],
        }

    def _generate_application_materials(self, match_results: Dict) -> Dict[str, str]:
        """Generate application materials"""
        return {
            "cover_letter": f"""Dear Hiring Manager,

I am excited to apply for the {match_results['job']['title']} position at {match_results['job']['company']}.

With {match_results['candidate']['experience_years']} years of experience and expertise in {', '.join(match_results['matched_skills'])}, I believe I would be a strong addition to your team.

Best regards,
{match_results['candidate']['name']}
"""
        }

    def _save_output(self, path: str, content: str):
        """Save output to file"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def _set_github_output(self, name: str, value: Any):
        """Set GitHub Actions output"""
        github_output = os.getenv("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"{name}={value}\n")


def main():
    """Main automation workflow"""
    automation = GitHubActionsAutomation()

    # Example 1: Single job analysis
    print("=" * 60)
    print("EXAMPLE 1: Single Job Analysis")
    print("=" * 60)

    cv_path = "data/my_cv.pdf"
    job_path = "data/target_job.pdf"
    if os.path.exists(cv_path) and os.path.exists(job_path):
        results = automation.run_automated_analysis(cv_path, job_path)
        print(f"\n📊 Results: {json.dumps(results, indent=2)}")
    else:
        print("⚠️  Sample files not found. Skipping single analysis.")

    # Example 2: Setup scheduled workflow
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Setup Scheduled Workflow")
    print("=" * 60)

    workflow_path = automation.schedule_analysis(cron_schedule="0 9 * * MON")
    print("✅ Workflow configured for weekly Monday 9am analysis:", workflow_path)

    # Example 3: Configure notifications
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Configure Notifications")
    print("=" * 60)

    config = automation.setup_notifications(
        email="your-email@example.com",
        slack_webhook="https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
    )
    print(f"✅ Notifications: {json.dumps(config, indent=2)}")

    # Example 4: Batch analysis
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Batch Job Analysis")
    print("=" * 60)

    jobs_dir = "data/jobs"
    if os.path.exists(jobs_dir):
        batch_results = automation.batch_analyze_jobs(jobs_dir, cv_path)
        print("\n📊 Top 3 matches:")
        for i, result in enumerate(batch_results[:3], 1):
            print(f"{i}. {result['job_file']} - {result['match_score']}%")
    else:
        print("⚠️  Jobs directory not found. Skipping batch analysis.")

    print("\n" + "=" * 60)
    print("✅ Automation Examples Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
