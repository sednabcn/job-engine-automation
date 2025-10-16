# ⚡ Quick Start - 5 Minutes

Get started with Advanced Job Engine immediately!

## 📦 Install
```bash
git clone https://github.com/yourusername/advanced-job-engine.git
cd advanced-job-engine
pip install -r requirements.txt
```

## 📄 Add Files
```bash
# Add your CV
cp ~/your_cv.pdf data/my_cv.pdf

# Add job description
cp ~/job_description.pdf data/target_job.pdf
```

## 🚀 Run Analysis
```bash
python src/python_advanced_job_engine.py
```

**Or use Python:**
```python
from src.python_advanced_job_engine import AdvancedJobEngine

engine = AdvancedJobEngine()
analysis = engine.analyze_from_files(
    cv_file="data/my_cv.pdf",
    job_file="data/target_job.pdf"
)

print(f"Match Score: {analysis['score']['total_score']}%")
print(f"Missing Skills: {analysis['gaps']['missing_required_skills']}")
```

## 📊 Understand Results

- **90%+**: Apply now! ✅
- **75-89%**: Minor gaps, apply soon 💛
- **60-74%**: 2-4 weeks learning needed 🟡
- **<60%**: 8-12 weeks preparation 🔴

## 🎯 Next Steps
```python
# 1. Get learning plan
plan = engine.create_learning_plan(analysis)

# 2. Create improvement strategy
strategy = engine.create_improvement_strategy(analysis, plan)

# 3. Generate skill tests
tests = engine.generate_skill_tests(analysis['gaps']['missing_required_skills'][:5])

# 4. Export everything
engine.export_all(analysis['job_id'])
```

**Files exported to:** `job_search_data/export_[id]/`

## 📚 Need Help?

- [Full Documentation](docs/user-guide.md)
- [Examples](examples/)
- [Troubleshooting](docs/troubleshooting.md)
- [GitHub Issues](https://github.com/yourusername/advanced-job-engine/issues)

---

**That's it! Start analyzing! 🚀**

Answers to Your Questions:
1. Should I create a local package?
Two options:
Option A - Simple (Recommended for Users):

No local package needed
Everything runs on GitHub Actions
Just upload your CV and run workflows from GitHub UI
Best for non-technical users

Option B - Advanced (For Developers):

Create local package for development
Use setup.py or pyproject.toml
Install with: pip install -e .
Good for testing before pushing to GitHub

2. Does the package create remotely?

No, the package is NOT created remotely
GitHub Actions runs your Python scripts directly
No package installation happens in workflows
Files are accessed relatively: src/python_advanced_job_engine.py

3. Easiest way as a USER:
🎯 SIMPLEST WORKFLOW (No coding required):

Fork the repo on GitHub
Upload your CV to data/ folder via GitHub web UI
Go to Actions tab → Select "Workflow Manager Dashboard"
Click "Run workflow" → Choose what you want
Download results from workflow artifacts

That's it! No local setup, no command line, no Python knowledge needed.
4. Do I need workflow contents?
Yes, but I can help you create them! To create the complete manager, I should see at least one of your existing workflows to understand:

How you're running the Python script
What inputs you expect
What outputs you generate
Any dependencies or setup steps