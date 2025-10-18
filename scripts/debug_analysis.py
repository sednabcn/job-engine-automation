#!/usr/bin/env python3
"""
Debug script to diagnose analysis issues
Run: python3 scripts/debug_analysis.py
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, "src")

from python_advanced_job_engine import AdvancedJobEngine
import json


def test_file_reading(engine, filepath):
    """Test if a file can be read"""
    print(f"\n{'='*60}")
    print(f"Testing: {filepath}")
    print('='*60)
    
    path = Path(filepath)
    
    # Check existence
    if not path.exists():
        print("❌ File does not exist")
        return False
    
    print(f"✅ File exists")
    print(f"   Size: {path.stat().st_size:,} bytes")
    
    # Check if empty
    if path.stat().st_size == 0:
        print("❌ File is empty (0 bytes)")
        return False
    
    # Try to read
    try:
        text = engine.read_document(str(filepath))
        words = len(text.split())
        lines = len(text.split('\n'))
        
        print(f"✅ File readable")
        print(f"   Words: {words:,}")
        print(f"   Lines: {lines:,}")
        print(f"   First 200 chars:")
        print(f"   {text[:200]}")
        
        if words < 50:
            print("⚠️  Warning: Very short document (< 50 words)")
        
        return True
        
    except Exception as e:
        print(f"❌ Cannot read file: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_analysis(engine, cv_file, job_file):
    """Test the analysis process step by step"""
    print(f"\n{'='*60}")
    print("Testing Analysis Process")
    print('='*60)
    
    try:
        # Step 1: Read CV
        print("\n1️⃣ Reading CV...")
        cv_text = engine.read_document(cv_file)
        print(f"   ✅ CV text: {len(cv_text)} chars, {len(cv_text.split())} words")
        
        # Step 2: Read Job
        print("\n2️⃣ Reading Job Description...")
        job_text = engine.read_document(job_file)
        print(f"   ✅ Job text: {len(job_text)} chars, {len(job_text.split())} words")
        
        # Step 3: Parse CV (using actual method)
        print("\n3️⃣ Parsing CV...")
        cv_data = engine.parse_cv(cv_text)
        print(f"   ✅ Parsed CV:")
        print(f"      Skills found: {sum(len(skills) for skills in cv_data['skills'].values())}")
        for category, skills in cv_data['skills'].items():
            if skills:
                print(f"      - {category}: {', '.join(skills[:3])}")
        print(f"      Experience: {cv_data['experience_years']} years")
        print(f"      Education: {', '.join(cv_data['education']) if cv_data['education'] else 'None'}")
        
        # Step 4: Parse Job (using actual method)
        print("\n4️⃣ Parsing Job Description...")
        job_data = engine.parse_job(job_text, "Target Job", "Target Company")
        print(f"   ✅ Parsed Job:")
        print(f"      Job ID: {job_data['id']}")
        print(f"      Required skills: {len(job_data['required_skills'])}")
        if job_data['required_skills']:
            print(f"         → {', '.join(job_data['required_skills'][:5])}")
        print(f"      Preferred skills: {len(job_data['preferred_skills'])}")
        if job_data['preferred_skills']:
            print(f"         → {', '.join(job_data['preferred_skills'][:5])}")
        print(f"      Required experience: {job_data['required_experience']} years")
        
        # Step 5: Full analysis
        print("\n5️⃣ Running full analysis...")
        analysis = engine.analyze_from_files(
            cv_file=cv_file,
            job_file=job_file
        )
        
        print(f"   ✅ Analysis complete")
        print(f"\n📊 Results:")
        print(f"   Job ID: {analysis.get('job_id', 'N/A')}")
        
        # Check score structure
        score_obj = analysis.get('score')
        if score_obj:
            print(f"   Score object type: {type(score_obj)}")
            print(f"   Score keys: {list(score_obj.keys())}")
            
            total = score_obj.get('total_score')
            print(f"   Total score: {total}")
            print(f"   Total score type: {type(total)}")
            
            if total is None:
                print("\n❌ ERROR: total_score is None!")
                print("   Full score object:")
                print(f"   {json.dumps(score_obj, indent=4)}")
                
                print("\n   Breakdown:")
                breakdown = score_obj.get('category_scores', {})
                for key, val in breakdown.items():
                    print(f"      {key}: {val} (type: {type(val)})")
                
                return False
            else:
                print(f"   ✅ Score: {total}%")
                
                # Show breakdown
                print(f"\n   📋 Category Breakdown:")
                for category, score in score_obj.get('category_scores', {}).items():
                    print(f"      {category}: {score:.1f}%")
        else:
            print("   ❌ No score object")
            return False
        
        # Check gaps
        gaps = analysis.get('gaps', {})
        print(f"\n   🔍 Gap Analysis:")
        print(f"      Missing required: {len(gaps.get('missing_required_skills', []))}")
        if gaps.get('missing_required_skills'):
            print(f"         → {', '.join(gaps['missing_required_skills'][:5])}")
        print(f"      Missing preferred: {len(gaps.get('missing_preferred_skills', []))}")
        if gaps.get('missing_preferred_skills'):
            print(f"         → {', '.join(gaps['missing_preferred_skills'][:3])}")
        
        # Check recommendations
        recommendations = analysis.get('recommendations', [])
        print(f"\n   💡 Recommendations: {len(recommendations)}")
        for rec in recommendations[:2]:
            print(f"      [{rec.get('priority', 'N/A')}] {rec.get('action', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main diagnostic function"""
    print("="*60)
    print("JOB ANALYSIS DEBUGGER")
    print("="*60)
    
    # Get files
    cv_file = os.environ.get("CV_FILE", "data/my_cv.txt")
    job_file = os.environ.get("JOB_FILE", "data/target_job.txt")
    
    print(f"\nConfiguration:")
    print(f"  CV: {cv_file}")
    print(f"  Job: {job_file}")
    
    # Initialize engine
    print(f"\n{'='*60}")
    print("Initializing Engine")
    print('='*60)
    
    try:
        engine = AdvancedJobEngine()
        print("✅ Engine initialized")
        print(f"   Data directory: {engine.data_dir}")
    except Exception as e:
        print(f"❌ Cannot initialize engine: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Test files
    cv_ok = test_file_reading(engine, cv_file)
    job_ok = test_file_reading(engine, job_file)
    
    if not cv_ok or not job_ok:
        print("\n❌ File reading failed - cannot proceed with analysis")
        return 1
    
    # Test analysis
    analysis_ok = test_analysis(engine, cv_file, job_file)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    
    if cv_ok and job_ok and analysis_ok:
        print("✅ All tests passed!")
        print("\n✨ Your setup is working correctly.")
        print("\n🎯 Next steps:")
        print("  1. Run: python3 scripts/run_analysis.py")
        print("  2. Or commit changes to trigger GitHub Actions")
        print("\n📝 If GitHub Actions fails:")
        print("  - Check the workflow logs for specific errors")
        print("  - Verify data files are committed to repository")
        print("  - Ensure requirements.txt includes all dependencies")
        return 0
    else:
        print("❌ Tests failed")
        print("\n🔍 Issues found:")
        if not cv_ok:
            print(f"  - CV file issue: {cv_file}")
        if not job_ok:
            print(f"  - Job file issue: {job_file}")
        if not analysis_ok:
            print(f"  - Analysis process issue")
        
        print("\n🛠️  Suggested fixes:")
        print("  1. Ensure files have real content (not empty)")
        print("  2. Check file formats (.txt works best for testing)")
        print("  3. Verify files are >100 words each")
        print("  4. Run: bash setup.sh (to create sample files)")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
