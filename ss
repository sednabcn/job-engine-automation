name: Auto Job Analysis

on:
  workflow_dispatch:
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

  push:
    paths:
      - 'data/**'

jobs:
  analyze:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Create output directories
      run: |
        mkdir -p job_search_data
        mkdir -p output

    - name: Run job analysis
      id: analysis
      run: |
        python << 'EOF'
        from src.python_advanced_job_engine import AdvancedJobEngine
        import json
        import os
        
        # Initialize engine
        engine = AdvancedJobEngine()
        
        # Get inputs
        cv_file = "${{ github.event.inputs.cv_file }}" or "data/my_cv.pdf"
        job_file = "${{ github.event.inputs.job_file }}" or "data/job_description.pdf"
        job_title = "${{ github.event.inputs.job_title }}" or None
        company = "${{ github.event.inputs.company_name }}" or None
        
        # Run analysis
        print(f"Analyzing: {cv_file} vs {job_file}")
        analysis = engine.analyze_from_files(
            cv_file=cv_file,
            job_file=job_file,
            job_title=job_title,
            company=company
        )
        
        # Generate learning plan
        print("Creating learning plan...")
        learning_plan = engine.create_learning_plan(analysis, mode="standard")
        
        # Generate improvement strategy
        print("Creating improvement strategy...")
        strategy = engine.create_improvement_strategy(analysis, learning_plan)
        
        # Generate application materials
        print("Generating application materials...")
        letters = engine.generate_recruiter_letter(analysis, learning_plan)
        
        # Generate skill tests
        print("Creating skill tests...")
        tests = engine.generate_skill_tests(analysis['gaps']['missing_required_skills'])
        
        # Save results
        job_id = analysis['job_id']
        
        # Save match score
        with open('output/match_score.json', 'w') as f:
            json.dump(analysis['score'], f, indent=2)
        
        # Save gap analysis
        with open('output/gap_analysis.json', 'w') as f:
            json.dump(analysis['gaps'], f, indent=2)
        
        # Save learning plan
        with open('output/learning_plan.json', 'w') as f:
            json.dump(learning_plan, f, indent=2)
        
        # Save improvement strategy
        with open('output/improvement_strategy.md', 'w') as f:
            f.write(strategy)
        
        # Save application materials
        with open('output/cover_letter.txt', 'w') as f:
            f.write(letters.get('cover_letter', ''))
        
        with open('output/linkedin_message.txt', 'w') as f:
            f.write(letters.get('linkedin_message', ''))
        
        with open('output/followup_email.txt', 'w') as f:
            f.write(letters.get('followup_email', ''))
        
        with open('output/networking_email.txt', 'w') as f:
            f.write(letters.get('networking_email', ''))
        
        # Save skill tests
        with open('output/skill_tests.json', 'w') as f:
            json.dump(tests, f, indent=2)
        
        # Create complete report
        report = f"""# Job Match Analysis Report
        
## Match Score: {analysis['score']['total_score']}%

### Score Breakdown
"""
        for category, score in analysis['score']['breakdown'].items():
            report += f"- {category.replace('_', ' ').title()}: {score}%\n"
        
        report += f"\n### Missing Required Skills ({len(analysis['gaps']['missing_required_skills'])})\n"
        for skill in analysis['gaps']['missing_required_skills']:
            report += f"- {skill}\n"
        
        report += f"\n### Missing Preferred Skills ({len(analysis['gaps']['missing_preferred_skills'])})\n"
        for skill in analysis['gaps']['missing_preferred_skills']:
            report += f"- {skill}\n"
        
        report += f"\n### Experience Gap: {analysis['gaps']['experience_gap']} years\n"
        report += f"### Education Gap: {analysis['gaps']['education_gap']}\n"
        
        with open('output/complete_report.md', 'w') as f:
            f.write(report)
        
        # Create summary
        summary = f"""ANALYSIS SUMMARY
        
Job ID: {job_id}
Match Score: {analysis['score']['total_score']}%
Status: {'STRONG CANDIDATE' if analysis['score']['total_score'] >= 75 else 'NEEDS IMPROVEMENT'}

Action: {'Apply now!' if analysis['score']['total_score'] >= 75 else f"Improve for {12 if analysis['score']['total_score'] < 60 else 4}-{24 if analysis['score']['total_score'] < 60 else 8} weeks"}

Files generated:
- complete_report.md
- match_score.json
- gap_analysis.json
- learning_plan.json
- improvement_strategy.md
- cover_letter.txt
- linkedin_message.txt
- followup_email.txt
- networking_email.txt
- skill_tests.json
"""
        
        with open('output/summary.txt', 'w') as f:
            f.write(summary)
        
        print(f"\n✓ Analysis complete! Score: {analysis['score']['total_score']}%")
        print(f"✓ Job ID: {job_id}")
        
        # Set output for next steps
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"score={analysis['score']['total_score']}\n")
            f.write(f"job_id={job_id}\n")
        
        EOF

    - name: Upload results as artifact
      uses: actions/upload-artifact@v4
      with:
        name: job-analysis-results
        path: output/
        retention-days: 90

    - name: Create summary
      run: |
        echo "## 🎯 Job Analysis Complete!" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "**Match Score:** ${{ steps.analysis.outputs.score }}%" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "📥 Download the 'job-analysis-results' artifact to view all reports" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        cat output/summary.txt >> $GITHUB_STEP_SUMMARY
```

---

## 2. Required Directory Structure:
```
.
├── .github/
│   └── workflows/
│       └── autojob-analysis.yml
├── data/
│   ├── my_cv.pdf
│   └── job_description.pdf
├── src/
│   └── python_advanced_job_engine.py
├── output/
│   └── (generated files will appear here)
├── job_search_data/
│   └── (data storage)
└── requirements.txt