#!/bin/bash
# Quick analysis script

CV_FILE="${1:-data/my_cv.pdf}"
JOB_FILE="${2:-data/target_job.pdf}"

echo "🎯 Running job analysis..."
echo "CV: $CV_FILE"
echo "Job: $JOB_FILE"
echo ""

python3 << EOF
from src.python_advanced_job_engine import AdvancedJobEngine

engine = AdvancedJobEngine()

print("📊 Analyzing match...")
analysis = engine.analyze_from_files(
    cv_file="$CV_FILE",
    job_file="$JOB_FILE"
)

print(f"\n{'='*60}")
print(f"MATCH SCORE: {analysis['score']['total_score']}%")
print(f"{'='*60}")

print(f"\nMissing Skills: {len(analysis['gaps']['missing_required_skills'])}")
for skill in analysis['gaps']['missing_required_skills'][:5]:
    print(f"  ❌ {skill}")

print(f"\nExperience Gap: {analysis['gaps']['experience_gap']} years")

print(f"\n{'='*60}")
print("Creating learning plan...")
plan = engine.create_learning_plan(analysis)
print(f"✅ {plan['estimated_duration']} plan created")

print("\nExporting results...")
result = engine.export_all(analysis['job_id'])
print(result)

print(f"\n{'='*60}")
print("✅ Analysis complete!")
print(f"{'='*60}")
EOF
