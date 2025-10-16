# System Architecture

## Table of Contents

1. [Overview](#overview)
2. [System Design Principles](#system-design-principles)
3. [Architecture Diagram](#architecture-diagram)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [Module Interactions](#module-interactions)
7. [Data Models](#data-models)
8. [State Management](#state-management)
9. [Extension Points](#extension-points)
10. [Deployment Architecture](#deployment-architecture)

## Overview

The Advanced Job Engine follows a modular, pipeline-based architecture designed for extensibility, maintainability, and clear separation of concerns. The system is built using Python 3.8+ and operates as both a standalone CLI tool and a library that can be integrated into other applications.

### Key Architectural Goals

- **Modularity**: Each component handles a specific responsibility
- **Extensibility**: Easy to add new analyzers, generators, or data sources
- **Testability**: Components can be tested in isolation
- **Maintainability**: Clear interfaces and minimal coupling
- **Performance**: Efficient processing of large documents and datasets

## System Design Principles

### 1. Separation of Concerns

Each module has a single, well-defined responsibility:
- Analyzers handle data extraction and interpretation
- Generators create output content
- Trackers manage state and progress
- Utils provide shared functionality

### 2. Pipeline Architecture

Data flows through a series of transformation stages:
```
Input Documents → Parsing → Analysis → Planning → Generation → Output
```

### 3. Data-Driven Configuration

System behavior is controlled through configuration files rather than code changes, allowing users to customize without modifying source code.

### 4. Fail-Safe Design

Each component validates inputs and handles errors gracefully, ensuring partial results are preserved even if later stages fail.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  CLI Interface  │  Python API  │  GitHub Actions  │  Web UI*    │
└────────┬────────┴──────┬──────┴─────────┬─────────┴─────────────┘
         │               │                │
         └───────────────┴────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │     Job Engine Core           │
         │  (Orchestration Layer)        │
         └───────┬───────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼───┐   ┌───▼───┐   ┌───▼───┐
│Analyze│   │Learn  │   │Track  │
│Module │   │Module │   │Module │
└───┬───┘   └───┬───┘   └───┬───┘
    │           │           │
┌───▼────────────▼───────────▼───┐
│     Data Access Layer          │
├─────────────────────────────────┤
│ CV Parser │ Job Parser │ DB    │
└─────────────────────────────────┘
    │           │           │
┌───▼────────────▼───────────▼───┐
│      Storage Layer              │
├─────────────────────────────────┤
│ File System │ JSON DB │ Cache  │
└─────────────────────────────────┘
```

## Core Components

### 1. Analyzers Package (`src/analyzers/`)

#### CV Parser (`cv_parser.py`)
**Responsibility**: Extract structured data from CV documents

**Key Functions**:
```python
class CVParser:
    def parse(self, file_path: str) -> CVData
    def extract_skills(self, text: str) -> List[Skill]
    def extract_experience(self, text: str) -> List[Experience]
    def detect_proficiency(self, skill: str, context: str) -> int
```

**Dependencies**: `utils.file_readers`, `utils.validators`

#### Job Parser (`job_parser.py`)
**Responsibility**: Parse job descriptions and extract requirements

**Key Functions**:
```python
class JobParser:
    def parse(self, file_path: str) -> JobDescription
    def classify_requirements(self, text: str) -> Requirements
    def extract_experience_requirements(self, text: str) -> ExperienceReq
```

#### Matcher (`matcher.py`)
**Responsibility**: Calculate match scores between candidates and jobs

**Key Functions**:
```python
class SkillMatcher:
    def calculate_match_score(self, cv_data: CVData, job_desc: JobDescription) -> MatchResult
    def score_technical_fit(self, candidate_skills: List[Skill], required_skills: List[Skill]) -> float
    def score_experience_fit(self, years: int, required_years: int) -> float
```

#### Gap Analyzer (`gap_analyzer.py`)
**Responsibility**: Identify and prioritize skill gaps

**Key Functions**:
```python
class GapAnalyzer:
    def analyze_gaps(self, cv_data: CVData, job_desc: JobDescription) -> List[Gap]
    def prioritize_gaps(self, gaps: List[Gap]) -> List[Gap]
    def classify_gap_severity(self, gap: Gap) -> str
```

### 2. Learning Package (`src/learning/`)

#### Plan Generator (`plan_generator.py`)
**Responsibility**: Create personalized learning plans

**Key Functions**:
```python
class PlanGenerator:
    def generate_plan(self, gaps: List[Gap], constraints: Constraints) -> LearningPlan
    def allocate_to_sprints(self, gaps: List[Gap], sprint_duration: int) -> List[Sprint]
    def estimate_learning_time(self, gap: Gap) -> int
```

#### Resource Database (`resource_db.py`)
**Responsibility**: Manage learning resource catalog

**Key Functions**:
```python
class ResourceDatabase:
    def query(self, skill: str, level: int, limit: int) -> List[Resource]
    def add_resource(self, resource: Resource) -> None
    def rate_resource(self, resource_id: str, rating: float) -> None
    def get_recommendations(self, skill: str, learner_profile: Profile) -> List[Resource]
```

#### Test Generator (`test_generator.py`)
**Responsibility**: Generate skill validation tests

**Key Functions**:
```python
class TestGenerator:
    def generate_test(self, skill: str, level: int) -> Test
    def create_questions(self, skill: str, level: int, count: int) -> List[Question]
    def evaluate_response(self, response: str, expected: str) -> float
```

### 3. Tracking Package (`src/tracking/`)

#### Sprint Manager (`sprint_manager.py`)
**Responsibility**: Manage learning sprint lifecycle

**Key Functions**:
```python
class SprintManager:
    def create_sprint(self, duration: int, goals: List[Goal]) -> Sprint
    def update_progress(self, sprint_id: str, skill: str, progress: float) -> None
    def complete_sprint(self, sprint_id: str) -> SprintSummary
    def get_active_sprint(self) -> Sprint
```

#### Quality Gates (`quality_gates.py`)
**Responsibility**: Evaluate readiness gates

**Key Functions**:
```python
class QualityGates:
    def evaluate_foundational(self, cv_data: CVData, job_desc: JobDescription) -> GateResult
    def evaluate_competitive(self, cv_data: CVData, job_desc: JobDescription) -> GateResult
    def evaluate_excellence(self, cv_data: CVData, job_desc: JobDescription) -> GateResult
```

#### Progress Tracker (`progress_tracker.py`)
**Responsibility**: Track and visualize progress

**Key Functions**:
```python
class ProgressTracker:
    def log_activity(self, activity: Activity) -> None
    def get_progress_summary(self, period: str) -> Summary
    def generate_dashboard(self) -> Dashboard
    def export_history(self, format: str) -> str
```

### 4. Generators Package (`src/generators/`)

#### Letter Generator (`letter_generator.py`)
**Responsibility**: Generate application materials

**Key Functions**:
```python
class LetterGenerator:
    def generate_cover_letter(self, match_result: MatchResult, template: str) -> str
    def generate_linkedin_message(self, job_desc: JobDescription, highlights: List[str]) -> str
    def generate_followup_email(self, context: dict) -> str
```

#### Report Generator (`report_generator.py`)
**Responsibility**: Create comprehensive reports

**Key Functions**:
```python
class ReportGenerator:
    def generate_analysis_report(self, match_result: MatchResult) -> Report
    def generate_learning_plan_report(self, plan: LearningPlan) -> Report
    def generate_progress_report(self, tracker: ProgressTracker) -> Report
```

### 5. Utils Package (`src/utils/`)

Provides shared functionality:
- File readers (PDF, DOCX, TXT)
- Data validators
- Formatters and converters
- Helper functions

## Data Flow

### Standard Mode Workflow

```
1. INPUT STAGE
   ┌─────────┐
   │ CV File │──┐
   └─────────┘  │
                ├──→ [File Readers] ──→ Raw Text
   ┌─────────┐  │
   │Job File │──┘
   └─────────┘

2. PARSING STAGE
   Raw Text ──→ [CV Parser] ──→ CVData
   Raw Text ──→ [Job Parser] ──→ JobDescription

3. ANALYSIS STAGE
   CVData + JobDescription ──→ [Matcher] ──→ MatchResult
   MatchResult ──→ [Gap Analyzer] ──→ Gap List

4. PLANNING STAGE
   Gap List ──→ [Plan Generator] ──→ Learning Plan
   Learning Plan ──→ [Resource DB] ──→ Enriched Plan

5. EVALUATION STAGE
   CVData + JobDescription ──→ [Quality Gates] ──→ Gate Results

6. GENERATION STAGE
   All Results ──→ [Report Generator] ──→ Reports
   Match Result ──→ [Letter Generator] ──→ Letters

7. OUTPUT STAGE
   Reports + Letters ──→ [File System] ──→ Export Package
```

### Reverse Mode Workflow

```
1. INPUT STAGE
   CV File ──→ [File Readers] ──→ Raw Text

2. PARSING STAGE
   Raw Text ──→ [CV Parser] ──→ CVData
   CVData ──→ [Skill Extractor] ──→ Master Skillset

3. ANALYSIS STAGE
   Master Skillset ──→ [Job Matcher] ──→ Job Recommendations
   (Matches against job database or market data)

4. PLANNING STAGE
   For each recommended job:
   Job + CVData ──→ [Gap Analyzer] ──→ Gaps
   Gaps ──→ [Plan Generator] ──→ Learning Plan

5. STRATEGY STAGE
   All Plans ──→ [Strategy Builder] ──→ Improvement Strategy
   (Identifies common skills across multiple opportunities)

6. OUTPUT STAGE
   Strategy + Plans ──→ [Report Generator] ──→ Export Package
```

## Module Interactions

### Interaction Patterns

#### 1. Parser → Analyzer Pattern
```python
# CVParser produces data consumed by Matcher
cv_data = cv_parser.parse(cv_file)
job_desc = job_parser.parse(job_file)
match_result = matcher.calculate_match_score(cv_data, job_desc)
```

#### 2. Analyzer → Learning Pattern
```python
# Gap Analyzer feeds Plan Generator
gaps = gap_analyzer.analyze_gaps(cv_data, job_desc)
prioritized_gaps = gap_analyzer.prioritize_gaps(gaps)
learning_plan = plan_generator.generate_plan(prioritized_gaps)
```

#### 3. Tracking → Analysis Feedback Loop
```python
# Progress tracking influences future analysis
tracker.update_progress(skill="Docker", new_level=3)
updated_cv_data = cv_parser.refresh_skills(tracker.get_current_skills())
new_match = matcher.calculate_match_score(updated_cv_data, job_desc)
```

### Dependency Graph

```
JobEngine (Main)
├── Analyzers
│   ├── CVParser
│   │   └── FileReaders
│   ├── JobParser
│   │   └── FileReaders
│   ├── Matcher
│   │   ├── CVParser
│   │   └── JobParser
│   └── GapAnalyzer
│       └── Matcher
├── Learning
│   ├── PlanGenerator
│   │   └── GapAnalyzer
│   ├── ResourceDB
│   └── TestGenerator
├── Tracking
│   ├── SprintManager
│   ├── QualityGates
│   │   └── Matcher
│   └── ProgressTracker
└── Generators
    ├── LetterGenerator
    └── ReportGenerator
```

## Data Models

### Core Data Structures

#### Skill
```python
@dataclass
class Skill:
    name: str
    level: int  # 1-5
    years_experience: float
    last_used: datetime
    context: List[str]
    verified: bool = False
```

#### CVData
```python
@dataclass
class CVData:
    skills: List[Skill]
    experience: List[Experience]
    education: List[Education]
    projects: List[Project]
    certifications: List[Certification]
    metadata: dict
```

#### JobDescription
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
    metadata: dict
```

#### MatchResult
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
```

#### Gap
```python
@dataclass
class Gap:
    skill: str
    current_level: int
    required_level: int
    priority: int
    category: str  # 'critical', 'important', 'nice-to-have'
    estimated_learning_time: int  # hours
```

#### LearningPlan
```python
@dataclass
class LearningPlan:
    sprints: List[Sprint]
    total_duration_weeks: int
    estimated_hours: int
    quality_gate_targets: dict
    resources: List[Resource]
```

## State Management

### State Persistence

The system maintains state across sessions using JSON files:

```
job_search_data/
├── workflow_state.json      # Current workflow state
├── master_skillset.json     # User's skill inventory
├── analyzed_jobs.json       # Job analysis history
├── learning_progress.json   # Learning plan progress
└── sprint_history.json      # Completed sprints
```

### State Manager

```python
class StateManager:
    def save_state(self, state: dict, state_type: str) -> None
    def load_state(self, state_type: str) -> dict
    def update_state(self, updates: dict, state_type: str) -> None
    def get_current_workflow_state(self) -> WorkflowState
```

### State Transitions

```
IDLE → ANALYZING → PLANNING → LEARNING → APPLYING → COMPLETED
  ↑                                           ↓
  └─────────────── RESET ←───────────────────┘
```

## Extension Points

### 1. Custom Analyzers

Add new analysis modules:

```python
from src.analyzers.base import BaseAnalyzer

class SoftSkillAnalyzer(BaseAnalyzer):
    def analyze(self, cv_data: CVData) -> SoftSkillsProfile:
        # Custom implementation
        pass
```

### 2. Custom Resource Providers

Integrate external learning platforms:

```python
from src.learning.resource_db import ResourceProvider

class CourseraProvider(ResourceProvider):
    def fetch_resources(self, skill: str, level: int) -> List[Resource]:
        # API integration
        pass
```

### 3. Custom Generators

Add new output formats:

```python
from src.generators.base import BaseGenerator

class PDFReportGenerator(BaseGenerator):
    def generate(self, data: dict) -> bytes:
        # PDF generation
        pass
```

### 4. Custom Quality Gates

Define organization-specific gates:

```python
from src.tracking.quality_gates import QualityGate

class CompanySpecificGate(QualityGate):
    def evaluate(self, cv_data: CVData, requirements: dict) -> GateResult:
        # Custom criteria
        pass
```

## Deployment Architecture

### Local Deployment

```
User Machine
├── Python 3.8+ Runtime
├── Job Engine Package
├── Data Directory (gitignored)
└── Configuration Files
```

### GitHub Actions Deployment

```
GitHub Repository
├── Workflow Files (.github/workflows/)
├── Secrets (CV content, API keys)
├── Job Descriptions (Issues or PRs)
└── Artifacts (Analysis results)
```

### Future: Web Service Deployment

```
Cloud Infrastructure
├── API Gateway
├── Application Server (FastAPI)
├── Database (PostgreSQL)
├── File Storage (S3)
├── Cache Layer (Redis)
└── Queue System (Celery)
```

## Security Considerations

### Data Protection

- CV data never leaves user's machine in local mode
- Sensitive data encrypted at rest
- No third-party data sharing without consent
- Secure credential management

### Input Validation

- All file inputs validated before processing
- SQL injection prevention (when database used)
- Path traversal protection
- Resource consumption limits

## Performance Optimization

### Caching Strategy

- Parsed documents cached in memory
- Resource database queries cached
- Skill matching results cached by hash

### Lazy Loading

- Resources loaded only when needed
- Large datasets streamed rather than loaded entirely
- Optional modules imported on demand

### Async Processing

Future enhancement for improved performance:
```python
async def analyze_multiple_jobs(cv_data, job_files):
    tasks = [analyze_job(cv_data, job) for job in job_files]
    results = await asyncio.gather(*tasks)
    return results
```

## Testing Architecture

### Test Layers

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test module interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Benchmark critical paths

### Test Data Management

```
tests/fixtures/
├── sample_cv.txt
├── sample_job.txt
├── sample_data.json
└── mock_responses/
```

## Monitoring and Logging

### Logging Strategy

```python
import logging

# Component-level loggers
logger = logging.getLogger('job_engine.analyzers.matcher')

# Log levels
logger.debug("Detailed matching calculation")
logger.info("Match score calculated: 87%")
logger.warning("Missing preferred skill: GraphQL")
logger.error("Failed to parse CV section")
```

### Metrics Collection

Track system performance:
- Parse time per document
- Match calculation time
- Resource query response time
- End-to-end workflow duration

## Version Compatibility

- Python: 3.8+
- Dependencies: Specified in requirements.txt
- Backward compatibility maintained for major versions
- Deprecation warnings for breaking changes

## Future Architecture Enhancements

1. **Microservices**: Break into independent services
2. **Event-Driven**: Use message queues for async processing
3. **ML Integration**: Add machine learning models
4. **Real-time Collaboration**: Multi-user support
5. **Cloud-Native**: Kubernetes deployment option