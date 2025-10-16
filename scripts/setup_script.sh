#!/bin/bash

# 🚀 Job Engine Automation - Complete Setup Script
# This script sets up your entire repository structure

set -e  # Exit on error

echo "=========================================="
echo "🚀 Job Engine Automation Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in a git repository
if [ ! -d .git ]; then
    print_error "Not a git repository. Run 'git init' first!"
    exit 1
fi

print_info "Creating directory structure..."

# Create main directories
mkdir -p .github/workflows
mkdir -p .github/scripts
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p src/{analyzers,learning,tracking,generators,utils}
mkdir -p data
mkdir -p job_search_data/exports
mkdir -p templates/letter_templates
mkdir -p docs/{tutorials,examples,images}
mkdir -p tests/{unit,integration,fixtures,mocks}
mkdir -p scripts
mkdir -p examples
mkdir -p benchmarks/results
mkdir -p tools

print_success "Directory structure created!"

# Create .gitkeep files for empty directories
find . -type d -empty -exec touch {}/.gitkeep \;

print_info "Creating .gitignore..."

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Data files (IMPORTANT: Keep your personal data private!)
data/*.pdf
data/*.docx
data/*.txt
data/*.json
!data/.gitkeep

# Generated data
job_search_data/
!job_search_data/.gitkeep

# Environment variables
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Test coverage
.coverage
htmlcov/
.pytest_cache/

# Temporary files
*.tmp
temp/
EOF

print_success ".gitignore created!"

print_info "Creating environment template..."

cat > .env.example << 'EOF'
# Job Engine Configuration

# API Keys (if needed for future features)
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here

# Email notifications (optional)
EMAIL_NOTIFICATIONS=false
EMAIL_ADDRESS=your_email@example.com

# GitHub Actions settings
GITHUB_TOKEN=${GITHUB_TOKEN}

# Analysis settings
DEFAULT_CV_PATH=data/my_cv.pdf
DEFAULT_JOB_PATH=data/target_job.pdf
MIN_MATCH_SCORE=70

# Learning plan settings
LEARNING_PLAN_WEEKS=12
HOURS_PER_WEEK=10

# Sprint settings
SPRINT_DURATION_DAYS=14
EOF

print_success ".env.example created!"

print_info "Creating README.md..."

cat > README.md << 'EOF'
# 🚀 Advanced Job Engine Automation

An intelligent system that analyzes your CV against job descriptions, identifies skill gaps, creates learning plans, and automates your job search workflow using GitHub Actions.

## ✨ Features

- 📊 **CV Analysis**: Parse and analyze your skills
- 🎯 **Job Matching**: Score how well you match job requirements
- 📚 **Learning Plans**: Generate personalized learning paths
- 🔄 **Reverse Job Search**: Find jobs that match YOUR skills
- 📦 **Batch Analysis**: Analyze multiple jobs at once
- ⏰ **Automation**: Scheduled weekly job searches
- 📝 **Content Generation**: Cover letters, LinkedIn messages, etc.

## 🚀 Quick Start (Easiest Way for Users)

### 1. Fork this repository
Click the "Fork" button at the top right

### 2. Add your CV
1. Go to your forked repo
2. Navigate to `data/` folder
3. Click "Add file" > "Upload files"
4. Upload your CV (PDF format recommended)
5. Name it `my_cv.pdf`

### 3. Run Analysis
1. Click "Actions" tab
2. Select "Workflow Manager Dashboard"
3. Click "Run workflow"
4. Choose "Run Job Analysis"
5. Click green "Run workflow" button

### 4. Get Results
- Results appear in Actions run logs
- Download artifacts for detailed reports

## 📖 Documentation

See `docs/` folder for:
- [Getting Started Guide](docs/getting-started.md)
- [User Guide](docs/user-guide.md)
- [Workflow Guide](docs/workflow-guide.md)
- [FAQ](docs/faq.md)

## 🛠️ Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/job-engine-automation.git
cd job-engine-automation

# Run setup script
chmod +x scripts/setup_local.sh
./scripts/setup_local.sh

# Activate virtual environment
source venv/bin/activate

# Run analysis locally
python src/python_advanced_job_engine.py --cv data/my_cv.pdf --job data/target_job.pdf
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License - See [LICENSE](LICENSE)

## 🆘 Support

- [Documentation](docs/)
- [Issues](https://github.com/yourusername/job-engine-automation/issues)
- [Discussions](https://github.com/yourusername/job-engine-automation/discussions)
EOF

print_success "README.md created!"

print_info "Creating requirements.txt..."

cat > requirements.txt << 'EOF'
# Core dependencies
PyPDF2>=3.0.0
python-docx>=1.1.0
pandas>=2.1.0
numpy>=1.24.0
requests>=2.31.0

# Text processing
nltk>=3.8.0
spacy>=3.7.0

# Data handling
pyyaml>=6.0
python-dotenv>=1.0.0

# Testing (optional for local dev)
pytest>=7.4.0
pytest-cov>=4.1.0

# Code quality (optional for local dev)
black>=23.0.0
flake8>=6.1.0
mypy>=1.5.0
EOF

print_success "requirements.txt created!"

print_info "Creating local setup script..."

cat > scripts/setup_local.sh << 'EOF'
#!/bin/bash

echo "Setting up local development environment..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create .env from template
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your settings."
fi

echo "✅ Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
EOF

chmod +x scripts/setup_local.sh

print_success "Local setup script created!"

print_info "Creating workflow manager..."

# The workflow manager was already created in the artifact above
# Just create a note about it

cat > .github/workflows/README.md << 'EOF'
# GitHub Workflows

## 🎯 For Users: Use the Workflow Manager!

**Easiest way**: Use `workflow-manager.yml`
- Go to Actions tab
- Select "Workflow Manager Dashboard"  
- Choose what you want to do
- Click "Run workflow"

## Available Workflows

1. **workflow-manager.yml** ⭐ START HERE
   - Central control panel for all workflows
   - Easiest way to run any analysis

2. **autojob-analysis.yml**
   - Analyze a single job posting
   - Triggered: Manual or when you upload to data/

3. **unified-reverse-job-engine.yml**
   - Find jobs matching YOUR skills
   - Triggered: Manual

4. **batch-analysis.yml**
   - Analyze multiple jobs at once
   - Triggered: Manual

5. **scheduled-analysis.yml**
   - Automatic weekly job search
   - Triggered: Every Monday at 9 AM

6. **ci-tests.yml**
   - Run automated tests
   - Triggered: On push/PR

7. **deploy-docs.yml**
   - Deploy documentation
   - Triggered: On push to main

8. **lint-and-format.yml**
   - Code quality checks
   - Triggered: On push/PR

9. **release.yml**
   - Create releases
   - Triggered: On tag push

## Quick Commands

```bash
# List all workflows
gh workflow list

# Run a specific workflow
gh workflow run workflow-manager.yml

# View workflow runs
gh run list

# View logs of latest run
gh run view --log
```
EOF

print_success "Workflow documentation created!"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
print_info "Next Steps:"
echo ""
echo "1. 📝 Add your CV to data/ folder:"
echo "   cp /path/to/your/cv.pdf data/my_cv.pdf"
echo ""
echo "2. 🚀 Push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Initial setup'"
echo "   git push origin main"
echo ""
echo "3. 🎯 Run your first analysis:"
echo "   • Go to GitHub repo > Actions tab"
echo "   • Select 'Workflow Manager Dashboard'"
echo "   • Click 'Run workflow'"
echo "   • Choose 'Run Job Analysis'"
echo ""
echo "4. 📦 For local development:"
echo "   ./scripts/setup_local.sh"
echo "   source venv/bin/activate"
echo ""
print_warning "Remember to keep data/ folder private (it's in .gitignore)"
echo ""
echo "=========================================="
echo "📚 Documentation: Check docs/ folder"
echo "🆘 Issues: Use GitHub Issues"
echo "💬 Questions: Use GitHub Discussions"
echo "=========================================="
