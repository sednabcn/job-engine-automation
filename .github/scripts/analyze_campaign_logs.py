#!/usr/bin/env python3
"""
Analyze Campaign Logs - GitHub Actions Script
Analyzes job search campaign logs and generates insights
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict


class CampaignLogAnalyzer:
    """Analyze job search campaign logs and generate reports"""
    
    def __init__(self, logs_dir: str = "job_search_data"):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_all_campaigns(self) -> Dict[str, Any]:
        """Analyze all campaign logs and generate comprehensive report"""
        print("🔍 Analyzing Campaign Logs...")
        print("=" * 70)
        
        # Load all analysis logs
        analyses = self._load_all_analyses()
        
        if not analyses:
            print("⚠️  No campaign logs found")
            return {'status': 'no_data', 'analyses': 0}
        
        print(f"📊 Found {len(analyses)} job analyses")
        
        # Generate analytics
        analytics = {
            'total_analyses': len(analyses),
            'date_range': self._get_date_range(analyses),
            'match_score_stats': self._calculate_match_stats(analyses),
            'top_matches': self._get_top_matches(analyses, limit=5),
            'skill_gaps_summary': self._analyze_skill_gaps(analyses),
            'company_analysis': self._analyze_companies(analyses),
            'recommendations_breakdown': self._analyze_recommendations(analyses),
            'learning_plan_stats': self._analyze_learning_plans(analyses),
            'trends': self._analyze_trends(analyses),
            'generated_at': datetime.now().isoformat()
        }
        
        # Display results
        self._display_analytics(analytics)
        
        # Save report
        report_path = self.logs_dir / 'campaign_analytics.json'
        with open(report_path, 'w') as f:
            json.dump(analytics, f, indent=2)
        
        print(f"\n💾 Analytics saved to: {report_path}")
        
        # Generate markdown report
        self._generate_markdown_report(analytics)
        
        return analytics
    
    def _load_all_analyses(self) -> List[Dict[str, Any]]:
        """Load all job analysis files"""
        analyses = []
        
        # Look for analysis files
        patterns = [
            'analyzed_jobs.json',
            'export_*/match_results.json',
            'automation_runs/*/match_results.json'
        ]
        
        for pattern in patterns:
            for file_path in self.logs_dir.glob(pattern):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            analyses.extend(data)
                        else:
                            analyses.append(data)
                except Exception as e:
                    print(f"⚠️  Error loading {file_path}: {e}")
        
        return analyses
    
    def _get_date_range(self, analyses: List[Dict]) -> Dict[str, str]:
        """Get date range of analyses"""
        dates = []
        for analysis in analyses:
            if 'timestamp' in analysis:
                dates.append(analysis['timestamp'])
        
        if not dates:
            return {'start': 'N/A', 'end': 'N/A', 'days': 0}
        
        dates.sort()
        start = datetime.fromisoformat(dates[0].replace('Z', '+00:00'))
        end = datetime.fromisoformat(dates[-1].replace('Z', '+00:00'))
        
        return {
            'start': start.strftime('%Y-%m-%d'),
            'end': end.strftime('%Y-%m-%d'),
            'days': (end - start).days + 1
        }
    
    def _calculate_match_stats(self, analyses: List[Dict]) -> Dict[str, float]:
        """Calculate match score statistics"""
        scores = [a.get('overall_score', 0) for a in analyses]
        
        if not scores:
            return {'average': 0, 'min': 0, 'max': 0, 'median': 0}
        
        scores.sort()
        n = len(scores)
        
        return {
            'average': round(sum(scores) / n, 1),
            'min': round(min(scores), 1),
            'max': round(max(scores), 1),
            'median': round(scores[n // 2], 1) if n > 0 else 0,
            'above_85': len([s for s in scores if s >= 85]),
            'above_70': len([s for s in scores if s >= 70]),
            'below_70': len([s for s in scores if s < 70])
        }
    
    def _get_top_matches(self, analyses: List[Dict], limit: int = 5) -> List[Dict]:
        """Get top matching jobs"""
        sorted_analyses = sorted(
            analyses, 
            key=lambda x: x.get('overall_score', 0), 
            reverse=True
        )
        
        top_matches = []
        for analysis in sorted_analyses[:limit]:
            top_matches.append({
                'job_title': analysis.get('job', {}).get('title', 'Unknown'),
                'company': analysis.get('job', {}).get('company', 'Unknown'),
                'score': analysis.get('overall_score', 0),
                'recommendation': analysis.get('recommendation', 'N/A')
            })
        
        return top_matches
    
    def _analyze_skill_gaps(self, analyses: List[Dict]) -> Dict[str, Any]:
        """Analyze common skill gaps across all analyses"""
        all_gaps = defaultdict(int)
        gap_priorities = defaultdict(list)
        
        for analysis in analyses:
            gaps = analysis.get('skill_gaps', [])
            for gap in gaps:
                skill = gap.get('skill', 'Unknown')
                all_gaps[skill] += 1
                gap_priorities[skill].append(gap.get('priority', 'unknown'))
        
        # Sort by frequency
        sorted_gaps = sorted(all_gaps.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_unique_gaps': len(all_gaps),
            'most_common_gaps': [
                {
                    'skill': skill,
                    'frequency': count,
                    'percentage': round(count / len(analyses) * 100, 1)
                }
                for skill, count in sorted_gaps[:10]
            ],
            'critical_gaps': [
                skill for skill, priorities in gap_priorities.items()
                if 'critical' in priorities
            ]
        }
    
    def _analyze_companies(self, analyses: List[Dict]) -> Dict[str, Any]:
        """Analyze companies applied to"""
        companies = defaultdict(lambda: {'count': 0, 'avg_score': 0, 'scores': []})
        
        for analysis in analyses:
            company = analysis.get('job', {}).get('company', 'Unknown')
            score = analysis.get('overall_score', 0)
            
            companies[company]['count'] += 1
            companies[company]['scores'].append(score)
        
        # Calculate averages
        for company in companies:
            scores = companies[company]['scores']
            companies[company]['avg_score'] = round(sum(scores) / len(scores), 1)
        
        # Sort by count
        sorted_companies = sorted(
            companies.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        return {
            'total_companies': len(companies),
            'top_companies': [
                {
                    'name': company,
                    'applications': data['count'],
                    'avg_match_score': data['avg_score']
                }
                for company, data in sorted_companies[:10]
            ]
        }
    
    def _analyze_recommendations(self, analyses: List[Dict]) -> Dict[str, int]:
        """Analyze recommendation distribution"""
        recommendations = defaultdict(int)
        
        for analysis in analyses:
            rec = analysis.get('recommendation', 'Unknown')
            recommendations[rec] += 1
        
        return dict(recommendations)
    
    def _analyze_learning_plans(self, analyses: List[Dict]) -> Dict[str, Any]:
        """Analyze learning plans generated"""
        total_hours = 0
        total_sprints = 0
        skills_to_learn = set()
        
        for analysis in analyses:
            learning_plan = analysis.get('learning_plan', {})
            if learning_plan:
                total_hours += learning_plan.get('total_hours', 0)
                total_sprints += len(learning_plan.get('sprints', []))
                skills_to_learn.update(learning_plan.get('skills_to_develop', []))
        
        return {
            'plans_created': sum(1 for a in analyses if a.get('learning_plan')),
            'total_learning_hours': total_hours,
            'avg_hours_per_plan': round(total_hours / len(analyses), 1) if analyses else 0,
            'total_sprints': total_sprints,
            'unique_skills_to_learn': len(skills_to_learn),
            'skills': list(skills_to_learn)
        }
    
    def _analyze_trends(self, analyses: List[Dict]) -> Dict[str, Any]:
        """Analyze trends over time"""
        # Sort by timestamp
        dated_analyses = [
            a for a in analyses 
            if 'timestamp' in a and 'overall_score' in a
        ]
        
        if not dated_analyses:
            return {'trend': 'insufficient_data'}
        
        dated_analyses.sort(key=lambda x: x['timestamp'])
        
        # Calculate trend (simple linear)
        scores = [a['overall_score'] for a in dated_analyses]
        if len(scores) < 2:
            return {'trend': 'insufficient_data'}
        
        # Simple trend: compare first half to second half
        mid = len(scores) // 2
        first_half_avg = sum(scores[:mid]) / mid
        second_half_avg = sum(scores[mid:]) / (len(scores) - mid)
        
        trend_direction = 'improving' if second_half_avg > first_half_avg else 'declining'
        trend_change = round(second_half_avg - first_half_avg, 1)
        
        return {
            'trend': trend_direction,
            'change': trend_change,
            'first_half_avg': round(first_half_avg, 1),
            'second_half_avg': round(second_half_avg, 1)
        }
    
    def _display_analytics(self, analytics: Dict[str, Any]):
        """Display analytics in console"""
        print("\n📊 CAMPAIGN ANALYTICS SUMMARY")
        print("=" * 70)
        
        print(f"\n📅 Date Range: {analytics['date_range']['start']} to {analytics['date_range']['end']}")
        print(f"📆 Campaign Duration: {analytics['date_range']['days']} days")
        print(f"📋 Total Analyses: {analytics['total_analyses']}")
        
        print("\n🎯 Match Score Statistics:")
        stats = analytics['match_score_stats']
        print(f"  • Average: {stats['average']}%")
        print(f"  • Range: {stats['min']}% - {stats['max']}%")
        print(f"  • Median: {stats['median']}%")
        print(f"  • Above 85%: {stats['above_85']} ({round(stats['above_85']/analytics['total_analyses']*100, 1)}%)")
        print(f"  • 70-85%: {stats['above_70'] - stats['above_85']}")
        print(f"  • Below 70%: {stats['below_70']}")
        
        print("\n🏆 Top 5 Matches:")
        for i, match in enumerate(analytics['top_matches'], 1):
            print(f"  {i}. {match['job_title']} at {match['company']}")
            print(f"     Score: {match['score']}% | {match['recommendation']}")
        
        print("\n🎓 Most Common Skill Gaps:")
        for gap in analytics['skill_gaps_summary']['most_common_gaps'][:5]:
            print(f"  • {gap['skill']}: {gap['frequency']} times ({gap['percentage']}%)")
        
        print("\n🏢 Top Companies:")
        for company in analytics['company_analysis']['top_companies'][:5]:
            print(f"  • {company['name']}: {company['applications']} applications (avg: {company['avg_match_score']}%)")
        
        print("\n💡 Recommendations Breakdown:")
        for rec, count in analytics['recommendations_breakdown'].items():
            percentage = round(count / analytics['total_analyses'] * 100, 1)
            print(f"  • {rec}: {count} ({percentage}%)")
        
        print("\n📚 Learning Plan Statistics:")
        lp = analytics['learning_plan_stats']
        print(f"  • Plans Created: {lp['plans_created']}")
        print(f"  • Total Learning Hours: {lp['total_learning_hours']}")
        print(f"  • Average per Plan: {lp['avg_hours_per_plan']} hours")
        print(f"  • Total Sprints: {lp['total_sprints']}")
        
        print("\n📈 Trends:")
        trend = analytics['trends']
        if trend.get('trend') != 'insufficient_data':
            print(f"  • Direction: {trend['trend'].upper()}")
            print(f"  • Change: {trend['change']:+.1f}%")
            print(f"  • First Half Avg: {trend['first_half_avg']}%")
            print(f"  • Second Half Avg: {trend['second_half_avg']}%")
        else:
            print("  • Insufficient data for trend analysis")
    
    def _generate_markdown_report(self, analytics: Dict[str, Any]):
        """Generate markdown report"""
        report_path = self.logs_dir / 'campaign_analytics_report.md'
        
        report = f"""# Job Search Campaign Analytics Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Campaign Duration:** {analytics['date_range']['start']} to {analytics['date_range']['end']} ({analytics['date_range']['days']} days)  
**Total Analyses:** {analytics['total_analyses']}

---

## 🎯 Match Score Statistics

| Metric | Value |
|--------|-------|
| Average Score | {analytics['match_score_stats']['average']}% |
| Median Score | {analytics['match_score_stats']['median']}% |
| Score Range | {analytics['match_score_stats']['min']}% - {analytics['match_score_stats']['max']}% |
| Above 85% | {analytics['match_score_stats']['above_85']} |
| 70-85% | {analytics['match_score_stats']['above_70'] - analytics['match_score_stats']['above_85']} |
| Below 70% | {analytics['match_score_stats']['below_70']} |

---

## 🏆 Top Matching Jobs

| Rank | Job Title | Company | Score | Recommendation |
|------|-----------|---------|-------|----------------|
"""
        
        for i, match in enumerate(analytics['top_matches'], 1):
            report += f"| {i} | {match['job_title']} | {match['company']} | {match['score']}% | {match['recommendation']} |\n"
        
        report += f"""
---

## 🎓 Most Common Skill Gaps

| Skill | Frequency | Percentage |
|-------|-----------|------------|
"""
        
        for gap in analytics['skill_gaps_summary']['most_common_gaps'][:10]:
            report += f"| {gap['skill']} | {gap['frequency']} | {gap['percentage']}% |\n"
        
        report += f"""
---

## 🏢 Company Analysis

| Company | Applications | Avg Match Score |
|---------|--------------|-----------------|
"""
        
        for company in analytics['company_analysis']['top_companies']:
            report += f"| {company['name']} | {company['applications']} | {company['avg_match_score']}% |\n"
        
        report += f"""
---

## 💡 Recommendations Distribution

| Recommendation | Count | Percentage |
|----------------|-------|------------|
"""
        
        total = analytics['total_analyses']
        for rec, count in analytics['recommendations_breakdown'].items():
            percentage = round(count / total * 100, 1)
            report += f"| {rec} | {count} | {percentage}% |\n"
        
        lp = analytics['learning_plan_stats']
        report += f"""
---

## 📚 Learning Plan Statistics

- **Plans Created:** {lp['plans_created']}
- **Total Learning Hours:** {lp['total_learning_hours']}
- **Average Hours per Plan:** {lp['avg_hours_per_plan']}
- **Total Sprints:** {lp['total_sprints']}
- **Unique Skills to Learn:** {lp['unique_skills_to_learn']}

### Skills to Develop
{chr(10).join(f'- {skill}' for skill in lp['skills'][:15])}

---

## 📈 Trends

"""
        
        trend = analytics['trends']
        if trend.get('trend') != 'insufficient_data':
            report += f"""- **Direction:** {trend['trend'].upper()} {'📈' if trend['trend'] == 'improving' else '📉'}
- **Change:** {trend['change']:+.1f}%
- **First Half Average:** {trend['first_half_avg']}%
- **Second Half Average:** {trend['second_half_avg']}%

"""
        else:
            report += "Insufficient data for trend analysis.\n"
        
        report += f"""
---

## 🎬 Next Steps

Based on this analysis:

1. **Focus on Top Matches:** Prioritize applications to companies where you scored {analytics['match_score_stats']['max']}%+
2. **Address Skill Gaps:** Focus learning on: {', '.join(gap['skill'] for gap in analytics['skill_gaps_summary']['most_common_gaps'][:3])}
3. **Target Companies:** Consider applying to similar roles at: {', '.join(c['name'] for c in analytics['company_analysis']['top_companies'][:3])}
4. **Improve Profile:** Work on skills appearing most frequently in gaps
5. **Continue Momentum:** {"Keep up the great work! Scores are improving." if trend.get('trend') == 'improving' else "Consider revisiting your approach or targeting different roles."}

---

*Generated by Advanced Job Engine Campaign Analytics*
"""
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"📄 Markdown report saved to: {report_path}")


def main():
    """Main execution"""
    analyzer = CampaignLogAnalyzer()
    
    try:
        analytics = analyzer.analyze_all_campaigns()
        
        # Output for GitHub Actions
        if analytics.get('status') != 'no_data':
            print("\n✅ Analysis completed successfully!")
            
            # Set GitHub Actions output
            if 'GITHUB_OUTPUT' in os.environ:
                with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                    f.write(f"total_analyses={analytics['total_analyses']}\n")
                    f.write(f"avg_match_score={analytics['match_score_stats']['average']}\n")
                    f.write(f"top_score={analytics['match_score_stats']['max']}\n")
            
            sys.exit(0)
        else:
            print("\n⚠️  No data to analyze")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error analyzing campaigns: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    import os
    main()
