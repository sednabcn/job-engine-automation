"""
Mock data for testing
Provides sample data structures for unit and integration tests
"""

from datetime import datetime, timedelta


# ============================================================================
# CV MOCK DATA
# ============================================================================

MOCK_CV_TEXT = """
John Doe
Senior Software Engineer
john.doe@email.com | +1-555-123-4567 | linkedin.com/in/johndoe
San Francisco, CA | github.com/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with 7+ years of expertise in Python development,
web applications, and cloud infrastructure. Proven track record of delivering
scalable solutions and leading technical teams.

WORK EXPERIENCE

Senior Python Developer | Tech Innovations Inc. | 2021 - Present
- Led development of microservices architecture serving 1M+ daily users
- Implemented CI/CD pipelines reducing deployment time by 60%
- Mentored team of 5 junior developers
- Technologies: Python, Django, PostgreSQL, Docker, Kubernetes, AWS

Python Developer | StartupXYZ | 2018 - 2021
- Built RESTful APIs handling 10k+ requests per second
- Developed data processing pipelines using Apache Spark
- Integrated payment systems with Stripe and PayPal
- Technologies: Python, Flask, MongoDB, Redis, RabbitMQ

Junior Developer | CodeCraft Solutions | 2016 - 2018
- Developed web applications using Django framework
- Wrote unit and integration tests achieving 90% coverage
- Collaborated with frontend team using React
- Technologies: Python, Django, PostgreSQL, Git, Jenkins

TECHNICAL SKILLS
Languages: Python, JavaScript, SQL, Bash
Frameworks: Django, Flask, FastAPI, React
Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
DevOps: Docker, Kubernetes, Jenkins, GitLab CI, AWS, Terraform
Tools: Git, Jira, Confluence, Postman

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2012 - 2016
GPA: 3.8/4.0

CERTIFICATIONS
- AWS Certified Solutions Architect - Associate (2022)
- Certified Kubernetes Administrator (2021)
- Python Institute PCAP (2019)

PROJECTS
Personal Finance Tracker | github.com/johndoe/finance-tracker
- Full-stack application with Django backend and React frontend
- Deployed on AWS using Docker containers
- 500+ GitHub stars

Open Source Contributions
- Django REST Framework: Bug fixes and documentation improvements
- Contributor to several Python packages on PyPI
"""

MOCK_CV_PARSED = {
    'contact': {
        'name': 'John Doe',
        'email': 'john.doe@email.com',
        'phone': '+1-555-123-4567',
        'location': 'San Francisco, CA',
        'linkedin': 'linkedin.com/in/johndoe',
        'github': 'github.com/johndoe'
    },
    'skills': [
        'Python', 'JavaScript', 'SQL', 'Bash',
        'Django', 'Flask', 'FastAPI', 'React',
        'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
        'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'AWS', 'Terraform',
        'Git', 'Apache Spark', 'RabbitMQ'
    ],
    'experience': [
        {
            'title': 'Senior Python Developer',
            'company': 'Tech Innovations Inc.',
            'start_date': '2021',
            'end_date': 'Present',
            'duration_years': 3,
            'skills_used': ['Python', 'Django', 'PostgreSQL', 'Docker', 'Kubernetes', 'AWS'],
            'achievements': [
                'Led development of microservices architecture serving 1M+ daily users',
                'Implemented CI/CD pipelines reducing deployment time by 60%',
                'Mentored team of 5 junior developers'
            ]
        },
        {
            'title': 'Python Developer',
            'company': 'StartupXYZ',
            'start_date': '2018',
            'end_date': '2021',
            'duration_years': 3,
            'skills_used': ['Python', 'Flask', 'MongoDB', 'Redis', 'RabbitMQ', 'Apache Spark'],
            'achievements': [
                'Built RESTful APIs handling 10k+ requests per second',
                'Developed data processing pipelines using Apache Spark'
            ]
        },
        {
            'title': 'Junior Developer',
            'company': 'CodeCraft Solutions',
            'start_date': '2016',
            'end_date': '2018',
            'duration_years': 2,
            'skills_used': ['Python', 'Django', 'PostgreSQL', 'Git', 'Jenkins'],
            'achievements': [
                'Developed web applications using Django framework',
                'Wrote unit and integration tests achieving 90% coverage'
            ]
        }
    ],
    'education': [
        {
            'degree': 'Bachelor of Science in Computer Science',
            'institution': 'University of California, Berkeley',
            'graduation_year': '2016',
            'gpa': '3.8/4.0'
        }
    ],
    'certifications': [
        'AWS Certified Solutions Architect - Associate (2022)',
        'Certified Kubernetes Administrator (2021)',
        'Python Institute PCAP (2019)'
    ],
    'years_experience': 7,
    'skill_levels': {
        'Python': 'expert',
        'Django': 'advanced',
        'Flask': 'advanced',
        'PostgreSQL': 'advanced',
        'Docker': 'advanced',
        'Kubernetes': 'intermediate',
        'AWS': 'intermediate'
    }
}


# ============================================================================
# JOB DESCRIPTION MOCK DATA
# ============================================================================

MOCK_JOB_DESCRIPTION = """
Senior Backend Engineer - Python/Django

Company: TechCorp Solutions
Location: Remote (US)
Salary: $140,000 - $180,000

ABOUT THE ROLE
We're seeking an experienced Senior Backend Engineer to join our growing team.
You'll be responsible for designing and implementing scalable backend services
that power our SaaS platform serving millions of users.

REQUIRED QUALIFICATIONS
- 5+ years of professional software development experience
- 3+ years of Python development experience
- Strong expertise in Django or Flask framework
- Experience with PostgreSQL and database optimization
- Proficiency with Docker and containerization
- Understanding of RESTful API design principles
- Experience with Git and version control
- Strong problem-solving and debugging skills

PREFERRED QUALIFICATIONS
- Experience with Kubernetes and orchestration
- Knowledge of AWS or other cloud platforms (Azure, GCP)
- Familiarity with Redis or other caching solutions
- Experience with GraphQL
- Understanding of microservices architecture
- CI/CD pipeline implementation experience
- Agile/Scrum methodology experience

NICE TO HAVE
- Experience with React or Vue.js
- Knowledge of machine learning or data science
- Contributions to open source projects
- Experience with Elasticsearch
- Terraform or infrastructure as code experience

RESPONSIBILITIES
- Design, develop, and maintain backend services and APIs
- Optimize database queries and improve application performance
- Collaborate with frontend and DevOps teams
- Write clean, maintainable, and well-tested code
- Participate in code reviews and technical discussions
- Mentor junior engineers
- Help shape technical strategy and architecture decisions

REQUIRED EDUCATION
- Bachelor's degree in Computer Science or related field, or equivalent experience

WHAT WE OFFER
- Competitive salary and equity package
- Comprehensive health, dental, and vision insurance
- 401(k) with company match
- Unlimited PTO policy
- Professional development budget
- Remote-first culture
- Latest equipment and tools
"""

MOCK_JOB_PARSED = {
    'title': 'Senior Backend Engineer - Python/Django',
    'company': 'TechCorp Solutions',
    'location': 'Remote (US)',
    'salary_range': '$140,000 - $180,000',
    'required_skills': [
        'Python', 'Django', 'Flask', 'PostgreSQL',
        'Docker', 'RESTful API', 'Git'
    ],
    'preferred_skills': [
        'Kubernetes', 'AWS', 'Azure', 'GCP', 'Redis',
        'GraphQL', 'microservices', 'CI/CD'
    ],
    'nice_to_have': [
        'React', 'Vue.js', 'Machine Learning',
        'Elasticsearch', 'Terraform'
    ],
    'experience_years': 5,
    'education': 'Bachelor degree in Computer Science or related field',
    'responsibilities': [
        'Design, develop, and maintain backend services and APIs',
        'Optimize database queries and improve application performance',
        'Collaborate with frontend and DevOps teams',
        'Write clean, maintainable, and well-tested code',
        'Participate in code reviews and technical discussions',
        'Mentor junior engineers'
    ],
    'seniority_level': 'senior'
}


# ============================================================================
# MATCH ANALYSIS MOCK DATA
# ============================================================================

MOCK_MATCH_ANALYSIS = {
    'job_title': 'Senior Backend Engineer - Python/Django',
    'company': 'TechCorp Solutions',
    'analysis_date': datetime.now().isoformat(),
    'score': {
        'total_score': 78.5,
        'skill_score': 80.0,
        'experience_score': 85.0,
        'education_score': 100.0,
        'breakdown': {
            'required_skills': 85.7,  # 6/7 required skills
            'preferred_skills': 62.5,  # 5/8 preferred skills
            'nice_to_have': 40.0      # 2/5 nice-to-have
        }
    },
    'matching_skills': [
        'Python', 'Django', 'Flask', 'PostgreSQL',
        'Docker', 'Git', 'AWS', 'Redis', 'microservices'
    ],
    'gaps': {
        'missing_required_skills': ['Kubernetes'],
        'missing_preferred_skills': ['GraphQL', 'CI/CD', 'Azure', 'GCP'],
        'missing_nice_to_have': ['React', 'Vue.js', 'Machine Learning']
    },
    'strengths': [
        '7+ years of Python development experience (requires 5+)',
        'Strong Django and Flask expertise',
        'Extensive AWS experience',
        'Proven track record with microservices',
        'Docker and containerization proficiency'
    ],
    'recommendations': [
        'Learn Kubernetes for container orchestration',
        'Gain experience with GraphQL APIs',
        'Set up CI/CD pipelines in personal projects',
        'Consider basic React knowledge for full-stack capability'
    ]
}


# ============================================================================
# LEARNING PLAN MOCK DATA
# ============================================================================

MOCK_LEARNING_PLAN = {
    'created_date': datetime.now().isoformat(),
    'target_score': 90,
    'current_score': 78.5,
    'estimated_duration': '3-4 months',
    'mode': 'reverse',
    'skills_to_learn': [
        'Kubernetes', 'GraphQL', 'CI/CD', 'React'
    ],
    'levels': {
        'study': [
            {
                'skill': 'Kubernetes',
                'priority': 'high',
                'estimated_hours': 40,
                'resources': [
                    {
                        'title': 'Kubernetes Fundamentals',
                        'type': 'course',
                        'provider': 'Udemy',
                        'url': 'https://udemy.com/kubernetes-fundamentals',
                        'duration': '12 hours',
                        'cost': 'free'
                    },
                    {
                        'title': 'Kubernetes Documentation',
                        'type': 'documentation',
                        'url': 'https://kubernetes.io/docs',
                        'cost': 'free'
                    }
                ]
            },
            {
                'skill': 'GraphQL',
                'priority': 'medium',
                'estimated_hours': 20,
                'resources': [
                    {
                        'title': 'GraphQL with Python',
                        'type': 'tutorial',
                        'provider': 'howtographql.com',
                        'url': 'https://howtographql.com/graphql-python',
                        'duration': '6 hours',
                        'cost': 'free'
                    }
                ]
            }
        ],
        'practice': [
            {
                'skill': 'CI/CD',
                'priority': 'high',
                'project_ideas': [
                    'Set up GitHub Actions for personal project',
                    'Create Jenkins pipeline for Django app',
                    'Implement automated testing and deployment'
                ],
                'estimated_hours': 30
            }
        ],
        'master': [
            {
                'skill': 'Kubernetes',
                'certification': 'Certified Kubernetes Administrator (CKA)',
                'project_goal': 'Deploy production-ready Django app on K8s cluster',
                'estimated_hours': 20
            }
        ]
    },
    'milestones': [
        {
            'name': 'Kubernetes Basics',
            'skills_required': ['Kubernetes'],
            'target_date': (datetime.now() + timedelta(days=30)).isoformat(),
            'deliverables': ['Complete K8s course', 'Deploy first app to K8s']
        },
        {
            'name': 'API Modernization',
            'skills_required': ['GraphQL'],
            'target_date': (datetime.now() + timedelta(days=60)).isoformat(),
            'deliverables': ['Build GraphQL API', 'Compare with REST implementation']
        },
        {
            'name': 'DevOps Automation',
            'skills_required': ['CI/CD'],
            'target_date': (datetime.now() + timedelta(days=90)).isoformat(),
            'deliverables': ['Full CI/CD pipeline', 'Automated testing suite']
        }
    ],
    'weekly_schedule': {
        'hours_per_week': 10,
        'study_hours': 5,
        'practice_hours': 5,
        'days': [
            {'day': 'Monday', 'hours': 2, 'focus': 'Theory/Study'},
            {'day': 'Tuesday', 'hours': 0, 'focus': 'Rest'},
            {'day': 'Wednesday', 'hours': 2, 'focus': 'Practice'},
            {'day': 'Thursday', 'hours': 2, 'focus': 'Theory/Study'},
            {'day': 'Friday', 'hours': 0, 'focus': 'Rest'},
            {'day': 'Saturday', 'hours': 2, 'focus': 'Project Work'},
            {'day': 'Sunday', 'hours': 2, 'focus': 'Review/Practice'}
        ]
    }
}


# ============================================================================
# SPRINT MOCK DATA
# ============================================================================

MOCK_SPRINT_DATA = {
    'sprint_number': 1,
    'skills_targeted': ['Kubernetes', 'CI/CD'],
    'project_goal': 'Deploy Django app on Kubernetes with automated CI/CD',
    'start_date': (datetime.now() - timedelta(days=10)).isoformat(),
    'end_date': None,
    'duration_weeks': 2,
    'completed': False,
    'daily_logs': [
        {
            'date': (datetime.now() - timedelta(days=9)).isoformat(),
            'hours_studied': 2.5,
            'topics_covered': ['Kubernetes architecture', 'Pods and Deployments'],
            'resources_used': ['Kubernetes docs', 'Udemy course'],
            'challenges': 'Understanding networking between pods',
            'progress_rating': 4,
            'notes': 'Good progress on basics'
        },
        {
            'date': (datetime.now() - timedelta(days=8)).isoformat(),
            'hours_studied': 3.0,
            'topics_covered': ['Services and Ingress', 'ConfigMaps'],
            'resources_used': ['Kubernetes docs', 'Hands-on labs'],
            'challenges': 'Configuring ingress controller',
            'progress_rating': 3,
            'notes': 'Ingress is tricky'
        },
        {
            'date': (datetime.now() - timedelta(days=7)).isoformat(),
            'hours_studied': 2.0,
            'topics_covered': ['Volumes and Persistence'],
            'resources_used': ['Kubernetes docs'],
            'challenges': None,
            'progress_rating': 5,
            'notes': 'Storage concepts clearer now'
        }
    ],
    'total_hours': 7.5,
    'completion_rate': 50.0,
    'test_scores': {},
    'project_url': None
}

MOCK_COMPLETED_SPRINT = {
    'sprint_number': 1,
    'skills_targeted': ['Docker', 'PostgreSQL'],
    'project_goal': 'Containerize Django application with PostgreSQL',
    'start_date': (datetime.now() - timedelta(days=28)).isoformat(),
    'end_date': (datetime.now() - timedelta(days=14)).isoformat(),
    'duration_weeks': 2,
    'completed': True,
    'daily_logs': [
        {'date': (datetime.now() - timedelta(days=27)).isoformat(), 'hours_studied': 2.0, 'progress_rating': 4},
        {'date': (datetime.now() - timedelta(days=26)).isoformat(), 'hours_studied': 2.5, 'progress_rating': 4},
        {'date': (datetime.now() - timedelta(days=25)).isoformat(), 'hours_studied': 3.0, 'progress_rating': 5},
        {'date': (datetime.now() - timedelta(days=24)).isoformat(), 'hours_studied': 2.0, 'progress_rating': 3},
        {'date': (datetime.now() - timedelta(days=23)).isoformat(), 'hours_studied': 1.5, 'progress_rating': 4},
        {'date': (datetime.now() - timedelta(days=21)).isoformat(), 'hours_studied': 3.0, 'progress_rating': 5},
        {'date': (datetime.now() - timedelta(days=20)).isoformat(), 'hours_studied': 2.5, 'progress_rating': 4},
        {'date': (datetime.now() - timedelta(days=19)).isoformat(), 'hours_studied': 2.0, 'progress_rating': 4},
        {'date': (datetime.now() - timedelta(days=18)).isoformat(), 'hours_studied': 3.0, 'progress_rating': 5},
        {'date': (datetime.now() - timedelta(days=17)).isoformat(), 'hours_studied': 2.5, 'progress_rating': 4},
        {'date': (datetime.now() - timedelta(days=16)).isoformat(), 'hours_studied': 2.0, 'progress_rating': 3},
        {'date': (datetime.now() - timedelta(days=15)).isoformat(), 'hours_studied': 3.5, 'progress_rating': 5},
        {'date': (datetime.now() - timedelta(days=14)).isoformat(), 'hours_studied': 4.0, 'progress_rating': 5}
    ],
    'total_hours': 33.5,
    'completion_rate': 100.0,
    'test_scores': {
        'Docker': 85,
        'PostgreSQL': 78
    },
    'project_url': 'https://github.com/johndoe/django-docker-postgres',
    'score_improvement': 8.5
}


# ============================================================================
# SKILL TEST MOCK DATA
# ============================================================================

MOCK_SKILL_TESTS = {
    'Kubernetes': {
        'skill': 'Kubernetes',
        'difficulty': 'intermediate',
        'questions': [
            {
                'question': 'What is a Pod in Kubernetes?',
                'type': 'multiple_choice',
                'options': [
                    'A single container',
                    'The smallest deployable unit that can contain one or more containers',
                    'A virtual machine',
                    'A cluster node'
                ],
                'correct_answer': 1,
                'explanation': 'A Pod is the smallest deployable unit in Kubernetes and can contain one or more tightly coupled containers.'
            },
            {
                'question': 'Write a YAML definition for a Deployment with 3 replicas of an nginx container.',
                'type': 'practical',
                'requirements': [
                    'apiVersion and kind specified',
                    'replicas: 3',
                    'nginx image specified',
                    'Valid selector and labels'
                ]
            },
            {
                'question': 'Explain the difference between a Service and an Ingress.',
                'type': 'open_ended',
                'key_points': [
                    'Service provides stable networking within cluster',
                    'Ingress manages external access',
                    'Ingress can handle routing rules',
                    'Service is L4, Ingress is L7'
                ]
            }
        ],
        'passing_score': 70,
        'estimated_time': '30 minutes'
    },
    'GraphQL': {
        'skill': 'GraphQL',
        'difficulty': 'beginner',
        'questions': [
            {
                'question': 'What is the main advantage of GraphQL over REST?',
                'type': 'multiple_choice',
                'options': [
                    'Faster performance',
                    'Clients can request exactly the data they need',
                    'Better security',
                    'Easier to implement'
                ],
                'correct_answer': 1
            },
            {
                'question': 'Write a simple GraphQL query to fetch a user\'s name and email.',
                'type': 'practical',
                'requirements': [
                    'Uses query keyword',
                    'Specifies fields (name, email)',
                    'Correct syntax'
                ]
            }
        ],
        'passing_score': 70,
        'estimated_time': '20 minutes'
    }
}


# ============================================================================
# WORKFLOW STATE MOCK DATA
# ============================================================================

MOCK_WORKFLOW_STATE = {
    'mode': 'reverse',
    'started_date': (datetime.now() - timedelta(days=30)).isoformat(),
    'baseline_score': 78.5,
    'current_score': 82.0,
    'target_score': 90,
    'current_stage': 'skill_building',
    'current_sprint': 2,
    'skills_mastered': ['Docker', 'PostgreSQL', 'CI/CD basics'],
    'skills_in_progress': ['Kubernetes', 'GraphQL'],
    'projects_completed': [
        {
            'name': 'Django Docker Deployment',
            'url': 'https://github.com/johndoe/django-docker',
            'skills': ['Docker', 'PostgreSQL'],
            'completion_date': (datetime.now() - timedelta(days=14)).isoformat()
        }
    ],
    'certifications_earned': [],
    'quality_gates_passed': ['foundation'],
    'application_ready': False,
    'next_milestones': [
        'Complete Kubernetes learning',
        'Build K8s deployment project',
        'Pass competency gate (80% score)'
    ]
}


# ============================================================================
# APPLICATION MATERIALS MOCK DATA
# ============================================================================

MOCK_COVER_LETTER = """
Dear Hiring Manager,

I am writing to express my strong interest in the Senior Backend Engineer position at TechCorp Solutions. With over 7 years of Python development experience and a proven track record of building scalable backend services, I am confident that my skills align exceptionally well with your requirements.

Your position requires extensive Python and Django expertise, and I have been working with these technologies for the past 7 years. At Tech Innovations Inc., I led the development of a microservices architecture that now serves over 1 million daily users. This experience has given me deep knowledge of building production-grade systems that scale.

I am particularly excited about your focus on system optimization and performance. In my current role, I implemented caching strategies using Redis and optimized database queries that reduced API response times by 40%. I also established CI/CD pipelines that decreased deployment time from hours to minutes.

While I am actively developing my Kubernetes expertise through hands-on projects and coursework, my strong foundation in Docker and container orchestration provides a solid base. I have already deployed several applications using Docker Compose and am committed to mastering K8s within the next 2-3 months.

What particularly attracts me to TechCorp Solutions is your commitment to engineering excellence and your modern tech stack. I am impressed by your focus on scalable architecture and would be thrilled to contribute my expertise in Python, Django, and AWS to your team.

I would welcome the opportunity to discuss how my background in backend development and my passion for building robust systems can contribute to TechCorp Solutions' continued success.

Thank you for considering my application.

Sincerely,
John Doe
"""

MOCK_LINKEDIN_MESSAGE = """
Hi [Hiring Manager Name],

I recently came across the Senior Backend Engineer opening at TechCorp Solutions and was immediately drawn to the role. With 7+ years specializing in Python/Django and experience building systems serving millions of users, I believe I could make valuable contributions to your team.

I'm particularly excited about your focus on scalable architecture and modern DevOps practices. I'd love to learn more about the role and share how my experience aligns with your needs.

Would you be open to a brief conversation?

Best regards,
John Doe
"""


# ============================================================================
# RESOURCE DATABASE MOCK DATA
# ============================================================================

MOCK_LEARNING_RESOURCES = {
    'Kubernetes': [
        {
            'title': 'Kubernetes Fundamentals',
            'type': 'course',
            'provider': 'Udemy',
            'url': 'https://udemy.com/kubernetes-fundamentals',
            'duration': '12 hours',
            'cost': 'free',
            'level': 'beginner',
            'rating': 4.6,
            'updated': '2024'
        },
        {
            'title': 'Kubernetes Documentation',
            'type': 'documentation',
            'provider': 'Kubernetes.io',
            'url': 'https://kubernetes.io/docs',
            'cost': 'free',
            'level': 'all',
            'quality': 'official'
        },
        {
            'title': 'Kubernetes in Action',
            'type': 'book',
            'author': 'Marko Luksa',
            'cost': 'paid',
            'level': 'intermediate',
            'rating': 4.7
        }
    ],
    'GraphQL': [
        {
            'title': 'GraphQL with Python',
            'type': 'tutorial',
            'provider': 'howtographql.com',
            'url': 'https://howtographql.com/graphql-python',
            'duration': '6 hours',
            'cost': 'free',
            'level': 'beginner'
        }
    ]
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_mock_cv(format='parsed'):
    """
    Get mock CV data
    
    Args:
        format: 'text' or 'parsed'
    
    Returns:
        Mock CV data in requested format
    """
    if format == 'text':
        return MOCK_CV_TEXT
    return MOCK_CV_PARSED


def get_mock_job(format='parsed'):
    """
    Get mock job description
    
    Args:
        format: 'text' or 'parsed'
    
    Returns:
        Mock job data in requested format
    """
    if format == 'text':
        return MOCK_JOB_DESCRIPTION
    return MOCK_JOB_PARSED


def get_mock_sprint(completed=False):
    """
    Get mock sprint data
    
    Args:
        completed: Whether to return completed sprint
    
    Returns:
        Mock sprint data
    """
    if completed:
        return MOCK_COMPLETED_SPRINT.copy()
    return MOCK_SPRINT_DATA.copy()


def create_custom_mock_analysis(score=75, missing_skills=None):
    """
    Create custom mock analysis with specified parameters
    
    Args:
        score: Overall match score
        missing_skills: List of missing skills
    
    Returns:
        Customized mock analysis
    """
    analysis = MOCK_MATCH_ANALYSIS.copy()
    analysis['score']['total_score'] = score
    
    if missing_skills:
        analysis['gaps']['missing_required_skills'] = missing_skills
    
    return analysis


# ============================================================================
# EXPORT ALL MOCK DATA
# ============================================================================

__all__ = [
    'MOCK_CV_TEXT',
    'MOCK_CV_PARSED',
    'MOCK_JOB_DESCRIPTION',
    'MOCK_JOB_PARSED',
    'MOCK_MATCH_ANALYSIS',
    'MOCK_LEARNING_PLAN',
    'MOCK_SPRINT_DATA',
    'MOCK_COMPLETED_SPRINT',
    'MOCK_SKILL_TESTS',
    'MOCK_WORKFLOW_STATE',
    'MOCK_COVER_LETTER',
    'MOCK_LINKEDIN_MESSAGE',
    'MOCK_LEARNING_RESOURCES',
    'get_mock_cv',
    'get_mock_job',
    'get_mock_sprint',
    'create_custom_mock_analysis'
]
