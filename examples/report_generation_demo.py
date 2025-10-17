"""
Report Generation Demo
---------------------
Shows how to generate reports, letters, and templates
based on analyzed CV and job data.
"""

from src.generators import report_generator, letter_generator, template_engine
from src.utils import file_readers

def main():
    # Load sample analysis JSON (mock results)
    analysis_data = file_readers.read_json_file("tests/fixtures/sample_data.json")

    # Generate report
    report = report_generator.ReportGenerator(analysis_data)
    report_content = report.generate_report()
    print("\n--- Generated Report ---\n", report_content)

    # Generate cover letter
    letter = letter_generator.LetterGenerator(
        candidate_name=analysis_data.get("name", "Candidate"),
        job_title=analysis_data.get("job_title", "Position")
    )
    cover_letter = letter.generate_letter()
    print("\n--- Cover Letter ---\n", cover_letter)

    # Use template engine to render any template
    template = "Hello {{ name }}, your score is {{ score }}%"
    rendered = template_engine.render_template(template, analysis_data)
    print("\n--- Rendered Template ---\n", rendered)

if __name__ == "__main__":
    main()
