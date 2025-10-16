# API Reference

## Table of Contents

1. [Overview](#overview)
2. [JobEngine Class](#jobengine-class)
3. [Analyzers Module](#analyzers-module)
4. [Learning Module](#learning-module)
5. [Tracking Module](#tracking-module)
6. [Generators Module](#generators-module)
7. [Utils Module](#utils-module)
8. [Data Types](#data-types)
9. [Exceptions](#exceptions)
10. [Examples](#examples)

## Overview

The Advanced Job Engine provides both a Python API and CLI interface. This document covers the Python API for programmatic integration.

### Installation

```python
# From source
from src.python_advanced_job_engine import JobEngine

# Future: From PyPI
# pip install advanced-job-engine
# from job_engine import JobEngine
```

### Quick Start

```python
from src.python_advanced_job_engine import JobEngine

# Initialize engine
engine = JobEngine()

# Standard mode: Analyze specific job
result = engine.analyze_job_fit(
    cv_path="data/my_cv.pdf",
    job_path="data/target_job.pdf"
)

# Reverse mode: Explore opportunities
recommendations = engine.discover_opportunities(
    cv_path="data/my_cv.pdf"
)
```

## JobEngine Class

Main orchestration class that coordinates all system components.

### Constructor

```python
JobEngine(config: Optional[dict] = None)
```

**Parameters:**
- `config` (dict, optional): Configuration overrides

**Returns:** JobEngine instance

**Example:**
```python
custom_config = {
    'scoring_weights': {
        'technical_skills': 0.50,
        'experience': 0.30,
        'education': 0.10,
        'soft_skills': 0.10
    },
    'learning_sprint_weeks': 3
}

engine = JobEngine(config=custom_config)
```

### Methods

#### analyze_job_fit

```python
analyze_job_fit(
    cv_path: str,
    job_path: str,
    mode: str = "standard",
    generate_plan: bool = True,
    generate_letters: bool = True
) -> AnalysisResult
```

Analyzes fit between CV and job description.

**Parameters:**
- `cv_path` (str): Path to CV file (PDF, DOCX, or TXT)
- `job_path` (str): Path to job description file
- `mode` (str): Analysis mode ("standard" or "detailed")
- `generate_plan` (bool): Whether to generate learning plan
- `generate_letters` (bool): Whether to generate application materials

**Returns:** `AnalysisResult` object containing:
- `match_score` (float): Overall match percentage
- `gaps` (List[Gap]): Identified skill gaps
- `learning_plan` (LearningPlan): Personalized learning plan
- `quality_gates` (dict): Quality gate evaluations
- `recommendations` (str): Actionable advice

**Raises:**
- `FileNotFoundError`: If CV or job file doesn't exist
- `ParseError`: If files can't be parsed
- `ValidationError`: If data validation fails

**Example:**
```python
result = engine.analyze_job_fit(
    cv_path="data/my_cv.pdf",
    job_path="data/senior_dev_job.pdf"
)

print(f"Match Score: {result.match_score}%")
print(f"Critical Gaps: {len(result.get_critical_gaps())}")
print(f"Learning Time: {result.learning_plan.total_hours} hours")
```

#### discover_opportunities

```python
discover_opportunities(
    cv_path: str,
    job_database: Optional[str] = None,
    min_match_score: int = 60
) -> List[JobRecommendation]
```

Reverse mode: Finds jobs matching your skills.

**Parameters:**
- `cv_path` (str): Path to CV file
- `job_database` (str, optional): Path to job database
- `min_match_score` (int): Minimum match score threshold

**Returns:** List of `JobRecommendation` objects

**Example:**
```python
opportunities = engine.discover_opportunities(
    cv_path="data/my_cv.pdf",
    min_match_score=70
)

for job in opportunities:
    print(f"{job.title} at {job.company}: {job.match_score}%")
```

#### update_skills

```python
update_skills(
    skill_updates: Dict[str, int],
    cv_path: Optional[str] = None
) -> None
```

Updates skill proficiency levels.

**Parameters:**
- `skill_updates` (dict): Mapping of skill name to new level
- `cv_path` (str, optional): Path to CV to update

**Example:**
```python
engine.update_skills({
    'Docker': 3,
    'Kubernetes': 2,
    'Python': 4
})
```

#### export_results

```python
export_results(
    analysis_result: AnalysisResult,
    output_dir: str = "job_search_data/export",
    formats: List[str] = ["json", "txt"]
) -> str
```

Exports analysis results to files.

**Parameters:**
- `analysis_result` (AnalysisResult): Result to export
- `output_dir` (str): Output directory path
- `formats` (List[str]): Export formats

**Returns:** Path to export directory

**Example:**
```python
export_path = engine.export_results(
    result,
    output_dir="exports/company_name",
    formats=["json", "pdf", "txt"]
)
```

## Analyzers Module

### CVParser

```python
from src.analyzers.cv_parser import CVParser
```

#### parse

```python
parse(file_path: str) -> CVData
```

Parses CV and extracts structured data.

**Parameters:**
- `file_path` (str): Path to CV file

**Returns:** `CVData` object

**Example:**
```python
parser = CVParser()
cv_data = parser.parse("data/my_cv.pdf")

print(f"Skills found: {len(cv_data.skills)}")
print(f"Experience: {cv_data.total_years_experience} years")
```

#### extract_skills

```python
extract_skills(text: str, context_window: int = 100) -> List[Skill]
```

Extracts skills from text with proficiency detection.

**Parameters:**
- `text` (str): Text to analyze
- `context_window` (int): Characters around skill mention to analyze

**Returns:** List of `Skill` objects

#### detect_proficiency

```python
detect_proficiency(skill: str, context: str) -> int
```

Determines proficiency level from context.

**Parameters:**
- `skill` (str): Skill name
- `context` (str): Surrounding text

**Returns:** Proficiency level (1-5)

### JobParser

```python
from src.analyzers.job_parser import JobParser
```

#### parse

```python
parse(file_path: str) -> JobDescription
```

Parses job description and extracts requirements.

**Parameters:**
- `file_path` (str): Path to job description file

**Returns:** `JobDescription` object

**Example:**
```python
parser = JobParser()
job = parser.parse("data/job_posting.pdf")

print(f"Required skills: {len(job.required_skills)}")
print(f"Nice-to-have: {len(job.preferred_skills)}")
```

#### classify_requirements

```python
classify_requirements(text: str) -> Requirements
```

Classifies skills as required vs. preferred.

**Parameters:**
- `text` (str): Job description text

**Returns:** `Requirements` object with categorized skills

### SkillMatcher

```python
from src.analyzers.matcher import SkillMatcher
```

#### calculate_match_score

```python
calculate_match_score(
    cv_data: CVData,
    job_desc: JobDescription,
    weights: Optional[dict] = None
) -> MatchResult
```

Calculates comprehensive match score.

**Parameters:**
- `cv_data` (CVData): Parsed CV data
- `job_desc` (JobDescription): Parsed job description
- `weights` (dict, optional): Custom scoring weights

**Returns:** `MatchResult` object

**Example:**
```python
matcher = SkillMatcher()
result = matcher.calculate_match_score(cv_data, job_desc)

print(f"Technical Match: {result.technical_score}%")
print(f"Experience Match: {result.experience_score}%")
print(f"Overall: {result.overall_score}%")
```

#### score_technical_fit

```python
score_technical_fit(
    candidate_skills: List[Skill],
    required_skills: List[SkillRequirement]
) -> float
```

Scores technical skill alignment.

**Parameters:**
- `candidate_skills` (List[Skill]): Candidate's skills
- `required_skills` (List[SkillRequirement]): Job requirements

**Returns:** Technical fit score (0-100)

### GapAnalyzer

```python
from src.analyzers.gap_analyzer import GapAnalyzer
```

#### analyze_gaps

```python
analyze_gaps(
    cv_data: CVData,
    job_desc: JobDescription
) -> List[Gap]
```

Identifies skill gaps.

**Parameters:**
- `cv_data` (CVData): Candidate data
- `job_desc` (JobDescription): Job requirements

**Returns:** List of `Gap` objects

**Example:**
```python
analyzer = GapAnalyzer()
gaps = analyzer.analyze_gaps(cv_data, job_desc)

critical_gaps = [g for g in gaps if g.category == 'critical']
print(f"Critical gaps: {len(critical_gaps)}")
```

#### prioritize_gaps

```python
prioritize_gaps(gaps: List[Gap]) -> List[Gap]
```

Sorts gaps by priority.

**Parameters:**
- `gaps` (List[Gap]): Unsorted gaps

**Returns:** Sorted list of gaps (highest priority first)

## Learning Module

### PlanGenerator

```python
from src.learning.plan_generator import PlanGenerator
```

#### generate_plan

```python
generate_plan(
    gaps: List[Gap],
    sprint_duration_weeks: int = 2,
    study_hours_per_week: int = 10
) -> LearningPlan
```

Creates personalized learning plan.

**Parameters:**
- `gaps` (List[Gap]): Skill gaps to address
- `sprint_duration_weeks` (int): Length of each sprint
- `study_hours_per_week` (int): Available study time

**Returns:** `LearningPlan` object

**Example:**
```python
generator = PlanGenerator()
plan = generator.generate_plan(
    gaps=critical_gaps,
    sprint_duration_weeks=2,
    study_hours_per_week=15
)

print(f"Total sprints: {len(plan.sprints)}")
print(f"Estimated completion: {plan.total_duration_weeks} weeks")
```

#### allocate_to_sprints

```python
allocate_to_sprints(
    gaps: List[Gap],
    sprint_duration: int
) -> List[Sprint]
```

Distributes gaps across learning sprints.

**Parameters:**
- `gaps` (List[Gap]): Gaps to allocate
- `sprint_duration` (int): Sprint length in weeks

**Returns:** List of `Sprint` objects

#### estimate_learning_time

```python
estimate_learning_time(gap: Gap) -> int
```

Estimates hours needed to close a gap.

**Parameters:**
- `gap` (Gap): Gap to estimate

**Returns:** Estimated hours

### ResourceDatabase

```python
from src.learning.resource_db import ResourceDatabase
```

#### query

```python
query(
    skill: str,
    level: Optional[int] = None,
    resource_type: Optional[str] = None,
    limit: int = 10
) -> List[Resource]
```

Queries learning resources.

**Parameters:**
- `skill` (str): Skill name
- `level` (int, optional): Target proficiency level
- `resource_type` (str, optional): Type filter (course, book, tutorial)
- `limit` (int): Maximum results

**Returns:** List of `Resource` objects

**Example:**
```python
db = ResourceDatabase()
resources = db.query(
    skill="Docker",
    level=3,
    resource_type="course",
    limit=5
)

for resource in resources:
    print(f"{resource.title} - {resource.duration_hours}h")
```

#### add_resource

```python
add_resource(resource: Resource) -> None
```

Adds custom learning resource.

**Parameters:**
- `resource` (Resource): Resource to add

**Example:**
```python
custom_resource = Resource(
    skill="Docker",
    title="Company Internal Training",
    type="course",
    duration_hours=8,
    level=2,
    url="http://internal.company.com/docker"
)

db.add_resource(custom_resource)
```

#### get_recommendations

```python
get_recommendations(
    skill: str,
    learner_profile: LearnerProfile
) -> List[Resource]
```

Gets personalized resource recommendations.

**Parameters:**
- `skill` (str): Skill name
- `learner_profile` (LearnerProfile): Learner preferences

**Returns:** Recommended resources

### TestGenerator

```python
from src.learning.test_generator import TestGenerator
```

#### generate_test

```python
generate_test(
    skill: str,
    level: int,
    question_count: int = 10
) -> Test
```

Generates skill assessment test.

**Parameters:**
- `skill` (str): Skill to test
- `level` (int): Target proficiency level
- `question_count` (int): Number of questions

**Returns:** `Test` object

**Example:**
```python
generator = TestGenerator()
test = generator.generate_test(
    skill="Python",
    level=3,
    question_count=15
)

print(f"Test: {test.title}")
print(f"Duration: {test.duration_minutes} minutes")
```

## Tracking Module

### SprintManager

```python
from src.tracking.sprint_manager import SprintManager
```

#### create_sprint

```python
create_sprint(
    duration_weeks: int,
    goals: List[Goal]
) -> Sprint
```

Creates new learning sprint.

**Parameters:**
- `duration_weeks` (int): Sprint duration
- `goals` (List[Goal]): Sprint goals

**Returns:** `Sprint` object

**Example:**
```python
manager = SprintManager()
sprint = manager.create_sprint(
    duration_weeks=2,
    goals=[
        Goal(skill="Docker", target_level=3),
        Goal(skill="Kubernetes", target_level=2)
    ]
)
```

#### update_progress

```python
update_progress(
    sprint_id: str,
    skill: str,
    progress: float
) -> None
```

Updates sprint progress.

**Parameters:**
- `sprint_id` (str): Sprint identifier
- `skill` (str): Skill being updated
- `progress` (float): Progress percentage (0-100)

#### complete_sprint

```python
complete_sprint(sprint_id: str) -> SprintSummary
```

Completes and summarizes sprint.

**Parameters:**
- `sprint_id` (str): Sprint to complete

**Returns:** `SprintSummary` with results

### QualityGates

```python
from src.tracking.quality_gates import QualityGates
```

#### evaluate_foundational

```python
evaluate_foundational(
    cv_data: CVData,
    job_desc: JobDescription
) -> GateResult
```

Evaluates foundational quality gate.

**Parameters:**
- `cv_data` (CVData): Current skills
- `job_desc` (JobDescription): Job requirements

**Returns:** `GateResult` object

**Example:**
```python
gates = QualityGates()
result = gates.evaluate_foundational(cv_data, job_desc)

if result.passes:
    print("✓ Foundational gate passed!")
else:
    print(f"Missing: {result.missing_criteria}")
```

#### evaluate_competitive

```python
evaluate_competitive(
    cv_data: CVData,
    job_desc: JobDescription
) -> GateResult
```

Evaluates competitive quality gate.

#### evaluate_excellence

```python
evaluate_excellence(
    cv_data: CVData,
    job_desc: JobDescription
) -> GateResult
```

Evaluates excellence quality gate.

### ProgressTracker

```python
from src.tracking.progress_tracker import ProgressTracker
```

#### log_activity

```python
log_activity(activity: Activity) -> None
```

Logs learning activity.

**Parameters:**
- `activity` (Activity): Activity to log

**Example:**
```python
tracker = ProgressTracker()
tracker.log_activity(Activity(
    skill="Docker",
    type="study",
    duration_hours=2,
    description="Completed container networking module",
    date=datetime.now()
))
```

#### get_progress_summary

```python
get_progress_summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> ProgressSummary
```

Gets progress summary for period.

**Parameters:**
- `start_date` (datetime, optional): Period start
- `end_date` (datetime, optional): Period end

**Returns:** `ProgressSummary` object

#### generate_dashboard

```python
generate_dashboard() -> Dashboard
```

Generates progress dashboard data.

**Returns:** `Dashboard` object with visualizable data

## Generators Module

### LetterGenerator

```python
from src.generators.letter_generator import LetterGenerator
```

#### generate_cover_letter

```python
generate_cover_letter(
    match_result: MatchResult,
    job_desc: JobDescription,
    cv_data: CVData,
    template: str = "professional"
) -> str
```

Generates cover letter.

**Parameters:**
- `match_result` (MatchResult): Analysis result
- `job_desc` (JobDescription): Job details
- `cv_data` (CVData): Your data
- `template` (str): Template style

**Returns:** Cover letter text

**Example:**
```python
generator = LetterGenerator()
letter = generator.generate_cover_letter(
    match_result=result,
    job_desc=job,
    cv_data=cv_data,
    template="growth_mindset"
)
```

#### generate_linkedin_message

```python
generate_linkedin_message(
    job_desc: JobDescription,
    highlights: List[str],
    contact_name: Optional[str] = None
) -> str
```

Generates LinkedIn outreach message.

**Parameters:**
- `job_desc` (JobDescription): Job details
- `highlights` (List[str]): Key points to mention
- `contact_name` (str, optional): Recipient name

**Returns:** LinkedIn message text

### ReportGenerator

```python
from src.generators.report_generator import ReportGenerator
```

#### generate_analysis_report

```python
generate_analysis_report(
    match_result: MatchResult,
    format: str = "markdown"
) -> str
```

Generates comprehensive analysis report.

**Parameters:**
- `match_result` (MatchResult): Analysis data
- `format` (str): Output format (markdown, html, txt)

**Returns:** Formatted report

**Example:**
```python
generator = ReportGenerator()
report = generator.generate_analysis_report(
    match_result=result,
    format="markdown"
)

with open("analysis_report.md", "w") as f:
    f.write(report)
```

## Utils Module

### File Readers

```python
from src.utils.file_readers import read_pdf, read_docx, read_txt
```

#### read_pdf

```python
read_pdf(file_path: str) -> str
```

Reads PDF file.

**Parameters:**
- `file_path` (str): Path to PDF

**Returns:** Extracted text

#### read_docx

```python
read_docx(file_path: str) -> str
```

Reads DOCX file.

#### read_txt

```python
read_txt(file_path: str, encoding: str = "utf-8") -> str
```

Reads text file.

### Validators

```python
from src.utils.validators import (
    validate_cv_data,
    validate_job_description,
    validate_skill_level
)
```

#### validate_cv_data

```python
validate_cv_data(cv_data: CVData) -> bool
```

Validates CV data structure.

**Parameters:**
- `cv_data` (CVData): Data to validate

**Returns:** True if valid

**Raises:** `ValidationError` with details

## Data Types

### CVData

```python
@dataclass
class CVData:
    skills: List[Skill]
    experience: List[Experience]
    education: List[Education]
    projects: List[Project]
    certifications: List[Certification]
    total_years_experience: float
    metadata: dict
```

### Skill

```python
@dataclass
class Skill:
    name: str
    level: int  # 1-5
    years_experience: float
    last_used: datetime
    context: List[str]
    verified: bool
    proficiency_details: dict
```

### JobDescription

```python
@dataclass
class JobDescription:
    title: str
    company: str
    required_skills: List[SkillRequirement]
    preferred_skills: List[SkillRequirement]
    experience_years: int
    education_requirements: List[str]
    responsibilities: List[str]
    benefits: List[str]
    metadata: dict
```

### MatchResult

```python
@dataclass
class MatchResult:
    overall_score: float
    technical_score: float
    experience_score: float
    education_score: float
    soft_skills_score: float
    strengths: List[str]
    gaps: List[Gap]
    recommendation: str
    quality_gate_status: dict
```

### Gap

```python
@dataclass
class Gap:
    skill: str
    current_level: int
    required_level: int
    priority: int
    category: str  # 'critical', 'important', 'nice-to-have'
    estimated_learning_time: int
    impact: str
    resources: List[Resource]
```

### LearningPlan

```python
@dataclass
class LearningPlan:
    sprints: List[Sprint]
    total_duration_weeks: int
    estimated_hours: int
    quality_gate_targets: dict
    resources: List[Resource]
    milestones: List[Milestone]
```

### Sprint

```python
@dataclass
class Sprint:
    id: str
    number: int
    duration_weeks: int
    goals: List[Goal]
    resources: List[Resource]
    estimated_hours: int
    status: str  # 'planned', 'active', 'completed'
```

## Exceptions

### ParseError

```python
class ParseError(Exception):
    """Raised when document parsing fails"""
    pass
```

### ValidationError

```python
class ValidationError(Exception):
    """Raised when data validation fails"""
    pass
```

### ConfigurationError

```python
class ConfigurationError(Exception):
    """Raised when configuration is invalid"""
    pass
```

### ResourceNotFoundError

```python
class ResourceNotFoundError(Exception):
    """Raised when requested resource doesn't exist"""
    pass
```

## Examples

### Complete Workflow Example

```python
from src.python_advanced_job_engine import JobEngine
from src.tracking.progress_tracker import ProgressTracker

# Initialize
engine = JobEngine()

# Analyze job fit
result = engine.analyze_job_fit(
    cv_path="data/my_cv.pdf",
    job_path="data/senior_role.pdf"
)

# Check quality gates
if result.quality_gate_status['foundational']['passes']:
    print("Ready to apply!")
else:
    print("Need to improve first")
    
    # Follow learning plan
    tracker = ProgressTracker()
    
    for sprint in result.learning_plan.sprints:
        print(f"\n=== Sprint {sprint.number} ===")
        for goal in sprint.goals:
            print(f"Study: {goal.skill} → Level {goal.target_level}")
        
        # Log progress
        tracker.log_activity(Activity(
            skill=goal.skill,
            type="study",
            duration_hours=10
        ))
    
    # Re-evaluate
    engine.update_skills({'Docker': 3, 'Kubernetes': 2})
    new_result = engine.analyze_job_fit(cv_path, job_path)
    print(f"\nNew match score: {new_result.match_score}%")

# Export everything
engine.export_results(result, formats=['json', 'pdf'])
```

### Batch Analysis Example

```python
import glob

engine = JobEngine()
results = []

for job_file in glob.glob("data/jobs/*.pdf"):
    result = engine.analyze_job_fit(
        cv_path="data/my_cv.pdf",
        job_path=job_file
    )
    results.append({
        'job': job_file,
        'score': result.match_score,
        'critical_gaps': len(result.get_critical_gaps())
    })

# Sort by match score
results.sort(key=lambda x: x['score'], reverse=True)

print("\n=== Job Rankings ===")
for i, r in enumerate(results, 1):
    print(f"{i}. {r['job']}: {r['score']}% (Gaps: {r['critical_gaps']})")
```

### Custom Resource Integration

```python
from src.learning.resource_db import ResourceDatabase, Resource

db = ResourceDatabase()

# Add company-specific resources
company_resources = [
    Resource(
        skill="Internal API",
        title="Company API Documentation",
        type="documentation",
        duration_hours=4,
        level=2,
        url="http://internal.company.com/api-docs"
    ),
    Resource(
        skill="Deployment Process",
        title="DevOps Training Module",
        type="internal_course",
        duration_hours=6,
        level=3,
        url="http://training.company.com/devops"
    )
]

for resource in company_resources:
    db.add_resource(resource)
```

## CLI Reference

For command-line usage, see:

```bash
# Help
python src/python_advanced_job_engine.py --help

# Standard analysis
python src/python_advanced_job_engine.py \
  --cv data/my_cv.pdf \
  --job data/job.pdf \
  --mode standard

# Reverse mode
python src/python_advanced_job_engine.py \
  --cv data/my_cv.pdf \
  --mode reverse

# Update progress
python src/python_advanced_job_engine.py \
  --update-progress \
  --skill "Docker" \
  --new-level 3
```

## Version Information

- **Current Version**: 2.0.0
- **Python Requirement**: 3.8+
- **API Stability**: Stable (breaking changes only in major versions)

## Support

For issues or questions:
- GitHub Issues: Report bugs and request features
- Documentation: Check other markdown files in `/docs`
- Examples: See `/examples` directory for more code samples