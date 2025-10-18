#!/bin/bash
# ===============================================================
# ONE-COMMAND SETUP for Job Search Automation
# ===============================================================
# Run this script to set up everything:
#   bash setup.sh
# ===============================================================

set -e  # Exit on error

echo "======================================================================"
echo "🚀 Job Search Automation - Complete Setup"
echo "======================================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# =====================================================================
# STEP 1: Create Directories
# =====================================================================

echo -e "${BLUE}📁 Step 1: Creating directory structure...${NC}"

mkdir -p data
mkdir -p job_search_data/templates
mkdir -p .github/workflows
mkdir -p src
mkdir -p output
mkdir -p batch_results

echo "✅ Directories created"

# =====================================================================
# STEP 2: Create Sample CV
# =====================================================================

echo -e "\n${BLUE}📄 Step 2: Creating sample CV...${NC}"

cat > data/my_cv.txt << 'CVEOF'
SARAH MARTINEZ
Senior Software Engineer

📧 sarah.martinez@email.com | 📱 +1 (555) 123-4567
🌐 github.com/smartinez | 💼 linkedin.com/in/smartinez
📍 San Francisco, CA

═══════════════════════════════════════════════════════════════

PROFESSIONAL SUMMARY

Results-driven Senior Software Engineer with 6+ years of experience building 
scalable web applications. Expertise in full-stack development using modern 
JavaScript frameworks and cloud technologies. Proven track record of leading 
technical initiatives and mentoring junior developers.

═══════════════════════════════════════════════════════════════

TECHNICAL SKILLS

Programming Languages:
• JavaScript/TypeScript (Expert) • Python (Advanced) • Java (Intermediate)
• SQL (Advanced) • HTML5/CSS3 (Expert)

Frontend: React.js, Vue.js, Next.js, Redux, Tailwind CSS
Backend: Node.js, Express.js, Django, Flask, GraphQL, REST APIs
Databases: PostgreSQL, MongoDB, Redis, MySQL
DevOps: AWS, Docker, Kubernetes, GitHub Actions, Jenkins, CI/CD
Tools: Git, JIRA, Jest, Cypress, DataDog

═══════════════════════════════════════════════════════════════

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | San Francisco, CA
March 2021 - Present

• Led development of customer dashboard serving 100K+ daily users with React 
  and TypeScript, improving load time by 45%
• Architected microservices infrastructure using Docker and Kubernetes
• Established CI/CD pipeline achieving 95% test coverage
• Mentored team of 4 junior developers
• Implemented GraphQL API reducing network requests by 60%
• Technologies: React, TypeScript, Node.js, PostgreSQL, Redis, AWS, Docker

Software Engineer | StartupXYZ | Mountain View, CA
June 2019 - February 2021

• Developed full-stack features for B2B SaaS platform using React and Python
• Built real-time analytics dashboard processing 1M+ events daily
• Optimized database queries reducing API response time by 70%
• Technologies: React, Python, Flask, PostgreSQL, Redis, AWS

Junior Developer | Digital Solutions Ltd. | San Jose, CA
August 2018 - May 2019

• Developed responsive web applications using React and Node.js
• Implemented automated testing with Jest and Cypress
• Technologies: React, Node.js, Express, MongoDB

═══════════════════════════════════════════════════════════════

EDUCATION

Bachelor of Science in Computer Science | GPA: 3.7/4.0
University of California, Berkeley
Graduated: May 2018

═══════════════════════════════════════════════════════════════

PROJECTS

E-Commerce Platform | github.com/smartinez/ecommerce
• Full-stack marketplace with 10K+ users
• Stack: Next.js, Node.js, PostgreSQL, Stripe, AWS

Data Visualization Dashboard | github.com/smartinez/dataviz
• Analytics platform processing 500K+ data points
• Stack: React, D3.js, Python, FastAPI, WebSocket

API Gateway | github.com/smartinez/api-gateway
• Microservices architecture handling 1M+ requests/day
• Stack: Node.js, Redis, Docker, Kubernetes

═══════════════════════════════════════════════════════════════

CERTIFICATIONS

✓ AWS Certified Solutions Architect - Associate (2022)
✓ MongoDB Certified Developer (2021)
✓ Certified Kubernetes Administrator (2023)
CVEOF

echo "✅ Created: data/my_cv.txt"

# =====================================================================
# STEP 3: Create Sample Job Description
# =====================================================================

echo -e "\n${BLUE}📋 Step 3: Creating sample job description...${NC}"

cat > data/target_job.txt << 'JOBEOF'
SENIOR FULL STACK ENGINEER

Company: InnovateTech Solutions
Location: San Francisco, CA (Hybrid)
Experience: 5-8 years
Salary: $150,000 - $200,000 + equity

═══════════════════════════════════════════════════════════════

ABOUT US

InnovateTech Solutions is a fast-growing fintech startup revolutionizing 
digital payments. We've raised $50M Series B and serve 1M+ customers.

═══════════════════════════════════════════════════════════════

THE ROLE

Senior Full Stack Engineer responsible for designing and implementing 
scalable web applications processing millions of transactions daily.

═══════════════════════════════════════════════════════════════

KEY RESPONSIBILITIES

• Design and develop full-stack features using React and Node.js
• Build and maintain microservices architecture
• Write clean, well-tested code following best practices
• Conduct code reviews and mentor junior developers
• Collaborate with cross-functional teams
• Optimize performance and database queries
• Implement security best practices
• Participate in on-call rotation

═══════════════════════════════════════════════════════════════

REQUIRED QUALIFICATIONS

Technical Skills:
• 5+ years professional software development experience
• Expert-level JavaScript/TypeScript proficiency
• Strong React.js and modern frontend experience
• Backend development with Node.js or Python
• PostgreSQL or similar relational databases
• RESTful API design and implementation
• Git and version control workflows
• Cloud platforms (AWS, GCP, or Azure)
• Docker and containerization
• CI/CD pipelines and DevOps practices

Soft Skills:
• Excellent problem-solving abilities
• Strong communication skills
• Team player with leadership qualities
• Agile/scrum experience
• Passion for learning new technologies

═══════════════════════════════════════════════════════════════

PREFERRED QUALIFICATIONS

• GraphQL experience
• Kubernetes knowledge
• Serverless architectures (Lambda)
• Fintech or payment processing background
• Microservices architecture experience
• Redis or caching technologies
• Monitoring tools (DataDog, New Relic)
• Open-source contributions
• TypeScript in production
• Message queues (RabbitMQ, Kafka)
• Event-driven architectures

═══════════════════════════════════════════════════════════════

EDUCATION

• Bachelor's degree in Computer Science or related field
• Advanced degree is a plus

═══════════════════════════════════════════════════════════════

TECH STACK

Frontend: React.js, TypeScript, Next.js, Redux, Tailwind CSS
Backend: Node.js, Express.js, Python, FastAPI, GraphQL
Data: PostgreSQL, Redis, MongoDB
Infrastructure: AWS, Docker, Kubernetes, GitHub Actions
Monitoring: DataDog, Sentry

═══════════════════════════════════════════════════════════════

WHAT WE OFFER

• Competitive salary ($150K - $200K)
• Equity package (stock options)
• Comprehensive health, dental, vision insurance
• 401(k) with 4% company match
• Unlimited PTO policy
• Flexible hybrid work (3 days in office)
• $2,500 annual learning budget
• Latest MacBook Pro and equipment
• Gym membership reimbursement
• Career growth opportunities
JOBEOF

echo "✅ Created: data/target_job.txt"

# =====================================================================
# STEP 4: Create Templates
# =====================================================================

echo -e "\n${BLUE}📝 Step 4: Creating templates...${NC}"

cat > job_search_data/templates/cover_letter_template.txt << 'TEMPLATE1'
Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company_name}.

With {match_score}% alignment to your requirements, I bring:
• {skill_1}
• {skill_2}
• {skill_3}

Recent achievements: {achievements}

I am actively developing: {learning_focus}

Portfolio: {portfolio_link}

Best regards,
{candidate_name}
TEMPLATE1

cat > job_search_data/templates/linkedin_message_template.txt << 'TEMPLATE2'
Hi {recruiter_name},

I'm interested in the {job_title} role at {company_name}.

Background:
• {skill_1}
• {skill_2}
• Match: {match_score}%

Portfolio: {portfolio_link}

Open to a brief chat?

Best,
{candidate_name}
TEMPLATE2

cat > job_search_data/templates/sprint_plan_template.txt << 'TEMPLATE3'
# Sprint {sprint_number}: {sprint_title}

**Duration:** 14 days
**Start:** {start_date}

## Goals
{sprint_goals}

## Skills
1. {skill_1}
2. {skill_2}

## Project
{project_description}

## Daily Log
Date: _____
Hours: ____
Progress: _____
TEMPLATE3

cat > job_search_data/templates/.gitkeep << 'TEMPLATE4'
TEMPLATE4

echo "✅ Created 4 template files"

# =====================================================================
# STEP 5: Create .gitignore
# =====================================================================

echo -e "\n${BLUE}🚫 Step 5: Creating .gitignore...${NC}"

cat > .gitignore << 'GITIGNORE'
# Dynamic job search data
job_search_data/*.json
job_search_data/analysis_*
job_search_data/sprint_*
job_search_data/learning_*

# Keep templates
!job_search_data/templates/

# Output directories
output/
batch_results/
PROGRESS_REPORT.md
*.log

# Python
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
.venv/
ENV/
.pytest_cache/
.coverage

# IDEs
.vscode/
.idea/
*.swp
.DS_Store

# Temp files
*.tmp
*.bak
GITIGNORE

echo "✅ Created .gitignore"

# =====================================================================
# STEP 6: Create requirements.txt
# =====================================================================

echo -e "\n${BLUE}📦 Step 6: Creating requirements.txt...${NC}"

cat > requirements.txt << 'REQS'
python-dateutil>=2.8.2
PyPDF2>=3.0.0
python-docx>=0.8.11
REQS

echo "✅ Created requirements.txt"

# =====================================================================
# STEP 7: Create README files
# =====================================================================

echo -e "\n${BLUE}📖 Step 7: Creating README files...${NC}"

cat > data/README.md << 'DATAREADME'
# Data Directory

## Files
- `my_cv.txt` - Sample CV
- `target_job.txt` - Sample job description

## Usage
Replace sample files with your own CV and job descriptions.

Supported formats: `.txt`, `.pdf`, `.docx`

## Testing
```bash
python3 -c "
from src.python_advanced_job_engine import AdvancedJobEngine
engine = AdvancedJobEngine()
print('CV:', len(engine.read_document('data/my_cv.txt').split()), 'words')
print('Job:', len(engine.read_document('data/target_job.txt').split()), 'words')
"
```
DATAREADME

cat > job_search_data/templates/README.md << 'TEMPLATEREADME'
# Templates Directory

Application material templates used by the automation system.

## Files
- `cover_letter_template.txt` - Cover letter
- `linkedin_message_template.txt` - LinkedIn outreach
- `sprint_plan_template.txt` - Learning sprint plans

## Variables
Use `{variable_name}` syntax for dynamic content:
- `{job_title}` - Target position
- `{company_name}` - Company name
- `{match_score}` - Match percentage
- `{candidate_name}` - Your name
- `{portfolio_link}` - Portfolio URL

## Customization
Edit templates to match your style while keeping variable syntax intact.
TEMPLATEREADME

echo "✅ Created README files"

# =====================================================================
# STEP 8: Verify Files
# =====================================================================

echo -e "\n${BLUE}🔍 Step 8: Verifying files...${NC}"

# Check CV
if [ -f "data/my_cv.txt" ] && [ -s "data/my_cv.txt" ]; then
    CV_SIZE=$(wc -c < data/my_cv.txt)
    CV_WORDS=$(wc -w < data/my_cv.txt)
    echo "✅ CV file: ${CV_SIZE} bytes, ${CV_WORDS} words"
else
    echo "❌ CV file missing or empty"
    exit 1
fi

# Check job description
if [ -f "data/target_job.txt" ] && [ -s "data/target_job.txt" ]; then
    JOB_SIZE=$(wc -c < data/target_job.txt)
    JOB_WORDS=$(wc -w < data/target_job.txt)
    echo "✅ Job file: ${JOB_SIZE} bytes, ${JOB_WORDS} words"
else
    echo "❌ Job file missing or empty"
    exit 1
fi

# Check templates
TEMPLATE_COUNT=$(find job_search_data/templates -type f ! -name '.gitkeep' | wc -l)
echo "✅ Templates: ${TEMPLATE_COUNT} files"

# =====================================================================
# STEP 9: Test Python Import (if available)
# =====================================================================

echo -e "\n${BLUE}🧪 Step 9: Testing Python imports...${NC}"

if command -v python3 &> /dev/null; then
    python3 << 'PYTEST'
import sys
from pathlib import Path

# Check if engine exists
engine_path = Path("src/python_advanced_job_engine.py")
if not engine_path.exists():
    print("⚠️  Warning: src/python_advanced_job_engine.py not found")
    print("   You'll need to add this file from your existing code")
    sys.exit(0)

try:
    sys.path.insert(0, 'src')
    from python_advanced_job_engine import AdvancedJobEngine
    engine = AdvancedJobEngine(data_dir="job_search_data")
    
    # Test reading files
    cv_text = engine.read_document("data/my_cv.txt")
    job_text = engine.read_document("data/target_job.txt")
    
    print(f"✅ Engine imported successfully")
    print(f"✅ CV readable: {len(cv_text.split())} words")
    print(f"✅ Job readable: {len(job_text.split())} words")
    
except ImportError as e:
    print(f"⚠️  Could not import engine: {e}")
    print("   Install dependencies: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
PYTEST
else
    echo "⚠️  Python3 not found, skipping import test"
fi

# =====================================================================
# SUMMARY
# =====================================================================

echo ""
echo "======================================================================"
echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo "======================================================================"
echo ""
echo "📁 Directory structure:"
echo "   ├── data/"
echo "   │   ├── my_cv.txt (${CV_WORDS} words)"
echo "   │   ├── target_job.txt (${JOB_WORDS} words)"
echo "   │   └── README.md"
echo "   ├── job_search_data/"
echo "   │   └── templates/ (${TEMPLATE_COUNT} files)"
echo "   ├── .gitignore"
echo "   └── requirements.txt"
echo ""
echo -e "${YELLOW}📋 NEXT STEPS:${NC}"
echo ""
echo "1️⃣  Install Python dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "2️⃣  Test locally (if you have the engine):"
echo "   python3 -c \\"
echo "   from src.python_advanced_job_engine import AdvancedJobEngine; \\"
echo "   engine = AdvancedJobEngine(); \\"
echo "   analysis = engine.analyze_from_files('data/my_cv.txt', 'data/target_job.txt'); \\"
echo "   print(f'Match Score: {analysis[\"score\"][\"total_score\"]}%')\""
echo ""
echo "3️⃣  Commit to GitHub:"
echo "   git add ."
echo "   git commit -m \"Complete setup with sample data\""
echo "   git push"
echo ""
echo "4️⃣  Run GitHub workflow:"
echo "   gh workflow run auto-job-analysis.yml \\"
echo "     -f cv_file=data/my_cv.txt \\"
echo "     -f job_file=data/target_job.txt"
echo ""
echo "5️⃣  Replace sample files with your real CV and job descriptions"
echo ""
echo "======================================================================"
echo -e "${GREEN}🎉 You're ready to go!${NC}"
echo "======================================================================"
