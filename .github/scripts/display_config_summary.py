#!/usr/bin/env python3
"""
Display Config Summary - GitHub Actions Script
Summarizes key settings from job search configuration files.
"""

import json
import sys
import traceback
from pathlib import Path
from typing import Any, Dict


class ConfigSummary:
    """Read and summarize job search configuration."""

    def __init__(self, data_dir: str = "job_search_data"):
        self.data_dir = Path(data_dir)
        self.config_path = self.data_dir / "config.json"
        self.info: list[str] = []
        self.warnings: list[str] = []
        self.errors: list[str] = []

    # ------------------------------------------------------------------
    # Main summary
    # ------------------------------------------------------------------
    def summarize(self) -> Dict[str, Any]:
        print("\n🧩 Displaying Configuration Summary...")
        print("=" * 70)

        if not self.config_path.exists():
            self.errors.append(f"Configuration file missing: {self.config_path}")
            self._display()
            return {"status": "error", "reason": "missing_config"}

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in {self.config_path}: {e}")
            self._display()
            return {"status": "error", "reason": "invalid_json"}

        # ---- Candidate info -------------------------------------------------
        candidate: Dict[str, Any] = config.get("candidate", {})
        if candidate:
            self.info.append(f"👤 Candidate: {candidate.get('name', 'Unknown')}")
            email = candidate.get("email", "")
            self.info.append(f"📧 Email: {email if '@' in email else 'Not configured'}")
            self.info.append(f"📄 CV Path: {candidate.get('cv_path', 'Not set')}")
        else:
            self.warnings.append("Candidate section missing from configuration")

        # ---- Automation -----------------------------------------------------
        automation: Dict[str, Any] = config.get("automation", {})
        if automation:
            status = "enabled ✅" if automation.get("enabled") else "disabled ❌"
            self.info.append(f"🤖 Automation: {status}")
            if automation.get("schedule"):
                self.info.append(f"   └─ Schedule: {automation['schedule']}")
        else:
            self.warnings.append("Automation section missing")

        # ---- Notifications --------------------------------------------------
        notifications: Dict[str, Any] = config.get("notifications", {})
        if notifications:
            enabled = notifications.get("enabled", False)
            self.info.append(f"🔔 Notifications: {'enabled ✅' if enabled else 'disabled ❌'}")
            if enabled:
                if notifications.get("email"):
                    self.info.append("   └─ Email notifications active")
                if notifications.get("slack_webhook"):
                    self.info.append("   └─ Slack notifications active")
                if not notifications.get("email") and not notifications.get("slack_webhook"):
                    self.warnings.append("Notifications enabled but no channel configured")
        else:
            self.warnings.append("Notifications section missing")

        # ---- Preferences ----------------------------------------------------
        preferences: Dict[str, Any] = config.get("preferences", {})
        if preferences:
            self.info.append("⚙️  Preferences:")
            for key, value in preferences.items():
                self.info.append(f"   └─ {key}: {value}")
        else:
            self.warnings.append("Preferences section missing")

        # ---- Analysis -------------------------------------------------------
        analysis: Dict[str, Any] = config.get("analysis", {})
        if analysis:
            self.info.append("📈 Analysis Settings:")
            for key, value in analysis.items():
                self.info.append(f"   └─ {key}: {value}")
        else:
            self.warnings.append("Analysis section missing")

        # ---- Summary Display ------------------------------------------------
        self._display()

        summary = {
            "status": "ok" if not self.errors else "error",
            "info": self.info,
            "warnings": self.warnings,
            "errors": self.errors,
        }

        return summary

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------
    def _display(self) -> None:
        """Print collected messages with sections."""
        if self.info:
            print("\n✅ INFORMATION")
            print("-" * 70)
            for line in self.info:
                print(line)

        if self.warnings:
            print("\n⚠️  WARNINGS")
            print("-" * 70)
            for line in self.warnings:
                print(line)

        if self.errors:
            print("\n❌ ERRORS")
            print("-" * 70)
            for line in self.errors:
                print(line)


def main():
    """Entry point."""
    summary_tool = ConfigSummary()
    try:
        summary = summary_tool.summarize()
        sys.exit(0 if summary.get("status") == "ok" else 1)
    except Exception as e:
        print(f"\n❌ Error displaying config summary: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
