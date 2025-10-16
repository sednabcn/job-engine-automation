# Troubleshooting Guide

## Table of Contents

1. [Common Issues](#common-issues)
2. [File Processing Errors](#file-processing-errors)
3. [Analysis Problems](#analysis-problems)
4. [Learning Plan Issues](#learning-plan-issues)
5. [Export and Output Problems](#export-and-output-problems)
6. [GitHub Actions Issues](#github-actions-issues)
7. [Performance Problems](#performance-problems)
8. [Data Validation Errors](#data-validation-errors)
9. [Debug Mode](#debug-mode)
10. [Getting Help](#getting-help)

## Common Issues

### Installation Problems

#### Issue: Module Not Found Error

```
ModuleNotFoundError: No module named 'src'
```

**Solutions:**

1. **Check Python Path:**
```bash
# Run from project root
cd /path/to/advanced-job-engine
python src/python_advanced_job_engine.py
```

2. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

3. **Check Python Version:**
```bash
python --version  # Should be 3.8 or higher
```

#### Issue: Permission Denied

```
PermissionError: [Errno 13] Permission denied: 'job_search_data/'
```

**Solutions:**

1. **Fix Directory Permissions:**
```bash
chmod 755 job_search_data/
mkdir -p data/ job_search_data/
```

2. **Check Write Access:**
```bash
ls -la job_search_data/
```

#### Issue: Dependencies Conflict

```
ERROR: pip's dependency resolver does not currently take into account all packages...
```

**Solutions:**

1. **Use Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Update pip:**
```bash
pip install --upgrade pip
```

## File Processing Errors

### PDF Reading Issues

#### Issue: Empty Text Extracted from PDF

**Symptoms:**
- Analysis shows no skills found
- Match score is 0%
- "Unable to extract text from PDF" warning

**Solutions:**

1. **Check PDF Type:**
```python
# Test if PDF is image-based
from src.utils.file_readers import is_image_pdf

if is_image_pdf("data/my_cv.pdf"):
    print("PDF contains images, OCR required")
```

2. **Convert Image PDF:**
```bash
# Use OCR tool
sudo apt-get install tesseract-ocr
python -c "from pdf2image import convert_from_path; images = convert_from_path('my_cv.pdf')"
```

3. **Alternative: Save as Text PDF:**
- Open PDF in viewer
- Print to PDF or Export as Text-based PDF

4. **Use Different Format:**
```bash
# Convert to DOCX or use TXT format
python src/python_advanced_job_engine.py --cv data/my_cv.docx
```

#### Issue: PDF Library Error

```
ImportError: PyPDF2 is not installed
```

**Solution:**
```bash
pip install PyPDF2 pdfplumber
```

### DOCX Reading Issues

#### Issue: Corrupted DOCX File

```
BadZipFile: File is not a zip file
```

**Solutions:**

1. **Verify File Integrity:**
```bash
file data/my_cv.docx  # Should show: Microsoft Word 2007+
```

2. **Repair Document:**
- Open in Microsoft Word
- File → Info → Check for Issues → Repair
- Save As → New file

3. **Re-save Document:**
- Open in Word
- Save As → Word Document (.docx)
- Enable "Maintain compatibility"

#### Issue: python-docx Not Installed

**Solution:**
```bash
pip install python-docx
```

### Encoding Issues

#### Issue: UnicodeDecodeError

```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Solutions:**

1. **Specify Encoding:**
```python
from src.utils.file_readers import read_txt

text = read_txt("data/my_cv.txt", encoding='latin-1')
```

2. **Convert File Encoding:**
```bash
iconv -f ISO-8859-1 -t UTF-8 my_cv.txt > my_cv_utf8.txt
```

3. **Common Encodings to Try:**
- `utf-8`
- `latin-1`
- `cp1252` (Windows)
- `iso-8859-1`

## Analysis Problems

### Low Match Scores

#### Issue: Consistently Low Scores (<50%)

**Diagnostic Steps:**

1. **Check Skills Detection:**
```python
from src.analyzers.cv_parser import CVParser

parser = CVParser()
cv_data = parser.parse("data/my_cv.pdf")
print(f"Skills found: {len(cv_data.skills)}")
for skill in cv_data.skills:
    print(f"- {skill.name}: Level {skill.level}")
```

2. **Verify Job Requirements Parsed:**
```python
from src.analyzers.job_parser import JobParser

parser = JobParser()
job = parser.parse("data/job.pdf")
print(f"Required: {len(job.required_skills)}")
print(f"Preferred: {len(job.preferred_skills)}")
```

**Solutions:**

1. **Update CV Format:**
- Use clear section headers: "Skills", "Technical Skills"
- List skills explicitly
- Include proficiency indicators

2. **Expand Skill Synonyms:**
```python
# Add to configuration
skill_synonyms = {
    'JavaScript': ['JS', 'ECMAScript', 'Node.js'],
    'Kubernetes': ['K8s', 'k8s'],
    'CI/CD': ['Continuous Integration', 'Continuous Deployment']
}
```

3. **Adjust Scoring Weights:**
```python
custom_config = {
    'scoring_weights': {
        'technical_skills': 0.50,  # Increase if technical role
        'experience': 0.25,
        'education': 0.10,
        'soft_skills': 0.15
    }
}
```

### Skills Not Detected

#### Issue: Skills in CV Not Found by Parser

**Diagnostic:**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

parser = CVParser()
cv_data = parser.parse("data/my_cv.pdf")
```

**Solutions:**

1. **Check Skill Database:**
```python
# View recognized skills
from src.analyzers.cv_parser import KNOWN_SKILLS
print(f"Known skills: {len(KNOWN_SKILLS)}")
```

2. **Add Custom Skills:**
```python
# Add to skill database
from src.analyzers.cv_parser import add_custom_skills

add_custom_skills([
    'CustomTool', 'InternalFramework', 'ProprietaryLanguage'
])
```

3. **Format Skills Clearly:**
```
# Good format
TECHNICAL SKILLS:
- Python (5 years, Expert)
- Docker (3 years, Proficient)
- AWS (2 years, Intermediate)

# Better than
"Experience with various technologies including Python, Docker, AWS..."
```

### Proficiency Levels Inaccurate

#### Issue: Skills Detected at Wrong Level

**Diagnostic:**
```python
# Check proficiency detection
parser = CVParser()
skill_mentions = parser.find_skill_mentions("Python", cv_text)
for mention in skill_mentions:
    print(f"Context: {mention.context}")
    print(f"Detected level: {mention.detected_level}")
```

**Solutions:**

1. **Use Explicit Proficiency Indicators:**
```
Good indicators:
- "Expert in Python (8 years)"
- "Advanced Docker knowledge"
- "Proficient with Kubernetes"
- "Basic understanding of GraphQL"
```

2. **Provide Context:**
```
Include:
- Years of experience
- Project complexity
- Team roles (led, mentored, assisted)
- Achievements with the skill
```

3. **Manual Override:**
```python
engine.update_skills({
    'Python': 4,  # Force level 4
    'Docker': 3
})
```

## Learning Plan Issues

### Unrealistic Time Estimates

#### Issue: Learning Plan Too Aggressive or Too Conservative

**Diagnostic:**
```python
plan = result.learning_plan
for sprint in plan.sprints:
    print(f"Sprint {sprint.number}: {sprint.estimated_hours}h in {sprint.duration_weeks}w")
    print(f"  Hours/week: {sprint.estimated_hours / sprint.duration_weeks}")
```

**Solutions:**

1. **Adjust Sprint Duration:**
```python
engine = JobEngine(config={
    'learning_sprint_weeks': 3,  # Increase from default 2
    'study_hours_per_week': 15   # Adjust based on availability
})
```

2. **Customize Learning Time Multipliers:**
```python
# For skills you learn faster
skill_time_adjustments = {
    'Docker': 0.8,  # 20% faster
    'React': 1.2    # 20% slower
}
```

3. **Split Complex Skills:**
- Break "Advanced Kubernetes" into smaller goals
- Focus on specific aspects first

### Too Many Gaps Identified

#### Issue: Learning Plan Has 20+ Gaps

**Solutions:**

1. **Filter by Priority:**
```python
critical_gaps = [g for g in result.gaps if g.category == 'critical']
plan = generator.generate_plan(critical_gaps)
```

2. **Focus on Job Requirements:**
```python
required_only = [g for g in result.gaps if g.is_required]
```

3. **Adjust Quality Gate:**
```python
# Lower threshold for foundational gate
custom_gates = {
    'foundational': {
        'required_skills_coverage': 0.70  # Down from 0.80
    }
}
```

### Resource Links Broken

#### Issue: Learning Resources Return 404

**Solutions:**

1. **Update Resource Database:**
```bash
python tools/update_resources.py
```

2. **Add Verified Resources:**
```python
from src.learning.resource_db import ResourceDatabase

db = ResourceDatabase()
db.add_resource(Resource(
    skill="Docker",
    title="Current Docker Course",
    url="https://verified-url.com",
    verified=True,
    verified_date=datetime.now()
))
```

3. **Use Local Resources:**
```python
# Reference local files or internal training
resource = Resource(
    skill="InternalTool",
    title="Company Documentation",
    type="documentation",
    url="file:///company/docs/internal-tool.pdf"
)
```

## Export and Output Problems

### Export Failures

#### Issue: Cannot Write to Export Directory

```
PermissionError: [Errno 13] Permission denied: 'job_search_data/export_20241015/'
```

**Solutions:**

1. **Check Permissions:**
```bash
ls -la job_search_data/
chmod 755