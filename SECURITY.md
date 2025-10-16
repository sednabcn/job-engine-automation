
### SECURITY.md

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please:

1. **Do NOT** open a public issue
2. Email security@projectdomain.com with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to resolve the issue.

## Security Considerations

### Data Privacy

- All personal data (CVs, job descriptions) stays local
- No data is sent to external servers
- GitHub Actions workflows process data in your private repository

### File Handling

- PDF/DOCX parsing uses trusted libraries (PyPDF2, python-docx)
- Input validation prevents malicious file processing
- Sanitization of extracted text

### Dependencies

- Regular dependency updates via Dependabot
- Security audits using `pip-audit`
- Minimal dependency footprint

## Best Practices

### For Users

1. **Sensitive Data**: Keep your repository private if it contains personal CVs
2. **API Keys**: Never commit API keys or credentials
3. **File Sources**: Only analyze files from trusted sources
4. **Updates**: Keep the tool updated to latest version

### For Contributors

1. **Code Review**: All PRs require security review
2. **Dependencies**: Add new dependencies sparingly
3. **Input Validation**: Always validate user input
4. **Testing**: Include security test cases

## Known Limitations

- PDF parsing may expose vulnerabilities in PyPDF2 library
- File size limits: Max 10MB per file to prevent DoS
- No encryption at rest (relies on filesystem security)

## Security Updates

We will disclose security issues via:
- GitHub Security Advisories
- CHANGELOG.md entries marked [SECURITY]
- Email notifications to registered users (coming soon)

## Contact

For security concerns: security@projectdomain.com
For general questions: contact@projectdomain.com
```
