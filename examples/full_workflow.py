#!/usr/bin/env python3
"""
Complete Workflow Example - All 7 steps
"""

from src.python_advanced_job_engine import AdvancedJobEngine

def main():
    print("="*80)
    print("COMPLETE JOB ANALYSIS WORKFLOW")
    print("="*80)
    
    # Initialize engine
    engine = AdvancedJobEngine()
    
    # STEP 1-2: Analyze job
    print("\n📊 Step 1-2: Analyzing job match...")
    analysis = engine.analyze_from_files(
        cv_file="data/my_cv.pdf",
        job_file="data/target_job.pdf",
        job_title="Senior ML Engineer",
        company="TechCorp"
    )
    print(f"✅ Match Score: {analysis['score']['total_score']}%")
    
    # STEP 3: Learning plan
    print("\n📚 Step 3: Creating learning plan...")
    plan = engine.create_learning_plan(analysis, mode="standard")
    print(f"✅ {plan['estimated_duration']} plan created")
    print(f"   - Study: {len(plan['levels']['study'])} skills")
    print(f"   - Practice: {len(plan['levels']['practice'])} skills")
    print(f"   - Courses: {len(plan['levels']['courses'])} recommendations")
    
    # STEP 4: Improvement strategy
    print("\n🎯 Step 4: Creating improvement strategy...")
    strategy = engine.create_improvement_strategy(analysis, plan)
    print(f"✅ Strategy: {len(strategy['phases'])} phases")
    print(f"   Target: {strategy['target_score']}%")
    
    # STEP 5: Skill tests
    print("\n📝 Step 5: Generating skill tests...")
    missing_skills = analysis['gaps']['missing_required_skills'][:5]
    tests = engine.generate_skill_tests(missing_skills)
    print(f"✅ Tests created for {len(tests['skills_covered'])} skills")
    
    # STEP 6: Update skillset (simulated)
    print("\n📊 Step 6: Updating skillset...")
    new_skills = ["Docker", "Kubernetes", "AWS"]
    update = engine.update_skillset(new_skills, category="technical")
    print(f"✅ Added {len(update['updated_skills'])} skills")
    print(f"   Total skills: {update['total_skills']}")
    
    # STEP 7: Application materials
    print("\n✉️  Step 7: Generating application materials...")
    letters = engine.generate_recruiter_letter(analysis, plan)
    print(f"✅ Generated {len(letters['templates'])} templates:")
    for template_type in letters['templates'].keys():
        print(f"   - {template_type}")
    
    # Export everything
    print("\n📦 Exporting complete package...")
    result = engine.export_all(analysis['job_id'])
    print(result)
    
    print("\n" + "="*80)
    print("✅ WORKFLOW COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    main()
