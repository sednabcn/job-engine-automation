"""
Utility modules
"""

from .data_loader import DataLoader.load_json, DataLoader.load_yaml, DataLoader.save_json, DataLoader.backup_json
from .file_readers import FileReader.read_file, FileReader.get_file_info, PDFReader,DOCXReader, TXTReader.read,CVReader,read_cv, JobDescriptionReader.read_job, read_cv, read_job_description,
from .formatters import TextFormatter.format_header, TextFormatter.format_section, TextFormatter.format_list, TextFormatter.format_table, TextFormatter.format_key_value, TextFormatter.format_box, SkillFormatter.format_skill_summary, SkillFormatter.format_skill_gap, MatchFormatter.format_match_score, MatchFormatter.format_match_report, LearningPlanFormatter.format_learning_plan,LearningPlanFormatter.format_learning_progress, SprintFormatter.format_sprint_summary, ReportFormatter.format_complete_report, ReportFormatter.format_executive_summary, JSONFormatter.format_json, JSONFormatter.format_json_compact, MarkdownFormatter.format_header, MarkdownFormatter.format_list, Markdown.format_code_block, MarkdownFormatter.format_table, MarkdownFormatter.format_link, Markdown.format_bold, MarkdownFormatter.format_italic, MarkdownFormatter.format_quote, HTMLFormatter.format_header, HTMLFormatter.format_paragraph, HTTMLFormatter.format_list, HTMMLFormatter.format_table, format_percentage, format_number, format_currency, format_file_size, format_duration, format_score_color, reset_color, format_progress_bar
from .helpers import clean_text, sanitize_inout, extract_keywords, normalize_skill_name, extract_years_experience, calculate_skill_score, fuzy_match_skills, levenstein_distance, parse_date, format_date, calculate_duration, time_ago, generate_id, merge_dicts, flatten_dict, get_nested_value, set_nested_value, chunk_list, ensure_directory, safe_filename, extract_email, extract_phone, extract_urls, truncate_text, pluralize
from .validators import ComfigValidator.validate_email, ConfigValidator.validate_phone, ConfigValidator.validate_url

__all__ = [
    "read_pdf",
    "read_docx",
    "read_txt",
    "load_json",
    "load_yaml",
    "validate_email",
    "validate_phone",
    "format_text",
    "format_table",
    "send_email",
    "merge_dicts",
]
