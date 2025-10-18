#!/usr/bin/env python3
"""
Job Analysis Script for GitHub Actions
Run: python3 scripts/run_analysis.py
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.python_advanced_job_engine import AdvancedJobEngine
import json
from datetime import datetime


def main():
    """Main analysis function"""
    
    # Get configuration from environment
    cv_file = os.environ.get("CV_FILE", "data/my_cv.txt")
    job_file = os.environ.get("JOB_FILE", "data/target_job.txt")
    job_title = os.environ.get("JOB_TITLE", "Target Role")
    company_name = os.environ.get("COMPANY_NAME", "Target Company")
    generate_materials = os.environ.get("GENERATE_MATERIALS", "true").lower() == "true"
    
    print("=" * 70)
    print("JOB ANALYSIS ENGINE")
    print("=" * 70)
    print(f"CV File: {cv_file}")
    print(f"Job File: {job_file}")
    print(f"Job Title: {job_title}")
    print(f"Company: {company_name}")
    print(f"Generate Materials: {generate_materials}")
    print()
    
    # Verify files exist
    if not Path(cv_file).exists():
        print(f"ERROR: CV file not found: {cv_file}")
        return 1
    
    if not Path(job_file).exists():
        print(f"ERROR: Job file not found: {job_file}")
        return 1
    
    # Initialize engine
    print("Initializing engine...")
    engine = AdvancedJobEngine()
    
    # Run analysis
    print("\n📊 Analyzing job match...")
    try:
        analysis = engine.analyze_from_files(
            cv_file=cv_file,
            job_file=job_file,
            job_title=job_title if job_title != "Target Role" else None,
            company=company_name if company_name != "Target Company" else None
        )
        
        # Validate analysis structure
        if not analysis or not isinstance(analysis, dict):
            print("ERROR: Analysis returned invalid data")
            return 1
        
        if "score" not in analysis:
            print("ERROR: Analysis missing 'score' key")
            print(f"Available keys: {list(analysis.keys())}")
            return 1
        
        if "job_id" not in analysis:
            print("ERROR: Analysis missing 'job_id' key")
            return 1
        
    except TypeError as e:
        print(f"ERROR: Type error in analysis: {e}")
        print("\nThis usually means:")
        print("  1. CV or job description is too short/empty")
        print("  2. Required fields missing in documents")
        print("  3. Engine configuration issue")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"ERROR: Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    score = analysis["score"]["total_score"]
    job_id = analysis["job_id"]
    
    print(f"\n✅ Analysis complete!")
    print(f"   Match Score: {score}%")
    print(f"   Job ID: {job_id}")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save core outputs
    print("\n💾 Saving outputs...")
    
    outputs = {
        "match_score.json": analysis["score"],
        "gap_analysis.json": analysis["gaps"],
        "full_analysis.json": analysis,
    }
    
    for filename, data in outputs.items():
        with open(output_dir / filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"   ✅ {filename}")
    
    # Generate learning plan
    print("\n📚 Creating learning plan...")
    try:
        learning_plan = engine.create_learning_plan(analysis, mode="standard")
        with open(output_dir / "learning_plan.json", "w") as f:
            json.dump(learning_plan, f, indent=2)
        print("   ✅ learning_plan.json")
    except Exception as e:
        print(f"   ⚠️  Learning plan error: {e}")
        learning_plan = {}
    
    # Generate improvement strategy
    print("\n🎯 Creating improvement strategy...")
    try:
        strategy = engine.create_improvement_strategy(analysis, learning_plan)
        with open(output_dir / "strategy.md", "w") as f:
            f.write(strategy)
        print("   ✅ strategy.md")
    except Exception as e:
        print(f"   ⚠️  Strategy error: {e}")
        strategy = ""
    
    # Generate application materials
    if generate_materials:
        print("\n✉️  Generating application materials...")
        try:
            letters = engine.generate_recruiter_letter(analysis, learning_plan)
            for letter_type, content in letters.items():
                with open(output_dir / f"{letter_type}.txt", "w") as f:
                    f.write(content)
                print(f"   ✅ {letter_type}.txt")
        except Exception as e:
            print(f"   ⚠️  Letters error: {e}")
    
    # Generate skill tests
    print("\n🧪 Creating skill tests...")
    try:
        missing_skills = analysis["gaps"]["missing_required_skills"][:10]
        tests = engine.generate_skill_tests(missing_skills)
        with open(output_dir / "skill_tests.json", "w") as f:
            json.dump(tests, f, indent=2)
        print(f"   ✅ skill_tests.json ({len(missing_skills)} skills)")
    except Exception as e:
        print(f"   ⚠️  Tests error: {e}")
    
    # Generate complete report
    print("\n📄 Generating report...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = [
        "# Job Match Analysis Report",
        "",
        f"**Generated:** {timestamp}",
        f"**Job ID:** {job_id}",
        f"**CV:** {cv_file}",
        f"**Job:** {job_file}",
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
    
    # Missing required skills
    missing_req = analysis["gaps"]["missing_required_skills"]
    report_lines.append(f"### Missing Required Skills ({len(missing_req)})")
    for skill in missing_req[:15]:
        report_lines.append(f"- {skill}")
    if len(missing_req) > 15:
        report_lines.append(f"\n... and {len(missing_req) - 15} more")
    
    report_lines.append("")
    
    # Missing preferred skills
    missing_pref = analysis["gaps"]["missing_preferred_skills"]
    report_lines.append(f"### Missing Preferred Skills ({len(missing_pref)})")
    for skill in missing_pref[:10]:
        report_lines.append(f"- {skill}")
    if len(missing_pref) > 10:
        report_lines.append(f"\n... and {len(missing_pref) - 10} more")
    
    # Experience and education gaps
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
    
    # Add recommendation based on score
    if score >= 75:
        report_lines.append("✅ **STRONG CANDIDATE** - Apply now!")
        report_lines.append("")
        report_lines.append("You have a strong match for this position. Your skills and experience align well with the requirements.")
    elif score >= 60:
        report_lines.append("⚠️  **NEEDS IMPROVEMENT** - Improve for 4-8 weeks")
        report_lines.append("")
        report_lines.append("You're close to being a strong candidate. Focus on the missing required skills for 4-8 weeks before applying.")
    else:
        report_lines.append("❌ **MAJOR GAPS** - Skill development needed (12-24 weeks)")
        report_lines.append("")
        report_lines.append("Significant skill gaps exist. Plan for 12-24 weeks of focused learning before applying.")
    
    # Write report
    report = "\n".join(report_lines)
    with open(output_dir / "complete_report.md", "w") as f:
        f.write(report)
    print("   ✅ complete_report.md")
    
    # Generate summary
    status = "success" if score >= 75 else "needs_improvement"
    status_text = "✅ STRONG CANDIDATE" if score >= 75 else "⚠️  NEEDS IMPROVEMENT"
    
    if score >= 75:
        action_text = "Apply now!"
    elif score >= 60:
        action_text = "Improve for 4-8 weeks"
    else:
        action_text = "Improve for 12-24 weeks"
    
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
        "  ✅ complete_report.md",
        "  ✅ match_score.json",
        "  ✅ gap_analysis.json",
        "  ✅ full_analysis.json",
        "  ✅ learning_plan.json",
        "  ✅ strategy.md",
        "  ✅ skill_tests.json"
    ]
    
    if generate_materials:
        summary_lines.extend([
            "  ✅ cover_letter.txt",
            "  ✅ linkedin_message.txt",
            "  ✅ followup_email.txt",
            "  ✅ networking_email.txt"
        ])
    
    summary = "\n".join(summary_lines)
    with open(output_dir / "summary.txt", "w") as f:
        f.write(summary)
    print("   ✅ summary.txt")
    
    # Final output
    print("\n" + "=" * 70)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"📊 Match Score: {score}%")
    print(f"🆔 Job ID: {job_id}")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print("=" * 70)
    
    # Write GitHub Actions outputs (if running in Actions)
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"score={score}\n")
            f.write(f"job_id={job_id}\n")
            f.write(f"status={status}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
