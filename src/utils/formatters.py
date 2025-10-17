"""
Formatters Module
Output formatting functions for reports, displays, and exports.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

_logger = logging.getLogger(__name__)


class TextFormatter:
    """Formatter for text-based outputs."""

    @staticmethod
    def format_header(text: str, level: int = 1, width: int = 80) -> str:
        """
        Format a text header.

        Args:
            text: Header text
            level: Header level (1-3)
            width: Total width

        Returns:
            Formatted header string
        """
        chars = {1: "=", 2: "-", 3: "."}
        char = chars.get(level, "-")

        if level == 1:
            return f"\n{char * width}\n{text.upper().center(width)}\n{char * width}\n"
        elif level == 2:
            return f"\n{text.upper()}\n{char * len(text)}\n"
        else:
            return f"\n{text}\n{char * len(text)}\n"

    @staticmethod
    def format_section(title: str, content: str, indent: int = 0) -> str:
        """
        Format a section with title and content.

        Args:
            title: Section title
            content: Section content
            indent: Indentation level

        Returns:
            Formatted section string
        """
        indent_str = "  " * indent
        return f"{indent_str}{title}:\n{indent_str}{content}\n"

    @staticmethod
    def format_list(items: List[str], bullet: str = "•", indent: int = 0) -> str:
        """
        Format a bulleted list.

        Args:
            items: List items
            bullet: Bullet character
            indent: Indentation level

        Returns:
            Formatted list string
        """
        indent_str = "  " * indent
        return "\n".join([f"{indent_str}{bullet} {item}" for item in items])

    @staticmethod
    def format_numbered_list(items: List[str], indent: int = 0) -> str:
        """
        Format a numbered list.

        Args:
            items: List items
            indent: Indentation level

        Returns:
            Formatted numbered list string
        """
        indent_str = "  " * indent
        return "\n".join([f"{indent_str}{i + 1}. {item}" for i, item in enumerate(items)])

    @staticmethod
    def format_table(
        headers: List[str], rows: List[List[Any]], col_widths: Optional[List[int]] = None
    ) -> str:
        """
        Format a simple ASCII table.

        Args:
            headers: Column headers
            rows: Table rows
            col_widths: Column widths (auto-calculated if None)

        Returns:
            Formatted table string
        """
        if not col_widths:
            col_widths = [
                max(len(str(h)), max(len(str(row[i])) for row in rows) if rows else 0)
                for i, h in enumerate(headers)
            ]

        # Format header
        header_row = " | ".join(str(h).ljust(w) for h, w in zip(headers, col_widths))
        separator = "-+-".join("-" * w for w in col_widths)

        # Format rows
        data_rows = [
            " | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)) for row in rows
        ]

        return f"{header_row}\n{separator}\n" + "\n".join(data_rows)

    @staticmethod
    def format_key_value(data: Dict[str, Any], indent: int = 0, separator: str = ": ") -> str:
        """
        Format key-value pairs.

        Args:
            data: Dictionary of key-value pairs
            indent: Indentation level
            separator: Separator between key and value

        Returns:
            Formatted key-value string
        """
        indent_str = "  " * indent
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{indent_str}{key}:")
                lines.append(TextFormatter.format_key_value(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{indent_str}{key}:")
                lines.append(TextFormatter.format_list([str(v) for v in value], indent=indent + 1))
            else:
                lines.append(f"{indent_str}{key}{separator}{value}")
        return "\n".join(lines)

    @staticmethod
    def format_box(text: str, width: int = 60, padding: int = 1) -> str:
        """
        Format text in a box.

        Args:
            text: Text to box
            width: Box width
            padding: Internal padding

        Returns:
            Boxed text string
        """
        lines = text.split("\n")
        padded_lines = [
            f"│{' ' * padding}{line.ljust(width - 2 * padding - 2)}{' ' * padding}│"
            for line in lines
        ]

        top = f"┌{'─' * (width - 2)}┐"
        bottom = f"└{'─' * (width - 2)}┘"

        return f"{top}\n" + "\n".join(padded_lines) + f"\n{bottom}"


class SkillFormatter:
    """Formatter for skill-related outputs."""

    @staticmethod
    def format_skill_summary(skills: Dict[str, Any]) -> str:
        """
        Format skill summary.

        Args:
            skills: Dictionary of skills

        Returns:
            Formatted skill summary
        """
        output = TextFormatter.format_header("SKILL SUMMARY", level=1)

        if not skills:
            return output + "No skills found.\n"

        # Group by level
        by_level: Dict[str, List[Dict[str, Any]]] = {}
        for skill_name, skill_data in skills.items():
            level = skill_data.get("level", "unknown")
            if level not in by_level:
                by_level[level] = []
            by_level[level].append(
                {
                    "name": skill_name,
                    "years": skill_data.get("years_experience", 0),
                    "score": skill_data.get("score", 0),
                }
            )

        # Format each level
        for level in ["expert", "advanced", "intermediate", "beginner"]:
            if level in by_level:
                output += TextFormatter.format_header(f"{level.upper()} SKILLS", level=2)
                for skill in sorted(by_level[level], key=lambda x: x["score"], reverse=True):
                    output += f"  • {skill['name']} ({skill['years']} years) - Score: {skill['score']:.1f}%\n"

        return output

    @staticmethod
    def format_skill_gap(gap_analysis: Dict[str, Any]) -> str:
        """
        Format skill gap analysis.

        Args:
            gap_analysis: Gap analysis data

        Returns:
            Formatted gap analysis
        """
        output = TextFormatter.format_header("SKILL GAP ANALYSIS", level=1)

        # Missing skills
        if gap_analysis.get("missing_skills"):
            output += TextFormatter.format_header("MISSING SKILLS", level=2)
            output += TextFormatter.format_list(gap_analysis["missing_skills"])
            output += "\n"

        # Weak skills
        if gap_analysis.get("weak_skills"):
            output += TextFormatter.format_header("SKILLS TO IMPROVE", level=2)
            for skill in gap_analysis["weak_skills"]:
                output += f"  • {skill['name']} (Current: {skill['current_level']} → Target: {skill['target_level']})\n"
            output += "\n"

        # Strong skills
        if gap_analysis.get("strong_skills"):
            output += TextFormatter.format_header("STRONG MATCHING SKILLS", level=2)
            output += TextFormatter.format_list(gap_analysis["strong_skills"])
            output += "\n"

        return output


class MatchFormatter:
    """Formatter for match score outputs."""

    @staticmethod
    def format_match_score(match_data: Dict[str, Any]) -> str:
        """
        Format match score display.

        Args:
            match_data: Match analysis data

        Returns:
            Formatted match score
        """
        score = match_data.get("overall_score", 0)

        output = TextFormatter.format_header("MATCH ANALYSIS", level=1)

        # Overall score with visual bar
        bar_length = 50
        filled = int(score / 100 * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)

        output += f"\nOverall Match Score: {score:.1f}%\n"
        output += f"[{bar}]\n\n"

        # Score interpretation
        if score >= 80:
            interpretation = "Excellent Match"
        elif score >= 60:
            interpretation = "Good Match"
        elif score >= 40:
            interpretation = "Fair Match"
        else:
            interpretation = "Poor Match"

        output += f"Assessment: {interpretation}\n\n"

        # Detailed breakdown
        if "breakdown" in match_data:
            output += TextFormatter.format_header("SCORE BREAKDOWN", level=2)
            for category, score in match_data["breakdown"].items():
                output += f"  {category.replace('_', ' ').title()}: {score:.1f}%\n"

        return output

    @staticmethod
    def format_match_report(job_title: str, company: str, match_data: Dict[str, Any]) -> str:
        """
        Format complete match report.

        Args:
            job_title: Job title
            company: Company name
            match_data: Match analysis data

        Returns:
            Formatted match report
        """
        output = TextFormatter.format_header("JOB MATCH REPORT", level=1)

        output += f"Position: {job_title}\n"
        output += f"Company: {company}\n"
        output += f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        output += MatchFormatter.format_match_score(match_data)

        return output


class LearningPlanFormatter:
    """Formatter for learning plan outputs."""

    @staticmethod
    def format_learning_plan(plan: Dict[str, Any]) -> str:
        """
        Format learning plan.

        Args:
            plan: Learning plan data

        Returns:
            Formatted learning plan
        """
        output = TextFormatter.format_header("LEARNING PLAN", level=1)

        output += f"Plan: {plan.get('title', 'Untitled')}\n"
        output += f"Total Estimated Time: {plan.get('total_hours', 0)} hours\n"
        output += f"Target Completion: {plan.get('target_date', 'Not set')}\n\n"

        # Group items by priority
        items = plan.get("items", [])
        by_priority: Dict[str, List[Dict[str, Any]]] = {"high": [], "medium": [], "low": []}

        for item in items:
            priority = item.get("priority", "medium")
            by_priority[priority].append(item)

        # Format each priority group
        for priority in ["high", "medium", "low"]:
            if by_priority[priority]:
                output += TextFormatter.format_header(f"{priority.upper()} PRIORITY ITEMS", level=2)
                for i, item in enumerate(by_priority[priority], 1):
                    output += f"\n{i}. {item['title']}\n"
                    output += f"   Type: {item.get('type', 'N/A')}\n"
                    output += f"   Time: {item.get('estimated_hours', 0)} hours\n"
                    if item.get("resources"):
                        output += "   Resources:\n"
                        for resource in item["resources"]:
                            output += f"     - {resource}\n"

        return output

    @staticmethod
    def format_learning_progress(progress: Dict[str, Any]) -> str:
        """
        Format learning progress.

        Args:
            progress: Progress data

        Returns:
            Formatted progress report
        """
        output = TextFormatter.format_header("LEARNING PROGRESS", level=1)

        total = progress.get("total_items", 0)
        completed = progress.get("completed_items", 0)
        percentage = (completed / total * 100) if total > 0 else 0

        output += f"Progress: {completed}/{total} items ({percentage:.1f}%)\n"
        output += f"Hours Logged: {progress.get('hours_logged', 0)}\n"
        output += f"Last Updated: {progress.get('last_updated', 'N/A')}\n\n"

        # Recently completed
        if progress.get("recent_completions"):
            output += TextFormatter.format_header("RECENTLY COMPLETED", level=2)
            for item in progress["recent_completions"][:5]:
                output += f"  ✓ {item['title']} - {item['completed_date']}\n"

        return output


class SprintFormatter:
    """Formatter for sprint outputs."""

    @staticmethod
    def format_sprint_plan(sprint: Dict[str, Any]) -> str:
        """
        Format sprint plan.

        Args:
            sprint: Sprint data

        Returns:
            Formatted sprint plan
        """
        output = TextFormatter.format_header("SPRINT PLAN", level=1)

        output += f"Sprint: {sprint.get('title', 'Untitled')}\n"
        output += f"Duration: {sprint.get('duration', 0)} days\n"
        output += f"Start Date: {sprint.get('start_date', 'Not set')}\n"
        output += f"End Date: {sprint.get('end_date', 'Not set')}\n\n"

        # Goals
        if sprint.get("goals"):
            output += TextFormatter.format_header("SPRINT GOALS", level=2)
            output += TextFormatter.format_numbered_list(sprint["goals"])
            output += "\n\n"

        # Tasks
        if sprint.get("tasks"):
            output += TextFormatter.format_header("TASKS", level=2)
            for task in sprint["tasks"]:
                status = task.get("status", "pending")
                symbol = "✓" if status == "completed" else "○"
                output += f"  {symbol} {task['title']} ({status})\n"

        return output

    @staticmethod
    def format_sprint_summary(sprint_history: List[Dict[str, Any]]) -> str:
        """
        Format sprint history summary.

        Args:
            sprint_history: List of sprint records

        Returns:
            Formatted sprint summary
        """
        output = TextFormatter.format_header("SPRINT HISTORY", level=1)

        if not sprint_history:
            return output + "No sprints completed yet.\n"

        total_sprints = len(sprint_history)
        completed_tasks = sum(s.get("completed_tasks", 0) for s in sprint_history)
        total_tasks = sum(s.get("total_tasks", 0) for s in sprint_history)

        output += f"Total Sprints: {total_sprints}\n"
        output += f"Tasks Completed: {completed_tasks}/{total_tasks}\n"
        output += f"Completion Rate: {(completed_tasks / total_tasks * 100):.1f}%\n\n"

        # Recent sprints
        output += TextFormatter.format_header("RECENT SPRINTS", level=2)
        for sprint in sprint_history[-5:]:
            output += f"\n{sprint['title']}\n"
            output += f"  Period: {sprint['start_date']} to {sprint['end_date']}\n"
            output += f"  Completed: {sprint['completed_tasks']}/{sprint['total_tasks']} tasks\n"

        return output


class ReportFormatter:
    """Formatter for complete reports."""

    @staticmethod
    def format_complete_report(data: Dict[str, Any]) -> str:
        """
        Format complete analysis report.

        Args:
            data: All analysis data

        Returns:
            Formatted complete report
        """
        output = TextFormatter.format_header("COMPLETE JOB APPLICATION ANALYSIS", level=1)

        output += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Match analysis
        if "match_analysis" in data:
            output += MatchFormatter.format_match_score(data["match_analysis"])
            output += "\n"

        # Skill gaps
        if "gap_analysis" in data:
            output += SkillFormatter.format_skill_gap(data["gap_analysis"])
            output += "\n"

        # Learning plan
        if "learning_plan" in data:
            output += LearningPlanFormatter.format_learning_plan(data["learning_plan"])
            output += "\n"

        # Sprint plan
        if "sprint_plan" in data:
            output += SprintFormatter.format_sprint_plan(data["sprint_plan"])

        return output

    @staticmethod
    def format_executive_summary(data: Dict[str, Any]) -> str:
        """
        Format executive summary.

        Args:
            data: Analysis data

        Returns:
            Formatted executive summary
        """
        output = TextFormatter.format_header("EXECUTIVE SUMMARY", level=1)

        # Key metrics
        match_score = data.get("match_analysis", {}).get("overall_score", 0)
        missing_skills = len(data.get("gap_analysis", {}).get("missing_skills", []))
        weak_skills = len(data.get("gap_analysis", {}).get("weak_skills", []))
        learning_hours = data.get("learning_plan", {}).get("total_hours", 0)

        output += "KEY METRICS\n"
        output += f"  Match Score: {match_score:.1f}%\n"
        output += f"  Skills to Acquire: {missing_skills}\n"
        output += f"  Skills to Improve: {weak_skills}\n"
        output += f"  Estimated Learning Time: {learning_hours} hours\n\n"

        # Recommendation
        output += "RECOMMENDATION\n"
        if match_score >= 80:
            output += "  ✓ APPLY NOW - You are highly qualified for this position.\n"
        elif match_score >= 60:
            output += "  ⚠ APPLY WITH CAUTION - Address skill gaps in cover letter.\n"
        elif match_score >= 40:
            output += "  ⏳ DEVELOP SKILLS FIRST - Complete learning plan before applying.\n"
        else:
            output += "  ✗ NOT RECOMMENDED - Significant skill gap present.\n"

        return output


class JSONFormatter:
    """Formatter for JSON outputs."""

    @staticmethod
    def format_json(data: Any, indent: int = 2, ensure_ascii: bool = False) -> str:
        """
        Format data as JSON.

        Args:
            data: Data to format
            indent: Indentation spaces
            ensure_ascii: Ensure ASCII output

        Returns:
            Formatted JSON string
        """
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, default=str)

    @staticmethod
    def format_json_compact(data: Any) -> str:
        """
        Format data as compact JSON.

        Args:
            data: Data to format

        Returns:
            Compact JSON string
        """
        return json.dumps(data, separators=(",", ":"), default=str)


class MarkdownFormatter:
    """Formatter for Markdown outputs."""

    @staticmethod
    def format_header(text: str, level: int = 1) -> str:
        """
        Format Markdown header.

        Args:
            text: Header text
            level: Header level (1-6)

        Returns:
            Markdown header
        """
        return f"{'#' * level} {text}\n\n"

    @staticmethod
    def format_list(items: List[str], ordered: bool = False) -> str:
        """
        Format Markdown list.

        Args:
            items: List items
            ordered: Use ordered list

        Returns:
            Markdown list
        """
        if ordered:
            return "\n".join([f"{i + 1}. {item}" for i, item in enumerate(items)]) + "\n\n"
        else:
            return "\n".join([f"- {item}" for item in items]) + "\n\n"

    @staticmethod
    def format_code_block(code: str, language: str = "") -> str:
        """
        Format Markdown code block.

        Args:
            code: Code content
            language: Programming language

        Returns:
            Markdown code block
        """
        return f"```{language}\n{code}\n```\n\n"

    @staticmethod
    def format_table(headers: List[str], rows: List[List[Any]]) -> str:
        """
        Format Markdown table.

        Args:
            headers: Column headers
            rows: Table rows

        Returns:
            Markdown table
        """
        header_row = "| " + " | ".join(headers) + " |"
        separator = "|" + "|".join(["---" for _ in headers]) + "|"
        data_rows = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]

        return "\n".join([header_row, separator] + data_rows) + "\n\n"

    @staticmethod
    def format_link(text: str, url: str) -> str:
        """
        Format Markdown link.

        Args:
            text: Link text
            url: Link URL

        Returns:
            Markdown link
        """
        return f"[{text}]({url})"

    @staticmethod
    def format_bold(text: str) -> str:
        """Format bold text."""
        return f"**{text}**"

    @staticmethod
    def format_italic(text: str) -> str:
        """Format italic text."""
        return f"*{text}*"

    @staticmethod
    def format_quote(text: str) -> str:
        """Format blockquote."""
        lines = text.split("\n")
        return "\n".join([f"> {line}" for line in lines]) + "\n\n"


class HTMLFormatter:
    """Formatter for HTML outputs."""

    @staticmethod
    def format_header(text: str, level: int = 1) -> str:
        """
        Format HTML header.

        Args:
            text: Header text
            level: Header level (1-6)

        Returns:
            HTML header
        """
        return f"<h{level}>{text}</h{level}>\n"

    @staticmethod
    def format_paragraph(text: str) -> str:
        """
        Format HTML paragraph.

        Args:
            text: Paragraph text

        Returns:
            HTML paragraph
        """
        return f"<p>{text}</p>\n"

    @staticmethod
    def format_list(items: List[str], ordered: bool = False) -> str:
        """
        Format HTML list.

        Args:
            items: List items
            ordered: Use ordered list

        Returns:
            HTML list
        """
        tag = "ol" if ordered else "ul"
        items_html = "\n".join([f"  <li>{item}</li>" for item in items])
        return f"<{tag}>\n{items_html}\n</{tag}>\n"

    @staticmethod
    def format_table(headers: List[str], rows: List[List[Any]]) -> str:
        """
        Format HTML table.

        Args:
            headers: Column headers
            rows: Table rows

        Returns:
            HTML table
        """
        header_row = "  <tr>\n" + "\n".join([f"    <th>{h}</th>" for h in headers]) + "\n  </tr>"
        data_rows = []
        for row in rows:
            row_html = (
                "  <tr>\n" + "\n".join([f"    <td>{cell}</td>" for cell in row]) + "\n  </tr>"
            )
            data_rows.append(row_html)

        return f"<table>\n{header_row}\n" + "\n".join(data_rows) + "\n</table>\n"


# Utility formatting functions


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format percentage value.

    Args:
        value: Percentage value (0-100)
        decimals: Decimal places

    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"


def format_number(value: float, decimals: int = 2, thousands_sep: str = ",") -> str:
    """
    Format number with thousands separator.

    Args:
        value: Number to format
        decimals: Decimal places
        thousands_sep: Thousands separator

    Returns:
        Formatted number string
    """
    if decimals == 0:
        return f"{int(value):,}".replace(",", thousands_sep)
    else:
        return f"{value:,.{decimals}f}".replace(",", thousands_sep)


def format_currency(value: float, currency: str = "$", decimals: int = 2) -> str:
    """
    Format currency value.

    Args:
        value: Currency amount
        currency: Currency symbol
        decimals: Decimal places

    Returns:
        Formatted currency string
    """
    return f"{currency}{format_number(value, decimals)}"


def format_file_size(bytes_size: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        bytes_size: Size in bytes

    Returns:
        Formatted size string
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(bytes_size)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"
    else:
        days = int(seconds / 86400)
        hours = int((seconds % 86400) / 3600)
        return f"{days}d {hours}h"


def format_score_color(score: float, ranges: Optional[Dict[str, tuple]] = None) -> str:
    """
    Get color code for score (for terminal output).

    Args:
        score: Score value (0-100)
        ranges: Custom color ranges

    Returns:
        ANSI color code
    """
    if ranges is None:
        ranges = {"red": (0, 40), "yellow": (40, 70), "green": (70, 100)}

    for color, (min_val, max_val) in ranges.items():
        if min_val <= score < max_val:
            if color == "red":
                return "\033[91m"
            elif color == "yellow":
                return "\033[93m"
            elif color == "green":
                return "\033[92m"

    return "\033[0m"  # Reset


def reset_color() -> str:
    """Get ANSI reset color code."""
    return "\033[0m"


def format_progress_bar(
    current: int, total: int, width: int = 50, fill: str = "█", empty: str = "░"
) -> str:
    """
    Format progress bar.

    Args:
        current: Current progress
        total: Total items
        width: Bar width
        fill: Fill character
        empty: Empty character

    Returns:
        Progress bar string
    """
    if total == 0:
        percentage = 0.0
    else:
        percentage = (current / total) * 100

    filled = int(width * current / total) if total > 0 else 0
    bar = fill * filled + empty * (width - filled)

    return f"[{bar}] {percentage:.1f}% ({current}/{total})"


# Export all formatters
__all__ = [
    "TextFormatter",
    "SkillFormatter",
    "MatchFormatter",
    "LearningPlanFormatter",
    "SprintFormatter",
    "ReportFormatter",
    "JSONFormatter",
    "MarkdownFormatter",
    "HTMLFormatter",
    "format_percentage",
    "format_number",
    "format_currency",
    "format_file_size",
    "format_duration",
    "format_score_color",
    "reset_color",
    "format_progress_bar",
]
