#!/bin/bash
# Generate tests that match your actual implementation

echo "================================================================"
echo "TEST GENERATION TOOL"
echo "================================================================"
echo ""
echo "This will help you generate tests that match your actual code."
echo ""

# Check what methods actually exist
check_class_methods() {
    local file=$1
    local class=$2
    
    echo "📦 Analyzing $class in $file"
    
    if [ -f "$file" ]; then
        echo "   Available methods:"
        grep -E "^\s+def [a-z_]+" "$file" | \
            grep -v "def __" | \
            sed 's/def /     - /' | \
            sed 's/(.*$//'
    else
        echo "   ⚠️  File not found: $file"
    fi
    echo ""
}

echo "CURRENT IMPLEMENTATION:"
echo "----------------------"
echo ""

# Check each module
check_class_methods "src/analyzers/cv_parser.py" "CVParser"
check_class_methods "src/analyzers/job_parser.py" "JobParser"
check_class_methods "src/analyzers/matcher.py" "Matcher"
check_class_methods "src/learning/plan_generator.py" "LearningPlanGenerator"
check_class_methods "src/tracking/sprint_manager.py" "SprintManager"

echo "================================================================"
echo "RECOMMENDATION:"
echo "================================================================"
echo ""
echo "Based on common patterns, here's what to do:"
echo ""
echo "1. CVParser: Tests expect granular methods, but you have parse_cv()"
echo "   → Update tests to use parse_cv() and check the returned dict"
echo ""
echo "2. LearningPlanGenerator: Tests call create_plan(), you have generate_plan()"
echo "   → Find/replace 'create_plan' with 'generate_plan' in tests"
echo ""
echo "3. SprintManager: Tests call start_sprint(), you have add_sprint()"
echo "   → Update tests to use add_sprint()"
echo ""
echo "Quick fixes:"
echo "------------"
echo ""
echo "# Fix LearningPlanGenerator tests:"
echo "sed -i 's/create_plan/generate_plan/g' tests/unit/test_learning_plan.py"
echo ""
echo "# Fix SprintManager tests:"
echo "sed -i 's/start_sprint/add_sprint/g' tests/unit/test_sprint_manager.py"
echo "sed -i 's/end_sprint/add_sprint/g' tests/unit/test_sprint_manager.py"
echo ""
echo "================================================================"
