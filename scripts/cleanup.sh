# 1. Remove all "auto-added placeholder" lines
find . -type f -name "*.py" -exec sed -i '/# auto-added placeholder/d' {} +

# 2. Run autopep8 or black to reindent and fix syntax structure
autopep8 --in-place --aggressive --aggressive $(find . -type f -name "*.py")

# or if you prefer black (after cleanup)
black .
