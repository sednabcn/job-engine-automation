# Required Fixes for Workflow-Script Compatibility

## Critical Issues to Fix

### 1. Fix Import Path in Workflow

**Current (line ~90):**
```python
from python_advanced_job_engine import AdvancedJobEngine
```

**Fix:**
```python
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
from python_advanced_job_engine import AdvancedJobEngine
```

---

### 2. Fix State Initialization Check

**Current:**
```python
mode = state.get('mode', 'none')
# ...
initialized={mode != 'none'}
```

**Fix:**
```python
mode = state.get('mode') or 'none'
# ...
initialized={'true' if mode and mode != 'none' else 'false'}
```

---

### 3. Add Missing `log_daily` Action

**Add to workflow (around line 350):**
```yaml
- name: 📝 Log Daily Progress
  if: github.event.inputs.action == 'log_daily'
  run: |
    python << 'PYTHON_EOF'
    from python_advanced_job_engine import AdvancedJobEngine
    
    engine = AdvancedJobEngine(data_dir="${{ env.DATA_DIR }}")
    
    if not engine.sprint_history or engine.sprint_history[-1].get('completed'):
        print("❌ No active sprint")
        exit(1)
    
    # Get inputs (would need workflow_dispatch inputs)
    hours = 3.0  # TODO: Get from input
    concepts = ["Concept 1", "Concept 2"]  # TODO: Get from input
    notes = "Daily progress"  # TODO: Get from input
    
    engine.log_daily(hours, concepts, notes)
    PYTHON_EOF
```

**Add workflow inputs:**
```yaml
workflow_dispatch:
  inputs:
    action:
      # ... existing ...
    hours:
      description: 'Hours spent today'
      required: false
      default: '3'
    concepts:
      description: 'Concepts learned (comma-separated)'
      required: false
      default: ''
    notes:
      description: 'Daily notes'
      required: false
      default: ''
```

---

### 4. Fix File Path Defaults

**Option A: Update workflow to match script**
```yaml
env:
  DATA_DIR: 'job_search_data'  # ✅ Matches script
```

**Option B: Update script to match workflow**
```python
def __init__(self, data_dir: str = "data"):  # Was "job_search_data"
```

**Recommended: Use Option A** (workflow matches script)

---

### 5. Add Error Handling to Workflow

**Wrap all Python blocks:**
```python
try:
    from python_advanced_job_engine import AdvancedJobEngine
    engine = AdvancedJobEngine(data_dir="${{ env.DATA_DIR }}")
    # ... rest of code ...
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Ensure script is at: src/python_advanced_job_engine.py")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
```

---

### 6. Fix Boolean Output Format

**Current:**
```python
f.write(f"initialized={mode != 'none'}\n")  # Writes Python bool
```

**Fix:**
```python
initialized = 'true' if (mode and mode != 'none') else 'false'
f.write(f"initialized={initialized}\n")  # Writes string 'true'/'false'
```

---

### 7. Add Workflow Inputs for Sprint End

**Update workflow_dispatch inputs:**
```yaml
project_url:
  description: 'Project URL (for end_sprint)'
  required: false
  default: ''
test_scores:
  description: 'Test scores JSON: {"skill": score}'
  required: false
  default: '{}'
```

**Update End Sprint action:**
```python
import json

project_url = "${{ github.event.inputs.project_url }}"
test_scores_str = "${{ github.event.inputs.test_scores }}"

if not project_url:
    project_url = "https://github.com/user/sprint-project"
    print("⚠️  Using default project URL")

if test_scores_str:
    test_scores = json.loads(test_scores_str)
else:
    # Default scores
    test_scores = {skill: 70.0 for skill in current_sprint['skills_targeted']}
```

---

### 8. Ensure Directory Structure

**Add to setup step:**
```yaml
- name: 📂 Ensure data directories exist
  run: |
    mkdir -p ${{ env.DATA_DIR }}
    mkdir -p data
    mkdir -p src
    
    # Verify script exists
    if [ ! -f "src/python_advanced_job_engine.py" ]; then
      echo "❌ Error: src/python_advanced_job_engine.py not found"
      exit 1
    fi
    
    echo "✅ Data directories created"
    echo "✅ Script verified"
```

---

## Summary of Mismatches

| Issue | Script | Workflow | Fix Priority |
|-------|--------|----------|--------------|
| Import path | `src/python_advanced_job_engine.py` | Assumes different path | 🔴 Critical |
| State `mode` | `None` | `'none'` string | 🔴 Critical |
| Boolean output | Python bool | String 'true'/'false' | 🔴 Critical |
| Data directory | `job_search_data/` | `data/` | 🟡 High |
| `log_daily` action | Exists in script | Missing in workflow | 🟡 High |
| Error handling | Has some | Missing in workflow | 🟡 High |
| Sprint end inputs | Needs real data | Uses fake data | 🟢 Medium |

---

## Testing Checklist

After fixes:

- [ ] Import works: `from python_advanced_job_engine import AdvancedJobEngine`
- [ ] State initialization: `mode` is properly checked
- [ ] Boolean outputs: `'true'`/`'false'` strings
- [ ] File paths: All use same `DATA_DIR`
- [ ] `log_daily` action works
- [ ] Error messages are helpful
- [ ] Sprint end accepts real inputs
- [ ] All Python blocks have try-except