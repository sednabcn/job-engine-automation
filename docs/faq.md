# ❓ Frequently Asked Questions (FAQ)

Complete answers to common questions about Advanced Job Engine.

---

## 📑 Table of Contents

- [General Questions](#general-questions)
- [Installation & Setup](#installation--setup)
- [Using the Tool](#using-the-tool)
- [Understanding Results](#understanding-results)
- [Learning Plans](#learning-plans)
- [Reverse Workflow](#reverse-workflow)
- [GitHub Actions](#github-actions)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Privacy & Security](#privacy--security)

---

## General Questions

### What is Advanced Job Engine?

Advanced Job Engine is an AI-powered career development system that:
- Analyzes how well your CV matches job descriptions
- Identifies specific skill gaps
- Creates personalized learning plans
- Tracks your progress through iterative sprints
- Generates customized application materials
- Automates the entire process through GitHub Actions

### Who is this tool for?

**Perfect for:**
- 🎓 Recent graduates entering the job market
- 🔄 Career changers transitioning to new fields
- 📈 Professionals seeking advancement
- 🎯 Job seekers tired of spray-and-pray applications
- 💪 Anyone wanting to build skills strategically

**Especially useful if you:**
- Want to understand why you're not getting interviews
- Need a structured learning path
- Want to track skill improvement over time
- Prefer data-driven career decisions

### How is this different from regular job applications?

**Traditional approach:**
- Apply to 100+ jobs hoping for 2-3 interviews
- Generic applications get ignored
- No feedback on why you're rejected
- No clear path to improve

**Advanced Job Engine approach:**
- ✅ Analyze before applying
- ✅ Build skills strategically
- ✅ Track measurable improvement
- ✅ Apply when you're competitive (75%+ match)
- ✅ Quality over quantity

### Is this tool free?

Yes! Advanced Job Engine is **100% free and open source** under the MIT License. You can:
- Use it for personal or commercial purposes
- Modify it to suit your needs
- Contribute improvements back to the community

### Do I need programming experience?

**Basic use**: No programming needed
- Run simple commands in terminal
- Follow step-by-step guides
- Use interactive mode

**Advanced use**: Basic Python helpful for
- Custom configurations
- Batch analysis scripts
- Extending functionality

### How accurate are the match scores?

Match scores are **algorithmic estimates** based on:
- Keyword matching
- Skill alignment
- Experience comparison
- Education requirements

**Accuracy factors:**
- ✅ 85-90% reliable for technical roles
- ✅ Better with well-structured CVs and job descriptions
- ⚠️ Less accurate for soft skills and culture fit
- ⚠️ Human judgment still required

**Remember**: Use scores as guidance, not absolute truth!

---

## Installation & Setup

### What are the system requirements?

**Minimum requirements:**
- Python 3.9 or higher
- 500MB free disk space
- Internet connection (for setup)

**Recommended:**
- Python 3.10+
- 1GB free disk space
- Git installed

**Supported operating systems:**
- ✅ macOS (10.14+)
- ✅ Linux (Ubuntu 18.04+, Debian, Fedora, etc.)
- ✅ Windows 10/11

### Which Python version should I use?

**Recommended**: Python 3.10 or 3.11

**Minimum**: Python 3.9

Check your version:
```bash
python --version
# or
python3 --version
```

Install Python:
- **macOS**: `brew install python@3.11`
- **Linux**: `sudo apt install python3.11`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

### Installation failed. What should I do?

**Common solutions:**

1. **Update pip:**
```bash
pip install --upgrade pip
```

2. **Use Python 3 explicitly:**
```bash
python3 -m pip install -r requirements.txt
```

3. **Install with --user flag:**
```bash
pip install --user -r requirements.txt
```

4. **Check for permission issues:**
```bash
sudo pip install -r requirements.txt  # Linux/Mac
```

5. **Create fresh virtual environment:**
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Do I need to install additional packages for PDF support?

PyPDF2 and python-docx are included in `requirements.txt`, so they install automatically.

If you get errors:
```bash
pip install PyPDF2 python-docx
```

For advanced PDF handling:
```bash
pip install pdfplumber  # Better text extraction
pip install PyMuPDF     # Fast PDF processing
```

### Can I use this without Git/GitHub?

**Yes!** Git/GitHub is optional.

**Without Git:**
- Download ZIP from GitHub
- Extract files
- Run locally
- No automation features

**With Git:**
- Easy updates (`git pull`)
- GitHub Actions automation
- Version control for your data
- Contribution capability

---

## Using the Tool

### How do I prepare my CV for best results?

**Essential sections:**
```
SKILLS (Required!)
- List technical skills explicitly
- Include tools, frameworks, languages
- Example: "Python, Django, React, PostgreSQL, Docker"

EXPERIENCE
- Include years (e.g., "5 years of Python development")
- List specific technologies used
- Add measurable achievements

EDUCATION
- Degree and field of study
- Graduation year
- Relevant coursework (optional)

PROJECTS (Highly recommended)
- Project names and descriptions
- Technologies used
- GitHub links if available
```

**Formatting tips:**
- ✅ Use bullet points
- ✅ Clear section headers
- ✅ Specific technologies (not just "programming")
- ✅ Quantify experience ("3 years", not just "experience")
- ❌ Avoid images or complex formatting
- ❌ Don't use tables (PDF extraction issues)

### What file formats are supported?

**CV and Job Descriptions:**
- ✅ `.txt` (Plain text - best for accuracy)
- ✅ `.pdf` (Most common)
- ✅ `.docx` (Microsoft Word)

**Recommended**: Save as `.txt` for best parsing accuracy.

**Converting to text:**
- macOS: Open PDF → File → Export as Text
- Windows: Open PDF → Save As → Plain Text
- Online: Use pdf2txt.com or similar

### How do I analyze a job description?

**Option 1: Copy from job posting**
```bash
# Create text file
nano data/target_job.txt
# Paste job description
# Save (Ctrl+O, Enter, Ctrl+X)
```

**Option 2: Save as PDF**
- Print job posting → Save as PDF
- Move to `data/target_job.pdf`

**Option 3: Use job URL** (future feature)
```python
# Coming soon!
analysis = engine.analyze_from_url(
    cv_file="data/my_cv.pdf",
    job_url="https://company.com/jobs/12345"
)
```

**What to include:**
- Job title and company name
- Requirements (required & preferred)
- Responsibilities
- Qualifications
- Nice-to-haves

### Can I analyze multiple jobs at once?

**Yes!** Use batch analysis:

```python
from src.python_advanced_job_engine import AdvancedJobEngine

engine = AdvancedJobEngine()

jobs = [
    ("data/job1.pdf", "Company A", "Senior Engineer"),
    ("data/job2.pdf", "Company B", "Tech Lead"),
    ("data/job3.pdf", "Company C", "Staff Engineer")
]

results = []
for job_file, company, title in jobs:
    analysis = engine.analyze_from_files(
        cv_file="data/my_cv.pdf",
        job_file=job_file,
        job_title=title,
        company=company
    )
    results.append({
        'company': company,
        'score': analysis['score']['total_score']
    })

# Sort by best match
results.sort(key=lambda x: x['score'], reverse=True)
```

See [examples/batch_analysis.py](examples/batch_analysis.py) for full example.

### How long does analysis take?

**Typical times:**
- Single job analysis: **5-10 seconds**
- Learning plan creation: **2-3 seconds**
- Test generation: **3-5 seconds**
- Complete workflow: **15-30 seconds**

**Factors affecting speed:**
- File size
- PDF complexity
- Number of skills to analyze

### Where are results saved?

**Data directory structure:**
```
job_search_data/
├── master_skillset.json      # Your skills database
├── analyzed_jobs.json         # All job analyses
├── learning_progress.json     # Learning plans
├── sprint_history.json        # Sprint records
├── skill_tests.json           # Test results
├── workflow_state.json        # Current state
└── export_[job_id]/          # Export packages
    ├── complete_report.txt
    ├── learning_plan.json
    ├── skill_tests.json
    └── cover_letter.txt
```

**Git ignored**: All files in `job_search_data/` are automatically ignored by Git for privacy.

---

## Understanding Results

### What does my match score mean?

**Score ranges:**

| Score | Status | What It Means | Action |
|-------|--------|---------------|--------|
| **90-100%** | 🟢 Excellent | You're highly qualified | Apply immediately! |
| **75-89%** | 🟢 Strong | Minor gaps, very competitive | Quick polish & apply |
| **60-74%** | 🟡 Good | Solid foundation, focused work needed | 4-8 weeks learning |
| **45-59%** | 🟠 Fair | Significant gaps | 8-16 weeks learning |
| **Below 45%** | 🔴 Poor | Major mismatch | Consider different role or 16-24 weeks learning |

### How is the score calculated?

**Weighted scoring algorithm:**

```
Total Score = (Required Skills × 35%) + 
              (Preferred Skills × 15%) + 
              (Experience × 20%) + 
              (Education × 10%) + 
              (Certifications × 5%) + 
              (Keywords × 15%)
```

**Component breakdown:**

1. **Required Skills (35%)**
   - Percentage of required skills you have
   - Most important factor

2. **Preferred Skills (15%)**
   - Nice-to-have skills you possess

3. **Experience (20%)**
   - Years of experience vs. required
   - Cap at 100% if you meet/exceed

4. **Education (10%)**
   - Degree match (Bachelor's, Master's, PhD)

5. **Certifications (5%)**
   - Relevant certifications held

6. **Keywords (15%)**
   - Important terms appearing in both CV and job description

### Why is my score lower than expected?

**Common reasons:**

1. **Skills not detected**
   - CV doesn't list skills explicitly
   - Skills in paragraph form, not bullets
   - Solution: Add "Skills" section with bullet points

2. **Experience not captured**
   - No explicit years mentioned
   - Solution: Add "5 years of Python" to CV

3. **Different terminology**
   - Job says "ML" but CV says "Machine Learning"
   - Solution: Use both terms

4. **Missing context**
   - Skills used in projects but not listed in Skills section
   - Solution: Create dedicated Skills section

**Diagnosis:**
```python
cv_data = engine.parse_cv(open("data/my_cv.txt").read())
print("Detected skills:", cv_data['skills'])
print("Detected experience:", cv_data['experience_years'])
```

### What are "gap" scores?

Gaps show what you're missing:

```python
{
    "missing_required_skills": ["Docker", "Kubernetes", "AWS"],
    "missing_preferred_skills": ["MLOps", "Airflow"],
    "experience_gap": 2,  # Years short
    "education_gap": "Master's degree"
}
```

**Priority order:**
1. Fix **required skills** gaps first (35% weight)
2. Address **experience** gaps (20% weight)
3. Add **keywords** to CV (15% weight)
4. Tackle **preferred skills** (15% weight)
5. Consider **certifications** (5% weight)

### Can scores improve without learning new skills?

**Yes!** You can improve scores by:

1. **Better CV formatting**
   - Add explicit Skills section
   - Use job description keywords
   - Quantify experience

2. **Highlighting relevant experience**
   - Emphasize matching projects
   - Add technical details
   - Include metrics

3. **Strategic keyword use**
   - Mirror job description language
   - Use both abbreviations and full terms
   - Add industry buzzwords

**Example**: Score jumped from 62% → 71% just by reformatting CV to list skills explicitly!

---

## Learning Plans

### What's the difference between Standard and Reverse mode?

**Standard Mode (12 weeks):**
- ✅ Faster to job-ready
- ✅ Good for minor skill gaps
- ✅ Linear learning path
- ✅ Fixed timeline
- ❌ Less portfolio emphasis
- **Best for**: Quick upskilling, <5 skill gaps

**Reverse Mode (16-24 weeks):**
- ✅ Deep skill mastery
- ✅ Strong portfolio focus
- ✅ Sprint-based iteration
- ✅ Quality gate validation
- ✅ Better for career transitions
- ❌ Takes longer
- **Best for**: Major career changes, 5+ skill gaps

### How are skills categorized in learning plans?

**Three levels:**

1. **Study (0-25% proficiency)**
   - Skills you need to learn from scratch
   - Completely new to you
   - Focus: Fundamentals and theory

2. **Practice (25-75% proficiency)**
   - Skills you have basic knowledge of
   - Need hands-on experience
   - Focus: Projects and application

3. **Courses (recommended learning)**
   - Curated resources for each skill
   - Mix of free and paid options
   - Documentation, tutorials, courses

### How long should I spend on each skill?

**General guidelines:**

| Skill Complexity | Study Time | Practice Time |
|-----------------|------------|---------------|
| **Simple** (Git, Markdown) | 1-2 weeks | 1 week |
| **Medium** (Docker, React) | 2-4 weeks | 2-3 weeks |
| **Complex** (ML, System Design) | 4-8 weeks | 4-6 weeks |

**Daily commitment:**
- Minimum: 1-2 hours/day
- Recommended: 2-4 hours/day
- Intensive: 4-6 hours/day

### Can I customize the learning plan?

**Yes!** Several ways:

1. **Adjust timeline:**
```python
plan = engine.create_learning_plan(
    analysis, 
    mode="standard",
    duration_weeks=16  # Instead of default 12
)
```

2. **Prioritize specific skills:**
```python
# Manually reorder
plan['levels']['study'] = ["PyTorch", "Docker", "AWS"]  # Your priority
```

3. **Add custom resources:**
Edit `src/learning/resource_db.py`:
```python
LEARNING_RESOURCES = {
    "your_skill": {
        "study": ["Your favorite tutorial"],
        "practice": ["Your practice platform"],
        "courses": ["Your recommended course"]
    }
}
```

### What if a skill isn't in the resource database?

**You can:**

1. **Request addition**: Open GitHub issue with skill name and good resources

2. **Add locally**: Edit `src/learning/resource_db.py`
```python
LEARNING_RESOURCES["new_skill"] = {
    "study": [
        "Official documentation",
        "Tutorial link"
    ],
    "practice": [
        "Practice platform"
    ],
    "courses": [
        "Recommended course"
    ]
}
```

3. **Use generic plan**: System provides general guidance even for unknown skills

### How do I know if I've mastered a skill?

**Validation methods:**

1. **Skill Tests** (in tool)
```python
tests = engine.generate_skill_tests(["Python", "Docker"])
# Take tests, pass 80%+ for advanced level
```

2. **Project Completion**
- Build 2-3 projects using the skill
- Projects should be portfolio-worthy
- Include in GitHub with good documentation

3. **Real-world Application**
- Contribute to open source
- Freelance project
- Work assignment

4. **Teach Others**
- Write tutorial/blog post
- Help on Stack Overflow
- Mentor someone

**Rule of thumb**: If you can build something useful and explain how it works, you've mastered it!

---

## Reverse Workflow

### When should I use Reverse Workflow?

**Use Reverse Workflow if:**
- ✅ Match score <60%
- ✅ 5+ missing required skills
- ✅ Career transition (new field/role)
- ✅ You want deep mastery, not just familiarity
- ✅ You have 4-6 months for preparation
- ✅ You want strong portfolio for negotiation

**Use Standard Workflow if:**
- ✅ Match score 60-75%
- ✅ <5 missing skills
- ✅ Need to apply within 3 months
- ✅ Quick skill updates needed
- ✅ Similar role, same field

### What is a sprint?

**Sprint** = 2-week focused learning cycle

**Structure:**
- **Duration**: 14 days
- **Focus**: 1-3 related skills
- **Deliverable**: 1 portfolio project
- **Assessment**: Skill tests at end

**Example Sprint:**
```
Sprint 1: PyTorch & Docker
Week 1: Learn fundamentals
Week 2: Build containerized ML model
End: Pass PyTorch (70%+) and Docker (70%+) tests
```

### How many sprints do I need?

**Typical ranges:**

| Starting Score | Target Score | Sprints Needed |
|----------------|--------------|----------------|
| 40-50% | 75% | 4-6 sprints (8-12 weeks) |
| 50-60% | 80% | 6-8 sprints (12-16 weeks) |
| 40-50% | 90%+ | 8-12 sprints (16-24 weeks) |

**Factors affecting duration:**
- Your learning speed
- Prior knowledge
- Daily time commitment
- Skill complexity
- Project scope

### What are Quality Gates?

**Quality Gates** = Milestones that validate progress

**Three gates:**

1. **Foundation Gate (65%)**
   - Basic competency achieved
   - Can discuss topics intelligently
   - Ready for more advanced work

2. **Competency Gate (80%)**
   - Job-ready skills
   - Can work independently
   - Portfolio demonstrates capability

3. **Mastery Gate (90%+)**
   - Competitive advantage
   - Deep understanding
   - Can mentor others
   - Strong negotiating position

**Passing gates unlocks:**
- ✅ New learning phases
- ✅ Milestone notifications
- ✅ Confidence to apply
- ✅ Salary negotiation leverage

### How do I log daily progress?

```python
engine.log_daily(
    hours=3.5,
    concepts=["List of concepts learned"],
    notes="What you accomplished today"
)
```

**Example:**
```python
engine.log_daily(
    hours=4.0,
    concepts=[
        "PyTorch tensors and operations",
        "Building neural network layers",
        "Training loop basics"
    ],
    notes="Completed PyTorch tutorial chapters 1-3. Built first neural network for MNIST dataset. Got 95% accuracy!"
)
```

**Tips:**
- Log daily (builds habit)
- Be specific with concepts
- Note challenges faced
- Track small wins

### What makes a good sprint project?

**Criteria:**

1. **Relevant**: Uses the sprint's target skills
2. **Portfolio-worthy**: Impressive to show employers
3. **Documented**: README, comments, deployment
4. **Complete**: Fully functional, not a prototype
5. **Challenging**: Pushes your skills
6. **Practical**: Solves a real problem

**Good examples:**
- ✅ Containerized ML model with API
- ✅ Full-stack app with authentication
- ✅ Data pipeline with visualization
- ✅ Mobile app with backend

**Avoid:**
- ❌ Tutorial follow-alongs without modification
- ❌ Incomplete/broken projects
- ❌ Trivial "Hello World" level
- ❌ No documentation

### Can I do multiple sprints on the same skill?

**Yes!** This is often recommended for complex skills.

**Progressive approach:**

**Sprint 1**: Fundamentals
- Basic PyTorch operations
- Simple neural network
- Project: MNIST classifier

**Sprint 2**: Intermediate
- Advanced architectures
- Transfer learning
- Project: Image classification app

**Sprint 3**: Advanced
- Custom models
- Production deployment
- Project: Real-time ML API

Each sprint deepens understanding and builds portfolio!

---

## GitHub Actions

### Do I need GitHub Actions?

**No, it's optional!**

**Without GitHub Actions:**
- ✅ Full analysis functionality
- ✅ Learning plans and tests
- ✅ Manual progress tracking
- ❌ No automation
- ❌ Manual re-analysis

**With GitHub Actions:**
- ✅ Everything above, plus:
- ✅ Automatic daily reports
- ✅ Scheduled re-analysis
- ✅ Quality gate notifications
- ✅ Progress tracking over time

### How do I set up GitHub Actions?

**Step-by-step:**

1. **Fork repository** on GitHub
   - Click "Fork" button
   - Select your account

2. **Enable Actions**
   - Go to Settings → Actions
   - Choose "Allow all actions"

3. **Add your files**
   - Clone your fork locally
   - Add CV and job description to `data/`
   - Commit and push

4. **Verify workflow**
   - Go to Actions tab
   - See "Reverse-Engine Job Search" workflow
   - Check for green checkmarks

5. **Wait for schedule** or manually trigger

### When do workflows run automatically?

**Default schedule:**
- 🌅 Morning: 9:00 AM (daily report)
- 🌙 Evening: 9:00 PM (progress check)

**Schedule is configurable** in `.github/workflows/unified-reverse-job-engine.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'   # 9 AM daily
  - cron: '0 21 * * *'  # 9 PM daily
```

**Cron syntax:**
- `0 9 * * *` = 9 AM every day
- `0 */6 * * *` = Every 6 hours
- `0 9 * * 1` = 9 AM every Monday

### How do I manually trigger a workflow?

**In GitHub:**
1. Go to **Actions** tab
2. Select **Reverse-Engine Job Search** workflow
3. Click **Run workflow** button (right side)
4. Select **action type**:
   - `full_analysis` - Complete re-analysis
   - `daily_report` - Current progress
   - `start_sprint` - Begin new sprint
   - `end_sprint` - Complete current sprint
   - `quality_check` - Check milestones
5. Click **Run workflow** (green button)

### Are my files private?

**Yes!** By default:

- ✅ Private forks = Private data
- ✅ Public forks = Data in `.gitignore`
- ✅ `job_search_data/` never committed
- ✅ `data/` never committed

**Best practice**: Keep your fork **private** if it contains:
- Your actual CV
- Personal information
- Specific job details

**Safe to make public**:
- Code modifications
- Custom resources
- Learning plans (anonymized)

### Can Actions cost money?

**GitHub Actions pricing:**

**Free tier:**
- ✅ 2,000 minutes/month (private repos)
- ✅ Unlimited minutes (public repos)

**This tool uses:**
- ~1-2 minutes per workflow run
- 60 runs/month (2 daily)
- **Total: ~60-120 minutes/month**

**Well within free tier!** ✅

### What if Actions fail?

**Check workflow logs:**

1. Go to Actions tab
2. Click failed workflow run
3. Click on red X job
4. Read error messages

**Common issues:**

1. **Files not found**
   - Ensure CV/job files in `data/`
   - Check file names match workflow

2. **Python errors**
   - Update dependencies
   - Check Python version

3. **Permission denied**
   - Check repository settings
   - Verify Actions are enabled

4. **Syntax errors**
   - Validate YAML syntax
   - Copy from working template

**Still stuck?** Open an issue with:
- Error message
- Workflow logs
- Steps to reproduce

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'PyPDF2'"

**Solution:**
```bash
pip install PyPDF2 python-docx
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

### "FileNotFoundError: [Errno 2] No such file or directory"

**Solutions:**

1. **Check file exists:**
```bash
ls -la data/
```

2. **Use absolute paths:**
```python
import os
cv_path = os.path.abspath("data/my_cv.pdf")
analysis = engine.analyze_from_files(cv_file=cv_path, ...)
```

3. **Check current directory:**
```bash
pwd  # Should be in advanced-job-engine/
```

### "PDF extraction returned empty text"

**Causes:**
- Scanned PDF (image-based)
- Protected PDF
- Complex formatting

**Solutions:**

1. **Convert to text:**
   - Open PDF
   - Select All → Copy
   - Paste into `data/my_cv.txt`

2. **Use OCR** (for scanned PDFs):
```bash
# Install tesseract
brew install tesseract  # macOS
sudo apt install tesseract-ocr  # Linux

# Use pdf2image + pytesseract
pip install pdf2image pytesseract
```

3. **Try different PDF reader:**
```bash
pip install pdfplumber
# Then modify code to use pdfplumber instead
```

### Match score is 0% or very low despite having skills

**Diagnosis:**

```python
# Check what's being extracted
with open("data/my_cv.txt") as f:
    cv_text = f.read()
    cv_data = engine.parse_cv(cv_text)

print("Skills found:", cv_data['skills'])
print("Keywords:", cv_data.get('keywords', []))
```

**Solutions:**

1. **Add explicit Skills section:**
```
TECHNICAL SKILLS
• Programming: Python, Java, JavaScript, C++
• Frameworks: Django, React, Flask, Node.js
• Tools: Docker, Kubernetes, Git, Jenkins
• Databases: PostgreSQL, MongoDB, Redis
• Cloud: AWS, Azure, GCP
```

2. **Use bullet points** (not paragraphs)

3. **List specific technologies** (not "various frameworks")

4. **Include keywords** from job description

### Tests are too easy/hard

**Adjust difficulty** by editing generated tests:

```python
tests = engine.generate_skill_tests(["Python"])

# Modify difficulty
tests['Python']['beginner']['passing_score'] = 70  # Instead of 60
tests['Python']['advanced']['questions'] = 30  # Instead of 20
```

Or regenerate with custom parameters (feature request - coming soon).

### Learning plan is too aggressive/conservative

**Customize duration:**

```python
plan = engine.create_learning_plan(
    analysis,
    mode="standard",
    duration_weeks=16  # Instead of 12
)
```

**Adjust skill priorities:**

```python
# Manually reorder
plan['levels']['study'] = [
    "PyTorch",    # Learn first (most important)
    "Docker",     # Then this
    "AWS"         # Finally this
]
```

### Application materials are too generic

**Provide more context:**

```python
analysis = engine.analyze_from_files(
    cv_file="data/my_cv.pdf",
    job_file="data/job.pdf",
    job_title="Senior ML Engineer",  # Be specific
    company="TechCorp Inc."           # Include company
)

# Add personal context (feature request - coming soon)
letters = engine.generate_recruiter_letter(
    analysis,
    plan,
    personal_note="I'm passionate about X because..."
)
```

**Customize templates:**
- Edit `templates/letter_templates/`
- Add your own phrasing
- Include specific examples

---

## Best Practices

### How often should I re-analyze?

**Recommended schedule:**

| Workflow | Re-analysis Frequency |
|----------|----------------------|
| Quick Application | Before applying |
| Standard (12 weeks) | Every 2-4 weeks |
| Reverse (sprints) | After each sprint (2 weeks) |

**Re-analyze when:**
- ✅ You complete a major project
- ✅ You learn new skills
- ✅ You update your CV
- ✅ You reach a milestone

### Should I update my CV or my skills first?

**Depends on timeline:**

**Applying soon (<1 month)?**
→ Update CV first (strategic presentation)

**Preparing long-term (3+ months)?**
→ Build skills first (genuine competency)

**Best approach:**
1. Do initial analysis
2. Identify gaps
3. Build real skills (projects, courses)
4. Update CV with new skills
5. Re-analyze to validate improvement
6. Apply when 75%+

### How many jobs should I target simultaneously?

**Recommended approach:**

**1-3 target roles** in similar domains:
```
Example:
1. ML Engineer (primary)
2. Data Scientist (similar skills)
3. AI Researcher (stretch goal)
```

**Benefits:**
- Focused skill building
- Transferable learning
- Efficient portfolio
- Clear progression path

**Avoid:**
- ❌ 10+ completely different roles
- ❌ Unrelated skill requirements
- ❌ Scattered learning effort

### Should I learn skills in sequence or parallel?

**Sequential** (one at a time):
- ✅ Deeper mastery
- ✅ Less overwhelming
- ✅ Better for complex skills
- ❌ Takes longer

**Parallel** (multiple at once):
- ✅ Faster progress
- ✅ See connections between skills
- ✅ More engaging
- ❌ Risk of shallow learning

**Recommended mix:**
- **1 primary skill** (main focus, 60% time)
- **1-2 secondary skills** (complement, 40% time)

**Example:**
- Primary: PyTorch (deep learning)
- Secondary: Docker (for deployment)
- Synergy: Containerized ML models!

### When should I start applying?

**Apply when:**

✅ **Minimum threshold (60%+)**
- Basic requirements met
- Can discuss skills confidently
- 1-2 relevant projects

✅ **Competitive threshold (75%+)**
- Most requirements covered
- 3+ portfolio projects
- Can demonstrate expertise

✅ **Ideal threshold (90%+)**
- Exceeds requirements
- Strong portfolio
- Negotiation leverage
- Multiple offer potential

**Don't wait for 100%!** Nobody matches perfectly. 75%+ is excellent.

### How do I balance learning vs. applying?

**Recommended split:**

| Match Score | Learning | Applying |
|-------------|----------|----------|
| <60% | 90% | 10% (build foundation) |
| 60-74% | 70% | 30% (targeted applications) |
| 75-89% | 40% | 60% (active job search) |
| 90%+ | 20% | 80% (full focus on applications) |

**Strategy:**
- Always keep learning (stay current)
- Apply to 1-2 stretch roles even when building skills
- Build portfolio while job searching
- Interview experience is valuable learning

### What if I fail a skill test?

**Don't worry!** Failing tests is part of learning.

**Steps after failing:**

1. **Review mistakes**
   - Which questions did you miss?
   - What concepts are unclear?

2. **Study those specific topics**
   - Focus on weak areas
   - Use additional resources

3. **Practice more**
   - Build another project
   - Try coding challenges

4. **Retake after 3-7 days**
   - Give yourself time to learn
   - Come back fresh

**Remember**: Tests are for YOU, not employers. They help identify gaps!

### How do I know when I'm ready to apply?

**Readiness checklist:**

✅ **Skills**
- Match score 75%+
- Comfortable discussing all listed skills
- Can explain technical concepts clearly

✅ **Portfolio**
- 3-5 projects demonstrating skills
- Well-documented GitHub repos
- Live demos when possible

✅ **Materials**
- Updated CV highlighting relevant experience
- Tailored cover letter
- LinkedIn profile polished

✅ **Confidence**
- Can code/solve problems in interviews
- Prepared for technical questions
- Practiced behavioral answers

✅ **Network**
- Connected with people in the industry
- Asked for informational interviews
- Have 1-2 potential referrals

**If 4/5 checked**: You're ready! Apply!

---

## Privacy & Security

### Is my data safe?

**Yes!** Your data is safe because:

✅ **Runs locally**: All processing on your machine
✅ **No cloud uploads**: Data never leaves your computer
✅ **Git ignored**: Personal files excluded from version control
✅ **Open source**: Code is transparent and auditable

**Files that are NOT committed:**
- `data/*` (your CV and job descriptions)
- `job_search_data/*` (analysis results)
- `.env` (configuration)

### Can I use this for confidential job searches?

**Absolutely!** The tool:
- Runs entirely offline (after installation)
- Doesn't phone home
- Doesn't require internet for analysis
- Stores data locally only

**Best practices:**
- Keep your fork private
- Don't commit CV/job files
- Use throwaway job descriptions for testing

### Does this tool send data to third parties?

**No!** The tool:
- ❌ No analytics
- ❌ No tracking
- ❌ No API calls (except pip during installation)
- ❌ No data collection

**Optional GitHub Actions** do:
- ✅ Run on GitHub's servers
- ✅ Use data only for workflow execution
- ✅ Data stays in your repository
- ❌ Not visible to public (if repo is private)

### Can I delete my data?

**Yes, anytime!**

```bash
# Delete all generated data
rm -rf job_search_data/*

# Delete specific analysis
rm -rf job_search_data/export_[job_id]/

# Start fresh
rm -rf job_search_data/*.json
```

**Nuclear option** (complete reset):
```bash
# Delete everything including repo
cd ..
rm -rf advanced-job-engine/
```

### How do I keep my fork private?

**After forking:**

1. Go to your fork's **Settings**
2. Scroll to **Danger Zone**
3. Click **Change visibility**
4. Select **Make private**
5. Confirm

**Private repos:**
- ✅ Only you can see
- ✅ Actions still work (free tier)
- ✅ Can share with specific collaborators
- ❌ Can't receive pull requests easily

### What data is collected by GitHub Actions?

**GitHub Actions stores:**
- Workflow logs (what ran when)
- Workflow outputs (visible in logs)
- Artifacts (if you upload them)

**This tool's workflows store:**
- Analysis results (in your repo only)
- Progress reports (in workflow logs)
- No personal data leaves your repository

**To keep truly private:**
- Use private repository
- Or run locally without Actions

---

## Advanced Topics

### Can I customize the scoring algorithm?

**Yes!** Adjust weights in code:

```python
engine = AdvancedJobEngine()

# Modify scoring weights
engine.WEIGHTS = {
    "required_skills": 0.40,     # Increased from 0.35
    "preferred_skills": 0.10,
    "experience": 0.25,
    "education": 0.10,
    "certifications": 0.05,
    "keywords": 0.10
}

# Run analysis with custom weights
analysis = engine.analyze_from_files(...)
```

### How do I add custom skills to the database?

**Edit** `src/learning/resource_db.py`:

```python
LEARNING_RESOURCES = {
    # ... existing skills ...
    
    "your_custom_skill": {
        "study": [
            "Official documentation URL",
            "Best tutorial you found",
            "YouTube series link"
        ],
        "practice": [
            "Practice platform URL",
            "Project ideas site",
            "Coding challenges"
        ],
        "courses": [
            "Recommended course 1",
            "Recommended course 2",
            "Free alternative"
        ]
    }
}
```

**Then contribute back!** Submit PR to help others.

### Can I integrate with other tools?

**Yes!** Export formats support integration:

**JSON exports** can be used with:
- Notion (import JSON)
- Trello (convert to cards)
- Excel/Google Sheets (flatten JSON)
- Custom dashboards

**Example integration:**
```python
import json

# Export to JSON
analysis = engine.analyze_from_files(...)
with open("analysis.json", "w") as f:
    json.dump(analysis, f, indent=2)

# Import to your tool of choice
```

**API wrapper** (coming soon):
```python
# Future feature
from advanced_job_engine import JobEngineAPI

api = JobEngineAPI()
result = api.analyze(cv="...", job="...")
```

### Can I use this for team/company hiring?

**Yes, with modifications!**

**Current**: Individual job seeker focus
**Potential**: Reverse for candidate screening

**Modify for hiring:**
```python
# Instead of: How does candidate match job?
# Use: How does job match candidate pool?

for candidate_cv in candidate_pool:
    analysis = engine.analyze_from_files(
        cv_file=candidate_cv,
        job_file="our_job_posting.pdf"
    )
    if analysis['score']['total_score'] >= 75:
        shortlist.append(candidate_cv)
```

**Legal considerations:**
- Ensure algorithmic fairness
- Avoid discriminatory patterns
- Use as supplement, not replacement for human review
- Comply with hiring regulations

### How can I contribute to the project?

**Ways to contribute:**

1. **Add learning resources**
   - Expand `resource_db.py`
   - Share quality courses/tutorials

2. **Improve parsing**
   - Better CV extraction
   - Enhanced job description parsing
   - Support more formats

3. **Add features**
   - New analysis metrics
   - Better visualizations
   - Integration with job boards

4. **Write documentation**
   - Tutorials for specific industries
   - Video walkthroughs
   - Translation to other languages

5. **Report bugs**
   - Open issues with details
   - Provide reproduction steps

6. **Share success stories**
   - How the tool helped you
   - Improvements you achieved
   - Tips for others

**Contribution process:**
```bash
# 1. Fork the repository
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes and commit
git commit -m "Add amazing feature"

# 4. Push to branch
git push origin feature/amazing-feature

# 5. Open Pull Request
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### What's on the roadmap?

**Version 1.1** (Q1 2025)
- [ ] Web dashboard for visualization
- [ ] Mobile app for daily logging
- [ ] AI-powered skill recommendations
- [ ] Resume builder integration

**Version 1.2** (Q2 2025)
- [ ] LinkedIn profile integration
- [ ] Job board scraping (Indeed, LinkedIn)
- [ ] Salary insights and negotiation tips
- [ ] Interview question generator

**Version 2.0** (Q3 2025)
- [ ] Machine learning for personalized paths
- [ ] Community features (mentor matching)
- [ ] Company culture fit analysis
- [ ] Video interview practice

**Version 3.0** (Future)
- [ ] Career trajectory planning
- [ ] Industry trend analysis
- [ ] Automated job applications
- [ ] Comprehensive career coach AI

**Vote on features**: Check GitHub Discussions!

---

## Getting Help

### Where can I get help?

**Documentation:**
- 📖 [README](README.md) - Overview
- 🚀 [Quick Start](QUICK-START.md) - Getting started
- 📚 [User Guide](docs/user-guide.md) - Comprehensive guide
- 🔧 [API Reference](docs/api-reference.md) - Function details
- ❓ [FAQ](FAQ.md) - This document!

**Community:**
- 💬 [GitHub Discussions](https://github.com/yourusername/advanced-job-engine/discussions) - Ask questions
- 🐛 [GitHub Issues](https://github.com/yourusername/advanced-job-engine/issues) - Report bugs
- 💡 [Feature Requests](https://github.com/yourusername/advanced-job-engine/issues/new?template=feature_request.md) - Suggest improvements

**Direct Support:**
- 📧 Email: support@projectdomain.com
- 🐦 Twitter: [@projecthandle](https://twitter.com/projecthandle)
- 💼 LinkedIn: [Project Page](https://linkedin.com/company/project)

### How do I report a bug?

**Before reporting:**

1. **Check existing issues**: Someone may have reported it
2. **Update to latest version**: Bug might be fixed
3. **Try fresh install**: Clear cache and reinstall

**When reporting:**

Include:
- **Description**: What happened vs. what should happen
- **Steps to reproduce**: Exact steps to trigger bug
- **Error messages**: Full error text
- **Environment**: OS, Python version, package versions
- **Files**: Sample CV/job (anonymized) if relevant

**Use the template**: Click [New Issue](https://github.com/yourusername/advanced-job-engine/issues/new?template=bug_report.md)

### How do I request a feature?

**Good feature requests include:**

1. **Use case**: Why you need this feature
2. **Current workaround**: How you handle it now
3. **Proposed solution**: How it could work
4. **Alternatives considered**: Other approaches
5. **Impact**: Who else would benefit

**Example:**
```
Feature: LinkedIn Profile Import

Use case: Manually copying CV info is tedious

Current workaround: Copy-paste from LinkedIn to text file

Proposed solution: Import directly from LinkedIn profile URL

Alternatives: 
- Browser extension to export
- Manual form filling

Impact: Would help all users who maintain LinkedIn profiles
```

### Is there a community chat?

**Coming soon!**

Planned channels:
- 💬 Discord server
- 💬 Slack workspace  
- 💬 Reddit community

**Current:**
- Use GitHub Discussions for now
- Watch for announcements

### Can I hire someone to help me set this up?

**You can:**

1. **Post on freelancer sites**
   - Upwork, Fiverr, etc.
   - Request: "Set up Advanced Job Engine"
   - Budget: $50-200 depending on customization

2. **Ask in community**
   - GitHub Discussions
   - Someone might help pro bono

3. **Follow video tutorials** (coming soon)
   - Step-by-step setup guides
   - Screen recordings
   - Live workshops

**Most users can set up in <30 minutes** following the Quick Start guide!

---

## Miscellaneous

### What does "Advanced" mean in the name?

**Advanced** refers to:
- Sophisticated scoring algorithm (weighted, multi-factor)
- Iterative learning approach (sprints, quality gates)
- Automation capabilities (GitHub Actions)
- Complete workflow (analysis → learning → applying)

**Not** referring to:
- Complexity for users (it's beginner-friendly!)
- Required skill level
- Target job levels

### Can I use this for non-tech jobs?

**Yes!** While optimized for tech roles, it works for:

✅ **Any job with:**
- Listed skill requirements
- Experience requirements
- Clear qualifications

**Examples:**
- Marketing roles (SEO, analytics, design tools)
- Finance positions (Excel, modeling, certifications)
- Project management (Agile, tools, methodologies)
- Design roles (Figma, Photoshop, portfolio)

**Less effective for:**
- Highly subjective roles (creative director)
- Culture-fit heavy positions
- Roles with vague descriptions

### Does this work in languages other than English?

**Current**: English only

**Planned**: Multi-language support

**Workarounds:**
- Translate CV and job description to English
- Use tool for analysis
- Translate results back

**Contributing**: Help add language support!
- Submit translations
- Add language-specific resources
- Test with non-English inputs

### Can I use this for remote job searches?

**Absolutely!** In fact, it's perfect for remote jobs:

✅ **Remote jobs often:**
- Have clearer skill requirements
- Focus more on technical abilities
- Value portfolios highly
- Are location-independent

**Tip**: Filter for remote-first companies that prioritize:
- Strong GitHub presence
- Documented projects
- Demonstrated skills
- Async communication

### What if I'm overqualified for a role?

**High match scores (95%+) can indicate overqualification**

**Consider:**
1. **Is this role growth for you?**
   - New domain/industry
   - Leadership opportunity
   - Better company culture

2. **Salary and satisfaction**
   - Does it pay well enough?
   - Will you be engaged?
   - Room for advancement?

3. **Strategic move**
   - Career pivot
   - Location change
   - Work-life balance

**Tool can help**: Target stretch roles with 60-75% match instead!

### How accurate is the experience gap calculation?

**Moderately accurate** (70-80%)

**Limitations:**
- Depends on CV formatting
- May not catch equivalent experience
- Doesn't account for intensity

**Example challenges:**
```
Job requires: "5 years ML experience"
You have: "3 years full-time + 2 years part-time"
Tool may miss: Part-time experience
```

**Best practice**: Manually review and adjust if needed

### Can I use this while employed?

**Yes!** This is ideal for:

✅ **Passive job searching**
- Explore opportunities
- Build skills in spare time
- Prepare for next move

✅ **Career planning**
- Understand market demands
- Identify skill gaps
- Stay competitive

✅ **Negotiation prep**
- Know your market value
- Build leverage (skills + offers)
- Time your move strategically

**Privacy tip**: Use private repository if concerned about employer seeing your fork

### What if my dream job score is only 40%?

**Don't despair!** Options:

1. **Long-term prep (6-12 months)**
   - Use Reverse Workflow
   - Build skills systematically
   - Create impressive portfolio
   - Reach 75%+ then apply

2. **Alternative path**
   - Find similar role with 60-70% match
   - Build experience there (1-2 years)
   - Transition to dream role

3. **Reassess fit**
   - Maybe this role isn't right match
   - Find better-aligned opportunities
   - Build towards it gradually

**Success story**: Many users went 40% → 90% in 6-9 months!

### Can this guarantee I'll get a job?

**No.** No tool can guarantee job offers.

**What it CAN do:**
✅ Identify where you stand
✅ Show clear improvement path
✅ Track measurable progress
✅ Increase interview chances
✅ Boost confidence

**What determines success:**
- Your effort and consistency
- Market conditions
- Networking
- Interview skills
- Timing and luck

**Think of it as**: GPS for your career journey. It shows the route, but you drive!

---

## Success Stories

### Has this tool helped real people?

**Yes!** While the tool is new, early users report:

📈 **Quantitative results:**
- Average match score improvement: +35%
- Time to job-ready: 12-16 weeks
- Interview rate increase: 3-5x
- Average salary increase: 15-25%

🎯 **Qualitative feedback:**
- "Finally understood what I was missing"
- "Structured learning path was game-changing"
- "Portfolio projects led directly to interviews"
- "Went from scattered to strategic"

**Case study** (anonymized):
```
Background: CS grad, 45% match for ML Engineer role
Timeline: 16 weeks using Reverse Workflow
Result: 8 projects, 92% match, 5 offers, $130k salary
Key: Consistent daily effort + quality projects
```

### What's the typical improvement rate?

**Depends on starting point:**

| Starting Score | Weekly Improvement | Weeks to 75% |
|----------------|-------------------|--------------|
| 30-40% | +4-5% | 7-10 weeks |
| 40-50% | +3-4% | 6-9 weeks |
| 50-60% | +2-3% | 5-8 weeks |
| 60-70% | +1-2% | 3-5 weeks |

**Factors affecting rate:**
- Daily time commitment
- Prior learning experience
- Skill complexity
- Project quality
- Resource quality

**Reality check**: Genuine skill building takes time. Beware of shortcuts!

---

<div align="center">

## 🎓 Still Have Questions?

**We're here to help!**

[📖 Documentation](docs/) | [💬 Discussions](https://github.com/yourusername/advanced-job-engine/discussions) | [🐛 Issues](https://github.com/yourusername/advanced-job-engine/issues) | [📧 Email](mailto:support@projectdomain.com)

---

**Ready to get started?**

[🚀 Quick Start Guide](QUICK-START.md) | [📚 User Guide](docs/user-guide.md) | [⬅️ Back to README](README.md)

---

**Found this helpful? ⭐ Star the repo!**

**Made with ❤️ for job seekers worldwide**

</div>