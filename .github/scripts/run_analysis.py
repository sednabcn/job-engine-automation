#!/usr/bin/env python3
"""
Main analysis script for GitHub Actions
Runs CV vs Job analysis and generates output

Location: .github/scripts/run_analysis.py
"""

import sys
import os
from pathlib import Path

# Calculate project root correctly for .github/scripts/ location
# __file__ = /path/to/project/.github/scripts/run_analysis.py
# .parent = /path/to/project/.github/scripts/
# .parent = /path/to/project/.github/
# .parent = /path/to/project/  ✅ CORRECT
project_root = Path(__file__).resolve().parent.parent.parent

# Add src directory to Python path
sys.path.insert(0, str(project_root / "src"))

# Verify path is correct
print(f"🔍 Project root: {project_root}")
print(f"🔍 Src path: {project_root / 'src'}")
print(f"🔍 Python path: {sys.path[0]}")

# Now import can work
try:
    from python_advanced_job_engine import AdvancedJobEngine
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print(f"📂 Current directory: {Path.cwd()}")
    print(f"📂 Contents of src/:")
    src_dir = project_root / "src"
    if src_dir.exists():
        for item in src_dir.iterdir():
            print(f"   - {item.name}")
    else:
        print(f"   ❌ src/ directory not found at {src_dir}")
    sys.exit(1)

import json


def set_github_output(name: str, value: str):
    """Set GitHub Actions output variable"""
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"::set-output name={name}::{value}")


def main():
    """Main analysis function"""
    print("=" * 80)
    print("JOB ANALYSIS - GITHUB ACTIONS")
    print("=" * 80)
    
    # Get file paths from environment
    cv_file = os.environ.get("CV_FILE", "data/my_cv.txt")
    job_file = os.environ.get("JOB_FILE", "data/target_job.txt")
    job_title = os.environ.get("JOB_TITLE", "Target Role")
    company_name = os.environ.get("COMPANY_NAME", "Target Company")
    generate_materials = os.environ.get("GENERATE_MATERIALS", "true").lower() == "true"
    
    print(f"\n📋 Configuration:")
    print(f"   CV File: {cv_file}")
    print(f"   Job File: {job_file}")
    print(f"   Job Title: {job_title}")
    print(f"   Company: {company_name}")
    print(f"   Generate Materials: {generate_materials}")
    
    # Convert to absolute paths
    cv_path = project_root / cv_file
    job_path = project_root / job_file
    
    # Verify files exist
    if not cv_path.exists():
        print(f"\n❌ Error: CV file not found: {cv_path}")
        sys.exit(1)
    
    if not job_path.exists():
        print(f"\n❌ Error: Job file not found: {job_path}")
        sys.exit(1)
    
    print(f"\n✅ Files verified")
    print(f"   CV: {cv_path.stat().st_size} bytes")
    print(f"   Job: {job_path.stat().st_size} bytes")
    
    # Initialize engine
    print(f"\n🔧 Initializing engine...")
    try:
        engine = AdvancedJobEngine()
        print("✅ Engine initialized")
    except Exception as e:
        print(f"❌ Failed to initialize engine: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Run analysis
    print(f"\n📊 Running analysis...")
    try:
        analysis = engine.analyze_from_files(
            cv_file=str(cv_path),
            job_file=str(job_path),
            job_title=job_title,
            company=company_name
        )
        print("✅ Analysis complete")
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Extract key results
    job_id = analysis.get("job_id", "unknown")
    score = analysis.get("score", {}).get("total_score", 0)
    missing_required = len(analysis.get("gaps", {}).get("missing_required_skills", []))
    missing_preferred = len(analysis.get("gaps", {}).get("missing_preferred_skills", []))
    
    print(f"\n📈 Results:")
    print(f"   Job ID: {job_id}")
    print(f"   Match Score: {score}%")
    print(f"   Missing Required Skills: {missing_required}")
    print(f"   Missing Preferred Skills: {missing_preferred}")
    
    # Determine status
    if score >= 80:
        status = "🟢 Strong Match"
    elif score >= 60:
        status = "🟡 Good Match"
    else:
        status = "🔴 Needs Development"
    
    print(f"   Status: {status}")
    
    # Set GitHub Actions outputs
    set_github_output("job_id", job_id)
    set_github_output("score", str(score))
    set_github_output("status", status)
    
    # Create output directory
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Save analysis JSON
    analysis_file = output_dir / "analysis.json"
    with open(analysis_file, "w") as f:
        json.dump(analysis, f, indent=2)
    print(f"\n💾 Saved: {analysis_file}")
    
    # Generate additional materials if requested
    if generate_materials:
        print(f"\n📝 Generating application materials...")
        
        try:
            # Learning plan
            learning_plan = engine.create_learning_plan(analysis)
            plan_file = output_dir / "learning_plan.json"
            with open(plan_file, "w") as f:
                json.dump(learning_plan, f, indent=2)
            print(f"   ✅ Learning plan: {plan_file}")
            
            # Strategy
            strategy = engine.create_improvement_strategy(analysis, learning_plan)
            strategy_file = output_dir / "strategy.json"
            with open(strategy_file, "w") as f:
                json.dump(strategy, f, indent=2)
            print(f"   ✅ Strategy: {strategy_file}")
            
            # Recruiter letters
            letters = engine.generate_recruiter_letter(analysis, learning_plan)
            
            # Save each letter type
            for letter_type, content in letters.get("templates", {}).items():
                letter_file = output_dir / f"{letter_type}.txt"
                with open(letter_file, "w") as f:
                    f.write(content)
                print(f"   ✅ {letter_type}: {letter_file}")
            
        except Exception as e:
            print(f"   ⚠️  Warning: Could not generate some materials: {e}")
            import traceback
            traceback.print_exc()
    
    # Create summary for GitHub Actions
    summary_file = output_dir / "summary.txt"
    with open(summary_file, "w") as f:
        f.write(f"### Analysis Results\n\n")
        f.write(f"**Job:** {job_title} at {company_name}\n")
        f.write(f"**Match Score:** {score}%\n")
        f.write(f"**Status:** {status}\n\n")
        
        f.write(f"### Gap Analysis\n\n")
        f.write(f"- **Missing Required Skills:** {missing_required}\n")
        
        gaps = analysis.get("gaps", {})
        if gaps.get("missing_required_skills"):
            f.write(f"\n**Skills to Learn:**\n")
            for skill in gaps["missing_required_skills"][:5]:
                f.write(f"- {skill}\n")
        
        f.write(f"\n### Recommendations\n\n")
        recommendations = analysis.get("recommendations", [])
        for rec in recommendations[:3]:
            f.write(f"- [{rec.get('priority', 'N/A')}] {rec.get('action', 'N/A')}\n")
        
        f.write(f"\n---\n")
        f.write(f"*Generated by Advanced Job Engine*\n")
    
    print(f"   ✅ Summary: {summary_file}")
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)
    
    # List all output files
    print(f"\n📂 Output files created:")
    for file in sorted(output_dir.glob("*")):
        print(f"   - {file.name}")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
