#!/bin/bash
# Setup script for Reverse-Engine Job Search System
# Run this after cloning the repo

set -e  # Exit on error

echo "🚀 Setting up Reverse-Engine Job Search System..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Create directory structure
echo "📁 Creating directory structure..."
mkdir -p .github/workflows
mkdir -p src
mkdir -p data
mkdir -p job_search_data

# Create .gitkeep files
touch data/.gitkeep
touch job_search_data/.gitkeep

echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# Step 2: Create requirements.txt
echo "📦 Creating requirements.txt..."
cat > requirements.txt << 'EOF'
PyPDF2>=3.0.0
python-docx>=0.8.11
python-dateutil>=2.8.2
EOF
echo -e "${GREEN}✅ requirements.txt created${NC}"
echo ""

# Step 3: Create .gitignore
echo "🔒 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Job search data (contains personal info)
job_search_data/
*.json

# Personal data files (KEEP PRIVATE!)
data/my_cv.txt
data/my_cv.pdf
data/my_cv.docx
data/target_job.txt
data/target_job.pdf
data/target_job.docx

# Keep directory structure
!data/.gitkeep
!job_search_data/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo
*.sublime-*

# OS
.DS_Store
Thumbs.db
desktop.ini

# Reports and exports
PROGRESS_REPORT.md
export_*/

# Test coverage
.coverage
htmlcov/
.pytest_cache/

# Logs
*.log
EOF
echo -e "${GREEN}✅ .gitignore created${NC}"
echo ""

# Step 4: Create sample CV template
echo "📄 Creating CV template..."
cat > data/my_cv_template.txt << 'EOF'
[Your Name]
[Your Title]
[your.email@example.com] | [+1-XXX-XXX-XXXX]

SUMMARY
Brief professional summary here...

EXPERIENCE
Job Title at Company Name (YYYY-YYYY)
- Achievement or responsibility 1
- Achievement or responsibility 2
- Achievement or responsibility 3

Previous Job Title at Previous Company (YYYY-YYYY)
- Achievement or responsibility 1
- Achievement or responsibility 2

SKILLS
Programming Languages: Python, JavaScript, Java
Frameworks: Django, Flask, React, Node.js
Tools: Docker, Kubernetes, Git, Jenkins
Databases: PostgreSQL, MongoDB, MySQL
Cloud: AWS, Azure, GCP

EDUCATION
Degree Name, University Name (YYYY)
- Relevant coursework or achievements

CERTIFICATIONS
- Certification Name (if applicable)

PROJECTS
- Project Name: Brief description
- Another Project: Brief description
EOF
echo -e "${GREEN}✅ CV template created at data/my_cv_template.txt${NC}"
echo ""

# Step 5: Create sample job description template
echo "📋 Creating job description template..."
cat > data/target_job_template.txt << 'EOF'
[Job Title]

Company: [Company Name]

ABOUT THE ROLE
Brief description of the position...

REQUIRED SKILLS:
- X+ years of experience in [field]
- Strong proficiency in [skill 1]
- Experience with [skill 2] and [skill 3]
- Knowledge of [skill 4]
- [Other requirements]

PREFERRED SKILLS:
- Experience with [preferred skill 1]
- Familiarity with [preferred skill 2]
- [Other nice-to-haves]

RESPONSIBILITIES:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]
- [Responsibility 4]

QUALIFICATIONS:
- Bachelor's/Master's degree in [field] or related field
- X+ years of professional experience
- Strong problem-solving and communication skills
- Ability to work in a team environment

NICE TO HAVE:
- [Bonus skill 1]
- [Bonus skill 2]
- Open source contributions
EOF
echo -e "${GREEN}✅ Job description template created at data/target_job_template.txt${NC}"
echo ""

# Step 6: Create README
echo "📖 Creating README.md..."
cat > README.md << 'EOF'
# Reverse-Engine Job Search System

Automated sprint-based job search and skill development system.

## 🚀 Quick Start

### 1. Add Your Data

```bash
# Copy templates and fill them out
cp data/my_cv_template.txt data/my_cv.txt
cp data/target_job_template.txt data/target_job.txt

# Edit with your actual information
nano data/my_cv.txt
nano data/target_job.txt
```

### 2. Install Dependencies (for local use)

```bash
pip install -r requirements.txt
```

### 3. Run Initial Analysis

#### Option A: GitHub Actions (Recommended)
1. Go to **Actions** tab
2. Select **"Reverse-Engine Job Search"** workflow
3. Click **"Run workflow"**
4. Select `full_analysis`
5. Enter paths: `data/my_cv.txt` and `data/target_job.txt`
6. Click **"Run workflow"**

#### Option B: Local Python
```bash
python src/python_advanced_job_engine.py
```

## 📊 Workflow Actions

| Action | Description | When to Use |
|--------|-------------|-------------|
| `full_analysis` | Analyze CV vs Job, create learning plan | First time & monthly |
| `start_sprint` | Begin 2-week learning sprint | Start of each sprint |
| `end_sprint` | Complete sprint, assess progress | End of each sprint |
| `daily_report` | View current progress dashboard | Daily/Weekly check-in |
| `quality_check` | Check quality gate status | Weekly |

## 📈 Typical Usage Flow

```
Week 1:  full_analysis → start_sprint
Week 2:  daily_report (monitor progress)
Week 3:  end_sprint → start_sprint (new sprint)
Week 4:  daily_report
Week 5:  end_sprint → quality_check
...repeat until ready to apply
```

## 🎯 Quality Gates

- **Foundation** (65%): 2 projects, beginner tests
- **Competency** (80%): 4 projects, intermediate tests
- **Mastery** (90%): 5 projects, advanced tests
- **Application Ready** (90%+): All gates + branding

## 📁 File Structure

```
.
├── .github/workflows/
│   └── reverse-engine.yml      # GitHub Actions workflow
├── src/
│   └── python_advanced_job_engine.py
├── data/
│   ├── my_cv.txt               # Your CV (YOU CREATE)
│   └── target_job.txt          # Target job (YOU CREATE)
└── job_search_data/            # Auto-generated
    ├── workflow_state.json
    ├── analyzed_jobs.json
    └── learning_progress.json
```

## 🔒 Privacy

- CV and job files are in `.gitignore`
- Personal data never committed to git
- All data stays in your repo
- Artifacts auto-delete after 90 days

## 💡 Pro Tips

1. **Log consistently**: Even 30 min/day counts
2. **Real projects**: Build deployable, not toy projects
3. **Update monthly**: Re-run analysis as you improve
4. **Track everything**: Use the daily logging
5. **Celebrate gates**: Each one is a milestone!

## 📝 Support

- Check workflow logs for errors
- Ensure Python 3.9+
- Verify file paths match
- Review .gitignore is working

## 📚 Documentation

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

---

**Status**: Ready to use! Start with `full_analysis` action.
EOF
echo -e "${GREEN}✅ README.md created${NC}"
echo ""

# Step 7: Check if files exist
echo "🔍 Checking for required files..."

missing_files=0

if [ ! -f "src/python_advanced_job_engine.py" ]; then
    echo -e "${YELLOW}⚠️  Missing: src/python_advanced_job_engine.py${NC}"
    echo "   You need to add this file manually"
    missing_files=$((missing_files + 1))
else
    echo -e "${GREEN}✅ Found: src/python_advanced_job_engine.py${NC}"
fi

if [ ! -f ".github/workflows/reverse-engine.yml" ]; then
    echo -e "${YELLOW}⚠️  Missing: .github/workflows/reverse-engine.yml${NC}"
    echo "   You need to add this file manually"
    missing_files=$((missing_files + 1))
else
    echo -e "${GREEN}✅ Found: .github/workflows/reverse-engine.yml${NC}"
fi

echo ""

# Step 8: Instructions
echo "🎉 Setup complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 NEXT STEPS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $missing_files -gt 0 ]; then
    echo -e "${YELLOW}1. Add the missing files listed above${NC}"
    echo ""
fi

echo "2. Create your CV file:"
echo "   cp data/my_cv_template.txt data/my_cv.txt"
echo "   # Then edit data/my_cv.txt with your info"
echo ""

echo "3. Create your job description file:"
echo "   cp data/target_job_template.txt data/target_job.txt"
echo "   # Then edit data/target_job.txt with target job"
echo ""

echo "4. Install Python dependencies (for local use):"
echo "   pip install -r requirements.txt"
echo ""

echo "5. Test locally (optional):"
echo "   python src/python_advanced_job_engine.py"
echo ""

echo "6. Commit and push to GitHub:"
echo "   git add ."
echo "   git commit -m \"Initial setup\""
echo "   git push"
echo ""

echo "7. Run first analysis on GitHub:"
echo "   • Go to Actions tab"
echo "   • Select 'Reverse-Engine Job Search' workflow"
echo "   • Click 'Run workflow'"
echo "   • Choose 'full_analysis'"
echo "   • Enter: data/my_cv.txt and data/target_job.txt"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✨ You're all set! Good luck with your job search! 🚀${NC}"
echo ""
