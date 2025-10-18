# Job Search Templates

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