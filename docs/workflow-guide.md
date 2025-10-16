# GitHub Actions Workflow Guide

## Table of Contents

1. [Overview](#overview)
2. [Setting Up Automation](#setting-up-automation)
3. [Workflow Modes](#workflow-modes)
4. [Configuration](#configuration)
5. [Secrets Management](#secrets-management)
6. [Triggering Workflows](#triggering-workflows)
7. [Understanding Results](#understanding-results)
8. [Advanced Workflows](#advanced-workflows)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

## Overview

The Advanced Job Engine includes powerful GitHub Actions workflows that automate your job search and skill development process. Run analyses directly from GitHub without local setup.

### Benefits of Automation

- **No Local Setup**: Run from any device with GitHub access
- **Scheduled Analysis**: Automatically track progress weekly
- **Version Control**: All results tracked in git history
- **Collaboration**: Share workflows with team members
- **CI/CD Integration**: Integrate with deployment pipelines

## Setting Up Automation

### Step 1: Fork or Clone Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/advanced-job-engine.git
cd advanced-job-engine

# Or fork via GitHub UI
```

### Step 2: Enable GitHub Actions

1. Go to repository **Settings**
2. Navigate to **Actions** → **General**
3. Under "Actions permissions", select:
   - ✓ Allow all actions and reusable workflows
4. Click **Save**

### Step 3: Add Required Secrets

Navigate to **Settings** → **Secrets and variables** → **Actions**

**Required Secrets:**
```
CV_CONTENT          Your CV text (required)
TARGET_JOB_CONTENT  Job description (for standard mode)
NOTIFICATION_EMAIL  Email for notifications (optional)
```

**Adding a Secret:**
1. Click **New repository secret**
2. Name: `CV_CONTENT`
3. Value: Paste your CV text
4. Click **Add secret**

### Step 4: Test Workflow

1. Go to **Actions** tab
2. Select **Unified Reverse Job Engine**
3. Click **Run workflow**
4. Select branch: `main`
5. Fill in parameters
6. Click **Run workflow**

## Workflow Modes

### Standard Mode

Analyzes your fit for a specific job posting.

**When to Use:**
- Applying to a specific position
- Want detailed gap analysis for one role
- Need customized application materials

**Workflow File:** `.github/workflows/unified-reverse-job-engine.yml`

**Manual Trigger:**
```yaml
workflow_dispatch:
  inputs:
    mode:
      description: 'Analysis mode'
      required: true
      default: 'standard'
      type: choice
      options:
        - standard
        - reverse
```

**Automated Trigger Example:**
```yaml
# Run when new job description is added
on:
  push:
    paths:
      - 'data/jobs/*.pdf'
      - 'data/jobs/*.txt'
```

### Reverse Mode

Discovers opportunities matching your skillset.

**When to Use:**
- Exploring career options
- Not targeting specific roles
- Want to see what's possible
- Career transition planning

**Configuration:**
```yaml
inputs:
  mode:
    default: 'reverse'
  min_match_score:
    description: 'Minimum match percentage'
    default: '70'
```

### Hybrid Mode

Combines both approaches for comprehensive analysis.

```yaml
strategy:
  matrix:
    mode: [standard, reverse]
```

## Configuration

### Workflow Input Parameters

#### Basic Parameters

```yaml
workflow_dispatch:
  inputs:
    mode:
      description: 'Analysis mode (standard/reverse)'
      required: true
      default: 'standard'
      type: choice
      options:
        - standard
        - reverse
    
    sprint_duration:
      description: 'Learning sprint duration (weeks)'
      required: false
      default: '2'
    
    study_hours:
      description: 'Study hours per week'
      required: false
      default: '10'
```

#### Advanced Parameters

```yaml
    generate_letters:
      description: 'Generate application materials'
      required: false
      default: 'true'
      type: boolean
    
    export_format:
      description: 'Export formats (comma-separated)'
      required: false
      default: 'json,txt'
    
    notification_enabled:
      description: 'Send email notifications'
      required: false
      default: 'false'
      type: boolean
```

### Environment Variables

Set in workflow file:

```yaml
env:
  CV_CONTENT: ${{ secrets.CV_CONTENT }}
  JOB_CONTENT: ${{ secrets.TARGET_JOB_CONTENT }}
  MIN_MATCH_SCORE: 60
  MAX_RESOURCES_PER_SKILL: 5
  ENABLE_CACHE: true
```

### Configuration File

Use `config.json` for persistent settings:

```json
{
  "scoring_weights": {
    "technical_skills": 0.40,
    "experience": 0.30,
    "education": 0.15,
    "soft_skills": 0.15
  },
  "learning_plan": {
    "sprint_duration_weeks": 2,
    "max_skills_per_sprint": 3,
    "study_hours_per_week": 10
  },
  "quality_gates": {
    "foundational": {
      "required_skills_met": 0.80,
      "min_skill_level": 2
    }
  }
}
```

## Secrets Management

### Required Secrets

#### CV_CONTENT

Your resume/CV in text format.

**Format:**
```text
JOHN DOE
Senior Software Engineer
john.doe@email.com | +1-555-0123

EXPERIENCE
Senior Developer at Company A (2020-Present)
- Built microservices using Python and Docker
- Led team of 5 developers
...

SKILLS
Python (Expert, 8 years)
Docker (Advanced, 4 years)
...
```

**Adding:**
1. Copy CV text
2. Settings → Secrets → New secret
3. Name: `CV_CONTENT`
4. Paste text
5. Save

#### TARGET_JOB_CONTENT

Job description for standard mode.

**Format:**
```text
Senior Backend Engineer
Company XYZ | Remote | $120k-$150k

REQUIREMENTS:
- 5+ years Python experience
- Strong Docker/Kubernetes knowledge
- AWS expertise
...
```

### Optional Secrets

#### NOTIFICATION_EMAIL

Email for workflow notifications.

```yaml
- name: Send notification
  if: success()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 587
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    to: ${{ secrets.NOTIFICATION_EMAIL }}
    subject: "Job Analysis Complete"
    body: "Your analysis is ready!"
```

#### API_KEYS

For external integrations:

```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  LINKEDIN_TOKEN: ${{ secrets.LINKEDIN_TOKEN }}
```

### Security Best Practices

1. **Never commit secrets** to repository
2. **Use environment-specific secrets** for different branches
3. **Rotate secrets regularly**
4. **Limit secret access** to necessary workflows
5. **Use encrypted secrets** for sensitive data

## Triggering Workflows

### Manual Trigger (workflow_dispatch)

Most common method for on-demand analysis.

**Via GitHub UI:**
1. Go to **Actions** tab
2. Select workflow
3. Click **Run workflow**
4. Fill parameters
5. Click **Run workflow** button

**Via GitHub CLI:**
```bash
gh workflow run unified-reverse-job-engine.yml \
  -f mode=standard \
  -f sprint_duration=2 \
  -f study_hours=15
```

**Via API:**
```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/WORKFLOW_ID/dispatches \
  -d '{"ref":"main","inputs":{"mode":"standard"}}'
```

### Automated Triggers

#### On Push

Run when code or data changes:

```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'data/**'
      - 'src/**'
```

#### On Pull Request

Validate changes before merging:

```yaml
on:
  pull_request:
    branches: [ main ]
    paths:
      - 'src/**'
      - 'tests/**'
```

#### On Schedule

Regular automated analysis:

```yaml
on:
  schedule:
    # Every Monday at 9 AM UTC
    - cron: '0 9 * * 1'
    
    # Daily at midnight
    - cron: '0 0 * * *'
    
    # First day of month
    - cron: '0 0 1 * *'
```

**Example - Weekly Progress Check:**
```yaml
name: Weekly Progress Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9 AM
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run analysis
        run: |
          python src/python_advanced_job_engine.py \
            --mode reverse \
            --update-progress
      
      - name: Commit results
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add job_search_data/
          git commit -m "Weekly progress update"
          git push
```

#### On Issue/PR Events

Trigger on specific events:

```yaml
on:
  issues:
    types: [opened, labeled]
  pull_request:
    types: [opened, synchronize]
```

**Example - Analyze Job from Issue:**
```yaml
name: Analyze Job from Issue

on:
  issues:
    types: [opened, labeled]

jobs:
  analyze-if-job-posting:
    if: contains(github.event.issue.labels.*.name, 'job-posting')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Extract job description
        id: extract
        run: |
          echo "${{ github.event.issue.body }}" > job.txt
      
      - name: Analyze job
        run: |
          python src/python_advanced_job_engine.py \
            --cv-secret CV_CONTENT \
            --job job.txt
      
      - name: Comment results
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const results = fs.readFileSync('results.txt', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: results
            });
```

## Understanding Results

### Workflow Output

#### Job Summary

Displayed in workflow run:

```yaml
- name: Generate summary
  run: |
    echo "## Analysis Results" >> $GITHUB_STEP_SUMMARY
    echo "Match Score: **87%**" >> $GITHUB_STEP_SUMMARY
    echo "Critical Gaps: **3**" >> $GITHUB_STEP_SUMMARY
    echo "Learning Time: **6 weeks**" >> $GITHUB_STEP_SUMMARY
```

#### Artifacts

Download results:

```yaml
- name: Upload results
  uses: actions/upload-artifact@v3
  with:
    name: analysis-results
    path: job_search_data/export_*/
    retention-days: 30
```

**Downloading:**
1. Go to workflow run
2. Scroll to **Artifacts**
3. Click to download

#### Logs

View detailed execution:

```yaml
- name: Run analysis
  run: |
    python src/python_advanced_job_engine.py \
      --cv-secret CV_CONTENT \
      --job-secret TARGET_JOB_CONTENT \
      --verbose
```

### Result Structure

```
artifact-download/
├── complete_report.txt          # Human-readable report
├── analysis_results.json        # Structured data
├── learning_plan.json           # Learning plan
├── skill_tests.json            # Generated tests
├── cover_letter.txt            # Application letter
├── linkedin_message.txt        # Outreach message
└── improvement_strategy.json   # Reverse mode strategy
```

### Interpreting Results

#### Match Score

```json
{
  "overall_score": 87,
  "technical_score": 92,
  "experience_score": 85,
  "education_score": 80,
  "recommendation": "Strong candidate - apply with confidence"
}
```

#### Gaps

```json
{
  "critical_gaps": [
    {
      "skill": "Kubernetes",
      "current": 1,
      "required": 3,
      "priority": 95
    }
  ],
  "important_gaps": [...],
  "nice_to_have": [...]
}
```

#### Learning Plan

```json
{
  "total_weeks": 6,
  "total_hours": 60,
  "sprints": [
    {
      "number": 1,
      "goals": ["Docker Level 3", "K8s Level 2"],
      "resources": [...]
    }
  ]
}
```

## Advanced Workflows

### Multi-Job Analysis

Analyze multiple jobs in parallel:

```yaml
name: Batch Job Analysis

on:
  workflow_dispatch:
    inputs:
      job_urls:
        description: 'Job URLs (one per line)'
        required: true

jobs:
  analyze:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        job: ${{ fromJSON(github.event.inputs.job_urls) }}
    steps:
      - uses: actions/checkout@v3
      
      - name: Fetch job description
        run: curl -o job.txt ${{ matrix.job }}
      
      - name: Analyze
        run: |
          python src/python_advanced_job_engine.py \
            --cv-secret CV_CONTENT \
            --job job.txt \
            --output results_${{ strategy.job-index }}.json
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: job-${{ strategy.job-index }}
          path: results_*.json
```

### Progress Tracking Integration

Track learning progress automatically:

```yaml
name: Update Progress

on:
  schedule:
    - cron: '0 20 * * 0'  # Sunday 8 PM
  workflow_dispatch:
    inputs:
      skill:
        required: true
      new_level:
        required: true

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Update skill level
        run: |
          python src/python_advanced_job_engine.py \
            --update-progress \
            --skill "${{ github.event.inputs.skill }}" \
            --new-level "${{ github.event.inputs.new_level }}"
      
      - name: Re-analyze jobs
        run: |
          python src/python_advanced_job_engine.py \
            --mode reverse \
            --min-match 70
      
      - name: Commit changes
        run: |
          git add job_search_data/
          git commit -m "Progress update: ${{ github.event.inputs.skill }}"
          git push
```

### Integration with External Services

#### Notion Integration

```yaml
- name: Send to Notion
  env:
    NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
    NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
  run: |
    python scripts/notion_integration.py \
      --results analysis_results.json \
      --database $NOTION_DATABASE_ID
```

#### Slack Notifications

```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1
  with:
    channel-id: 'job-search'
    slack-message: |
      New analysis complete!
      Match Score: ${{ steps.analyze.outputs.score }}%
      Critical Gaps: ${{ steps.analyze.outputs.gaps }}
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

#### Email Reports

```yaml
- name: Email report
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 587
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    to: ${{ secrets.NOTIFICATION_EMAIL }}
    from: Job Engine Bot
    subject: Weekly Analysis Report
    body: file://complete_report.txt
    attachments: analysis_results.json
```

## Troubleshooting

### Common Issues

#### Workflow Doesn't Run

**Check:**
```yaml
# Verify workflow is enabled
# Settings → Actions → Disable/Enable

# Check branch protection rules
# Settings → Branches → Branch protection rules

# Verify path filters
on:
  push:
    paths:
      - 'data/**'  # Make sure this matches your structure
```

#### Secrets Not Found

```yaml
# Debug secrets availability
- name: Check secrets
  run: |
    if [ -z "${{ secrets.CV_CONTENT }}" ]; then
      echo "CV_CONTENT not set"
      exit 1
    fi
```

#### Artifact Upload Fails

```yaml
# Check file exists before upload
- name: Upload artifact
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: results
    path: |
      job_search_data/export_*
      !job_search_data/export_*/*.log
    if-no-files-found: warn
```

### Debug Mode

Enable detailed logging:

```yaml
- name: Run with debug
  env:
    ACTIONS_STEP_DEBUG: true
  run: |
    python src/python_advanced_job_engine.py \
      --verbose \
      --debug \
      --log-file workflow_debug.log
```

## Best Practices

### Workflow Organization

1. **Use descriptive names**
```yaml
name: "Job Analysis: Standard Mode"
```

2. **Add documentation**
```yaml
# This workflow analyzes job fit and generates learning plans
# Runs: Manual trigger or on job description upload
# Outputs: Analysis report, learning plan, application materials
```

3. **Group related steps**
```yaml
- name: Setup
  run: |
    mkdir -p data job_search_data
    echo "$CV_CONTENT" > data/cv.txt
```

### Performance Optimization

1. **Cache dependencies**
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

2. **Parallel execution**
```yaml
strategy:
  matrix:
    mode: [standard, reverse]
  max-parallel: 2
```

3. **Conditional execution**
```yaml
- name: Generate letters
  if: ${{ github.event.inputs.generate_letters == 'true' }}
  run: python generate_letters.py
```

### Security

1. **Minimize secret exposure**
```yaml
- name: Process CV
  env:
    CV_DATA: ${{ secrets.CV_CONTENT }}
  run: |
    # Use secret only in this step
    echo "$CV_DATA" | python process.py
```

2. **Use read-only tokens** when possible

3. **Audit workflow runs** regularly

### Maintainability

1. **Version workflows**
```yaml
# .github/workflows/analyze-v2.yml
name: Job Analysis v2.0
```

2. **Use reusable workflows**
```yaml
# .github/workflows/analyze.yml
on:
  workflow_call:
    inputs:
      mode:
        required: true
        type: string
```

3. **Document changes**
```yaml
# Changelog:
# v2.0 - Added reverse mode support
# v1.1 - Improved error handling
# v1.0 - Initial release
```

## Example Workflows

See complete examples in:
- `.github/workflows/unified-reverse-job-engine.yml`
- `examples/automation_example.py`
- `docs/tutorials/automation.md`

## Next Steps

- Review [Troubleshooting Guide](troubleshooting.md) for common issues
- Check [User Guide](user-guide.md) for feature details
- Explore [Examples](../examples/) for more workflows