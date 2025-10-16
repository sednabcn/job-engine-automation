# User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Operating Modes](#operating-modes)
4. [Standard Workflow](#standard-workflow)
5. [Reverse Workflow](#reverse-workflow)
6. [Configuration](#configuration)
7. [Understanding Results](#understanding-results)
8. [Advanced Features](#advanced-features)
9. [Best Practices](#best-practices)

## Introduction

The Advanced Job Engine is a comprehensive career development tool that analyzes your skills against job requirements, creates personalized learning plans, and generates professional application materials. This guide covers everything you need to know to use the system effectively.

## Core Concepts

### Skills and Proficiency Levels

The engine uses a 5-level proficiency system:
- **Level 1**: Basic awareness, theoretical knowledge
- **Level 2**: Practical experience, can work with guidance
- **Level 3**: Independent work, solid understanding
- **Level 4**: Advanced expertise, can mentor others
- **Level 5**: Master level, industry recognized expert

### Quality Gates

Quality gates ensure you're ready before applying:
- **Foundational**: Core skills at minimum level
- **Competitive**: Skills that give you an edge
- **Excellence**: Skills for top-tier positions

### Match Scoring

Jobs are scored on multiple dimensions:
- **Technical Match**: How well your skills align
- **Experience Match**: Your experience vs requirements
- **Growth Potential**: Learning curve steepness
- **Overall Fit**: Weighted combination of all factors

## Operating Modes

### Standard Mode: Job → Skills Analysis

Use when you have a specific job posting:
1. Upload your CV
2. Upload job description
3. Get gap analysis
4. Receive learning plan
5. Track progress

**Best for**: Active job seekers, specific applications

### Reverse Mode: Skills → Job Discovery

Use when exploring opportunities:
1. Upload your CV
2. System analyzes your skillset
3. Receives job recommendations
4. Gets improvement strategies
5. Prepares for multiple opportunities

**Best for**: Career exploration, market research, passive candidates

## Standard Workflow

### Step 1: Prepare Your Documents

**CV Requirements**:
```
✓ Clear sections: Experience, Skills, Education
✓ Quantifiable achievements
✓ Technologies and tools used
✓ Projects and their outcomes
✓ Supported formats: PDF, DOCX, TXT
```

**Job Description**:
```
✓ Complete posting text
✓ Required skills section
✓ Nice-to-have skills
✓ Experience requirements
✓ Company information
```

### Step 2: Run Analysis

**Command Line**:
```bash
python src/python_advanced_job_engine.py \
  --cv data/my_cv.pdf \
  --job data/target_job.pdf \
  --mode standard
```

**Python API**:
```python
from src.python_advanced_job_engine import JobEngine

engine = JobEngine()
results = engine.analyze_job_fit(
    cv_path="data/my_cv.pdf",
    job_path="data/target_job.pdf"
)
```

### Step 3: Review Results

The engine generates:
- **Complete Analysis Report**: Comprehensive breakdown
- **Skills Gap Analysis**: What you need to learn
- **Learning Plan**: Structured improvement path
- **Quality Gate Status**: Readiness assessment
- **Application Materials**: Cover letter, emails

### Step 4: Follow Learning Plan

The learning plan includes:
- **2-Week Sprints**: Focused learning periods
- **Priority Resources**: Curated learning materials
- **Skill Tests**: Validate your learning
- **Milestones**: Track your progress

### Step 5: Track Progress

Update your progress:
```bash
python src/python_advanced_job_engine.py \
  --update-progress \
  --skill "Docker" \
  --new-level 3
```

## Reverse Workflow

### Step 1: Skillset Analysis

```bash
python src/python_advanced_job_engine.py \
  --cv data/my_cv.pdf \
  --mode reverse
```

The system:
- Extracts all your skills
- Determines proficiency levels
- Identifies your strengths
- Maps career possibilities

### Step 2: Job Recommendations

Based on your skills, receive:
- **High Match Jobs** (80%+ fit)
- **Growth Opportunity Jobs** (60-80% fit)
- **Stretch Jobs** (40-60% fit with learning plan)

### Step 3: Strategic Planning

For each job category:
- Gap analysis
- Learning priorities
- Timeline estimates
- Resource recommendations

### Step 4: Skill Improvement Strategy

Focus on skills that:
- Appear in multiple target roles
- Have high market demand
- Build on your existing expertise
- Fill critical gaps

## Configuration

### Basic Configuration

Create `.env` file:
```bash
# Paths
CV_PATH=data/my_cv.pdf
JOB_PATH=data/target_job.pdf

# Analysis settings
MIN_MATCH_SCORE=60
LEARNING_SPRINT_WEEKS=2

# Output preferences
EXPORT_FORMAT=json,txt
GENERATE_LETTERS=true
```

### Advanced Settings

Edit `config.json`:
```json
{
  "scoring_weights": {
    "technical_skills": 0.40,
    "experience": 0.30,
    "education": 0.15,
    "soft_skills": 0.15
  },
  "quality_gates": {
    "foundational": {
      "required_skills_met": 0.80,
      "min_skill_level": 2
    },
    "competitive": {
      "required_skills_met": 0.90,
      "nice_to_have_met": 0.50,
      "min_skill_level": 3
    }
  },
  "learning_plan": {
    "sprint_duration_weeks": 2,
    "max_skills_per_sprint": 3,
    "study_hours_per_week": 10
  }
}
```

## Understanding Results

### Match Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100% | Excellent fit | Apply immediately |
| 80-89% | Strong match | Minor preparation needed |
| 70-79% | Good fit | 2-4 weeks preparation |
| 60-69% | Moderate fit | 1-2 months learning |
| <60% | Significant gaps | 3+ months recommended |

### Gap Analysis Report

```
=== SKILL GAPS ===

CRITICAL GAPS (Must Have):
- Docker: You have Level 1, Need Level 3
  Impact: High | Priority: Urgent
  
- Kubernetes: You have None, Need Level 2
  Impact: High | Priority: Urgent

IMPORTANT GAPS (Nice to Have):
- GraphQL: You have Level 2, Need Level 3
  Impact: Medium | Priority: Moderate
```

### Learning Plan Structure

```
=== 2-WEEK LEARNING PLAN ===

Sprint 1: Foundation Building
Week 1-2: Docker Fundamentals
- [ ] Docker Deep Dive (Udemy) - 12 hours
- [ ] Practice: 5 container projects
- [ ] Goal: Reach Level 2

Sprint 2: Orchestration
Week 3-4: Kubernetes Basics
- [ ] Kubernetes for Beginners - 15 hours
- [ ] Deploy 3 applications
- [ ] Goal: Reach Level 2

Sprint 3: Advanced Topics
Week 5-6: Production Practices
- [ ] CI/CD with Docker & K8s - 10 hours
- [ ] Build complete pipeline
- [ ] Goal: Docker Level 3, K8s Level 2
```

### Quality Gate Status

```
QUALITY GATE: FOUNDATIONAL
Status: ✓ PASSED

Requirements:
✓ 85% of required skills met (target: 80%)
✓ Minimum skill level: 2.3 (target: 2.0)
✓ Critical skills covered: 8/8

QUALITY GATE: COMPETITIVE
Status: ⚠ IN PROGRESS

Requirements:
✓ 92% of required skills met (target: 90%)
⚠ 40% of nice-to-have met (target: 50%)
✓ Minimum skill level: 3.1 (target: 3.0)

Recommendation: Complete Sprint 2 to pass Competitive gate
```

## Advanced Features

### Batch Job Analysis

Analyze multiple jobs at once:
```bash
python scripts/batch_analysis.py \
  --cv data/my_cv.pdf \
  --jobs-folder data/jobs/ \
  --output job_comparison.json
```

### Custom Resource Database

Add your own learning resources:
```python
from src.learning.resource_db import ResourceDatabase

db = ResourceDatabase()
db.add_resource({
    "skill": "Docker",
    "title": "My Company's Docker Course",
    "type": "internal_training",
    "duration_hours": 8,
    "level": "intermediate",
    "url": "http://internal.company.com/courses/docker"
})
```

### Automated Progress Tracking

Integrate with your study system:
```python
from src.tracking.progress_tracker import ProgressTracker

tracker = ProgressTracker()
tracker.log_study_session(
    skill="Docker",
    duration_hours=2,
    activities=["Completed labs 1-5", "Built sample app"],
    self_assessment=3
)
```

### Export and Sharing

Export your results:
```bash
# Export everything
python src/python_advanced_job_engine.py --export-all

# Export specific items
python src/python_advanced_job_engine.py \
  --export learning_plan,skill_tests \
  --format pdf
```

## Best Practices

### For Job Seekers

1. **Keep CV Updated**: Update immediately after learning new skills
2. **Be Honest About Levels**: Overestimating hurts your learning plan
3. **Follow Sprint Structure**: Don't skip ahead in learning plans
4. **Take Skill Tests**: Validate your progress objectively
5. **Update Progress Weekly**: Keeps recommendations accurate

### For Career Changers

1. **Start with Reverse Mode**: Understand your transferable skills
2. **Focus on Gaps**: Prioritize skills that appear across multiple jobs
3. **Build Portfolio**: Create projects for each new skill
4. **Network While Learning**: Don't wait until "ready"
5. **Track Market Trends**: Re-run analysis monthly

### For Continuous Development

1. **Quarterly Skills Audit**: Run reverse mode every 3 months
2. **Keep Learning Log**: Document all learning activities
3. **Maintain Skill Levels**: Practice to avoid decay
4. **Explore Adjacent Roles**: See what's one step away
5. **Build T-Shaped Skills**: Deep expertise + broad knowledge

### Optimizing Learning Plans

1. **Adjust Sprint Duration**: Match to your available time
2. **Parallel vs Sequential**: Balance based on complexity
3. **Mix Learning Types**: Theory + Practice + Projects
4. **Use Company Resources**: Leverage existing subscriptions
5. **Study Groups**: Learn skills with peers when possible

### Application Strategy

1. **Quality Gates First**: Don't apply before Foundational gate
2. **Customize Materials**: Use generated letters as templates
3. **Track Applications**: Note which skills were emphasized
4. **Request Feedback**: Learn from rejections
5. **Iterate CV**: Update based on what worked

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Low match scores | Check if job requirements are realistic |
| Missing skills detected | Update CV with complete skill list |
| Inaccurate proficiency | Review proficiency level guidelines |
| Learning plan too aggressive | Adjust sprint duration in config |
| Quality gates not passing | Focus on critical gaps first |
| Export failures | Check file permissions in output folder |

For detailed troubleshooting, see [troubleshooting.md](troubleshooting.md).

## Getting Help

- **Documentation**: Check [index.md](index.md) for all guides
- **Examples**: See [examples/](examples/) folder for code samples
- **Issues**: Report bugs on GitHub Issues
- **Community**: Join discussions on GitHub Discussions
- **FAQ**: See [faq.md](faq.md) for common questions

## Next Steps

- **New Users**: Start with [getting-started.md](getting-started.md)
- **Automation**: See [workflow-guide.md](workflow-guide.md)
- **Deep Dive**: Read [architecture.md](architecture.md)
- **API Usage**: Check [api-reference.md](api-reference.md)