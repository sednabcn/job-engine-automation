#!/usr/bin/env python3
"""
Reverse Workflow Example - Sprint-based learning
"""

from src.python_advanced_job_engine import AdvancedJobEngine
from datetime import datetime

def main():
    print("="*80)
    print("REVERSE WORKFLOW - SPRINT-BASED LEARNING")
    print("="*80)
    
    engine = AdvancedJobEngine()
    
    # Initial analysis
    print("\n📊 Initial Analysis...")
    analysis = engine.analyze_from_files(
        cv_file="data/my_cv.pdf",
        job_file="data/target_job.pdf"
    )
    baseline = analysis['score']['total_score']
    print(f"Baseline Score: {baseline}%")
    
    # Create reverse-mode learning plan
    print("\n📚 Creating reverse-mode learning plan (16-24 weeks)...")
    plan = engine.create_learning_plan(analysis, mode="reverse")
    
    # Demonstration: Sprint 1
    print("\n" + "="*80)
    print("SPRINT 1: Foundation Building")
    print("="*80)
    
    sprint = engine.start_sprint(
        skills=["PyTorch", "Docker"],
        project_goal="Build and containerize a simple ML model"
    )
    
    print("\n📝 Simulating daily logs...")
    # Day 1
    engine.log_daily(
        hours=3.5,
        concepts=["PyTorch tensors", "Basic neural networks"],
        notes="Completed PyTorch intro tutorial"
    )
    
    # Day 2
    engine.log_daily(
        hours=4.0,
        concepts=["Docker basics", "Creating images"],
        notes="Built first Docker container"
    )
    
    # Day 3
    engine.log_daily(
        hours=3.0,
        concepts=["Training models", "Model persistence"],
        notes="Trained and saved PyTorch model"
    )
    
    print("\n🏁 Ending Sprint 1...")
    result = engine.end_sprint(
        project_url="https://github.com/user/sprint1-pytorch-docker",
        test_scores={"PyTorch": 68, "Docker": 72}
    )
    
    print(f"\nSprint Results:")
    print(f"  Skills Mastered: {result.get('skills_mastered', [])}")
    print(f"  Total Hours: {result.get('total_hours', 0)}h")
    
    # Check quality gates
    print("\n🚪 Checking quality gates...")
    gates = engine.check_quality_gates()
    
    # Display progress
    print("\n📊 Progress Dashboard:")
    engine.display_progress_dashboard()
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Continue with Sprint 2 (different skills)")
    print("2. Build progressively complex projects")
    print("3. Pass quality gates: Foundation → Competency → Mastery")
    print("4. Reach 90%+ match score")
    print("5. Professional positioning")
    print("6. Strategic applications")
    print("\n✅ Sprint-based learning in progress!")

if __name__ == "__main__":
    main()
