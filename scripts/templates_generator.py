"""
Job Search Templates Generator
Creates all necessary template files for the job search automation system
"""

import os
from pathlib import Path

def create_templates():
    """Generate all template files in job_search_data/templates/"""
    
    templates_dir = Path("job_search_data/templates")
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    templates = {
        # =============================================
        # COVER LETTER TEMPLATE
        # =============================================
        "cover_letter_template.txt": """Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my background in {top_skills} and proven track record in {key_achievements}, I am excited about the opportunity to contribute to your team.

## Why I'm a Great Fit

Your job posting emphasizes {key_requirements}. I bring:

{matching_skills_section}

## Recent Accomplishments

{achievements_section}

## Addressing Growth Areas

I notice your position requires {missing_skills}. To bridge this gap, I have:

{learning_progress_section}

## What Excites Me About This Role

{motivation_section}

I am particularly drawn to {company_name} because {company_research}. I would welcome the opportunity to discuss how my background, skills, and enthusiasm can contribute to your team's success.

Thank you for considering my application. I look forward to speaking with you.

Best regards,
{candidate_name}
{contact_info}

---
Attachments:
- Resume/CV
- Portfolio: {portfolio_link}
- GitHub: {github_link}
- LinkedIn: {linkedin_link}
""",

        # =============================================
        # LINKEDIN MESSAGE TEMPLATE
        # =============================================
        "linkedin_message_template.txt": """Subject: {job_title} at {company_name} - Impressed by Your Work

Hi {recruiter_name},

I hope this message finds you well. I recently came across the {job_title} opening at {company_name} and was immediately drawn to it.

Quick context on my background:
• {skill_1} with {experience_1}
• {skill_2} with {experience_2}
• {skill_3} with {experience_3}

What caught my attention:
{company_highlight}

I've been actively developing skills in {growth_areas} to strengthen my candidacy. Recent projects include:
→ {project_1}
→ {project_2}

Current match score: {match_score}% (and growing!)

Would you be open to a brief conversation about this role? I'd love to learn more about the team's priorities and share how I could contribute.

Portfolio: {portfolio_link}

Thanks for your consideration!

Best,
{candidate_name}
""",

        # =============================================
        # FOLLOW-UP EMAIL TEMPLATE
        # =============================================
        "followup_email_template.txt": """Subject: Following Up - {job_title} Application

Dear {recruiter_name},

I hope this email finds you well. I wanted to follow up on my application for the {job_title} position submitted on {application_date}.

Since applying, I've continued to strengthen my qualifications:

{recent_progress}

Key highlights of my application:
• Match Score: {match_score}%
• Relevant Projects: {project_count}
• Skills Mastered: {skills_count}

Strong alignment in:
✓ {strength_1}
✓ {strength_2}
✓ {strength_3}

Growing in:
→ {growth_area_1} - {progress_1}
→ {growth_area_2} - {progress_2}

I remain very interested in this opportunity and would welcome the chance to discuss how I can contribute to {company_name}.

Portfolio: {portfolio_link}
Latest Project: {recent_project_link}

Thank you for your time and consideration.

Best regards,
{candidate_name}
{phone}
{email}
""",

        # =============================================
        # NETWORKING EMAIL TEMPLATE
        # =============================================
        "networking_email_template.txt": """Subject: Advice from a {their_role} - Career Transition Question

Hi {contact_name},

I hope this message finds you well. My name is {candidate_name}, and I'm working toward a career in {target_field}.

I came across your profile and was impressed by your work on {their_achievement}. I'm particularly interested in {specific_area} and would greatly appreciate any insights you might share.

My background:
• {background_summary}
• Current focus: {current_learning}
• Recent projects: {project_highlights}

I'm specifically curious about:
1. {question_1}
2. {question_2}
3. {question_3}

Would you be open to a 15-minute coffee chat (virtual or in-person)? I'd love to learn from your experience.

No pressure at all - I know you're busy! Even a brief email response would be incredibly valuable.

Thank you for considering.

Best regards,
{candidate_name}
Portfolio: {portfolio_link}
LinkedIn: {linkedin_link}
""",

        # =============================================
        # REJECTION RESPONSE TEMPLATE
        # =============================================
        "rejection_response_template.txt": """Subject: Thank You - Future Opportunities at {company_name}

Dear {recruiter_name},

Thank you for considering my application for the {job_title} position and for taking the time to inform me of your decision.

While I'm disappointed, I remain very interested in {company_name} and would welcome the opportunity to be considered for future openings.

Since my application, I've continued growing:
{recent_improvements}

I'm particularly interested in:
• {interest_area_1}
• {interest_area_2}
• {interest_area_3}

If you have a moment, I would greatly appreciate any feedback on my application. Understanding areas for improvement would be invaluable as I continue developing my skills.

Thank you again for your consideration. I hope our paths cross again in the future.

Best regards,
{candidate_name}
Portfolio: {portfolio_link}
""",

        # =============================================
        # COLD APPLICATION EMAIL TEMPLATE
        # =============================================
        "cold_application_template.txt": """Subject: {job_title} Candidate - {unique_value_proposition}

Dear {hiring_manager_name},

I'm reaching out to express interest in {job_title} opportunities at {company_name}. While I don't see an active posting, I believe my background aligns well with your team's needs.

Why I'm reaching out:
{company_research}

What I bring:
• {skill_category_1}: {specific_skills_1}
• {skill_category_2}: {specific_skills_2}
• {skill_category_3}: {specific_skills_3}

Recent work:
{project_showcase}

My approach to continuous growth:
✓ Current match score for similar roles: {match_score}%
✓ Active learning: {current_learning}
✓ {sprint_count} completed learning sprints
✓ {project_count} relevant projects

I understand timing might not be right, but I'd welcome the opportunity to connect and discuss how I could contribute to {company_name}'s success.

Portfolio: {portfolio_link}
GitHub: {github_link}

Would you be open to a brief conversation?

Best regards,
{candidate_name}
{contact_info}
""",

        # =============================================
        # INTERVIEW PREP TEMPLATE
        # =============================================
        "interview_prep_template.txt": """# Interview Preparation: {job_title} at {company_name}

## Company Research
- Founded: {company_founded}
- Mission: {company_mission}
- Recent news: {recent_news}
- Products/Services: {products}
- Culture: {culture_notes}

## Role Analysis
- Key responsibilities: {responsibilities}
- Required skills: {required_skills}
- Team structure: {team_info}
- Growth opportunities: {growth_potential}

## My Match Profile
- Overall score: {match_score}%
- Strengths: {top_strengths}
- Growth areas: {growth_areas}
- Recent progress: {recent_improvements}

## STAR Stories Prepared

### Story 1: {achievement_1_title}
**Situation:** {situation_1}
**Task:** {task_1}
**Action:** {action_1}
**Result:** {result_1}

### Story 2: {achievement_2_title}
**Situation:** {situation_2}
**Task:** {task_2}
**Action:** {action_2}
**Result:** {result_2}

### Story 3: {achievement_3_title}
**Situation:** {situation_3}
**Task:** {task_3}
**Action:** {action_3}
**Result:** {result_3}

## Technical Prep
- Skills to review: {technical_review}
- Practice problems: {practice_links}
- Portfolio pieces to highlight: {portfolio_highlights}

## Questions to Ask Them
1. {question_1}
2. {question_2}
3. {question_3}
4. {question_4}
5. {question_5}

## Addressing Gaps
**Gap:** {gap_1}
**Response:** {gap_response_1}

**Gap:** {gap_2}
**Response:** {gap_response_2}

## Logistics
- Date/Time: {interview_datetime}
- Format: {interview_format}
- Duration: {interview_duration}
- Interviewer(s): {interviewer_names}
- What to bring: {materials_needed}

## Post-Interview
- Send thank you within 24 hours
- Mention specific discussion points
- Reiterate interest
- Address any concerns raised
""",

        # =============================================
        # PROJECT SHOWCASE TEMPLATE
        # =============================================
        "project_showcase_template.txt": """# Project: {project_name}

## Overview
{project_description}

**Live Demo:** {demo_link}
**Source Code:** {github_link}
**Documentation:** {docs_link}

## Technical Details

### Technologies Used
{tech_stack}

### Key Features
1. {feature_1}
2. {feature_2}
3. {feature_3}
4. {feature_4}

### Architecture
{architecture_description}

## Skills Demonstrated
✓ {skill_1}
✓ {skill_2}
✓ {skill_3}
✓ {skill_4}

## Challenges & Solutions

**Challenge 1:** {challenge_1}
**Solution:** {solution_1}

**Challenge 2:** {challenge_2}
**Solution:** {solution_2}

## Metrics/Results
- {metric_1}
- {metric_2}
- {metric_3}

## Learning Outcomes
{learning_summary}

## Future Enhancements
→ {enhancement_1}
→ {enhancement_2}
→ {enhancement_3}

---
*Developed as part of Sprint {sprint_number} - {completion_date}*
""",

        # =============================================
        # SKILL TEST TEMPLATE
        # =============================================
        "skill_test_template.txt": """# Skill Assessment: {skill_name}

**Level:** {difficulty_level}
**Estimated Time:** {time_estimate}
**Passing Score:** 70%

## Knowledge Check (40%)

### Question 1 (10 points)
{question_1}

**Your Answer:**
{answer_space}

**Correct Answer:**
{correct_answer_1}

---

### Question 2 (10 points)
{question_2}

**Your Answer:**
{answer_space}

**Correct Answer:**
{correct_answer_2}

---

### Question 3 (10 points)
{question_3}

**Your Answer:**
{answer_space}

**Correct Answer:**
{correct_answer_3}

---

### Question 4 (10 points)
{question_4}

**Your Answer:**
{answer_space}

**Correct Answer:**
{correct_answer_4}

## Practical Exercise (60%)

### Exercise Description
{exercise_description}

### Requirements
1. {requirement_1}
2. {requirement_2}
3. {requirement_3}
4. {requirement_4}

### Evaluation Criteria
- Code quality (15 points)
- Functionality (20 points)
- Best practices (15 points)
- Documentation (10 points)

### Submission
**Repository:** {submission_repo}
**Deadline:** {deadline}

## Scoring

| Component | Points | Score |
|-----------|--------|-------|
| Knowledge Check | 40 | ___ |
| Practical Exercise | 60 | ___ |
| **Total** | **100** | **___** |

**Result:** {pass_fail}

## Feedback
{feedback_notes}

## Next Steps
{next_steps}

---
*Test taken: {test_date}*
*Graded by: {grader}*
""",

        # =============================================
        # SPRINT PLAN TEMPLATE
        # =============================================
        "sprint_plan_template.txt": """# Sprint {sprint_number}: {sprint_title}

**Start Date:** {start_date}
**Target End Date:** {end_date}
**Duration:** 14 days

## Goals
{sprint_goals}

## Skills to Master
1. **{skill_1}** - {skill_1_description}
2. **{skill_2}** - {skill_2_description}
3. **{skill_3}** - {skill_3_description}

## Project Goal
{project_description}

**Deliverable:** {deliverable}
**Repository:** {repo_link}

## Daily Breakdown

### Week 1: Foundation & Learning

**Days 1-3: Theory & Basics**
- [ ] Study {skill_1} fundamentals
- [ ] Complete tutorial: {tutorial_1_link}
- [ ] Practice exercises: {exercises_1}
- Target: 3-4 hours/day

**Days 4-7: Practice & Application**
- [ ] Build mini-project 1: {mini_project_1}
- [ ] Study {skill_2} concepts
- [ ] Complete tutorial: {tutorial_2_link}
- Target: 3-4 hours/day

### Week 2: Integration & Mastery

**Days 8-10: Advanced Topics**
- [ ] Study {skill_3} advanced features
- [ ] Integrate skills in main project
- [ ] Code review and refactoring
- Target: 4-5 hours/day

**Days 11-13: Project Completion**
- [ ] Complete project features
- [ ] Write documentation
- [ ] Prepare presentation
- Target: 4-5 hours/day

**Day 14: Testing & Submission**
- [ ] Take skill tests
- [ ] Submit project
- [ ] Complete sprint retrospective
- Target: 3-4 hours

## Resources
- Documentation: {docs_links}
- Tutorials: {tutorial_links}
- Community: {community_links}
- Mentor/Support: {mentor_info}

## Success Criteria
✓ Complete project with all features
✓ Pass skill tests (70%+ each)
✓ Document learning journey
✓ Deploy working demo

## Daily Log Template
```
Date: ___________
Hours: ____
Concepts learned: 
- 
- 
Notes:


Challenges:


Tomorrow's plan:

```

## Sprint Retrospective (Day 14)
**What went well:**


**What could improve:**


**Skills gained:**


**Next sprint focus:**


---
*Created: {creation_date}*
*Status: {status}*
""",

        # =============================================
        # LEARNING PLAN TEMPLATE
        # =============================================
        "learning_plan_template.txt": """# Learning Plan: {job_title} at {company_name}

**Generated:** {generation_date}
**Mode:** {mode}
**Current Match Score:** {current_score}%
**Target Score:** {target_score}%
**Gap to Close:** {score_gap}%

## Executive Summary
{summary}

## Estimated Timeline
**Total Duration:** {total_duration}
**Sprints Required:** {sprint_count}
**Hours Per Week:** {hours_per_week}
**Target Completion:** {completion_date}

---

## Phase 1: Foundation (Tier 1 Critical Skills)

### Skills to Master
{tier1_skills}

### Estimated Duration
{tier1_duration}

### Success Criteria
- [ ] Pass beginner-level tests for each skill
- [ ] Complete 2 foundational projects
- [ ] Reach 65% match score (Foundation Gate)

### Recommended Resources
{tier1_resources}

---

## Phase 2: Competency (Tier 2 Important Skills)

### Skills to Master
{tier2_skills}

### Estimated Duration
{tier2_duration}

### Success Criteria
- [ ] Pass intermediate-level tests
- [ ] Complete 2 intermediate projects
- [ ] Reach 80% match score (Competency Gate)

### Recommended Resources
{tier2_resources}

---

## Phase 3: Mastery (Tier 3 Nice-to-Have Skills)

### Skills to Master
{tier3_skills}

### Estimated Duration
{tier3_duration}

### Success Criteria
- [ ] Pass advanced-level tests
- [ ] Complete 1 production-grade project
- [ ] Reach 90% match score (Mastery Gate)

### Recommended Resources
{tier3_resources}

---

## Phase 4: Positioning (Professional Branding)

### Activities
1. **Portfolio Development**
   - Showcase top 5 projects
   - Professional documentation
   - Live demos

2. **Professional Presence**
   - LinkedIn optimization
   - GitHub profile polish
   - Technical blog/articles

3. **Networking**
   - Connect with {networking_count} professionals
   - Attend {events_count} events/meetups
   - Contribute to open source

4. **Application Preparation**
   - Customize resume
   - Prepare STAR stories
   - Mock interviews

### Duration
{phase4_duration}

---

## Quality Gates

| Gate | Requirements | Status |
|------|-------------|--------|
| Foundation | 65% score, 2 projects | {foundation_status} |
| Competency | 80% score, 4 projects | {competency_status} |
| Mastery | 90% score, 5 projects | {mastery_status} |
| Application Ready | All gates + branding | {application_status} |

---

## Skill Prioritization Matrix

### Must Have (Do First)
{must_have_skills}

### Should Have (Do Second)
{should_have_skills}

### Nice to Have (Do If Time)
{nice_to_have_skills}

---

## Weekly Schedule Template

**Monday-Friday (Weekday Learning)**
- Morning: {weekday_morning_plan}
- Lunch: {weekday_lunch_plan}
- Evening: {weekday_evening_plan}
- Target: 2-3 hours/day

**Saturday-Sunday (Weekend Deep Dive)**
- Morning: {weekend_morning_plan}
- Afternoon: {weekend_afternoon_plan}
- Evening: {weekend_evening_plan}
- Target: 5-6 hours/day

**Total Weekly:** {total_weekly_hours} hours

---

## Progress Tracking

### Milestones
- [ ] Week 4: Foundation Gate (65%)
- [ ] Week 8: Competency Gate (80%)
- [ ] Week 12: Mastery Gate (90%)
- [ ] Week 14: Application Ready

### Sprint Schedule
{sprint_schedule}

---

## Risk Mitigation

**Challenge:** {challenge_1}
**Mitigation:** {mitigation_1}

**Challenge:** {challenge_2}
**Mitigation:** {mitigation_2}

**Challenge:** {challenge_3}
**Mitigation:** {mitigation_3}

---

## Success Metrics

### Quantitative
- Match score improvement: {score_improvement}%
- Skills mastered: {skills_target}
- Projects completed: {projects_target}
- Test pass rate: 100%

### Qualitative
- Confidence level in target role
- Quality of portfolio projects
- Professional network growth
- Interview performance

---

*Generated by Reverse-Engine Job Search System*
*Next review: {next_review_date}*
""",

        # =============================================
        # README FOR TEMPLATES
        # =============================================
        "README.md": """# Job Search Templates

This directory contains templates used by the Reverse-Engine Job Search automation system.

## Templates Overview

### Application Materials
- `cover_letter_template.txt` - Customizable cover letter with skill matching
- `linkedin_message_template.txt` - Professional networking messages
- `followup_email_template.txt` - Post-application follow-ups
- `networking_email_template.txt` - Cold outreach to professionals
- `rejection_response_template.txt` - Professional responses to rejections
- `cold_application_template.txt` - Proactive job inquiries

### Planning & Tracking
- `learning_plan_template.txt` - Comprehensive skill development roadmap
- `sprint_plan_template.txt` - 2-week focused learning sprints
- `interview_prep_template.txt` - Complete interview preparation guide

### Assessment
- `skill_test_template.txt` - Self-assessment skill tests
- `project_showcase_template.txt` - Project documentation format

## Template Variables

All templates use `{variable_name}` syntax for replacements:

### Common Variables
- `{job_title}` - Target job position
- `{company_name}` - Target company
- `{match_score}` - Current CV-job match percentage
- `{candidate_name}` - Your name
- `{portfolio_link}` - Your portfolio URL
- `{github_link}` - Your GitHub profile
- `{linkedin_link}` - Your LinkedIn profile

### Skill-Related
- `{top_skills}` - Your strongest skills
- `{missing_skills}` - Skills to develop
- `{current_learning}` - What you're currently learning
- `{skills_mastered}` - Skills you've completed

### Progress Tracking
- `{sprint_number}` - Current sprint number
- `{project_count}` - Number of completed projects
- `{skills_count}` - Number of mastered skills
- `{total_hours}` - Learning hours invested

## Usage

Templates are automatically populated by the job search engine when:
1. Analyzing a new job posting
2. Generating application materials
3. Creating learning plans
4. Starting new sprints

### Manual Customization

You can edit any template to match your:
- Writing style
- Industry norms
- Personal branding
- Cultural context

**Note:** Keep variable placeholders `{like_this}` intact for automation to work.

## Best Practices

1. **Keep variables intact** - Don't modify `{variable_name}` syntax
2. **Customize tone** - Adjust language to match your style
3. **Add sections** - Include additional content as needed
4. **Test locally** - Review generated output before sending
5. **Version control** - Commit template changes to track improvements

## Template Development

To create new templates:

1. Create new `.txt` file in this directory
2. Use `{variable_name}` for dynamic content
3. Add clear section headers
4. Include usage instructions in comments
5. Update this README

## Questions?

See main project README or open an issue on GitHub.

---
*Part of the Reverse-Engine Job Search Automation System*
"""
    }
    
    # Create all template files
    for filename, content in templates.items():
        filepath = templates_dir / filename
        filepath.write_text(content.strip())
        print(f"✅ Created: {filepath}")
    
    print(f"\n🎉 Successfully created {len(templates)} templates in {templates_dir}/")
    print("\n📋 Template files created:")
    for filename in sorted(templates.keys()):
        print(f"   - {filename}")
    
    return templates_dir

if __name__ == "__main__":
    create_templates()
