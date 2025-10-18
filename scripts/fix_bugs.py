#!/usr/bin/env python3
"""
Automatic bug fixer for advanced-job-engine
Fixes the two .update() → .append() bugs
"""

from pathlib import Path
import sys

def main():
    engine_file = Path("src/python_advanced_job_engine.py")
    
    if not engine_file.exists():
        print("❌ File not found: src/python_advanced_job_engine.py")
        print("   Make sure you're running this from the project root directory")
        sys.exit(1)
    
    print("🔧 Fixing bugs in python_advanced_job_engine.py")
    print("=" * 60)
    
    # Read file
    print("\n📖 Reading file...")
    content = engine_file.read_text()
    
    # Create backup
    backup = engine_file.with_suffix('.py.backup')
    backup.write_text(content)
    print(f"✅ Backup created: {backup}")
    
    # Count bugs before fixing
    bugs_found = 0
    
    if "self.analyzed_jobs.update(analysis)" in content:
        bugs_found += 1
        print(f"\n🐛 Bug #1 found: analyzed_jobs.update(analysis)")
    
    if "self.learning_progress.update(plan)" in content:
        bugs_found += 1
        print(f"🐛 Bug #2 found: learning_progress.update(plan)")
    
    if bugs_found == 0:
        print("\n✅ No bugs found! File is already correct.")
        sys.exit(0)
    
    print(f"\n🔨 Fixing {bugs_found} bug(s)...")
    
    # Fix bug #1: analyzed_jobs
    original_content = content
    content = content.replace(
        "self.analyzed_jobs.update(analysis)",
        "self.analyzed_jobs.append(analysis)"
    )
    if content != original_content:
        print("   ✅ Fixed: analyzed_jobs.update() → analyzed_jobs.append()")
    
    # Fix bug #2: learning_progress
    original_content = content
    content = content.replace(
        "self.learning_progress.update(plan)",
        "self.learning_progress.append(plan)"
    )
    if content != original_content:
        print("   ✅ Fixed: learning_progress.update() → learning_progress.append()")
    
    # Write fixed version
    engine_file.write_text(content)
    print(f"\n💾 Saved fixed version to: {engine_file}")
    
    print("\n" + "=" * 60)
    print("✅ All bugs fixed successfully!")
    print("\n📋 Summary:")
    print(f"   - Bugs fixed: {bugs_found}")
    print(f"   - Backup: {backup}")
    print(f"   - Fixed file: {engine_file}")
    
    print("\n🧪 Next step: Run the debug script")
    print("   python3 scripts/debug_analysis.py")
    
    print("\n💡 To restore backup if needed:")
    print(f"   cp {backup} {engine_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
