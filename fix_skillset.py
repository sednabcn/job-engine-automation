#!/usr/bin/env python3
"""
Quick fix for KeyError: 'technical_skills'
Repairs or creates master_skillset.json with correct structure
"""

import json
import shutil
from pathlib import Path
from datetime import datetime


def fix_skillset_file(data_dir: str = "job_search_data"):
    """Fix the master_skillset.json file"""
    
    print("🔧 Fixing master_skillset.json")
    print("=" * 70)
    
    # Ensure directory exists
    data_path = Path(data_dir)
    data_path.mkdir(exist_ok=True)
    
    skillset_file = data_path / "master_skillset.json"
    
    # Backup existing file if it exists
    if skillset_file.exists():
        backup_file = data_path / "master_skillset.json.backup"
        shutil.copy(skillset_file, backup_file)
        print(f"📦 Backed up existing file to: {backup_file}")
        
        # Try to read existing file
        try:
            with open(skillset_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            print(f"📄 Read existing file")
            print(f"   Keys found: {list(existing.keys())}")
        except Exception as e:
            print(f"⚠️  Could not read existing file: {e}")
            existing = {}
    else:
        print("📄 No existing file found - will create new one")
        existing = {}
    
    # Create correct structure
    correct_structure = {
        "technical_skills": {
            "programming": [],
            "frameworks": [],
            "tools": [],
            "databases": [],
            "cloud": [],
        },
        "soft_skills": [],
        "certifications": [],
        "languages": [],
        "domains": [],
        "last_updated": datetime.now().isoformat(),
    }
    
    # Merge existing data with correct structure
    if existing:
        print("\n🔄 Merging existing data with correct structure...")
        
        # Preserve technical skills if they exist
        if "technical_skills" in existing and isinstance(existing["technical_skills"], dict):
            for category in correct_structure["technical_skills"]:
                if category in existing["technical_skills"]:
                    correct_structure["technical_skills"][category] = existing["technical_skills"][category]
        
        # Preserve other fields
        for key in ["soft_skills", "certifications", "languages", "domains"]:
            if key in existing and isinstance(existing[key], list):
                correct_structure[key] = existing[key]
    
    # Save corrected structure
    with open(skillset_file, 'w', encoding='utf-8') as f:
        json.dump(correct_structure, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Fixed: {skillset_file}")
    print(f"\n📊 Structure:")
    print(f"   technical_skills:")
    for subcat, skills in correct_structure["technical_skills"].items():
        print(f"      {subcat}: {len(skills)} skills")
    print(f"   soft_skills: {len(correct_structure['soft_skills'])} skills")
    print(f"   certifications: {len(correct_structure['certifications'])} items")
    print(f"   languages: {len(correct_structure['languages'])} items")
    print(f"   domains: {len(correct_structure['domains'])} items")
    
    print("\n" + "=" * 70)
    print("🎉 Done! You can now run your script again.")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    
    # Get data directory from command line or use default
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "job_search_data"
    
    try:
        fix_skillset_file(data_dir)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
