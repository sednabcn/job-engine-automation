#!/usr/bin/env python3
"""Test that data files are readable"""

import sys
from pathlib import Path
from src.python_advanced_job_engine import AdvancedJobEngine

def test_files():
    engine = AdvancedJobEngine()
    
    test_files = [
        "data/my_cv.pdf",
        "data/my_cv.txt",
        "data/my_cv.docx",
        "data/target_job.pdf",
        "data/target_job.txt",
        "data/target_job.docx"
    ]
    
    found_cv = False
    found_job = False
    
    print("🔍 Checking data files...\n")
    
    for filepath in test_files:
        path = Path(filepath)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {filepath} ({size:,} bytes)")
            
            try:
                text = engine.read_document(filepath)
                words = len(text.split())
                print(f"   → {words} words extracted")
                print(f"   → Preview: {text[:100]}...\n")
                
                if 'cv' in filepath.lower():
                    found_cv = True
                if 'job' in filepath.lower() or 'target' in filepath.lower():
                    found_job = True
                    
            except Exception as e:
                print(f"   ❌ Error reading: {e}\n")
        else:
            print(f"⏭️  {filepath} (not found)")
    
    print("\n" + "="*50)
    if found_cv and found_job:
        print("✅ Ready to run analysis!")
        return 0
    else:
        if not found_cv:
            print("❌ No readable CV file found")
        if not found_job:
            print("❌ No readable job description found")
        print("\n💡 Add files to data/ directory")
        return 1

if __name__ == "__main__":
    sys.exit(test_files())
