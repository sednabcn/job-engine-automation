# 🔧 Fix: Empty PDF Files Error

## Problem
```
PyPDF2.errors.EmptyFileError: Cannot read an empty file
```

Your `data/my_cv.pdf` and `data/target_job.pdf` files are empty (0 bytes).

---

## ✅ Solution: Add Real Content

### Option 1: Create Test Files Locally

```bash
# 1. Create sample CV (text format is easier for testing)
cat > data/my_cv.txt << 'EOF'
JOHN DOE
Software Engineer

EXPERIENCE
Senior Developer at Tech Corp (2020-Present)
- Built scalable web applications using React and Node.js
- Implemented CI/CD pipelines with GitHub Actions
- Led team of 5 developers

Junior Developer at StartupXYZ (2018-2020)
- Developed REST APIs using Python and Flask
- Worked with PostgreSQL databases
- Participated in agile development

SKILLS
Programming Languages: Python, JavaScript, TypeScript, Java
Frameworks: React, Node.js, Django, Flask, Spring Boot
Databases: PostgreSQL, MongoDB, Redis
DevOps: Docker, Kubernetes, GitHub Actions, AWS
Tools: Git, VS Code, Jira, Postman

EDUCATION
Bachelor of Science in Computer Science
University of Technology (2014-2018)

PROJECTS
- E-commerce Platform: Built full-stack application with 10k users
- Data Analytics Dashboard: Real-time analytics using React and D3.js
- API Gateway: Microservices architecture with Docker
EOF

# 2. Create sample job description
cat > data/target_job.txt << 'EOF'
Full Stack Engineer - Senior Level

ABOUT THE ROLE
We're looking for an experienced Full Stack Engineer to join our growing team.
You'll work on cutting-edge web applications serving millions of users.

REQUIRED SKILLS
- 5+ years experience with JavaScript/TypeScript
- Strong React and Node.js expertise
- Experience with PostgreSQL or similar databases
- Understanding of CI/CD and DevOps practices
- Experience with cloud platforms (AWS/GCP/Azure)

PREFERRED SKILLS
- GraphQL experience
- Kubernetes knowledge
- Python or Java background
- Agile/Scrum experience
- Open source contributions

RESPONSIBILITIES
- Design and implement scalable web applications
- Write clean, maintainable code
- Collaborate with cross-functional teams
- Mentor junior developers
- Participate in code reviews

REQUIREMENTS
- Bachelor's degree in Computer Science or equivalent
- Strong communication skills
- Team player with leadership qualities

BENEFITS
- Competitive salary
- Remote work options
- Health insurance
- Professional development budget
EOF

# 3. Commit these files
git add data/my_cv.txt data/target_job.txt
git commit -m "Add sample CV and job description"
git push
```

### Option 2: Use Your Real Files

```bash
# Copy your actual CV and job description
cp ~/path/to/your/real_cv.pdf data/my_cv.pdf
cp ~/path/to/job_description.pdf data/target_job.pdf

# Or if you have .docx files
cp ~/path/to/your/cv.docx data/my_cv.docx
cp ~/path/to/job.docx data/target_job.docx

# Commit
git add data/
git commit -m "Add CV and job description"
git push
```

### Option 3: Create PDFs Online

If you need PDFs specifically:

1. Go to https://www.google.com/docs
2. Create a new document
3. Paste your CV content
4. **File → Download → PDF Document (.pdf)**
5. Save as `my_cv.pdf`
6. Repeat for job description
7. Upload to your repo's `data/` folder

---

## 🔍 Verify Files Are Not Empty

```bash
# Check file sizes
ls -lh data/

# Should show something like:
# -rw-r--r-- 1 user user 15K Oct 18 12:00 my_cv.pdf
# -rw-r--r-- 1 user user 8.5K Oct 18 12:00 target_job.pdf

# NOT:
# -rw-r--r-- 1 user user 0 Oct 18 12:00 my_cv.pdf  ❌ EMPTY!

# View text files
cat data/my_cv.txt

# Extract text from PDFs (to verify content)
python3 << 'EOF'
import PyPDF2
with open('data/my_cv.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    print(f"Pages: {len(reader.pages)}")
    print(f"First page text: {reader.pages[0].extract_text()[:200]}")
EOF
```

---

## 🎯 Update Workflow to Handle Missing Files

Add this to your workflow before analysis:

```yaml
- name: 🔍 Verify Input Files
  run: |
    echo "Checking data files..."
    
    # Check if CV exists and is not empty
    if [ ! -f "${{ github.event.inputs.cv_file }}" ]; then
      echo "❌ Error: CV file not found: ${{ github.event.inputs.cv_file }}"
      echo "💡 Available files:"
      ls -lh data/
      exit 1
    fi
    
    if [ ! -s "${{ github.event.inputs.cv_file }}" ]; then
      echo "❌ Error: CV file is empty: ${{ github.event.inputs.cv_file }}"
      exit 1
    fi
    
    # Check if job file exists and is not empty
    if [ ! -f "${{ github.event.inputs.job_file }}" ]; then
      echo "❌ Error: Job file not found: ${{ github.event.inputs.job_file }}"
      exit 1
    fi
    
    if [ ! -s "${{ github.event.inputs.job_file }}" ]; then
      echo "❌ Error: Job file is empty: ${{ github.event.inputs.job_file }}"
      exit 1
    fi
    
    echo "✅ Files verified:"
    ls -lh "${{ github.event.inputs.cv_file }}"
    ls -lh "${{ github.event.inputs.job_file }}"
```

---

## 🐛 Enhanced Error Handling in Python

Update your `python_advanced_job_engine.py`:

```python
def _read_pdf(self, path: Path) -> str:
    """Read text from PDF file with better error handling"""
    try:
        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {path}")
        
        # Check if file is empty
        if path.stat().st_size == 0:
            raise Exception(f"PDF file is empty (0 bytes): {path}")
        
        # Check minimum size (PDFs have headers ~50 bytes minimum)
        if path.stat().st_size < 50:
            raise Exception(f"PDF file too small ({path.stat().st_size} bytes), likely corrupted: {path}")
        
        with open(path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            
            if len(pdf_reader.pages) == 0:
                raise Exception(f"PDF has no pages: {path}")
            
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text += page.extract_text()
                except Exception as e:
                    print(f"⚠️  Warning: Could not read page {page_num+1}: {e}")
            
            if not text.strip():
                raise Exception(f"PDF contains no extractable text: {path}")
            
            return text
            
    except PyPDF2.errors.EmptyFileError:
        raise Exception(f"PDF file is empty or corrupted: {path}")
    except Exception as e:
        raise Exception(f"Error reading PDF {path}: {str(e)}")
```

---

## 📋 Quick Test Script

Create `test_files.py`:

```python
#!/usr/bin/env python3
"""Test that data files are readable"""

import sys
from pathlib import Path
from src.python_advanced_job_engine import AdvancedJobEngine

def test_files():
    engine = AdvancedJobEngine()
    
    test_files = [
        "data/my_cv.pdf",
        "data/my_cv.txt",
        "data/my_cv.docx",
        "data/target_job.pdf",
        "data/target_job.txt",
        "data/target_job.docx"
    ]
    
    found_cv = False
    found_job = False
    
    print("🔍 Checking data files...\n")
    
    for filepath in test_files:
        path = Path(filepath)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {filepath} ({size:,} bytes)")
            
            try:
                text = engine.read_document(filepath)
                words = len(text.split())
                print(f"   → {words} words extracted")
                print(f"   → Preview: {text[:100]}...\n")
                
                if 'cv' in filepath.lower():
                    found_cv = True
                if 'job' in filepath.lower() or 'target' in filepath.lower():
                    found_job = True
                    
            except Exception as e:
                print(f"   ❌ Error reading: {e}\n")
        else:
            print(f"⏭️  {filepath} (not found)")
    
    print("\n" + "="*50)
    if found_cv and found_job:
        print("✅ Ready to run analysis!")
        return 0
    else:
        if not found_cv:
            print("❌ No readable CV file found")
        if not found_job:
            print("❌ No readable job description found")
        print("\n💡 Add files to data/ directory")
        return 1

if __name__ == "__main__":
    sys.exit(test_files())
```

Run it:

```bash
python3 test_files.py
```

---

## 🚀 Complete Setup Commands

```bash
# 1. Ensure you're in your repo
cd advanced-job-engine

# 2. Create sample files
cat > data/my_cv.txt << 'EOF'
[Your CV content here - at least 100 words]
EOF

cat > data/target_job.txt << 'EOF'
[Job description here - at least 100 words]
EOF

# 3. Test locally first
python3 -c "
from src.python_advanced_job_engine import AdvancedJobEngine
engine = AdvancedJobEngine()
cv = engine.read_document('data/my_cv.txt')
job = engine.read_document('data/target_job.txt')
print(f'CV: {len(cv.split())} words')
print(f'Job: {len(job.split())} words')
print('✅ Files are readable!')
"

# 4. Commit and push
git add data/
git commit -m "Add CV and job description files"
git push

# 5. Trigger workflow
gh workflow run auto-job-analysis.yml \
  -f cv_file=data/my_cv.txt \
  -f job_file=data/target_job.txt
```

---

## ⚠️ Common Issues

### Issue: "File not found"
**Fix:** Check exact path
```bash
git ls-files data/
```

### Issue: "Cannot extract text from PDF"
**Fix:** PDF might be image-based. Convert to text:
- Use https://www.adobe.com/acrobat/online/pdf-to-word.html
- Or use OCR tools

### Issue: "Permission denied"
**Fix:** Check file permissions
```bash
chmod 644 data/*.pdf
```

---

## ✅ Verification Checklist

Before running workflow:

- [ ] Files exist in `data/` directory
- [ ] Files are not empty (size > 0)
- [ ] Files are committed to git
- [ ] Files are readable by PyPDF2/python-docx
- [ ] Content makes sense (not corrupted)
- [ ] File paths in workflow match actual files

---

## 🎯 Next Steps

Once files are properly set up:

1. **Test locally first** (saves GitHub Actions minutes)
2. **Push to GitHub**
3. **Run workflow manually** with correct file paths
4. **Check output** for match score
5. **Iterate** based on results