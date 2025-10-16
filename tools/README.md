All three tool files are now complete! Here's a quick summary of what each does:

generate_docs.py - Automatically generates documentation from your source code, including API references, module overviews, configuration guides, and usage examples.
update_resources.py - Manages your learning resources database, allows adding/updating resources, validates links, and can export resources to markdown format.
validate_data.py - Validates all your data files (CVs, job descriptions, JSON files, outputs) to ensure they have the correct format and required content.

You can run them like this:
bash# Generate documentation
python tools/generate_docs.py

# Add a learning resource
python tools/update_resources.py add --skill GraphQL --title "GraphQL Tutorial" --url "https://example.com" --type tutorial --difficulty beginner

# Validate data files
python tools/validate_data.py job_search_data/RetryClaude does not have the ability to run the code it generates yet.Claude can make mistakes. Please double-check responses. Sonnet 4.5