"""
Skill Gap Analysis Demo
----------------------
Demonstrates parsing a CV and a Job Description,
computing matched skills and identifying gaps.
"""

from src.analyzers import cv_parser, gap_analyzer
from src.utils import file_readers

def main():
    # Load sample CV and job description
    cv_text = file_readers.read_text_file("tests/fixtures/sample_cv.txt")
    job_text = file_readers.read_text_file("tests/fixtures/sample_job.txt")

    # Parse CV
    parser = cv_parser.CVParser()
    cv_data = parser.parse(cv_text)

    # Analyze skill gaps
    gap_results = gap_analyzer.analyze(cv_data, job_text)

    # Print results
    print("Candidate Name:", cv_data.get("name"))
    print("CV Skills:", cv_data.get("skills"))
    print("Matched Skills:", gap_results.get("matched_keywords"))
    print("Missing Skills:", gap_results.get("missing_keywords"))
    print("Match Score:", gap_results.get("score"), "%")

if __name__ == "__main__":
    main()
