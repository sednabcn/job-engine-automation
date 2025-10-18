#!/usr/bin/env python3
"""
Job Analysis Script for GitHub Actions
Reads environment variables and runs analysis
"""

import sys
import os
sys.path.insert(0, "src")

from python_advanced_job_engine import AdvancedJobEngine
import json
from datetime import datetime
from pathlib import Path

def main():
    # Get configuration from environment
    cv_file = os.environ.get("CV_FILE")
    job_file = os.environ.get("JOB_FILE")
    job_title = os.environ.get("JOB_TITLE", "Target Role")
    company_name = os.environ.get("COMPANY_NAME", "Target Company")
    generate_materials = os.environ.get("GENERATE_MATERIALS", "true").lower() == "true"
    
    print("=" * 70)
    print("JOB ANALYSIS ENGINE")
    print("=" * 70)
    print(f"CV: {cv_file}")
    print(f"Job: {job_file}")
    print(f"Title: {job_title}")
    print(f"Company: {company_name}")
    print(f"Generate Materials: {generate_materials}")
    print()
    
    # Initialize engine
    engine = AdvancedJobEngine()
    
    # Run analysis
    print("Running analysis...")
    try:
        analysis = engine.analyze_from_files(
            cv_file=cv_file,
            job_file=job_file,
            job_title=job_title if job_title != "Target Role" else None,
            company=company_name if company_name != "Target Company" else None
        )
    except Exception as e:
        print(f"ERROR: Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    score = analysis["score"]["total_score"]
    job_id = analysis["job_id"]
    
    print(f"\nMatch Score: {score}%")
    print(f"Job ID: {job_id}")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save outputs
    print("\nSaving outputs...")
    
    with open(output_dir / "match_score.json", "w") as f:
        json.dump(analysis["score"], f, indent=2)
    print("  ✅ match_score.json")
    
    with open(output_dir / "gap_analysis.json", "w") as f:
        json.dump(analysis["gaps"], f, indent=2)
    print("  ✅ gap_analysis.json")
    
    with open(output_dir / "full_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    print("  ✅ full_analysis.json")
    
    # Learning plan
    print("\nCreating learning plan...")
    learning_plan = engine.create_learning_plan(analysis, mode="standard")
    with open(output_dir / "learning_plan.json", "w") as f:
        json.dump(learning_plan, f, indent=2)
    print("  ✅ learning_plan.json")
    
    # Strategy
    print("\nCreating strategy...")
    strategy = engine.create_improvement_strategy(analysis, learning_plan)
    with open(output_dir / "strategy.md", "w") as f:
        f.write(strategy)
    print("  ✅ strategy.md")
    
    # Application materials
    if generate_materials:
        print("\nGenerating application materials...")
        letters = engine.generate_recruiter_letter(analysis, learning_plan)
        for letter_type, content in letters.items():
            with open(output_dir / f"{letter_type}.txt", "w") as f:
                f.write(content)
            print(f"  ✅ {letter_type}.txt")
    
    # Skill tests
    print("\nGenerating skill tests...")
    missing_skills = analysis["gaps"]["missing_required_skills"][:10]
    tests = engine.generate_skill_tests(missing_skills)
    with open(output_dir / "skill_tests.json", "w") as f:
        json.dump(tests, f, indent=2)
    print("  ✅ skill_tests.json")
    
    # Generate complete report
    print("\nGenerating report...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = [
        "# Job Match Analysis Report",
        "",
        f"**Generated:** {timestamp}",
        f"**Job ID:** {job_id}",
        "",
        "---",
        "",
        f"## Match Score: {score}%",
        "",
        "### Score Breakdown"
    ]
    
    for category, cat_score in analysis["score"]["breakdown"].items():
        category_name = category.replace("_", " ").title()
        report_lines.append(f"- {category_name}: {cat_score}%")
    
    report_lines.extend([
        "",
        "---",
        "",
        "## Gap Analysis",
        ""
    ])
    
    missing_req = analysis["gaps"]["missing_required_skills"]
    report_lines.append(f"### Missing Required Skills ({len(missing_req)})")
    for skill in missing_req[:15]:
        report_lines.append(f"- {skill}")
    if len(missing_req) > 15:
        report_lines.append(f"\n... and {len(missing_req) - 15} more")
    
    report_lines.append("")
    
    missing_pref = analysis["gaps"]["missing_preferred_skills"]
    report_lines.append(f"### Missing Preferred Skills ({len(missing_pref)})")
    for skill in missing_pref[:10]:
        report_lines.append(f"- {skill}")
    
    exp_gap = analysis["gaps"]["experience_gap"]
    edu_gap = analysis["gaps"]["education_gap"]
    report_lines.extend([
        "",
        f"### Experience Gap: {exp_gap} years",
        f"### Education Gap: {edu_gap}",
        "",
        "---",
        "",
        "## Recommendation",
        ""
    ])
    
    if score >= 75:
        report_lines.append("✅ **STRONG CANDIDATE** - Apply now!")
    elif score >= 60:
        report_lines.append("⚠️  **NEEDS IMPROVEMENT** - Improve for 4-8 weeks")
    else:
        report_lines.append("❌ **MAJOR GAPS** - Skill development needed (12-24 weeks)")
    
    report = "\n".join(report_lines)
    with open(output_dir / "complete_report.md", "w") as f:
        f.write(report)
    print("  ✅ complete_report.md")
    
    # Generate summary
    status = "success" if score >= 75 else "needs_improvement"
    status_text = "STRONG CANDIDATE" if score >= 75 else "NEEDS IMPROVEMENT"
    
    weeks_min = 4 if score >= 60 else 12
    weeks_max = 8 if score >= 60 else 24
    action_text = "Apply now!" if score >= 75 else f"Improve for {weeks_min}-{weeks_max} weeks"
    
    summary_lines = [
        "ANALYSIS SUMMARY",
        "",
        f"Job ID: {job_id}",
        f"Match Score: {score}%",
        f"Status: {status_text}",
        "",
        f"Action: {action_text}",
        "",
        "Files generated:",
        "  - complete_report.md",
        "  - match_score.json",
        "  - gap_analysis.json",
        "  - full_analysis.json",
        "  - learning_plan.json",
        "  - strategy.md",
        "  - skill_tests.json"
    ]
    
    if generate_materials:
        summary_lines.extend([
            "  - cover_letter.txt",
            "  - linkedin_message.txt",
            "  - followup_email.txt",
            "  - networking_email.txt"
        ])
    
    summary = "\n".join(summary_lines)
    with open(output_dir / "summary.txt", "w") as f:
        f.write(summary)
    print("  ✅ summary.txt")
    
    print("\n" + "=" * 70)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 70)
    
    # Write GitHub outputs
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"score={score}\n")
            f.write(f"job_id={job_id}\n")
            f.write(f"status={status}\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
