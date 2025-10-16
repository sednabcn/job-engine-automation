#!/usr/bin/env python3
"""
Batch Analysis Example - Analyze multiple jobs
"""

from src.python_advanced_job_engine import AdvancedJobEngine
from pathlib import Path

def main():
    print("="*80)
    print("BATCH JOB ANALYSIS")
    print("="*80)
    
    engine = AdvancedJobEngine()
    
    # Define jobs to analyze
    jobs = [
        {
            "file": "data/job1_ml_engineer.pdf",
            "title": "Senior ML Engineer",
            "company": "TechCorp"
        },
        {
            "file": "data/job2_data_scientist.pdf",
            "title": "Data Scientist",
            "company": "DataCo"
        },
        {
            "file": "data/job3_ai_researcher.pdf",
            "title": "AI Researcher",
            "company": "ResearchLab"
        }
    ]
    
    results = []
    
    # Analyze each job
    for job in jobs:
        if not Path(job["file"]).exists():
            print(f"\n⚠️  Skipping {job['file']} (not found)")
            continue
        
        print(f"\n📊 Analyzing: {job['title']} at {job['company']}...")
        
        analysis = engine.analyze_from_files(
            cv_file="data/my_cv.pdf",
            job_file=job["file"],
            job_title=job["title"],
            company=job["company"]
        )
        
        results.append({
            "title": job["title"],
            "company": job["company"],
            "score": analysis['score']['total_score'],
            "missing_skills": len(analysis['gaps']['missing_required_skills']),
            "experience_gap": analysis['gaps']['experience_gap'],
            "job_id": analysis['job_id']
        })
        
        print(f"  ✅ Score: {analysis['score']['total_score']}%")
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Display comparison
    print("\n" + "="*80)
    print("COMPARISON RESULTS (Best to Worst)")
    print("="*80)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']} at {result['company']}")
        print(f"   Score: {result['score']}%")
        print(f"   Missing Skills: {result['missing_skills']}")
        print(f"   Experience Gap: {result['experience_gap']} years")
        
        # Recommendation
        if result['score'] >= 75:
            print(f"   💚 Recommendation: APPLY NOW")
        elif result['score'] >= 60:
            print(f"   💛 Recommendation: Quick upskilling (2-4 weeks)")
        else:
            print(f"   ❤️  Recommendation: Significant prep needed (8-12 weeks)")
    
    print("\n" + "="*80)
    print("✅ Batch analysis complete!")
    print("="*80)

if __name__ == "__main__":
    main()




