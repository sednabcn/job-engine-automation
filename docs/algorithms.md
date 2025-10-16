# Algorithms and Scoring Methods

## Table of Contents

1. [Overview](#overview)
2. [Skill Extraction](#skill-extraction)
3. [Match Scoring Algorithm](#match-scoring-algorithm)
4. [Proficiency Level Detection](#proficiency-level-detection)
5. [Gap Analysis](#gap-analysis)
6. [Learning Plan Generation](#learning-plan-generation)
7. [Quality Gate Evaluation](#quality-gate-evaluation)
8. [Customization](#customization)

## Overview

The Advanced Job Engine uses multiple algorithms to analyze CVs, match them against job descriptions, and generate personalized learning plans. This document explains the mathematical models and decision logic behind each component.

## Skill Extraction

### CV Parsing Algorithm

**Input**: Raw CV text (from PDF, DOCX, or TXT)  
**Output**: Structured skill inventory with proficiency levels

#### Step 1: Text Normalization
```
normalized_text = lowercase(raw_text)
normalized_text = remove_special_chars(normalized_text)
normalized_text = standardize_spacing(normalized_text)
```

#### Step 2: Section Detection
```python
def detect_sections(text):
    section_headers = {
        'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
        'experience': ['experience', 'work history', 'employment'],
        'education': ['education', 'academic', 'qualifications'],
        'projects': ['projects', 'portfolio']
    }
    
    for section_type, keywords in section_headers.items():
        for keyword in keywords:
            if keyword in text:
                extract_section(text, keyword, section_type)
```

#### Step 3: Skill Pattern Matching
```python
skill_patterns = [
    r'\b(python|java|javascript|c\+\+)\b',  # Languages
    r'\b(docker|kubernetes|aws|azure)\b',   # Tools
    r'\b(agile|scrum|devops|ci\/cd)\b'      # Methodologies
]

for pattern in skill_patterns:
    matches = regex.findall(pattern, text)
    for match in matches:
        skills.add(standardize_skill_name(match))
```

#### Step 4: Context-Based Proficiency Detection
```python
def detect_proficiency(skill, context_window):
    proficiency_indicators = {
        5: ['expert', 'architect', 'led team', 'designed system'],
        4: ['advanced', 'mentored', 'optimized', 'architected'],
        3: ['proficient', 'experienced', 'implemented', 'developed'],
        2: ['familiar', 'worked with', 'assisted', 'learned'],
        1: ['basic', 'exposure', 'aware', 'studied']
    }
    
    for level, indicators in proficiency_indicators.items():
        if any(indicator in context_window for indicator in indicators):
            return level
    
    return estimate_from_experience(skill, context_window)
```

### Job Description Parsing

**Input**: Job posting text  
**Output**: Required skills, nice-to-have skills, experience requirements

#### Requirement Classification
```python
def classify_requirements(text):
    required_indicators = ['required', 'must have', 'essential', 'mandatory']
    preferred_indicators = ['preferred', 'nice to have', 'bonus', 'plus']
    
    requirements = {
        'required': [],
        'preferred': [],
        'experience_years': None
    }
    
    for sentence in sentences:
        if any(indicator in sentence for indicator in required_indicators):
            requirements['required'].extend(extract_skills(sentence))
        elif any(indicator in sentence for indicator in preferred_indicators):
            requirements['preferred'].extend(extract_skills(sentence))
    
    requirements['experience_years'] = extract_years_experience(text)
    return requirements
```

## Match Scoring Algorithm

### Overall Match Score

The overall match score is a weighted combination of multiple factors:

```
OverallScore = (w₁ × TechnicalScore) + 
               (w₂ × ExperienceScore) + 
               (w₃ × EducationScore) + 
               (w₄ × SoftSkillsScore)
```

**Default Weights**:
- w₁ (Technical) = 0.40
- w₂ (Experience) = 0.30
- w₃ (Education) = 0.15
- w₄ (Soft Skills) = 0.15

### Technical Skills Score

```python
def calculate_technical_score(candidate_skills, required_skills, preferred_skills):
    # Required skills matching
    required_matches = 0
    required_level_bonus = 0
    
    for skill in required_skills:
        if skill.name in candidate_skills:
            candidate_level = candidate_skills[skill.name].level
            required_level = skill.required_level
            
            # Base match
            required_matches += 1
            
            # Level bonus/penalty
            level_difference = candidate_level - required_level
            required_level_bonus += min(level_difference * 0.1, 0.2)
    
    required_score = (required_matches / len(required_skills)) * 100
    required_score += required_level_bonus
    
    # Preferred skills matching
    preferred_matches = sum(1 for skill in preferred_skills 
                           if skill.name in candidate_skills)
    preferred_score = (preferred_matches / len(preferred_skills)) * 100
    
    # Combined score (70% required, 30% preferred)
    technical_score = (0.7 * required_score) + (0.3 * preferred_score)
    
    return min(technical_score, 100)
```

### Experience Score

```python
def calculate_experience_score(candidate_years, required_years):
    if candidate_years >= required_years:
        # Meets or exceeds requirement
        base_score = 100
        
        # Diminishing returns for extra experience
        extra_years = candidate_years - required_years
        bonus = min(extra_years * 2, 10)  # Max 10% bonus
        
        return min(base_score + bonus, 100)
    else:
        # Below requirement - linear penalty
        years_short = required_years - candidate_years
        penalty = years_short * 15  # 15% penalty per year short
        
        return max(100 - penalty, 0)
```

### Skill Level Comparison

When comparing skill proficiency levels:

```python
def level_match_score(candidate_level, required_level):
    """
    Returns a score from 0-100 based on level comparison
    """
    if candidate_level >= required_level:
        # Meets or exceeds
        excess = candidate_level - required_level
        return 100 + (excess * 5)  # Bonus for exceeding
    else:
        # Below requirement
        gap = required_level - candidate_level
        
        # Penalties increase with gap size
        if gap == 1:
            return 70  # Minor gap
        elif gap == 2:
            return 40  # Moderate gap
        elif gap == 3:
            return 15  # Significant gap
        else:
            return 0   # Too large a gap
```

## Proficiency Level Detection

### Experience-Based Estimation

When explicit proficiency indicators aren't found:

```python
def estimate_proficiency_from_experience(skill, cv_data):
    # Find all mentions of the skill
    mentions = find_skill_mentions(skill, cv_data)
    
    # Analyze recency
    recency_score = calculate_recency(mentions)
    
    # Analyze frequency
    frequency = len(mentions)
    
    # Analyze context depth
    context_score = analyze_context_depth(mentions)
    
    # Calculate years of experience with skill
    years_experience = calculate_skill_experience_years(mentions)
    
    # Combine factors
    estimated_level = (
        (years_experience * 0.4) +
        (recency_score * 0.2) +
        (min(frequency / 5, 1) * 0.2) +
        (context_score * 0.2)
    ) * 5  # Scale to 1-5
    
    return round(max(1, min(5, estimated_level)))
```

### Context Depth Analysis

```python
def analyze_context_depth(mentions):
    """
    Analyzes how deeply the skill is discussed
    Returns score 0-1
    """
    depth_indicators = {
        'surface': ['used', 'familiar', 'aware'],
        'practical': ['developed', 'implemented', 'built', 'created'],
        'advanced': ['optimized', 'designed', 'architected', 'scaled'],
        'expert': ['led', 'established', 'innovated', 'authored']
    }
    
    depth_scores = {'surface': 0.25, 'practical': 0.5, 
                   'advanced': 0.75, 'expert': 1.0}
    
    scores = []
    for mention in mentions:
        for depth_level, indicators in depth_indicators.items():
            if any(indicator in mention.lower() for indicator in indicators):
                scores.append(depth_scores[depth_level])
                break
    
    return sum(scores) / len(scores) if scores else 0.25
```

## Gap Analysis

### Priority Scoring

Gaps are prioritized based on multiple factors:

```python
def calculate_gap_priority(skill, required_level, candidate_level):
    # Impact factor (0-1)
    if skill in critical_skills:
        impact = 1.0
    elif skill in important_skills:
        impact = 0.7
    else:
        impact = 0.4
    
    # Urgency factor based on gap size
    gap_size = required_level - candidate_level
    urgency = min(gap_size / 4, 1.0)
    
    # Market demand factor (if available)
    market_demand = get_market_demand_score(skill)  # 0-1
    
    # Combined priority score
    priority = (
        (impact * 0.4) +
        (urgency * 0.4) +
        (market_demand * 0.2)
    ) * 100
    
    return round(priority)
```

### Gap Classification

```python
def classify_gap(priority_score, skill_importance):
    if skill_importance == 'required':
        if priority_score >= 80:
            return 'CRITICAL'
        elif priority_score >= 60:
            return 'HIGH'
        else:
            return 'MEDIUM'
    else:  # preferred/nice-to-have
        if priority_score >= 70:
            return 'MEDIUM'
        else:
            return 'LOW'
```

## Learning Plan Generation

### Sprint Allocation Algorithm

```python
def allocate_skills_to_sprints(gaps, sprint_duration_weeks, hours_per_week):
    """
    Allocates skill gaps to learning sprints
    """
    sprints = []
    current_sprint = Sprint(duration_weeks=sprint_duration_weeks)
    
    # Sort gaps by priority
    sorted_gaps = sorted(gaps, key=lambda g: g.priority, reverse=True)
    
    for gap in sorted_gaps:
        # Estimate learning time
        learning_time = estimate_learning_time(
            skill=gap.skill,
            current_level=gap.current_level,
            target_level=gap.target_level
        )
        
        # Check if it fits in current sprint
        available_hours = (sprint_duration_weeks * hours_per_week) - current_sprint.allocated_hours
        
        if learning_time <= available_hours:
            current_sprint.add_skill(gap, learning_time)
        else:
            # Start new sprint
            if current_sprint.skills:
                sprints.append(current_sprint)
            current_sprint = Sprint(duration_weeks=sprint_duration_weeks)
            current_sprint.add_skill(gap, learning_time)
    
    if current_sprint.skills:
        sprints.append(current_sprint)
    
    return sprints
```

### Learning Time Estimation

```python
def estimate_learning_time(skill, current_level, target_level):
    """
    Estimates hours needed to reach target level
    """
    # Base hours per level increase
    base_hours = {
        (0, 1): 10,   # No knowledge to basic
        (1, 2): 20,   # Basic to working knowledge
        (2, 3): 40,   # Working to proficient
        (3, 4): 60,   # Proficient to advanced
        (4, 5): 100   # Advanced to expert
    }
    
    total_hours = 0
    for level in range(current_level, target_level):
        level_pair = (level, level + 1)
        hours = base_hours.get(level_pair, 30)
        
        # Adjust for skill complexity
        complexity_multiplier = get_skill_complexity(skill)
        hours *= complexity_multiplier
        
        total_hours += hours
    
    return total_hours
```

### Resource Matching

```python
def match_resources_to_skill(skill, current_level, target_level):
    """
    Finds optimal learning resources for skill progression
    """
    resources = []
    
    for level in range(current_level + 1, target_level + 1):
        # Query resource database
        level_resources = resource_db.query(
            skill=skill,
            level=level,
            sort_by='rating',
            limit=3
        )
        
        # Score resources
        scored_resources = []
        for resource in level_resources:
            score = calculate_resource_score(
                resource=resource,
                learner_profile=get_learner_profile(),
                skill=skill,
                target_level=level
            )
            scored_resources.append((resource, score))
        
        # Select best resources
        best_resources = sorted(scored_resources, 
                               key=lambda x: x[1], 
                               reverse=True)[:2]
        
        resources.extend([r[0] for r in best_resources])
    
    return resources
```

## Quality Gate Evaluation

### Foundational Gate

```python
def evaluate_foundational_gate(candidate_skills, required_skills):
    """
    Checks if candidate meets minimum requirements
    """
    criteria = {
        'required_skills_coverage': 0.80,  # 80% of required skills
        'minimum_skill_level': 2.0,        # Average level 2
        'critical_skills_met': 1.0         # 100% of critical skills
    }
    
    # Check required skills coverage
    met_skills = sum(1 for skill in required_skills 
                    if skill.name in candidate_skills)
    coverage = met_skills / len(required_skills)
    
    # Check minimum skill levels
    candidate_levels = [candidate_skills[s.name].level 
                       for s in required_skills 
                       if s.name in candidate_skills]
    avg_level = sum(candidate_levels) / len(candidate_levels) if candidate_levels else 0
    
    # Check critical skills
    critical_skills = [s for s in required_skills if s.is_critical]
    critical_met = sum(1 for skill in critical_skills 
                      if skill.name in candidate_skills)
    critical_coverage = critical_met / len(critical_skills) if critical_skills else 1.0
    
    # Evaluate
    passes = (
        coverage >= criteria['required_skills_coverage'] and
        avg_level >= criteria['minimum_skill_level'] and
        critical_coverage >= criteria['critical_skills_met']
    )
    
    return {
        'passes': passes,
        'coverage': coverage,
        'avg_level': avg_level,
        'critical_coverage': critical_coverage
    }
```

### Competitive Gate

```python
def evaluate_competitive_gate(candidate_skills, job_requirements):
    """
    Checks if candidate is competitive for the position
    """
    criteria = {
        'required_skills_coverage': 0.90,
        'preferred_skills_coverage': 0.50,
        'minimum_skill_level': 3.0,
        'standout_skills': 2  # Number of skills at level 4+
    }
    
    # Required skills
    required_met = sum(1 for skill in job_requirements['required']
                      if skill.name in candidate_skills and
                      candidate_skills[skill.name].level >= skill.required_level)
    required_coverage = required_met / len(job_requirements['required'])
    
    # Preferred skills
    preferred_met = sum(1 for skill in job_requirements['preferred']
                       if skill.name in candidate_skills)
    preferred_coverage = preferred_met / len(job_requirements['preferred']) if job_requirements['preferred'] else 1.0
    
    # Skill levels
    all_levels = [s.level for s in candidate_skills.values()]
    avg_level = sum(all_levels) / len(all_levels)
    
    # Standout skills
    standout_count = sum(1 for s in candidate_skills.values() if s.level >= 4)
    
    passes = (
        required_coverage >= criteria['required_skills_coverage'] and
        preferred_coverage >= criteria['preferred_skills_coverage'] and
        avg_level >= criteria['minimum_skill_level'] and
        standout_count >= criteria['standout_skills']
    )
    
    return {
        'passes': passes,
        'required_coverage': required_coverage,
        'preferred_coverage': preferred_coverage,
        'avg_level': avg_level,
        'standout_skills': standout_count
    }
```

### Excellence Gate

```python
def evaluate_excellence_gate(candidate_skills, job_requirements, market_data):
    """
    Checks if candidate exceeds expectations
    """
    criteria = {
        'required_skills_coverage': 1.0,
        'preferred_skills_coverage': 0.75,
        'minimum_skill_level': 3.5,
        'expert_skills': 1,  # At least 1 skill at level 5
        'unique_strengths': 2  # Skills not in job description
    }
    
    # All previous checks
    competitive_result = evaluate_competitive_gate(candidate_skills, job_requirements)
    
    # Expert skills
    expert_count = sum(1 for s in candidate_skills.values() if s.level == 5)
    
    # Unique strengths (valuable skills not mentioned)
    job_skills = set(s.name for s in job_requirements['required'] + job_requirements['preferred'])
    unique_valuable = sum(1 for skill_name, skill in candidate_skills.items()
                         if skill_name not in job_skills and
                         skill.level >= 3 and
                         is_market_valuable(skill_name, market_data))
    
    # Level coverage
    all_levels = [s.level for s in candidate_skills.values()]
    avg_level = sum(all_levels) / len(all_levels)
    
    passes = (
        competitive_result['required_coverage'] >= criteria['required_skills_coverage'] and
        competitive_result['preferred_coverage'] >= criteria['preferred_skills_coverage'] and
        avg_level >= criteria['minimum_skill_level'] and
        expert_count >= criteria['expert_skills'] and
        unique_valuable >= criteria['unique_strengths']
    )
    
    return {
        'passes': passes,
        'expert_skills': expert_count,
        'unique_strengths': unique_valuable,
        'avg_level': avg_level
    }
```

## Customization

### Adjusting Scoring Weights

Modify weights in configuration:

```python
custom_weights = {
    'technical_skills': 0.50,  # Increase for technical roles
    'experience': 0.25,
    'education': 0.10,
    'soft_skills': 0.15
}

engine = JobEngine(scoring_weights=custom_weights)
```

### Custom Skill Complexity

Define complexity for specific skills:

```python
skill_complexity = {
    'Python': 1.0,           # Standard
    'Machine Learning': 1.5, # More complex
    'Kubernetes': 1.8,       # Highly complex
    'HTML': 0.7              # Less complex
}
```

### Custom Quality Gate Thresholds

Adjust gate criteria:

```python
custom_gates = {
    'foundational': {
        'required_skills_coverage': 0.75,  # Lower for entry-level
        'minimum_skill_level': 1.5
    },
    'competitive': {
        'required_skills_coverage': 0.85,
        'minimum_skill_level': 2.5
    }
}
```

## Performance Considerations

### Computational Complexity

| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| CV Parsing | O(n) | O(n) |
| Skill Matching | O(m × n) | O(m + n) |
| Gap Analysis | O(n log n) | O(n) |
| Sprint Allocation | O(n log n) | O(n) |
| Resource Matching | O(n × r) | O(r) |

Where:
- n = number of skills
- m = number of job requirements
- r = number of resources in database

### Optimization Strategies

1. **Caching**: Cache parsed CVs and job descriptions
2. **Indexing**: Index skill database for fast lookups
3. **Parallel Processing**: Process multiple jobs concurrently
4. **Lazy Loading**: Load resources only when needed

## Validation and Testing

### Algorithm Validation

Test cases for scoring accuracy:

```python
test_cases = [
    {
        'candidate': {'Python': 3, 'Docker': 2},
        'required': {'Python': 3, 'Docker': 3},
        'expected_score': 75-85
    },
    {
        'candidate': {'Python': 4, 'Docker': 4, 'AWS': 3},
        'required': {'Python': 3, 'Docker': 3},
        'expected_score': 95-100
    }
]
```

### Edge Cases

Handled scenarios:
- Missing required skills (score = 0 for that skill)
- Skills at level 0 (treated as non-existent)
- Empty job descriptions (validation error)
- Conflicting skill names (standardization)
- Ambiguous proficiency (conservative estimation)

## References

- **TF-IDF**: Used for skill relevance in context
- **Weighted Scoring**: Industry standard for multi-factor evaluation
- **Gradient-based Priority**: Ensures smooth priority distribution
- **Learning Curve Theory**: Based on adult learning research

## Version History

- **v1.0**: Initial scoring algorithms
- **v1.1**: Added quality gates
- **v1.2**: Improved proficiency detection
- **v2.0**: Introduced learning plan generation
- **v2.1**: Added market demand factors

## Future Enhancements

Planned improvements:
- Machine learning for proficiency prediction
- Natural language processing for deeper context analysis
- Market trend integration for dynamic skill prioritization
- Collaborative filtering for resource recommendations