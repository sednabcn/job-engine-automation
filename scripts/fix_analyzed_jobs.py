#!/usr/bin/env python3
"""
Fix the analyzed_jobs.json structure from dict to list
"""

import json
from pathlib import Path

json_file = Path("job_search_data/analyzed_jobs.json")

if not json_file.exists():
    print("✅ File doesn't exist - will be created as list automatically")
    exit(0)

print("📖 Reading analyzed_jobs.json...")
with open(json_file, 'r') as f:
    data = json.load(f)

# Check if it's already a list
if isinstance(data, list):
    print("✅ Already in correct format (list)")
    exit(0)

# It's a dict - need to convert
print("🔧 Converting from dict to list format...")

# Create backup
backup_file = json_file.with_suffix('.json.backup')
print(f"💾 Creating backup: {backup_file}")
with open(backup_file, 'w') as f:
    json.dump(data, f, indent=2)

# Extract the analysis from the mixed structure
analysis = {}
metadata_keys = ['version', 'last_updated', 'total_jobs_analyzed', 'jobs']

for key, value in data.items():
    if key not in metadata_keys:
        analysis[key] = value

# Create new list structure
if analysis:
    new_data = [analysis]
    print(f"✅ Extracted 1 analysis")
else:
    new_data = []
    print("⚠️  No analysis data found, creating empty list")

# Write corrected structure
print("✍️  Writing corrected structure...")
with open(json_file, 'w') as f:
    json.dump(new_data, f, indent=2)

print("✅ Fixed! Structure is now a list")
print(f"\n📋 Summary:")
print(f"   - Backup saved: {backup_file}")
print(f"   - Analyses in list: {len(new_data)}")
print(f"\n🧪 Now run: python3 scripts/debug_analysis.py")
