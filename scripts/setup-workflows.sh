
## 5. Quick Start Script: `scripts/setup-workflows.sh`
```bash
#!/bin/bash

# Quick Setup Script for GitHub Actions Workflows
# Run this locally to verify setup before pushing to GitHub

echo "🚀 Advanced Job Engine - Workflow Setup"
echo "========================================"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    echo "Please run: git init"
    exit 1
fi

echo "✅ Git repository detected"

# Create directory structure
echo ""
echo "📁 Creating directory structure..."

mkdir -p .github/workflows
mkdir -p data
mkdir -p output
mkdir -p batch_results
mkdir -p progress_tracking
mkdir -p src

echo "✅ Directories created"

# Check for workflow files
echo ""
echo "📄 Checking workflow files..."

workflows=(
    ".github/workflows/auto-job-analysis.yml"
    ".github/workflows/scheduled-analysis.yml"
    ".github/workflows/batch-analysis.yml"
)

missing_workflows=0

for workflow in "${workflows[@]}"; do
    if [ -f "$workflow" ]; then
        echo "✅ Found: $workflow"
    else
        echo "❌ Missing: $workflow"
        missing_workflows=$((missing_workflows + 1))
    fi
done

if [ $missing_workflows -gt 0 ]; then
    echo ""
    echo "⚠️  Warning: $missing_workflows workflow file(s) missing"
    echo "Please create the missing workflow files"
fi

# Check for required Python files
echo ""
echo "🐍 Checking Python files..."

if [ -f "requirements.txt" ]; then
    echo "✅ Found: requirements.txt"
else
    echo "❌ Missing: requirements.txt"
    echo "Creating basic requirements.txt..."
    cat > requirements.txt << 'EOL'
PyPDF2>=3.0.0
pdfplumber>=0.9.0
python-docx>=0.8.11
requests>=2.31.0
python-dotenv>=1.0.0
EOL
    echo "✅ Created: requirements.txt"
fi

if [ -d "src" ]; then
    if [ -f "src/python_advanced_job_engine.py" ]; then
        echo "✅ Found: src/python_advanced_job_engine.py"
    else
        echo "❌ Missing: src/python_advanced_job_engine.py"
        echo "⚠️  This is required for workflows to run"
    fi
else
    echo "❌ Missing: src/ directory"
fi

# Check for data files
echo ""
echo "📂 Checking data directory..."

if [ -d "data" ]; then
    file_count=$(ls -1 data/ 2>/dev/null | wc -l)
    if [ $file_count -eq 0 ]; then
        echo "⚠️  data/ directory is empty"
        echo "Please upload your CV and job descriptions to data/"
    else
        echo "✅ Found $file_count file(s) in data/"
        ls -1 data/
    fi
else
    echo "❌ Missing: data/ directory"
fi

# Check GitHub configuration
echo ""
echo "🔧 Checking GitHub configuration..."

if git remote get-url origin > /dev/null 2>&1; then
    remote_url=$(git remote get-url origin)
    echo "✅ Git remote configured: $remote_url"
else
    echo "⚠️  No git remote configured"
    echo "After creating GitHub repo, run:"
    echo "  git remote add origin https://github.com/USERNAME/REPO.git"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo ""
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Sensitive
secrets/
*.env
.env.local

# OS
.DS_Store
Thumbs.db

# Output
output/temp/
*.tmp
*.log

# IDE
.vscode/
.idea/
*.swp
EOL
    echo "✅ Created: .gitignore"
fi

# Summary
echo ""
echo "========================================"
echo "📊 Setup Summary"
echo "========================================"
echo ""

if [ $missing_workflows -eq 0 ]; then
    echo "✅ All workflow files present"
else
    echo "❌ $missing_workflows workflow file(s) missing"
fi

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt present"
else
    echo "❌ requirements.txt missing"
fi

if [ -f "src/python_advanced_job_engine.py" ]; then
    echo "✅ Main Python file present"
else
    echo "❌ Main Python file missing"
fi

echo ""
echo "========================================"
echo "📝 Next Steps"
echo "========================================"
echo ""
echo "1. Upload your files to data/:"
echo "   - data/my_cv.pdf"
echo "   - data/job_description.pdf"
echo ""
echo "2. Commit and push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Setup workflows'"
echo "   git push origin main"
echo ""
echo "3. On GitHub:"
echo "   - Go to Actions tab"
echo "   - Enable workflows"
echo "   - Run 'Auto Job Analysis'"
echo ""
echo "4. Download results from Artifacts"
echo ""
echo "🚀 You're ready to go!"
echo ""
```
