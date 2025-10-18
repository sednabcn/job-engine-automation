#!/usr/bin/env python3
"""
Create Sample Data Files for Job Search Automation
Generates realistic CV and job description files for testing
"""

import os
from pathlib import Path
from datetime import datetime

def create_sample_cv(format='txt'):
    """Create a sample CV in specified format"""
    
    cv_content = """SARAH MARTINEZ
Senior Software Engineer

📧 sarah.martinez@email.com | 📱 +1 (555) 123-4567
🌐 github.com/smartinez | 💼 linkedin.com/in/smartinez
📍 San Francisco, CA

═══════════════════════════════════════════════════════════════

PROFESSIONAL SUMMARY

Results-driven Senior Software Engineer with 6+ years of experience building 
scalable web applications. Expertise in full-stack development using modern 
JavaScript frameworks and cloud technologies. Proven track record of leading 
technical initiatives and mentoring junior developers. Passionate about 
writing clean, maintainable code and implementing DevOps best practices.

═══════════════════════════════════════════════════════════════

TECHNICAL SKILLS

Programming Languages:
• JavaScript/TypeScript (Expert) • Python (Advanced) • Java (Intermediate)
• SQL (Advanced) • HTML5/CSS3 (Expert)

Frontend Technologies:
• React.js • Vue.js • Next.js • Redux • React Query
• Tailwind CSS • Material-UI • Webpack • Vite

Backend Technologies:
• Node.js • Express.js • NestJS • Django • Flask
• GraphQL • REST APIs • WebSocket • Microservices

Databases & Caching:
• PostgreSQL • MongoDB • Redis • MySQL • DynamoDB

DevOps & Cloud:
• AWS (EC2, S3, Lambda, RDS) • Docker • Kubernetes
• GitHub Actions • Jenkins • Terraform • CI/CD

Tools & Practices:
• Git • Agile/Scrum • TDD/BDD • Jest/Vitest • Cypress
• JIRA • Figma • Postman • DataDog • Sentry

═══════════════════════════════════════════════════════════════

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | San Francisco, CA
March 2021 - Present

• Led development of customer-facing dashboard serving 100K+ daily active users
  using React, TypeScript, and Node.js, improving page load time by 45%
  
• Architected and implemented microservices infrastructure using Docker and 
  Kubernetes, reducing deployment time from hours to minutes
  
• Established CI/CD pipeline with GitHub Actions, achieving 95% test coverage
  and enabling 10+ production deployments per day
  
• Mentored team of 4 junior developers, conducting code reviews and technical
  training sessions, resulting in 30% improvement in code quality metrics
  
• Implemented GraphQL API layer replacing legacy REST endpoints, reducing 
  network requests by 60% and improving mobile app performance
  
• Technologies: React, TypeScript, Node.js, PostgreSQL, Redis, AWS, Docker,
  Kubernetes, GraphQL, GitHub Actions

────────────────────────────────────────────────────────────────

Software Engineer | StartupXYZ | Mountain View, CA
June 2019 - February 2021

• Developed full-stack features for B2B SaaS platform using React and Python,
  contributing to 200% user growth over 18 months
  
• Built real-time analytics dashboard using React, D3.js, and WebSocket,
  processing 1M+ events daily with sub-second latency
  
• Optimized database queries and implemented Redis caching, reducing API
  response time by 70% and cutting infrastructure costs by $5K/month
  
• Collaborated with product and design teams in agile environment, delivering
  15+ major features across 8 sprint cycles
  
• Technologies: React, Python, Flask, PostgreSQL, Redis, AWS S3, REST APIs

────────────────────────────────────────────────────────────────

Junior Developer | Digital Solutions Ltd. | San Jose, CA
August 2018 - May 2019

• Developed responsive web applications using React and Node.js for clients
  in e-commerce and healthcare sectors
  
• Implemented automated testing suites using Jest and Cypress, achieving
  80% code coverage and reducing bugs by 40%
  
• Participated in code reviews and pair programming sessions, adhering to
  company coding standards and best practices
  
• Technologies: React, Node.js, Express, MongoDB, Jest, Cypress

═══════════════════════════════════════════════════════════════

EDUCATION

Bachelor of Science in Computer Science | GPA: 3.7/4.0
University of California, Berkeley | Berkeley, CA
Graduated: May 2018

Relevant Coursework:
• Data Structures & Algorithms • Database Systems • Web Development
• Software Engineering • Operating Systems • Computer Networks

═══════════════════════════════════════════════════════════════

PROJECTS

E-Commerce Platform | github.com/smartinez/ecommerce-platform
• Built full-stack online marketplace with 10K+ registered users
• Stack: Next.js, Node.js, PostgreSQL, Stripe API, AWS
• Features: Real-time inventory, payment processing, admin dashboard

Data Visualization Dashboard | github.com/smartinez/data-viz-dashboard
• Interactive analytics platform processing 500K+ data points
• Stack: React, D3.js, Python, FastAPI, WebSocket
• Real-time updates, custom charts, export capabilities

API Gateway Service | github.com/smartinez/api-gateway
• Microservices architecture with load balancing and rate limiting
• Stack: Node.js, Redis, Docker, Kubernetes, Kong
• Handles 1M+ requests/day with 99.9% uptime

═══════════════════════════════════════════════════════════════

CERTIFICATIONS

✓ AWS Certified Solutions Architect - Associate (2022)
✓ MongoDB Certified Developer (2021)
✓ Certified Kubernetes Administrator (CKA) (2023)

═══════════════════════════════════════════════════════════════

ACHIEVEMENTS & CONTRIBUTIONS

• Open Source Contributor: 500+ contributions to React and Next.js repos
• Tech Speaker: Presented at ReactConf 2023 on "Performance Optimization"
• Hackathon Winner: 1st place at TechCrunch Disrupt Hackathon (2022)
• Blog Author: Technical articles on Medium with 10K+ total views

═══════════════════════════════════════════════════════════════

LANGUAGES

• English (Native)
• Spanish (Professional Working Proficiency)
• Portuguese (Basic)
"""
    
    return cv_content.strip()


def create_sample_job_description(format='txt'):
    """Create a sample job description in specified format"""
    
    job_content = """SENIOR FULL STACK ENGINEER

Company: InnovateTech Solutions
Location: San Francisco, CA (Hybrid - 3 days onsite)
Type: Full-time
Experience: 5-8 years
Salary: $150,000 - $200,000 + equity

═══════════════════════════════════════════════════════════════

ABOUT US

InnovateTech Solutions is a fast-growing fintech startup revolutionizing 
digital payments. We've raised $50M Series B and serve 1M+ customers across 
North America. Our mission is to make financial services accessible and 
transparent for everyone.

We're looking for a talented Senior Full Stack Engineer to join our 
Platform Engineering team. You'll work on cutting-edge technology solving 
complex problems at scale.

═══════════════════════════════════════════════════════════════

THE ROLE

As a Senior Full Stack Engineer, you'll be responsible for designing and 
implementing scalable web applications that process millions of transactions 
daily. You'll collaborate with product managers, designers, and engineers 
to deliver features that delight our users.

This is a hands-on role where you'll write code daily while also providing 
technical leadership and mentoring junior team members.

═══════════════════════════════════════════════════════════════

KEY RESPONSIBILITIES

• Design and develop scalable full-stack features using React and Node.js
• Build and maintain microservices architecture handling high-traffic loads
• Write clean, maintainable, well-tested code following best practices
• Participate in architectural decisions and technical planning
• Conduct code reviews and provide constructive feedback to team members
• Mentor junior developers and contribute to team's technical growth
• Collaborate with cross-functional teams in agile development environment
• Optimize application performance and database queries
• Implement security best practices and ensure data protection
• Participate in on-call rotation for production support (1 week/month)

═══════════════════════════════════════════════════════════════

REQUIRED QUALIFICATIONS

Technical Skills:
• 5+ years of professional software development experience
• Expert-level proficiency in JavaScript/TypeScript
• Strong experience with React.js and modern frontend frameworks
• Solid backend development experience with Node.js or Python
• Experience with PostgreSQL or similar relational databases
• Understanding of RESTful API design and implementation
• Proficiency with Git and version control workflows
• Experience with cloud platforms (AWS, GCP, or Azure)
• Knowledge of Docker and containerization
• Understanding of CI/CD pipelines and DevOps practices

Soft Skills:
• Excellent problem-solving and analytical abilities
• Strong communication skills (written and verbal)
• Ability to work independently and in team settings
• Experience working in agile/scrum environments
• Passion for learning new technologies
• Attention to detail and commitment to quality

═══════════════════════════════════════════════════════════════

PREFERRED QUALIFICATIONS

• Experience with GraphQL
• Knowledge of Kubernetes and container orchestration
• Experience with serverless architectures (Lambda, Cloud Functions)
• Background in fintech or payment processing systems
• Experience with microservices architecture
• Knowledge of Redis or other caching technologies
• Experience with monitoring tools (DataDog, New Relic, Sentry)
• Contributions to open-source projects
• Experience with TypeScript in production environments
• Knowledge of security best practices (OWASP, encryption, etc.)
• Experience with message queues (RabbitMQ, Kafka)
• Understanding of event-driven architectures
• Previous experience in high-growth startup environment

═══════════════════════════════════════════════════════════════

EDUCATION

• Bachelor's degree in Computer Science, Engineering, or related field
  (or equivalent practical experience)
• Advanced degree is a plus but not required

═══════════════════════════════════════════════════════════════

WHAT YOU'LL WORK WITH

Frontend Stack:
• React.js, TypeScript, Next.js
• Redux, React Query
• Tailwind CSS, Material-UI
• Vite, Webpack

Backend Stack:
• Node.js, Express.js, NestJS
• Python, FastAPI (for ML services)
• GraphQL, REST APIs
• WebSocket for real-time features

Data & Infrastructure:
• PostgreSQL (primary database)
• Redis (caching and sessions)
• MongoDB (logging and analytics)
• AWS (EC2, S3, Lambda, RDS, CloudFront)
• Docker, Kubernetes
• GitHub Actions for CI/CD
• DataDog for monitoring
• Sentry for error tracking

═══════════════════════════════════════════════════════════════

WHAT WE OFFER

Compensation & Benefits:
• Competitive base salary ($150K - $200K based on experience)
• Equity package (stock options)
• Annual performance bonus
• Comprehensive health, dental, and vision insurance
• 401(k) with company match (4%)
• Life and disability insurance

Work-Life Balance:
• Flexible hybrid work model (3 days in office)
• Unlimited PTO policy
• Paid parental leave (16 weeks)
• Flexible working hours
• Work-from-home stipend ($1,000)

Professional Development:
• Annual learning & development budget ($2,500)
• Conference attendance support
• Internal tech talks and workshops
• Mentorship program
• Career growth opportunities

Perks:
• Latest MacBook Pro and accessories
• Catered lunch 3x per week
• Gym membership reimbursement
• Commuter benefits
• Team building events and offsites
• Stock in standing desks and ergonomic equipment

═══════════════════════════════════════════════════════════════

OUR ENGINEERING CULTURE

• Engineering-driven decision making
• Strong emphasis on code quality and testing (80%+ coverage required)
• Continuous integration and deployment (10+ deploys/day)
• Collaborative code reviews
• Regular tech talks and knowledge sharing
• Quarterly hack weeks
• Open source contribution encouraged
• Innovation time (20% time for personal projects)

═══════════════════════════════════════════════════════════════

INTERVIEW PROCESS

1. Initial Screen (30 min) - Recruiter call
2. Technical Phone Screen (60 min) - Coding exercise
3. Take-home Project (4-6 hours) - Build a feature
4. Onsite Interviews (4 hours):
   - System Design (90 min)
   - Coding Deep Dive (90 min)
   - Behavioral & Culture Fit (60 min)
5. Final Interview - Meet the team & leadership

We strive to complete the entire process within 2 weeks.

═══════════════════════════════════════════════════════════════

EQUAL OPPORTUNITY EMPLOYER

InnovateTech Solutions is an equal opportunity employer. We celebrate 
diversity and are committed to creating an inclusive environment for all 
employees. We do not discriminate based on race, religion, color, national 
origin, gender, sexual orientation, age, marital status, veteran status, or 
disability status.

═══════════════════════════════════════════════════════════════

TO APPLY

Please submit:
• Your resume/CV
• Link to your GitHub profile
• Link to your portfolio or personal website (if available)
• Brief cover letter explaining why you're interested in this role

We review applications on a rolling basis and will contact qualified 
candidates within 1 week.

Questions? Email: careers@innovatetech.com
"""
    
    return job_content.strip()


def save_file(content, filepath, format='txt'):
    """Save content to file in specified format"""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == 'txt':
        path.write_text(content, encoding='utf-8')
    else:
        # For PDF/DOCX, we'll save as TXT with instructions
        path.write_text(content, encoding='utf-8')
    
    return path


def main():
    """Main function to create sample files"""
    
    print("=" * 70)


if __name__ == "__main__":
    main() * 70)
    print("🚀 Creating Sample Data Files for Job Search Automation")
    print("=" * 70)
    print()
    
    # Ensure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Create CV files
    print("📄 Creating sample CV...")
    cv_content = create_sample_cv()
    
    cv_txt = save_file(cv_content, "data/my_cv.txt", "txt")
    print(f"  ✅ Created: {cv_txt}")
    print(f"     Size: {cv_txt.stat().st_size:,} bytes")
    print(f"     Words: {len(cv_content.split()):,}")
    
    # Create job description files
    print()
    print("📋 Creating sample job description...")
    job_content = create_sample_job_description()
    
    job_txt = save_file(job_content, "data/target_job.txt", "txt")
    print(f"  ✅ Created: {job_txt}")
    print(f"     Size: {job_txt.stat().st_size:,} bytes")
    print(f"     Words: {len(job_content.split()):,}")
    
    # Create README
    print()
    print("📖 Creating data directory README...")
    readme_content = """# Data Directory

## Files

- `my_cv.txt` - Sample CV (Sarah Martinez - Senior Software Engineer)
- `target_job.txt` - Sample Job Description (Senior Full Stack Engineer)

## Usage

### Replace with Your Files

1. Delete or rename the sample files
2. Add your own CV and job descriptions
3. Supported formats: `.txt`, `.pdf`, `.docx`

### Example Commands

```bash
# Test locally
python3 -c "
from src.python_advanced_job_engine import AdvancedJobEngine
engine = AdvancedJobEngine()
analysis = engine.analyze_from_files(
    cv_file='data/my_cv.txt',
    job_file='data/target_job.txt'
)
print(f'Match Score: {analysis[\"score\"][\"total_score\"]}%')
"

# Run workflow
gh workflow run auto-job-analysis.yml \\
  -f cv_file=data/my_cv.txt \\
  -f job_file=data/target_job.txt
```

## Tips

- Keep filenames simple (no spaces)
- Use descriptive names for multiple jobs
- Update CV after completing each sprint
- Save multiple job postings for batch analysis

## File Formats

### Text (.txt)
✅ Simple and reliable
✅ Easy to edit
✅ Version control friendly
⚠️ No formatting

### PDF (.pdf)
✅ Professional appearance
✅ Preserves formatting
⚠️ Harder to edit
⚠️ Text extraction can fail

### Word (.docx)
✅ Easy to edit
✅ Common format
⚠️ Requires python-docx library
⚠️ Can have compatibility issues
"""
    
    readme_path = save_file(readme_content, "data/README.md", "txt")
    print(f"  ✅ Created: {readme_path}")
    
    # Summary
    print()
    print("=" * 70)
    print("✅ SETUP COMPLETE")
    print("=" * 70)
    print()
    print("📁 Files created in data/ directory:")
    print("   • my_cv.txt (sample CV)")
    print("   • target_job.txt (sample job description)")
    print("   • README.md (instructions)")
    print()
    print("🧪 Test the files:")
    print("   python3 -c \"from src.python_advanced_job_engine import AdvancedJobEngine; \\")
    print("   engine = AdvancedJobEngine(); \\")
    print("   print('CV:', len(engine.read_document('data/my_cv.txt').split()), 'words'); \\")
    print("   print('Job:', len(engine.read_document('data/target_job.txt').split()), 'words')\"")
    print()
    print("📤 Commit to GitHub:")
    print("   git add data/")
    print("   git commit -m \"Add sample CV and job description\"")
    print("   git push")
    print()
    print("🚀 Run workflow:")
    print("   gh workflow run auto-job-analysis.yml \\")
    print("     -f cv_file=data/my_cv.txt \\")
    print("     -f job_file=data/target_job.txt")
    print()
    print("="
