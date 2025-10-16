This comprehensive mock data file provides:

Complete CV sample - Both text and parsed formats
Job description samples - Text and structured data
Match analysis results - Scores, gaps, recommendations
Learning plans - Multi-level learning structure
Sprint data - Active and completed sprint examples
Skill tests - Multiple question types
Workflow state - Progress tracking data
Application materials - Cover letters and messages
Resource database - Learning resource metadata
Utility functions - Helper functions to get/customize mock data

Use it in your tests like:
pythonfrom tests.mocks.mock_data import MOCK_CV_PARSED, get_mock_job

# In test
def test_something():
    cv = MOCK_CV_PARSED
    job = get_mock_job(format='parsed')
    # ... test logic