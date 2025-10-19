# Ultimate Job Search Engine - Automation Guide

## 🚀 Quick Start

Your workflow now has **3 levels of automation**:

---

## Option 1: COMPLETE FLOW (Fully Automated Setup)

**Perfect for:** First-time setup, getting everything done in one go

### How to Use:
1. Go to **Actions** → **Ultimate Job Search Engine**
2. Click **Run workflow**
3. Select:
   - **action**: `complete_flow`
   - **cv_path**: `data/my_cv.pdf`
   - **job_path**: `data/target_job.pdf`
   - **job_metadata**: `Software Engineer|Google`
4. Click **Run workflow**

### What It Does Automatically:
- ✅ Analyzes CV vs job description
- ✅ Creates reverse learning plan
- ✅ Generates improvement strategy
- ✅ Creates skill tests
- ✅ Generates application materials (cover letters, etc.)
- ✅ Initializes your workflow state

### Result:
You're ready to start learning! Next step: `start_sprint` or `auto_sprint_cycle`

---

## Option 2: AUTO SPRINT CYCLE (Automated Learning)

**Perfect for:** Daily learning automation, hands-off sprint management

### How to Use:

#### First Run (Starts Sprint):
```yaml
action: auto_sprint_cycle
cv_path: data/my_cv.pdf
job_path: data/target_job.pdf
sprint_data: {"hours":0,"concepts":[],"notes":""}
```

#### Daily Runs (Logs Progress):
```yaml
action: auto_sprint_cycle
sprint_data: {"hours":3,"concepts":["React Hooks","State Management"],"notes":"Built todo app"}
```

#### Final Run (Ends Sprint with Project):
```yaml
action: auto_sprint_cycle
sprint_data: {"hours":4,"concepts":["Testing"],"notes":"Completed","project_url":"https://github.com/user/project","test_scores":{"React":85,"TypeScript":78}}
```

### What It Does:
- 🚀 **No active sprint?** → Starts new sprint automatically
- 📝 **Active sprint?** → Logs your daily progress
- 🏁 **Sprint complete (14 days or project URL)?** → Ends sprint and starts next one

### Workflow:
```
Run 1:  Start Sprint → Skills selected from learning plan
Run 2:  Log Day 1   → Hours + concepts logged
Run 3:  Log Day 2   → Hours + concepts logged
...
Run 15: Log Day 14  → Hours + concepts logged
Run 16: End Sprint  → Completes sprint, starts new one automatically
```

---

## Option 3: WORKFLOW CHAINING (Option B)

**Perfect for:** Fully automated workflow progression

### How to Use:
Add `chain_next` to your options:

```yaml
action: complete_flow
options: generate_materials,chain_next
```

### What It Does:
After completing an action, **automatically triggers the next recommended action**:

```
complete_flow (finishes) 
    ↓ (auto-triggers)
start_sprint 
    ↓ (manual: run auto_sprint_cycle 14 times)
auto_sprint_cycle (sprint ends)
    ↓ (auto-triggers if chain_next enabled)
auto_sprint_cycle (new sprint starts)
```

---

## 📋 Complete Lifecycle Examples

### Example 1: Fully Automated (Recommended)

**Day 1 - Initial Setup:**
```yaml
action: complete_flow
cv_path: data/my_cv.pdf
job_path: data/target_job.pdf
job_metadata: Senior Developer|TechCorp
options: generate_materials,chain_next
```

**Day 2 - Start Auto Learning:**
```yaml
action: auto_sprint_cycle
sprint_data: {"hours":3,"concepts":["Skill1","Skill2"],"notes":"Started learning"}
options: chain_next
```

**Days 3-15 - Keep Logging:**
```yaml
action: auto_sprint_cycle
sprint_data: {"hours":4,"concepts":["Practiced Skill1"],"notes":"Making progress"}
options: chain_next
```

**Day 16 - Complete Sprint:**
```yaml
action: auto_sprint_cycle
sprint_data: {"hours":5,"concepts":["Final touches"],"notes":"Done!","project_url":"https://github.com/user/project","test_scores":{"Skill1":85,"Skill2":80}}
options: chain_next
```

**Repeat** until match score ≥ 90%!

---

### Example 2: Manual Control

**Step 1: Analysis**
```yaml
action: full_analysis
cv_path: data/my_cv.pdf
job_path: data/target_job.pdf
job_metadata: Data Scientist|AI Startup
```

**Step 2: Start Sprint**
```yaml
action: start_sprint
```

**Step 3: Log Daily (repeat 14 times)**
```yaml
action: log_daily
sprint_data: {"hours":3,"concepts":["Python","Pandas"],"notes":"Learned data manipulation"}
```

**Step 4: End Sprint**
```yaml
action: end_sprint
sprint_data: {"project_url":"https://github.com/user/data-project","test_scores":{"Python":90,"Pandas":85}}
```

**Step 5: Check Progress**
```yaml
action: quality_check
```

**Step 6: Repeat 2-5** until ready!

---

### Example 3: Batch Analysis Multiple Jobs

```yaml
action: batch_analysis
cv_path: data/my_cv.pdf
job_path: data/job1.pdf,data/job2.pdf,data/job3.pdf
options: generate_comparison
```

**Output:**
- Individual analysis for each job
- Comparison report ranking all jobs
- Best match identified

---

## 🎯 Action Reference

| Action | When to Use | What It Does |
|--------|-------------|--------------|
| `complete_flow` | First setup | Full lifecycle: analysis → plan → materials |
| `auto_sprint_cycle` | Daily learning | Smart sprint management: start → log → end |
| `full_analysis` | Manual analysis | Analyze CV vs single job |
| `batch_analysis` | Compare jobs | Analyze CV vs multiple jobs |
| `start_sprint` | Manual sprint start | Begin 14-day sprint |
| `log_daily` | Manual daily log | Log hours/concepts/notes |
| `end_sprint` | Manual sprint end | Complete sprint with project |
| `quality_check` | Check readiness | Check if application-ready |
| `generate_materials` | Need materials | Create cover letters, etc. |
| `daily_report` | Check progress | View current status |

---

## ⚙️ Input Reference

### cv_path
- Path to your CV file
- Formats: `.txt`, `.pdf`, `.docx`
- Example: `data/my_cv.pdf`

### job_path
- Single job: `data/job.pdf`
- Multiple jobs: `data/job1.pdf,data/job2.pdf,data/job3.pdf`

### job_metadata
- Format: `"Job Title|Company Name"`
- Example: `"Senior Developer|Google"`

### sprint_data (JSON)
```json
{
  "hours": 3,
  "concepts": ["React", "TypeScript"],
  "notes": "Built todo app",
  "project_url": "https://github.com/user/project",
  "test_scores": {"React": 85, "TypeScript": 78}
}
```

### options (comma-separated)
- `generate_materials` - Generate cover letters
- `generate_comparison` - Generate comparison report (batch analysis)
- `send_email` - Send email notification
- `chain_next` - Auto-trigger next workflow

### email_to
- Your email address for notifications
- Requires: `send_email` in options
- Requires: GitHub secrets `EMAIL_USERNAME` and `EMAIL_PASSWORD`

---

## 🔄 Recommended Workflows

### For Beginners (Fully Automated):
```
1. complete_flow (with chain_next)
2. auto_sprint_cycle (daily, with chain_next)
3. Repeat step 2 until score ≥ 90%
4. Apply to jobs! 🎉
```

### For Control Freaks (Manual):
```
1. full_analysis
2. start_sprint
3. log_daily (14 times)
4. end_sprint
5. quality_check
6. Repeat 2-5 until ready
7. generate_materials
8. Apply! 🎉
```

### For Job Hunters (Compare Multiple):
```
1. batch_analysis (with generate_comparison)
2. Review comparison report
3. Pick best match
4. complete_flow for best job
5. Start learning!
```

---

## 📅 Scheduled Runs

The workflow runs **automatically twice daily**:
- 9 AM UTC
- 9 PM UTC

**What it does:**
- Runs `daily_report`
- Shows current progress
- Reminds you to log daily work

---

## 💡 Pro Tips

1. **Use `complete_flow` first** - Gets everything set up in one go
2. **Use `auto_sprint_cycle` daily** - Automates the entire learning process
3. **Add `chain_next` option** - For maximum automation
4. **Check `daily_report` output** - Monitor progress
5. **Download artifacts** - Review detailed reports after each run

---

## 🆘 Troubleshooting

### "Workflow not initialized"
**Solution:** Run `complete_flow` or `full_analysis` first

### "No active sprint"
**Solution:** Run `start_sprint` or `auto_sprint_cycle`

### "File not found"
**Solution:** Make sure CV and job files exist in `data/` folder

### "Invalid JSON in sprint_data"
**Solution:** Check JSON syntax, use online JSON validator

### Workflow keeps skipping steps
**This is normal!** Only relevant steps run for each action

---

## 📊 Understanding Results

After each run, check **Artifacts** section:
- `job-search-state-v1` - Your persistent state
- `progress-report-XXXX` - Detailed progress report
- `job-analysis-output-XXXX` - Analysis results, plans, materials

Download and read `PROGRESS_REPORT.md` for:
- Current match score
- Skills mastered
- Projects completed
- Next recommended actions
- Quality gate status

---

## 🎯 Goal

**Target:** 90% match score
**Method:** Complete sprints until target reached
**Result:** Application-ready! Start applying! 🚀

---

**Remember:** The workflow is designed to help you **systematically improve** your skills to match your dream job. Trust the process! 💪