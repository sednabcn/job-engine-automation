"""
Report Generator Module
Generates formatted reports from data with support for multiple output formats.
"""

import json
from datetime import datetime
from typing import Any, Dict, List


class ReportGenerator:
    """
    A class for generating formatted reports from data.
    Supports multiple output formats including text, HTML, and JSON.
    """

    def __init__(self, title: str = "Report", author: str = "System"):
        """
        Initialize the ReportGenerator.

        Args:
            title: The title of the report
            author: The author of the report
        """
        self.title = title
        self.author = author
        self.created_at = datetime.now()
        self.sections: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {}

    def add_section(self, section_title: str, content: Any, section_type: str = "text") -> None:
        """
        Add a section to the report.

        Args:
            section_title: Title of the section
            content: Content of the section (string, dict, list, etc.)
            section_type: Type of section ('text', 'table', 'list', 'data')
        """
        self.sections.append(
            {
                "title": section_title,
                "content": content,
                "type": section_type,
                "added_at": datetime.now(),
            }
        )

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add metadata to the report.

        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value

    def generate_text(self) -> str:
        """
        Generate a plain text version of the report.

        Returns:
            Formatted text report as a string
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"{self.title.upper()}")
        lines.append("=" * 80)
        lines.append(f"Author: {self.author}")
        lines.append(f"Generated: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        if self.metadata:
            lines.append("-" * 80)
            lines.append("METADATA")
            lines.append("-" * 80)
            for key, value in self.metadata.items():
                lines.append(f"{key}: {value}")
            lines.append("")

        for idx, section in enumerate(self.sections, 1):
            lines.append("-" * 80)
            lines.append(f"{idx}. {section['title'].upper()}")
            lines.append("-" * 80)

            if section["type"] == "text":
                lines.append(str(section["content"]))
            elif section["type"] == "list":
                for item in section["content"]:
                    lines.append(f"  • {item}")
            elif section["type"] == "table":
                lines.append(self._format_table(section["content"]))
            elif section["type"] == "data":
                lines.append(json.dumps(section["content"], indent=2))

            lines.append("")

        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)

        return "\n".join(lines)

    def generate_html(self) -> str:
        """
        Generate an HTML version of the report.

        Returns:
            HTML report as a string
        """
        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            f"    <title>{self.title}</title>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; margin: 40px; }",
            "        h1 { color: #333; border-bottom: 3px solid #007bff; }",
            "        h2 { color: #555; border-bottom: 1px solid #ddd; margin-top: 30px; }",
            "        .metadata { background: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; }",
            "        .section { margin: 20px 0; }",
            "        table { border-collapse: collapse; width: 100%; margin: 15px 0; }",
            "        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "        th { background-color: #007bff; color: white; }",
            "        ul { line-height: 1.8; }",
            "        .footer { margin-top: 40px; padding-top: 20px; border-top: 2px solid #ddd; color: #666; }",
            "    </style>",
            "</head>",
            "<body>",
            f"    <h1>{self.title}</h1>",
            f"    <p><strong>Author:</strong> {self.author}</p>",
            f"    <p><strong>Generated:</strong> {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>",
        ]

        if self.metadata:
            html.append("    <div class='metadata'>")
            html.append("        <h3>Metadata</h3>")
            for key, value in self.metadata.items():
                html.append(f"        <p><strong>{key}:</strong> {value}</p>")
            html.append("    </div>")

        for section in self.sections:
            html.append("    <div class='section'>")
            html.append(f"        <h2>{section['title']}</h2>")

            if section["type"] == "text":
                html.append(f"        <p>{section['content']}</p>")
            elif section["type"] == "list":
                html.append("        <ul>")
                for item in section["content"]:
                    html.append(f"            <li>{item}</li>")
                html.append("        </ul>")
            elif section["type"] == "table":
                html.append(self._format_html_table(section["content"]))
            elif section["type"] == "data":
                html.append(f"        <pre>{json.dumps(section['content'], indent=2)}</pre>")

            html.append("    </div>")

        html.extend(
            [
                "    <div class='footer'>",
                "        <p>End of Report</p>",
                "    </div>",
                "</body>",
                "</html>",
            ]
        )

        return "\n".join(html)

    def generate_json(self) -> str:
        """
        Generate a JSON version of the report.

        Returns:
            JSON report as a string
        """
        report_data = {
            "title": self.title,
            "author": self.author,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
            "sections": [
                {
                    "title": section["title"],
                    "content": section["content"],
                    "type": section["type"],
                    "added_at": section["added_at"].isoformat(),
                }
                for section in self.sections
            ],
        }
        return json.dumps(report_data, indent=2)

    def save(self, filepath: str, format: str = "text") -> None:
        """
        Save the report to a file.

        Args:
            filepath: Path where the report should be saved
            format: Output format ('text', 'html', 'json')
        """
        format = format.lower()

        if format == "text":
            content = self.generate_text()
        elif format == "html":
            content = self.generate_html()
        elif format == "json":
            content = self.generate_json()
        else:
            raise ValueError(f"Unsupported format: {format}")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def _format_table(self, data: List[Dict[str, Any]]) -> str:
        """Format table data as plain text."""
        if not data:
            return "No data"

        headers = list(data[0].keys())
        col_widths = {h: len(h) for h in headers}

        for row in data:
            for header in headers:
                col_widths[header] = max(col_widths[header], len(str(row.get(header, ""))))

        lines = []
        header_line = "  ".join(h.ljust(col_widths[h]) for h in headers)
        lines.append(header_line)
        lines.append("-" * len(header_line))

        for row in data:
            row_line = "  ".join(str(row.get(h, "")).ljust(col_widths[h]) for h in headers)
            lines.append(row_line)

        return "\n".join(lines)

    def _format_html_table(self, data: List[Dict[str, Any]]) -> str:
        """Format table data as HTML."""
        if not data:
            return "<p>No data</p>"

        headers = list(data[0].keys())
        html = ["        <table>"]
        html.append("            <tr>")
        for header in headers:
            html.append(f"                <th>{header}</th>")
        html.append("            </tr>")

        for row in data:
            html.append("            <tr>")
            for header in headers:
                html.append(f"                <td>{row.get(header, '')}</td>")
            html.append("            </tr>")

        html.append("        </table>")
        return "\n".join(html)

    def clear(self) -> None:
        """Clear all sections and metadata from the report."""
        self.sections = []
        self.metadata = {}

    def __str__(self) -> str:
        """String representation of the report."""
        return self.generate_text()

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"ReportGenerator(title='{self.title}', sections={len(self.sections)})"


# Example usage
if __name__ == "__main__":
    # Create a report
    report = ReportGenerator(title="Monthly Sales Report", author="Data Team")

    # Add metadata
    report.add_metadata("Period", "January 2025")
    report.add_metadata("Department", "Sales")

    # Add sections
    report.add_section(
        "Executive Summary",
        "This report provides an overview of sales performance for January 2025.",
    )

    report.add_section(
        "Key Metrics",
        ["Total Revenue: $150,000", "New Customers: 45", "Conversion Rate: 12.5%"],
        section_type="list",
    )

    report.add_section(
        "Regional Performance",
        [
            {"Region": "North", "Sales": 50000, "Growth": "15%"},
            {"Region": "South", "Sales": 45000, "Growth": "8%"},
            {"Region": "East", "Sales": 35000, "Growth": "12%"},
            {"Region": "West", "Sales": 20000, "Growth": "-3%"},
        ],
        section_type="table",
    )

    # Print text version
    print(report.generate_text())

    # Save in different formats
    # report.save("report.txt", format="text")
    # report.save("report.html", format="html")
    # report.save("report.json", format="json")
