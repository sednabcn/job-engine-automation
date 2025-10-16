# GitHub Actions Workflows Guide

This repository includes three powerful workflows for automated job analysis.

## Available Workflows

### 1. 🎯 Auto Job Analysis
**File:** `.github/workflows/auto-job-analysis.yml`

**Purpose:** Analyze a single CV against a single job description

**Triggers:**
- Manual: Actions tab → Run workflow
- Automatic: When you upload files to `data/` folder

**Usage:**
1. Upload `data/my_cv.pdf` and `data/job_description.pdf`
2. Go to Actions → Auto Job Analysis → Run workflow
3. Wait 2-3 minutes
4. Download results artifact

**Outputs:**
- Complete analysis report
- Match score breakdown
- Learning plan
- Application materials
- Skill tests

---

### 2. 📊 Scheduled Re-Analysis
**File:** `.github/workflows/scheduled-analysis.yml`

**Purpose:** Automatically re-analyze all jobs monthly to track progress

**Triggers:**
- Automatic: 1st of every month at 9 AM UTC
- Manual: Actions tab → Run workflow

**Usage:**
1. Upload CV and job files once
2. Workflow runs automatically monthly
3. Tracks score improvements over time
4. Commits progress data to repository

**Outputs:**
- Monthly progress report
- Score trends
- Historical comparison
- Improvement tracking

---

### 3. 🔄 Batch Analysis
**File:** `.github/workflows/batch-analysis.yml`

**Purpose:** Analyze multiple jobs at once and compare them

**Triggers:**
- Manual only

**Usage:**
1. Upload multiple job files to `data/`
2. Go to Actions → Batch Job Analysis → Run workflow
3. Enter comma-separated file paths:
```
   data/job1.pdf,data/job2.pdf,data/job3.pdf
```
4. Wait for completion
5. Download batch results

**Outputs:**
- Individual analysis for each job
- Comparison report ranking all jobs
- Side-by-side score comparison
- Recommendations on which to apply to

---

## Setup Steps

1. **Fork Repository**
```
   Click "Fork" button on GitHub
```

2. **Enable Workflows**
```
   Go to Actions tab
   Click "I understand my workflows, enable them"
```

3. **Upload Your Files**
```
   data/my_cv.pdf          ← Your CV
   data/job_*.pdf          ← Job descriptions
```

4. **Run Workflows**
```
   Actions tab → Select workflow → Run workflow
```

---

## File Structure
your-repo/
├── .github/
│   └── workflows/
│       ├── auto-job-analysis.yml      # Single job analysis
│       ├── scheduled-analysis.yml     # Monthly re-analysis
│       └── batch-analysis.yml         # Multiple jobs
├── data/
│   ├── my_cv.pdf                      # Your CV
│   ├── job_description.pdf            # Job 1
│   ├── job_backend.pdf                # Job 2
│   └── job_frontend.pdf               # Job 3
├── output/                            # Generated reports
├── batch_results/                     # Batch analysis results
└── progress_tracking/                 # Historical data

---

## Tips

✅ **DO:**
- Keep CV filename consistent: `my_cv.pdf`
- Use descriptive job filenames: `job_senior_backend_google.pdf`
- Run batch analysis to compare multiple opportunities
- Check monthly reports to track improvement

❌ **DON'T:**
- Don't rename files frequently (breaks tracking)
- DonRetryClaude does not have the ability to run the code it generates yet.RContinueTips (continued)
❌ DON'T:

Don't rename files frequently (breaks tracking)
Don't delete progress_tracking/ folder (loses history)
Don't run too many workflows at once (rate limits)
Don't commit sensitive info in job descriptions


Workflow Inputs Reference
Auto Job Analysis Inputs
InputTypeRequiredDefaultDescriptioncv_filestringNodata/my_cv.pdfPath to your CVjob_filestringNodata/job_description.pdfPath to job descriptionjob_titlestringNo-Job title (for reports)company_namestringNo-Company name (for letters)generate_materialsbooleanNotrueGenerate cover letter, etc.send_notificationbooleanNofalseSend email when done
Batch Analysis Inputs
InputTypeRequiredDefaultDescriptioncv_filestringNodata/my_cv.pdfPath to your CVjob_filesstringYes-Comma-separated job filesgenerate_comparisonbooleanNotrueCreate comparison report

Troubleshooting
Workflow Won't Run
Problem: Yellow dot stuck, workflow not starting
Solutions:

Check Actions are enabled: Settings → Actions → Allow all actions
Verify workflow file syntax (no YAML errors)
Check GitHub Actions status: https://www.githubstatus.com
Wait a few minutes and refresh


Workflow Failed
Problem: Red X, workflow failed
Solutions:

Click on failed workflow → View logs
Check error message in logs
Common issues:

File not found: Check file path matches exactly
Python error: Check requirements.txt is present
Import error: Verify src/ folder exists with code files




No Artifact Generated
Problem: Workflow succeeded but no download available
Solutions:

Check "Artifacts" section at bottom of workflow run page
Artifacts expire after 90 days (scheduled) or 365 days (monthly)
Re-run workflow if artifact expired
Check workflow logs for upload errors


Scheduled Workflow Not Running
Problem: Monthly workflow doesn't trigger automatically
Solutions:

Check cron schedule is uncommented in YAML
Verify repository is active (workflows disabled on inactive repos)
Check workflow hasn't been manually disabled
GitHub may delay scheduled workflows up to 15 minutes


Email Notifications Not Working
Problem: No emails received after workflow
Solutions:

Verify secrets are set:

Settings → Secrets → Actions
SMTP_USERNAME, SMTP_PASSWORD, NOTIFICATION_EMAIL


Check email provider allows SMTP:

Gmail: Enable "Less secure app access" or use App Password
Outlook: Enable SMTP in settings


Check spam folder
Verify email address is correct in secrets


Advanced Customization
Change Schedule Time
Edit .github/workflows/scheduled-analysis.yml:
yamlschedule:
  - cron: '0 9 1 * *'  # Current: 9 AM on 1st of month
  
# Examples:
  - cron: '0 0 * * 1'  # Weekly: Every Monday at midnight
  - cron: '0 12 1,15 * *'  # Bi-weekly: 1st and 15th at noon
  - cron: '0 6 * * *'  # Daily: Every day at 6 AM
Cron format: minute hour day month weekday

Add More Outputs
Edit any workflow file, add to the analysis step:
python# In the Python script section
with open('output/custom_report.txt', 'w') as f:
    f.write("Your custom content here")
Files saved to output/ will be included in artifacts automatically.

Change Retention Days
Edit artifact upload step:
yaml- name: Upload results as artifact
  uses: actions/upload-artifact@v4
  with:
    name: job-analysis-results
    path: output/
    retention-days: 30  # Change from 90 to 30 days
Options: 1-90 days (free tier), 1-400 days (paid plans)

Add Notifications to Slack/Discord
Add step to any workflow:
For Slack:
yaml- name: Notify Slack
  if: success()
  uses: slackapi/slack-github-action@v1.24.0
  with:
    payload: |
      {
        "text": "Job Analysis Complete! Score: ${{ steps.analysis.outputs.score }}%"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
For Discord:
yaml- name: Notify Discord
  if: success()
  uses: sarisia/actions-status-discord@v1
  with:
    webhook: ${{ secrets.DISCORD_WEBHOOK }}
    title: "Job Analysis Complete"
    description: "Match Score: ${{ steps.analysis.outputs.score }}%"

Run on Different Events
Add to on: section of any workflow:
yamlon:
  # Manual trigger
  workflow_dispatch:
  
  # When pushing to main branch
  push:
    branches:
      - main
  
  # When creating pull request
  pull_request:
    branches:
      - main
  
  # When files change
  push:
    paths:
      - 'data/**.pdf'
      - 'data/**.docx'
  
  # On schedule
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday
  
  # When release is published
  release:
    types: [published]

GitHub Actions Limits
Free Tier:

2,000 minutes/month for private repos
Unlimited for public repos
500 MB artifact storage
90 day artifact retention

Each workflow run uses approximately:

2-3 minutes for single job analysis
5-10 minutes for batch analysis (3-5 jobs)
10-20 minutes for monthly re-analysis (10+ jobs)

Tips to save minutes:

Use workflow manually instead of auto-triggers
Reduce scheduled frequency
Make repository public (unlimited minutes)
Use smaller file sizes


Security Best Practices
Protect Sensitive Information
DO:

✅ Store API keys in GitHub Secrets
✅ Use environment variables for credentials
✅ Review job descriptions before committing
✅ Use .gitignore for sensitive files

DON'T:

❌ Commit API keys in workflow files
❌ Store passwords in YAML files
❌ Include personal info in public repos
❌ Share webhook URLs publicly


Recommended .gitignore
gitignore# Sensitive data
secrets/
*.env
.env.local

# Personal information
personal_notes/
salary_negotiations/

# Large files
*.psd
*.ai
large_datasets/

# Temporary files
output/temp/
*.tmp
*.log

# OS files
.DS_Store
Thumbs.db

Examples
Example 1: Single Job Analysis
bash# Step 1: Upload files via GitHub web interface
data/my_cv.pdf
data/google_senior_engineer.pdf

# Step 2: Go to Actions tab
# Step 3: Click "Auto Job Analysis"
# Step 4: Click "Run workflow"
# Step 5: Fill inputs:
Job Title: Senior Software Engineer
Company: Google
Generate Materials: Yes

# Step 6: Wait 2-3 minutes
# Step 7: Download artifact
Result: Complete analysis with 78% match score, learning plan, cover letter

Example 2: Compare 5 Jobs
bash# Step 1: Upload files
data/my_cv.pdf
data/google_backend.pdf
data/meta_fullstack.pdf
data/amazon_sde2.pdf
data/netflix_senior.pdf
data/apple_engineer.pdf

# Step 2: Go to Actions → Batch Job Analysis
# Step 3: Run workflow with:
Job Files: data/google_backend.pdf,data/meta_fullstack.pdf,data/amazon_sde2.pdf,data/netflix_senior.pdf,data/apple_engineer.pdf

# Step 4: Wait 5-8 minutes
# Step 5: Download batch results
Result: Comparison report ranking all 5 jobs, showing Netflix (85%) as best match

Example 3: Track Monthly Progress
bash# Step 1: Initial setup (Month 1)
Upload: data/my_cv.pdf, data/dream_job.pdf
Run: Auto Job Analysis
Result: 65% match

# Step 2: Enable scheduled workflow
Edit: .github/workflows/scheduled-analysis.yml
Uncomment schedule section
Commit changes

# Step 3: Month 2 (automatic)
Workflow runs on 1st of month
Result: 72% match (+7%)

# Step 4: Month 3 (automatic)
Workflow runs automatically
Result: 78% match (+6%)

# Step 5: View progress
Check: progress_tracking/results_2024-*.json
Download: Monthly comparison reports
```

**Result:** Visual progress tracking showing 65% → 78% improvement over 3 months

---

## FAQ

**Q: Do I need to install Python locally?**
A: No! Everything runs on GitHub's servers.

**Q: Can I use this on mobile?**
A: Yes! Upload files and trigger workflows from GitHub mobile app.

**Q: How much does it cost?**
A: Free for public repos. Private repos get 2000 minutes/month free.

**Q: Can I analyze Word documents?**
A: Yes! Supports PDF, DOCX, and TXT formats.

**Q: What if my CV changes?**
A: Just upload the new version to `data/my_cv.pdf` (same filename).

**Q: Can I analyze jobs from LinkedIn/Indeed?**
A: Yes! Copy job text and save as PDF or TXT file.

**Q: How do I share results with friends?**
A: Download artifact, unzip, and share specific files.

**Q: Can I run this for someone else's CV?**
A: Yes! Upload their CV with different filename and specify in inputs.

**Q: What if analysis fails?**
A: Check workflow logs for errors. Most common: file not found or wrong format.

**Q: Can I customize the reports?**
A: Yes! Edit the Python code in workflow files.

---

## Support

**Issues:**
- GitHub Issues: Report bugs or request features
- Discussions: Ask questions and share tips

**Resources:**
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Workflow Syntax](https://docs.github.com/actions/reference/workflow-syntax-for-github-actions)
- [Cron Schedule Expression](https://crontab.guru/)

**Community:**
- Share your results and improvements
- Help others troubleshoot
- Contribute workflow enhancements

---

## Contributing

Want to improve the workflows? Here's how:

1. Fork repository
2. Create new branch: `git checkout -b feature/better-workflow`
3. Make changes to workflow files
4. Test thoroughly
5. Submit Pull Request
6. Describe changes and benefits

**Popular contributions:**
- New notification methods
- Additional output formats
- Better error handling
- Performance improvements
- Documentation updates

---

## Changelog

**v1.0.0** (2024-10)
- Initial release
- Auto job analysis workflow
- Scheduled re-analysis workflow
- Batch analysis workflow

**Future Plans:**
- Integration with LinkedIn API
- Automatic job scraping
- Resume builder workflow
- Interview prep generator
- Salary negotiation calculator

---

## License

MIT License - Use freely for personal and commercial purposes

---

**Happy Job Hunting! 🚀**

Remember: This tool helps you prepare, but your skills, experience, and personality matter most. Use the insights to improve, but don't let a score define your worth. You've got this! 💪
```

---

## 5. Quick Start Script: `scripts/setup-workflows.sh`
```bash
#!/bin/bash

# Quick Setup Script for GitHub Actions Workflows
# Run this locally to verify setup before pushing to GitHub

echo "🚀 Advanced Job Engine - Workflow Setup"
echo "========================================"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    echo "Please run: git init"
    exit 1
fi

echo "✅ Git repository detected"

# Create directory structure
echo ""
echo "📁 Creating directory structure..."

mkdir -p .github/workflows
mkdir -p data
mkdir -p output
mkdir -p batch_results
mkdir -p progress_tracking
mkdir -p src

echo "✅ Directories created"

# Check for workflow files
echo ""
echo "📄 Checking workflow files..."

workflows=(
    ".github/workflows/auto-job-analysis.yml"
    ".github/workflows/scheduled-analysis.yml"
    ".github/workflows/batch-analysis.yml"
)

missing_workflows=0

for workflow in "${workflows[@]}"; do
    if [ -f "$workflow" ]; then
        echo "✅ Found: $workflow"
    else
        echo "❌ Missing: $workflow"
        missing_workflows=$((missing_workflows + 1))
    fi
done

if [ $missing_workflows -gt 0 ]; then
    echo ""
    echo "⚠️  Warning: $missing_workflows workflow file(s) missing"
    echo "Please create the missing workflow files"
fi

# Check for required Python files
echo ""
echo "🐍 Checking Python files..."

if [ -f "requirements.txt" ]; then
    echo "✅ Found: requirements.txt"
else
    echo "❌ Missing: requirements.txt"
    echo "Creating basic requirements.txt..."
    cat > requirements.txt << 'EOL'
PyPDF2>=3.0.0
pdfplumber>=0.9.0
python-docx>=0.8.11
requests>=2.31.0
python-dotenv>=1.0.0
EOL
    echo "✅ Created: requirements.txt"
fi

if [ -d "src" ]; then
    if [ -f "src/python_advanced_job_engine.py" ]; then
        echo "✅ Found: src/python_advanced_job_engine.py"
    else
        echo "❌ Missing: src/python_advanced_job_engine.py"
        echo "⚠️  This is required for workflows to run"
    fi
else
    echo "❌ Missing: src/ directory"
fi

# Check for data files
echo ""
echo "📂 Checking data directory..."

if [ -d "data" ]; then
    file_count=$(ls -1 data/ 2>/dev/null | wc -l)
    if [ $file_count -eq 0 ]; then
        echo "⚠️  data/ directory is empty"
        echo "Please upload your CV and job descriptions to data/"
    else
        echo "✅ Found $file_count file(s) in data/"
        ls -1 data/
    fi
else
    echo "❌ Missing: data/ directory"
fi

# Check GitHub configuration
echo ""
echo "🔧 Checking GitHub configuration..."

if git remote get-url origin > /dev/null 2>&1; then
    remote_url=$(git remote get-url origin)
    echo "✅ Git remote configured: $remote_url"
else
    echo "⚠️  No git remote configured"
    echo "After creating GitHub repo, run:"
    echo "  git remote add origin https://github.com/USERNAME/REPO.git"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo ""
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Sensitive
secrets/
*.env
.env.local

# OS
.DS_Store
Thumbs.db

# Output
output/temp/
*.tmp
*.log

# IDE
.vscode/
.idea/
*.swp
EOL
    echo "✅ Created: .gitignore"
fi

# Summary
echo ""
echo "========================================"
echo "📊 Setup Summary"
echo "========================================"
echo ""

if [ $missing_workflows -eq 0 ]; then
    echo "✅ All workflow files present"
else
    echo "❌ $missing_workflows workflow file(s) missing"
fi

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt present"
else
    echo "❌ requirements.txt missing"
fi

if [ -f "src/python_advanced_job_engine.py" ]; then
    echo "✅ Main Python file present"
else
    echo "❌ Main Python file missing"
fi

echo ""
echo "========================================"
echo "📝 Next Steps"
echo "========================================"
echo ""
echo "1. Upload your files to data/:"
echo "   - data/my_cv.pdf"
echo "   - data/job_description.pdf"
echo ""
echo "2. Commit and push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Setup workflows'"
echo "   git push origin main"
echo ""
echo "3. On GitHub:"
echo "   - Go to Actions tab"
echo "   - Enable workflows"
echo "   - Run 'Auto Job Analysis'"
echo ""
echo "4. Download results from Artifacts"
echo ""
echo "🚀 You're ready to go!"
echo ""
```

---

## 6. Sample Data Files

### `data/README.md`
```markdown
# Data Directory

Upload your files here for analysis.

## Required Files

### Your CV
**Filename:** `my_cv.pdf` (or .docx, .txt)
**Content:** Your resume/CV

### Job Descriptions
**Filenames:** Any descriptive name
- `job_description.pdf`
- `google_senior_backend.pdf`
- `meta_e5_fullstack.pdf`

## Supported Formats

- ✅ PDF (.pdf)
- ✅ Word (.docx)
- ✅ Text (.txt)

## File Size Limits

- Maximum per file: 25 MB
- Recommended: Under 5 MB

## Tips

1. **Use descriptive filenames:**
   - Good: `amazon_sde3_seattle_backend.pdf`
   - Bad: `job1.pdf`

2. **Keep CV filename consistent:**
   - Always use `my_cv.pdf`
   - Easier for tracking progress

3. **One job per file:**
   - Don't combine multiple jobs in one PDF
   - Each job = separate file

4. **Clean formatting:**
   - Remove headers/footers
   - Remove excessive whitespace
   - Use standard fonts

## Privacy

- Files stay in YOUR repository
- Not shared with anyone
- Delete anytime

## Examples
```
data/
├── my_cv.pdf                          ← Your CV
├── google_l5_backend_python.pdf       ← Job 1
├── meta_e5_fullstack_react.pdf        ← Job 2
├── amazon_sde3_aws_services.pdf       ← Job 3
└── netflix_senior_streaming.pdf       ← Job 4

That's all the workflow files! You now have:

1. ✅ Main analysis workflow
2. ✅ Scheduled monthly re-analysis
3. ✅ Batch comparison workflow
4. ✅ Complete documentation
5. ✅ Setup script
6. ✅ Sample data structure

Everything is ready to upload to GitHub and start analyzing jobs with zero local setup!RetryClaude does not have the ability to run the code it generates yet.Claude can make mistakes. Please double-check responses.