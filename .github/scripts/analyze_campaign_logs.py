#!/usr/bin/env python3
"""
Analyze Campaign Logs - GitHub Actions Script
Analyzes job search campaign logs and generates insights.
"""

import json
import sys
import traceback
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class CampaignLogAnalyzer:
    """Analyze job search campaign logs and generate reports."""

    def __init__(self, logs_dir: str = "job_search_data"):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def analyze_all_campaigns(self) -> Dict[str, Any]:
        """Analyze all campaign logs and generate comprehensive report."""
        print("🔍 Analyzing Campaign Logs...")
        print("=" * 70)

        analyses = self._load_all_analyses()

        if not analyses:
            print("⚠️  No campaign logs found")
            return {"status": "no_data", "analyses": 0}

        print(f"📊 Found {len(analyses)} job analyses")

        analytics = {
            "total_analyses": len(analyses),
            "date_range": self._get_date_range(analyses),
            "match_score_stats": self._calculate_match_stats(analyses),
            "top_matches": self._get_top_matches(analyses, limit=5),
            "skill_gaps_summary": self._analyze_skill_gaps(analyses),
            "company_analysis": self._analyze_companies(analyses),
            "recommendations_breakdown": self._analyze_recommendations(analyses),
            "learning_plan_stats": self._analyze_learning_plans(analyses),
            "trends": self._analyze_trends(analyses),
            "generated_at": datetime.now().isoformat(),
        }

        self._display_analytics(analytics)

        report_path = self.logs_dir / "campaign_analytics.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(analytics, f, indent=2)
        print(f"\n💾 Analytics saved to: {report_path}")

        self._generate_markdown_report(analytics)
        return analytics

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _load_all_analyses(self) -> List[Dict[str, Any]]:
        analyses: List[Dict[str, Any]] = []
        patterns = [
            "analyzed_jobs.json",
            "export_*/match_results.json",
            "automation_runs/*/match_results.json",
        ]

        for pattern in patterns:
            for file_path in self.logs_dir.glob(pattern):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            analyses.extend(data)
                        else:
                            analyses.append(data)
                except Exception as e:
                    print(f"⚠️  Error loading {file_path}: {e}")

        return analyses

    def _get_date_range(self, analyses: List[Dict]) -> Dict[str, Any]:
        dates: List[str] = [a["timestamp"] for a in analyses if "timestamp" in a]
        if not dates:
            return {"start": "N/A", "end": "N/A", "days": 0}
        dates.sort()
        start = datetime.fromisoformat(dates[0].replace("Z", "+00:00"))
        end = datetime.fromisoformat(dates[-1].replace("Z", "+00:00"))
        return {
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d"),
            "days": (end - start).days + 1,
        }

    def _calculate_match_stats(self, analyses: List[Dict]) -> Dict[str, Any]:
        scores: List[float] = [a.get("overall_score", 0) for a in analyses]
        if not scores:
            return {"average": 0, "min": 0, "max": 0, "median": 0}
        scores.sort()
        n = len(scores)
        return {
            "average": round(sum(scores) / n, 1),
            "min": round(min(scores), 1),
            "max": round(max(scores), 1),
            "median": round(scores[n // 2], 1),
            "above_85": len([s for s in scores if s >= 85]),
            "above_70": len([s for s in scores if s >= 70]),
            "below_70": len([s for s in scores if s < 70]),
        }

    def _get_top_matches(self, analyses: List[Dict], limit: int = 5) -> List[Dict]:
        top_matches: List[Dict[str, Any]] = []
        sorted_analyses = sorted(analyses, key=lambda x: x.get("overall_score", 0), reverse=True)
        for analysis in sorted_analyses[:limit]:
            top_matches.append(
                {
                    "job_title": analysis.get("job", {}).get("title", "Unknown"),
                    "company": analysis.get("job", {}).get("company", "Unknown"),
                    "score": analysis.get("overall_score", 0),
                    "recommendation": analysis.get("recommendation", "N/A"),
                }
            )
        return top_matches

    def _analyze_skill_gaps(self, analyses: List[Dict]) -> Dict[str, Any]:
        all_gaps = defaultdict(int)
        gap_priorities = defaultdict(list)
        for analysis in analyses:
            gaps = analysis.get("skill_gaps", [])
            for gap in gaps:
                skill = gap.get("skill", "Unknown")
                all_gaps[skill] += 1
                gap_priorities[skill].append(gap.get("priority", "unknown"))

        sorted_gaps = sorted(all_gaps.items(), key=lambda x: x[1], reverse=True)
        return {
            "total_unique_gaps": len(all_gaps),
            "most_common_gaps": [
                {
                    "skill": skill,
                    "frequency": count,
                    "percentage": round(count / len(analyses) * 100, 1),
                }
                for skill, count in sorted_gaps[:10]
            ],
            "critical_gaps": [
                skill for skill, priorities in gap_priorities.items() if "critical" in priorities
            ],
        }

    def _analyze_companies(self, analyses: List[Dict]) -> Dict[str, Any]:
        companies = defaultdict(lambda: {"count": 0, "scores": []})
        for analysis in analyses:
            company = analysis.get("job", {}).get("company", "Unknown")
            score = analysis.get("overall_score", 0)
            companies[company]["count"] += 1
            companies[company]["scores"].append(score)
        for company in companies:
            scores = companies[company]["scores"]
            companies[company]["avg_score"] = round(sum(scores) / len(scores), 1)
        sorted_companies = sorted(companies.items(), key=lambda x: x[1]["count"], reverse=True)
        return {
            "total_companies": len(companies),
            "top_companies": [
                {
                    "name": company,
                    "applications": data["count"],
                    "avg_match_score": data["avg_score"],
                }
                for company, data in sorted_companies[:10]
            ],
        }

    def _analyze_recommendations(self, analyses: List[Dict]) -> Dict[str, int]:
        recommendations = defaultdict(int)
        for analysis in analyses:
            rec = analysis.get("recommendation", "Unknown")
            recommendations[rec] += 1
        return dict(recommendations)

    def _analyze_learning_plans(self, analyses: List[Dict]) -> Dict[str, Any]:
        total_hours = 0
        total_sprints = 0
        skills_to_learn = set()
        for analysis in analyses:
            learning_plan = analysis.get("learning_plan", {})
            if learning_plan:
                total_hours += learning_plan.get("total_hours", 0)
                total_sprints += len(learning_plan.get("sprints", []))
                skills_to_learn.update(learning_plan.get("skills_to_develop", []))
        return {
            "plans_created": sum(1 for a in analyses if a.get("learning_plan")),
            "total_learning_hours": total_hours,
            "avg_hours_per_plan": round(total_hours / len(analyses), 1) if analyses else 0,
            "total_sprints": total_sprints,
            "unique_skills_to_learn": len(skills_to_learn),
            "skills": list(skills_to_learn),
        }

    def _analyze_trends(self, analyses: List[Dict]) -> Dict[str, Any]:
        dated_analyses = [a for a in analyses if "timestamp" in a and "overall_score" in a]
        if len(dated_analyses) < 2:
            return {"trend": "insufficient_data"}
        dated_analyses.sort(key=lambda x: x["timestamp"])
        scores = [a["overall_score"] for a in dated_analyses]
        mid = len(scores) // 2
        first_half_avg = sum(scores[:mid]) / mid
        second_half_avg = sum(scores[mid:]) / (len(scores) - mid)
        trend_direction = "improving" if second_half_avg > first_half_avg else "declining"
        trend_change = round(second_half_avg - first_half_avg, 1)
        return {
            "trend": trend_direction,
            "change": trend_change,
            "first_half_avg": round(first_half_avg, 1),
            "second_half_avg": round(second_half_avg, 1),
        }

    def _display_analytics(self, analytics: Dict[str, Any]):
        print("\n📊 CAMPAIGN ANALYTICS SUMMARY")
        print("=" * 70)
        stats = analytics["match_score_stats"]
        print(
            f"\n📅 Date Range: {analytics['date_range']['start']} → {analytics['date_range']['end']} "
            f"({analytics['date_range']['days']} days)"
        )
        print(f"📋 Total Analyses: {analytics['total_analyses']}")
        print(f"🎯 Average Score: {stats['average']}% (Range {stats['min']}–{stats['max']}%)")

    def _generate_markdown_report(self, analytics: Dict[str, Any]):
        report_path = self.logs_dir / "campaign_analytics_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(analytics, indent=2))
        print(f"📄 Markdown report saved to: {report_path}")


def main():
    """Main execution."""
    analyzer = CampaignLogAnalyzer()
    try:
        analytics = analyzer.analyze_all_campaigns()
        sys.exit(0 if analytics.get("status") != "no_data" else 1)
    except Exception as e:
        print(f"\n❌ Error analyzing campaigns: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
