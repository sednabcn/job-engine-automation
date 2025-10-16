# 🤖 Complete GitHub Actions Automation - Zero Local Setup

**Upload CV + Job Description → Get Complete Analysis Automatically**

No Python installation. No local setup. Just GitHub.

---

## 📋 Table of Contents

- [Quick Start (5 Minutes)](#quick-start-5-minutes)
- [How It Works](#how-it-works)
- [Setup Instructions](#setup-instructions)
- [Usage - Upload Files Only](#usage---upload-files-only)
- [What You Get Automatically](#what-you-get-automatically)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

---

## Quick Start (5 Minutes)

### Step 1: Fork Repository (1 minute)
```
1. Go to: https://github.com/yourusername/advanced-job-engine
2. Click "Fork" button (top right)
3. Wait for fork to complete
4. You now have your own copy!
```

### Step 2: Enable GitHub Actions (30 seconds)
```
1. Go to your forked repo
2. Click "Actions" tab
3. Click "I understand my workflows, enable them"
```

### Step 3: Upload Your Files (2 minutes)
```
1. Click "Add file" → "Upload files"
2. Upload your CV: data/my_cv.pdf
3. Upload job description: data/job_description.pdf
4. Click "Commit changes"
```

### Step 4: Trigger Analysis (1 minute)
```
1. Go to "Actions" tab
2. Click "Auto Job Analysis" workflow
3. Click "Run workflow" button
4. Click green "Run workflow"
5. Wait 2-3 minutes
```

### Step 5: Download Results (30 seconds)
```
1. Click on the completed workflow run
2. Scroll to "Artifacts" section
3. Download "job-analysis-results"
4. Unzip and read reports!
```

**That's it! No Python, no terminal, no setup.**

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  YOU (GitHub Web Interface)                                 │
├─────────────────────────────────────────────────────────────┤
│  1. Upload CV (data/my_cv.pdf)                             │
│  2. Upload Job (data/job_description.pdf)                  │
│  3. Click "Run workflow" button                             │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  GITHUB ACTIONS (Cloud Runner - Automatic)                  │
├─────────────────────────────────────────────────────────────┤
│  1. ✓ Setup Python environment                              │
│  2. ✓ Install all dependencies                              │
│  3. ✓ Read your CV and job description                      │
│  4. ✓ Run complete analysis                                 │
│  5. ✓ Generate learning plan                                │
│  6. ✓ Create improvement strategy                           │
│  7. ✓ Generate application materials                        │
│  8. ✓ Create skill tests                                    │
│  9. ✓ Package everything into ZIP                           │
│  10. ✓ Upload as artifact                                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  RESULTS (Download from GitHub)                             │
├─────────────────────────────────────────────────────────────┤
│  📦 job-analysis-results.zip                                │
│     ├── 📄 complete_report.md (detailed analysis)           │
│     ├── 📄 match_score.json (your score breakdown)          │
│     ├── 📄 learning_plan.json (personalized roadmap)        │
│     ├── 📄 improvement_strategy.md (step-by-step plan)      │
│     ├── 📄 cover_letter.txt (customized letter)             │
│     ├── 📄 linkedin_message.txt (outreach message)          │
│     ├── 📄 skill_tests.json (assessment questions)          │
│     └── 📄 summary.txt (quick overview)                     │
└─────────────────────────────────────────────────────────────┘
```

**Benefits:**
- ✅ No local Python installation needed
- ✅ No command line or terminal
- ✅ Works on any device (Windows, Mac, Linux, even mobile)
- ✅ Always uses latest code version
- ✅ Free (GitHub Actions free tier: 2000 mins/month)
- ✅ Automatic updates when code improves

---

## Setup Instructions

### One-Time Setup (10 minutes)

#### 1. Fork the Repository

**Via GitHub Web:**
```
1. Go to: https://github.com/yourusername/advanced-job-engine
2. Click "Fork" (top right corner)
3. Select your account as destination
4. Wait for fork to complete (~30 seconds)
5. You now have: github.com/YOUR_USERNAME/advanced-job-engine
```

**What this does:** Creates your personal copy of the project where you can upload files and run workflows.

#### 2. Enable GitHub Actions

**Steps:**
```
1. Go to YOUR forked repository
2. Click "Actions" tab (top menu)
3. You'll see: "Workflows aren't being run on this forked repository"
4. Click green button: "I understand my workflows, enable them"
```

**What this does:** Activates automation so workflows can run when you trigger them.

#### 3. Verify Workflow Files Exist

**Check these files exist in your repo:**
```
.github/workflows/auto-job-analysis.yml        ✓ Main workflow
.github/workflows/scheduled-analysis.yml       ✓ Optional: Auto-run weekly
.github/workflows/batch-analysis.yml           ✓ Optional: Multiple jobs
```

**If missing:** The workflows should be in the original repo. If not, see "Creating Workflow Files" section below.

#### 4. Set Up Repository Secrets (Optional)

**For email notifications (optional):**
```
1. Go to: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add secrets:
   - Name: NOTIFICATION_EMAIL
     Value: your-email@example.com
   
   - Name: SMTP_PASSWORD (if using email alerts)
     Value: your-smtp-password
```

**For now, skip this - it's optional.**

---

## Usage - Upload Files Only

### Method 1: Single Job Analysis (Most Common)

#### Step 1: Prepare Your Files

**Your CV:**
- Format: PDF, DOCX, or TXT
- Filename: **my_cv.pdf** (or .docx, .txt)
- Location: Save to your computer

**Job Description:**
- Format: PDF, DOCX, or TXT
- Filename: **job_description.pdf** (or any name)
- Content: Copy-paste from job site, or save posting as PDF

#### Step 2: Upload to GitHub

**Via Web Interface:**
```
1. Go to your repository on GitHub
2. Navigate to: Click on "data" folder
3. Click "Add file" → "Upload files"
4. Drag and drop:
   - my_cv.pdf
   - job_description.pdf
5. Scroll down, add commit message: "Add CV and job for analysis"
6. Click "Commit changes"
```

**Repository structure after upload:**
```
your-repo/
├── data/
│   ├── my_cv.pdf              ← Your CV here
│   └── job_description.pdf    ← Job here
├── .github/workflows/
│   └── auto-job-analysis.yml
└── src/
    └── ... (code files)
```

#### Step 3: Run the Workflow

**Trigger analysis:**
```
1. Click "Actions" tab (top menu)
2. Left sidebar: Click "Auto Job Analysis"
3. Right side: Click "Run workflow" dropdown button
4. Select branch: "main" (or "master")
5. (Optional) Change job title/company in inputs
6. Click green "Run workflow" button
```

**Workflow inputs (optional):**
```yaml
CV File Path: data/my_cv.pdf              # Default, change if different
Job File Path: data/job_description.pdf   # Default, change if different
Job Title: Senior Software Engineer        # Optional: for better reporting
Company Name: TechCorp Inc.               # Optional: for customized letters
```

#### Step 4: Wait for Completion

**Monitor progress:**
```
1. You'll see workflow run appear with yellow dot (running)
2. Click on the run to see live progress
3. Watch steps complete:
   ✓ Set up job
   ✓ Checkout code
   ✓ Set up Python
   ✓ Install dependencies
   ✓ Run analysis
   ✓ Generate reports
   ✓ Upload artifacts
4. Wait 2-3 minutes
5. Yellow dot → Green checkmark ✓ (success!)
```

**Live log example:**
```
Run Analysis
  Reading CV from data/my_cv.pdf...
  Reading job description from data/job_description.pdf...
  Parsing CV...
  Extracting job requirements...
  Calculating match score...
  Match Score: 78%
  Generating learning plan...
  Creating improvement strategy...
  Generating application materials...
  Creating skill tests...
  ✓ Analysis complete!
```

#### Step 5: Download Results

**Get your analysis:**
```
1. Scroll to bottom of workflow run page
2. Find "Artifacts" section
3. Click "job-analysis-results" to download ZIP
4. Save to computer
5. Unzip the file
6. Open reports in any text editor or browser
```

**What you get:**
```
job-analysis-results/
├── 📄 complete_report.md          # Main analysis (open in browser/editor)
├── 📄 match_score.json            # Your score: 78%
├── 📄 gap_analysis.json           # Missing skills list
├── 📄 learning_plan.json          # 12-week roadmap
├── 📄 improvement_strategy.md     # Step-by-step plan
├── 📄 cover_letter.txt            # Customized letter
├── 📄 linkedin_message.txt        # Connection request message
├── 📄 followup_email.txt          # Follow-up template
├── 📄 skill_tests.json            # Self-assessment questions
└── 📄 summary.txt                 # Quick 1-page overview
```

---

### Method 2: Multiple Jobs (Batch Analysis)

**Analyze several jobs at once:**

#### Step 1: Upload Multiple Job Files
```
data/
├── my_cv.pdf                    ← Your CV (one file)
├── job_backend_senior.pdf       ← Job 1
├── job_fullstack_mid.pdf        ← Job 2
├── job_devops_lead.pdf          ← Job 3
└── job_data_engineer.pdf        ← Job 4
```

#### Step 2: Run Batch Workflow
```
1. Actions → "Batch Job Analysis"
2. Run workflow
3. Input job files (comma-separated):
   data/job_backend_senior.pdf,data/job_fullstack_mid.pdf,data/job_devops_lead.pdf
4. Run workflow
```

#### Step 3: Download Batch Results
```
batch-analysis-results/
├── job_backend_senior/
│   ├── complete_report.md
│   ├── match_score.json (Score: 78%)
│   └── ...
├── job_fullstack_mid/
│   ├── complete_report.md
│   ├── match_score.json (Score: 72%)
│   └── ...
├── job_devops_lead/
│   ├── complete_report.md
│   ├── match_score.json (Score: 65%)
│   └── ...
└── comparison_summary.md         # Side-by-side comparison
```

---

### Method 3: Scheduled Auto-Analysis

**Automatically re-analyze monthly to track progress:**

#### Step 1: Enable Scheduled Workflow
```
1. Edit file: .github/workflows/scheduled-analysis.yml
2. Uncomment the schedule section:

schedule:
  - cron: '0 9 1 * *'  # 9 AM on 1st of each month

3. Commit the change
```

#### Step 2: It Runs Automatically
```
✓ 1st of every month at 9 AM UTC
✓ Analyzes your latest CV vs saved jobs
✓ Tracks score improvements over time
✓ Emails you results (if configured)
✓ No manual trigger needed!
```

#### Step 3: View Progress Reports
```
Each month you get:
- Current match score
- Score improvement: +5% (73% → 78%)
- Skills acquired: Kubernetes, Docker
- Next focus areas
- Updated learning plan
```

---

## What You Get Automatically

### 📊 Complete Analysis Report

**File:** `complete_report.md`

**Contents:**
```markdown
# Job Match Analysis Report

## Match Score: 78%
**Status:** ðŸŸ¡ Strong Candidate (Minor Improvements Needed)

---

## Score Breakdown

| Category | Score | Weight | Contribution |
|----------|-------|--------|--------------|
| Required Skills | 80% | 35% | 28.0% |
| Experience | 100% | 20% | 20.0% |
| Keywords | 85% | 15% | 12.75% |
| Preferred Skills | 50% | 15% | 7.5% |
| Education | 100% | 10% | 10.0% |
| Certifications | 0% | 5% | 0.0% |
| **Total** | **78%** | **100%** | **78.25%** |

---

## Gap Analysis

### Missing Required Skills (2)
1. ❌ **Kubernetes** (High Priority)
   - Estimated learning time: 30 hours
   - Difficulty: Intermediate
   - Resources: [Kubernetes Official Docs](https://kubernetes.io/docs/)

2. ❌ **GraphQL** (High Priority)
   - Estimated learning time: 20 hours
   - Difficulty: Beginner
   - Resources: [How to GraphQL](https://www.howtographql.com/)

### Missing Preferred Skills (2)
1. ⚠️ **Redis** (Bonus Points)
   - Estimated learning time: 15 hours
   - Would increase score to: 82%

2. ⚠️ **Kafka** (Nice to Have)
   - Estimated learning time: 25 hours
   - Would increase score to: 84%

---

## Recommendations

### Immediate Actions (This Week)
1. ✅ **Update CV** with job-specific keywords
2. ✅ **Start Kubernetes tutorial** (highest priority)
3. ✅ **Begin GraphQL course** (quick win)

### Short-term Goals (4-8 Weeks)
1. 🎯 Complete Kubernetes learning
2. 🎯 Build 2 projects demonstrating K8s skills
3. 🎯 Master GraphQL API development
4. 🎯 Re-analyze to reach 85%+ score

### When to Apply
- **Now:** You're competitive at 78%, but...
- **Better:** Reach 85% in 6-8 weeks for stronger position
- **Best:** Multiple offers → negotiate from strength

---

## Your Learning Plan

See: `learning_plan.json` for detailed 12-week roadmap
See: `improvement_strategy.md` for step-by-step execution plan
```

---

### 📚 Learning Plan

**File:** `learning_plan.json`

**Structure:**
```json
{
  "mode": "standard",
  "duration_weeks": 12,
  "target_score": 85,
  "current_score": 78,
  
  "phases": [
    {
      "phase": 1,
      "name": "Foundation Building",
      "weeks": "1-4",
      "focus": ["Kubernetes", "GraphQL"],
      "goals": [
        "Complete Kubernetes basics tutorial",
        "Build simple K8s deployment",
        "Learn GraphQL fundamentals",
        "Create GraphQL API project"
      ],
      "estimated_hours": 50,
      "expected_score_after": 82
    },
    {
      "phase": 2,
      "name": "Practice & Portfolio",
      "weeks": "5-8",
      "focus": ["Advanced K8s", "Production GraphQL"],
      "goals": [
        "Deploy multi-container app with K8s",
        "Implement GraphQL subscriptions",
        "Set up CI/CD pipeline",
        "Document projects on GitHub"
      ],
      "estimated_hours": 40,
      "expected_score_after": 85
    },
    {
      "phase": 3,
      "name": "Polish & Apply",
      "weeks": "9-12",
      "focus": ["Portfolio polish", "Application materials"],
      "goals": [
        "Create portfolio website",
        "Write technical blog posts",
        "Update CV and LinkedIn",
        "Generate customized applications"
      ],
      "estimated_hours": 30,
      "expected_score_after": 88
    }
  ],
  
  "study_resources": [
    {
      "skill": "Kubernetes",
      "priority": "high",
      "resources": [
        {
          "title": "Kubernetes Official Tutorial",
          "url": "https://kubernetes.io/docs/tutorials/",
          "type": "tutorial",
          "estimated_hours": 10,
          "difficulty": "beginner"
        },
        {
          "title": "Kubernetes for Developers",
          "url": "https://www.udemy.com/course/kubernetes-for-developers/",
          "type": "course",
          "estimated_hours": 15,
          "difficulty": "intermediate",
          "cost": "$19.99"
        }
      ]
    },
    {
      "skill": "GraphQL",
      "priority": "high",
      "resources": [
        {
          "title": "How to GraphQL",
          "url": "https://www.howtographql.com/",
          "type": "tutorial",
          "estimated_hours": 8,
          "difficulty": "beginner"
        }
      ]
    }
  ],
  
  "practice_projects": [
    {
      "name": "Containerized Microservices",
      "skills": ["Kubernetes", "Docker", "Python"],
      "description": "Deploy Python microservices on Kubernetes cluster",
      "estimated_hours": 20,
      "difficulty": "intermediate"
    },
    {
      "name": "GraphQL API Server",
      "skills": ["GraphQL", "Node.js", "PostgreSQL"],
      "description": "Build full-featured GraphQL API with subscriptions",
      "estimated_hours": 15,
      "difficulty": "intermediate"
    }
  ]
}
```

---

### 🎯 Improvement Strategy

**File:** `improvement_strategy.md`

**Example:**
```markdown
# Improvement Strategy: 78% → 88%

## Overview
Target: Reach 88% match score in 12 weeks
Current: 78% (Strong foundation, focused improvements needed)
Gap: Focus on 2 missing required skills

---

## Week-by-Week Plan

### Weeks 1-2: Kubernetes Fundamentals
**Daily commitment:** 2 hours (14 hours total)

**Monday-Wednesday: Core Concepts**
- [ ] Day 1: Kubernetes architecture (pods, nodes, clusters)
- [ ] Day 2: kubectl basics, deploying first app
- [ ] Day 3: Services and networking

**Thursday-Sunday: Hands-on Practice**
- [ ] Day 4-5: Build simple deployment with 3 containers
- [ ] Day 6-7: Document learning, push to GitHub

**Milestone:** Deploy working multi-container app on local K8s
**Test:** Complete beginner Kubernetes quiz (target: 70%+)

---

### Weeks 3-4: GraphQL Mastery
**Daily commitment:** 1.5 hours (10 hours total)

**Days 1-7: Learn GraphQL**
- [ ] Complete "How to GraphQL" tutorial
- [ ] Build simple GraphQL server (Node.js + Express)
- [ ] Implement queries, mutations, subscriptions
- [ ] Connect to PostgreSQL database

**Days 8-14: Project Development**
- [ ] Build task management API with GraphQL
- [ ] Add authentication
- [ ] Deploy to Heroku/Render
- [ ] Write comprehensive README

**Milestone:** Production-ready GraphQL API on GitHub
**Test:** GraphQL concepts quiz (target: 80%+)

---

### Weeks 5-8: Integration Project
**Weekly commitment:** 10 hours (40 hours total)

**Project: Full-Stack App with K8s + GraphQL**
- [ ] Week 5: Design architecture, set up project
- [ ] Week 6: Build GraphQL backend
- [ ] Week 7: Containerize with Docker
- [ ] Week 8: Deploy on Kubernetes cluster

**Deliverable:** 
- Working application demonstrating both skills
- Comprehensive documentation
- Deployment guide
- Architecture diagram

**Milestone:** Re-analyze CV (expected: 85%+)

---

### Weeks 9-12: Professional Branding
**Weekly commitment:** 8 hours (32 hours total)

**Week 9-10: Portfolio Development**
- [ ] Create portfolio website
- [ ] Showcase top 3 projects
- [ ] Write project case studies
- [ ] Add resume/CV download

**Week 11: Content Creation**
- [ ] Write 2 technical blog posts:
  - "Deploying Microservices with Kubernetes"
  - "Building Scalable APIs with GraphQL"
- [ ] Share on LinkedIn, dev.to

**Week 12: Application Sprint**
- [ ] Update CV with new projects
- [ ] Update LinkedIn profile
- [ ] Re-analyze all target jobs
- [ ] Generate customized applications
- [ ] Apply to top 5 positions

---

## Daily Routine

**Weekday Structure (2 hours):**
- 6:00-6:30 AM: Review previous day's concepts
- 6:30-7:30 AM: Tutorial/course learning
- 7:30-8:00 PM: Practice exercises or coding
- Before bed: 15-min review and note-taking

**Weekend Structure (4-5 hours Saturday, 3-4 hours Sunday):**
- Morning: Project building (3-4 hours)
- Afternoon: Documentation and refinement (1-2 hours)
- Evening: Skill assessment and planning next week

---

## Progress Tracking

**Weekly Checklist:**
- [ ] Completed planned learning hours: ___/14
- [ ] Finished all tutorials: Yes/No
- [ ] Built practice project: Yes/No
- [ ] Pushed code to GitHub: Yes/No
- [ ] Took skill assessment: Score: ___%
- [ ] Updated learning notes: Yes/No

**Monthly Re-analysis:**
- [ ] Month 1: Re-run analysis (target: 82%)
- [ ] Month 2: Re-run analysis (target: 85%)
- [ ] Month 3: Re-run analysis (target: 88%+)

---

## Quality Gates

**✓ Foundation Gate (82%):** Weeks 1-4
- Basic understanding of K8s and GraphQL
- 1-2 small projects demonstrating skills
- Can discuss topics in interviews

**✓ Competency Gate (85%):** Weeks 5-8
- Job-ready proficiency
- Impressive portfolio project
- Ready for technical interviews

**✓ Mastery Gate (88%+):** Weeks 9-12
- Production experience demonstrated
- Professional portfolio
- Competitive advantage for applications

---

## Success Metrics

**Technical Skills:**
- [ ] Can deploy apps to Kubernetes independently
- [ ] Can design and build GraphQL APIs
- [ ] Portfolio has 3+ projects showcasing skills

**Application Readiness:**
- [ ] CV updated with quantified achievements
- [ ] LinkedIn profile optimized
- [ ] GitHub profile professional and active
- [ ] Ready to discuss projects in detail

**Outcome Goals:**
- [ ] Reach 88%+ match score
- [ ] Apply to 5-7 target positions
- [ ] Get 3-5 interviews (60%+ conversion)
- [ ] Receive 2+ job offers
- [ ] Negotiate 15-20% higher salary

---

## Accountability

**Weekly Review (Sunday evening):**
1. Review accomplished tasks
2. Identify blockers or challenges
3. Adjust next week's plan if needed
4. Celebrate wins (no matter how small!)

**Support System:**
- Join Kubernetes Slack community
- Participate in GraphQL Discord
- Find accountability partner (optional)
- Share progress on LinkedIn (builds visibility)

---

## Emergency Adjustments

**If Falling Behind:**
- Reduce daily commitment from 2h to 1.5h
- Extend timeline by 2-4 weeks
- Focus on required skills only (skip preferred)
- Simplify project scope

**If Ahead of Schedule:**
- Add Redis or Kafka (preferred skills)
- Build additional portfolio project
- Start applying earlier
- Help others (answer questions, build reputation)

---

## Final Push (Week 12)

**Monday-Wednesday: Application Preparation**
- Finalize all portfolio projects
- Update all profiles (CV, LinkedIn, GitHub)
- Generate customized application materials
- Research target companies deeply

**Thursday-Friday: Applications**
- Apply to top 5 positions
- Personalized cover letters for each
- Connect with employees on LinkedIn
- Send thoughtful messages

**Weekend: Follow-up**
- Send follow-up emails to applied positions
- Continue networking
- Prepare for interview calls
- Practice technical interview questions

---

**Remember:**
- Progress > Perfection
- Consistency > Intensity
- Learning > Completion
- Portfolio > Certificates

You've got this! 🚀
```

---

### ✉️ Application Materials

**Files Generated:**
1. `cover_letter.txt` - Customized for the job
2. `linkedin_message.txt` - Connection request template
3. `followup_email.txt` - Follow-up after applying
4. `networking_email.txt` - Reach out to employees

**Example Cover Letter:**
```
Dear Hiring Manager,

I am writing to express my strong interest in the Senior Backend Engineer 
position at InnovateTech Solutions. With 5 years of Python development 
experience and a proven track record building scalable systems, I am 
excited about the opportunity to contribute to your team.

Your job posting emphasizes expertise in Django, Docker, and cloud 
infrastructure - areas where I have substantial hands-on experience. 
At my current role at TechCorp, I:

• Built microservices architecture serving 2M+ daily users using Python/Django
• Reduced API response time by 40% through Redis caching and optimization
• Led a team of 4 developers while maintaining high code quality standards
• Deployed containerized applications using Docker and AWS ECS

I am particularly drawn to InnovateTech's focus on [mention something 
specific about the company]. I have been actively expanding my skills 
in Kubernetes and GraphQL through hands-on projects, which align 
perfectly with your technology stack.

I would welcome the opportunity to discuss how my experience in building 
scalable backend systems and leading technical projects can contribute 
to InnovateTech's continued success.

Thank you for considering my application. I look forward to speaking with you.

Best regards,
[Your Name]
[Your Email]
[Your Phone]
[LinkedIn Profile]
[GitHub Profile]

---
Projects mentioned in CV:
- github.com/yourname/microservices-platform (Docker + Django)
- github.com/yourname/graphql-api-server (GraphQL + Node.js)
```

---

### 🧪 Skill Tests

**File:** `skill_tests.json`

**Self-assessment questions to validate learning:**

```json
{
  "Kubernetes": {
    "beginner": [
      {
        "question": "What is a Pod in Kubernetes?",
        "type": "multiple_choice",
        "options": [
          "A) A single container",
          "B) The smallest deployable unit that can contain one or more containers",
          "C) A type of service",
          "D) A storage volume"
        ],
        "correct_answer": "B",
        "explanation": "A Pod is the smallest deployable unit in Kubernetes and can contain one or more tightly coupled containers."
      },
      {
        "question": "Explain the difference between a Deployment and a Pod.",
        "type": "short_answer",
        "key_points": [
          "Pod is a running instance",
          "Deployment manages Pods",
          "Deployment provides scaling and rolling updates",
          "Deployment ensures desired state"
        ]
      }
    ],
    "intermediate": [
      {
        "question": "How would you expose a service externally in Kubernetes?",
        "type": "multiple_choice",
        "options": [
          "A) Use a ClusterIP service",
          "B) Use a NodePort or LoadBalancer service",
          "C) Pods are automatically exposed",
          "D) Use a ConfigMap"
        ],
        "correct_answer": "B"
      }
    ],
    "advanced": [
      {
        "question": "Design a rolling update strategy for zero-downtime deployment",
        "type": "coding",
        "task": "Write a Kubernetes Deployment YAML with appropriate update strategy"
      }
    ]
  },
  
  "GraphQL": {
    "beginner": [
      {
        "question": "What is the main advantage of GraphQL over REST?",
        "type": "multiple_choice",
        "options": [
          "A) Faster server performance",
          "B) Clients can request exactly the data they need",
          "C) Easier to implement",
          "D) Better security"
        ],
        "correct_answer": "B"
      }
    ],
    "intermediate": [
      {
        "question": "Implement a GraphQL mutation to create a user",
        "type": "coding",
        "starter_code": "type Mutation {\n  createUser(input: CreateUserInput!): User\n}",
        "task": "Write the resolver function"
      }
    ]
  }
}
```

**Usage:**
1. Take tests after learning each skill
2. Track scores to measure progress
3. Re-take tests before re-analyzing CV
4. Use to identify weak areas

---

## Advanced Configuration

### Workflow Customization

**Edit:** `.github/workflows/auto-job-analysis.yml`

```yaml
name: Auto Job Analysis

on:
  workflow_dispatch:  # Manual trigger
    inputs:
      cv_file:
        description: 'Path to CV file'
        required: false
        default: 'data/my_cv.pdf'
      job_file:
        description: 'Path to job description file'
        required: false
        default: 'data/job_description.pdf'
      job_title:
        description: 'Job title (optional)'
        required: false
        default: ''
      company_name:
        description: 'Company name (optional)'
        required: false
        default: ''
      generate_materials:
        description: 'Generate application materials?'
        required: false
        type: boolean
        default: true
      send_notification:
        description: 'Send email notification?'
        required: false
        type: boolean
        default: false

  push:  # Auto-trigger on file upload
    paths:
      - 'data/**.pdf'
      - 'data/**.docx'
      - 'data/**.txt'

  schedule:  # Auto-run monthly
    - cron: '0 9 1 * *'  # 9 AM on 1st of each month

jobs:
  analyze:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v