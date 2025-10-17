#!/usr/bin/env python3
"""
Full Workflow Example - Complete Job Analysis Process
Demonstrates the complete end-to-end workflow of the Advanced Job Engine
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class AdvancedJobEngine:
    """Main job analysis engine - complete workflow"""

    def __init__(self, data_dir: str = "job_search_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()

    def run_complete_workflow(
        self,
        cv_path: str,
        job_path: str,
        generate_materials: bool = True,
        create_learning_plan: bool = True,
    ) -> Dict[str, Any]:
        """
        Execute complete job analysis workflow

        Steps:
        1. Parse CV and extract candidate profile
        2. Parse job description and requirements
        3. Perform skill matching and gap analysis
        4. Generate quality gate assessment
        5. Create personalized learning plan
        6. Generate application materials
        7. Export comprehensive report

        Args:
            cv_path: Path to CV file (PDF, DOCX, or TXT)
            job_path: Path to job description file
            generate_materials: Generate cover letter and other materials
            create_learning_plan: Generate personalized learning plan

        Returns:
            Complete analysis results dictionary
        """
        print("🚀 Starting Advanced Job Analysis Workflow")
        print("=" * 70)

        # Step 1: Parse CV
        print("\n📄 Step 1/7: Parsing CV...")
        candidate = self._parse_cv(cv_path)
        print(f"✓ Extracted profile for {candidate['name']}")
        print(f"  • Experience: {candidate['experience_years']} years")
        print(f"  • Skills: {len(candidate['skills'])} identified")
        # Step 2: Parse Job Description
        print("\n💼 Step 2/7: Parsing Job Description...")
        job = self._parse_job_description(job_path)
        print(f"✓ Analyzed position: {job['title']} at {job['company']}")
        print(f"  • Required skills: {len(job['required_skills'])}")
        print(f"  • Preferred skills: {len(job['preferred_skills'])}")

        # Step 3: Skill Matching & Gap Analysis
        print("\n🎯 Step 3/7: Performing Skill Matching...")
        match_results = self._calculate_match(candidate, job)
        print(f"✓ Match Score: {match_results['overall_score']}%")
        print(f"  • Technical Skills: {match_results['technical_score']}%")
        print(f"  • Experience Match: {match_results['experience_score']}%")
        print(f"  • Recommendation: {match_results['recommendation']}")

        # Step 4: Quality Gate Assessment
        print("\n🚪 Step 4/7: Evaluating Quality Gates...")
        quality_gates = self._assess_quality_gates(match_results)
        print("✓ Quality Gate Results:")
        print(
            f"  • Foundational: {
                '✓ PASSED' if quality_gates['foundational']['passed'] else '✗ FAILED'}"
        )
        print(
            f"  • Competitive: {
                '✓ PASSED' if quality_gates['competitive']['passed'] else '⚠ NEARLY PASSED'}"
        )
        print(
            f"  • Excellence: {
                '✓ PASSED' if quality_gates['excellence']['passed'] else '✗ NOT PASSED'}"
        )
        # Step 5: Learning Plan Generation
        learning_plan = None
        if create_learning_plan and match_results.get("skill_gaps"):
            print("\n📚 Step 5/7: Generating Learning Plan...")
            learning_plan = self._generate_learning_plan(match_results["skill_gaps"])
            print(f"✓ Created {len(learning_plan['sprints'])}-sprint learning plan")
            print(f"  • Total duration: {learning_plan['total_weeks']} weeks")
            print(f"  • Study time: {learning_plan['total_hours']} hours")
        else:
            print("\n📚 Step 5/7: Skipping Learning Plan (no gaps or disabled)")

        # Step 6: Application Materials
        application_materials = None
        if generate_materials:
            print("\n✏️  Step 6/7: Generating Application Materials...")
            application_materials = self._generate_application_materials(
                candidate, job, match_results
            )
            print("✓ Generated application materials:")
            print("  • Cover letter")
            print("  • LinkedIn message")
            print("  • Follow-up email")
            print("  • Networking email")
        else:
            print("\n✏️  Step 6/7: Skipping Application Materials (disabled)")

        # Step 7: Generate Complete Report
        print("\n📊 Step 7/7: Generating Comprehensive Report...")
        report = self._generate_complete_report(
            candidate, job, match_results, quality_gates, learning_plan, application_materials
        )

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_dir = self.data_dir / f"export_{timestamp}"
        export_dir.mkdir(exist_ok=True)

        self._save_results(
            export_dir,
            {
                "report": report,
                "learning_plan": learning_plan,
                "application_materials": application_materials,
                "match_results": match_results,
                "quality_gates": quality_gates,
            },
        )

        print(f"✓ Complete report saved to: {export_dir}")

        print("\n" + "=" * 70)
        print("✅ Workflow Complete!")
        print("=" * 70)

        return {
            "timestamp": timestamp,
            "export_dir": str(export_dir),
            "match_score": match_results["overall_score"],
            "recommendation": match_results["recommendation"],
            "quality_gates": quality_gates,
            "learning_plan": learning_plan,
            "candidate": candidate,
            "job": job,
        }

    def _parse_cv(self, cv_path: str) -> Dict[str, Any]:
        """Parse CV and extract candidate information"""
        # Simplified parsing - in real implementation would use PyPDF2, docx, etc.
        return {
            "name": "Alex Johnson",
            "email": "alex.johnson@email.com",
            "location": "San Francisco, CA",
            "experience_years": 8.3,
            "current_role": "Senior Software Engineer",
            "current_company": "TechCorp Solutions",
            "skills": {
                "Python": {"level": 5, "years": 8},
                "Go": {"level": 3, "years": 2},
                "Kubernetes": {"level": 4, "years": 4},
                "Docker": {"level": 5, "years": 6},
                "AWS": {"level": 4, "years": 5},
                "PostgreSQL": {"level": 5, "years": 7},
                "Redis": {"level": 4, "years": 5},
                "Microservices": {"level": 5, "years": 6},
                "REST API": {"level": 5, "years": 7},
                "CI/CD": {"level": 4, "years": 5},
            },
            "certifications": ["AWS Solutions Architect", "CKA", "Docker Certified"],
            "education": {
                "degree": "BS Computer Science",
                "institution": "UC Berkeley",
                "year": 2016,
            },
            "achievements": [
                "Led migration to microservices (2M+ users)",
                "Reduced deployment time by 75%",
                "Achieved 99.95% uptime",
                "Reduced costs by 40%",
            ],
        }

    def _parse_job_description(self, job_path: str) -> Dict[str, Any]:
        """Parse job description and extract requirements"""
        return {
            "title": "Staff Backend Engineer",
            "company": "CloudNative Systems",
            "location": "Remote (US)",
            "salary_range": "$180,000 - $230,000",
            "experience_required": 8,
            "required_skills": {
                "Python": 5,
                "Go": 5,
                "Microservices": 5,
                "Kubernetes": 4,
                "Docker": 4,
                "AWS": 4,
                "PostgreSQL": 4,
                "REST API": 4,
                "CI/CD": 4,
                "Redis": 3,
            },
            "preferred_skills": {
                "GraphQL": 3,
                "Service Mesh": 2,
                "gRPC": 2,
                "Terraform": 3,
                "Monitoring": 3,
            },
            "responsibilities": [
                "Design scalable distributed systems",
                "Lead architectural decisions",
                "Mentor engineering team",
                "Drive technical excellence",
            ],
        }

    def _calculate_match(self, candidate: Dict, job: Dict) -> Dict[str, Any]:
        """Calculate comprehensive match score"""
        # Match required skills
        required_matches = []
        skill_gaps = []

        for skill, required_level in job["required_skills"].items():
            candidate_skill = candidate["skills"].get(skill, {"level": 0, "years": 0})
            candidate_level = candidate_skill["level"]

            if candidate_level >= required_level:
                required_matches.append(
                    {
                        "skill": skill,
                        "required": required_level,
                        "actual": candidate_level,
                        "status": "match",
                    }
                )
            elif candidate_level >= required_level - 1:
                required_matches.append(
                    {
                        "skill": skill,
                        "required": required_level,
                        "actual": candidate_level,
                        "status": "close",
                    }
                )
            else:
                skill_gaps.append(
                    {
                        "skill": skill,
                        "required": required_level,
                        "actual": candidate_level,
                        "gap": required_level - candidate_level,
                        "priority": "critical" if required_level >= 4 else "important",
                    }
                )

        # Calculate scores
        required_coverage = (len(required_matches) / len(job["required_skills"])) * 100
        technical_score = min(required_coverage * 1.1, 100)  # Bonus for exceeding

        experience_score = min(
            (candidate["experience_years"] / job["experience_required"]) * 100, 100
        )

        overall_score = (technical_score * 0.7) + (experience_score * 0.3)

        # Determine recommendation
        if overall_score >= 85:
            recommendation = "Excellent Match - Apply Immediately"
        elif overall_score >= 70:
            recommendation = "Strong Match - Apply Soon"
        elif overall_score >= 60:
            recommendation = "Good Match - Consider Learning Plan"
        else:
            recommendation = "Skills Gap - Focus on Development"

        return {
            "overall_score": round(overall_score, 1),
            "technical_score": round(technical_score, 1),
            "experience_score": round(experience_score, 1),
            "recommendation": recommendation,
            "required_matches": required_matches,
            "skill_gaps": skill_gaps,
            "required_coverage": round(required_coverage, 1),
        }

    def _assess_quality_gates(self, match_results: Dict) -> Dict[str, Any]:
        """Assess quality gate passage"""
        coverage = match_results["required_coverage"]
        score = match_results["overall_score"]

        return {
            "foundational": {
                "passed": coverage >= 80 and score >= 70,
                "score": score,
                "requirements": {"coverage": 80, "score": 70},
            },
            "competitive": {
                "passed": coverage >= 90 and score >= 85,
                "score": score,
                "requirements": {"coverage": 90, "score": 85},
            },
            "excellence": {
                "passed": coverage >= 100 and score >= 95,
                "score": score,
                "requirements": {"coverage": 100, "score": 95},
            },
        }

    def _generate_learning_plan(self, skill_gaps: List[Dict]) -> Dict[str, Any]:
        """Generate personalized learning plan"""
        if not skill_gaps:
            return None

        # Sort gaps by priority
        critical_gaps = [g for g in skill_gaps if g["priority"] == "critical"]
        important_gaps = [g for g in skill_gaps if g["priority"] == "important"]

        sprints = []
        sprint_num = 1

        # Create sprints for critical gaps
        for gap in critical_gaps:
            sprints.append(
                {
                    "sprint": sprint_num,
                    "duration_weeks": 2,
                    "skill": gap["skill"],
                    "current_level": gap["actual"],
                    "target_level": gap["required"],
                    "estimated_hours": 40 + (gap["gap"] * 20),
                    "priority": "critical",
                    "resources": [
                        f"{gap['skill']} Fundamentals Course",
                        f"Advanced {gap['skill']} Patterns",
                        f"Production {gap['skill']} Projects",
                    ],
                }
            )
            sprint_num += 1

        # Create sprints for important gaps
        for gap in important_gaps:
            sprints.append(
                {
                    "sprint": sprint_num,
                    "duration_weeks": 2,
                    "skill": gap["skill"],
                    "current_level": gap["actual"],
                    "target_level": gap["required"],
                    "estimated_hours": 30 + (gap["gap"] * 15),
                    "priority": "important",
                    "resources": [f"{gap['skill']} Introduction", f"{gap['skill']} Best Practices"],
                }
            )
            sprint_num += 1

        total_weeks = sum(s["duration_weeks"] for s in sprints)
        total_hours = sum(s["estimated_hours"] for s in sprints)

        return {
            "sprints": sprints,
            "total_weeks": total_weeks,
            "total_hours": total_hours,
            "weekly_commitment": round(total_hours / total_weeks, 1),
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "skills_to_develop": [gap["skill"] for gap in skill_gaps],
        }

    def _generate_application_materials(
        self, candidate: Dict, job: Dict, match_results: Dict
    ) -> Dict[str, str]:
        """Generate application materials"""
        materials = {}

        # Cover Letter
        materials[
            "cover_letter"
        ] = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job['title']} position at {job['company']}. With {candidate['experience_years']} years of experience in backend engineering and a proven track record of building scalable distributed systems, I am excited about the opportunity to contribute to your team.

In my current role as {candidate['current_role']} at {candidate['current_company']}, I have:
{chr(10).join(f'• {achievement}' for achievement in candidate['achievements'][:3])}

My technical expertise aligns strongly with your requirements, particularly in Python, microservices architecture, and Kubernetes. I am confident that my experience building cloud-native systems serving millions of users would be valuable as {job['company']} continues to scale.

I would welcome the opportunity to discuss how my background and skills align with {job['company']}'s goals. Thank you for considering my application.

Best regards,
{candidate['name']}
{candidate['email']}"""

        # LinkedIn Message
        materials[
            "linkedin_message"
        ] = f"""Hi [Hiring Manager],

I recently came across the {job['title']} opening at {job['company']} and was immediately drawn to your mission.

With {candidate['experience_years']}+ years building scalable backend systems and expertise in Python, Kubernetes, and microservices, I believe I could contribute significantly to your team.

Would you be open to a brief conversation about this opportunity?

Best,
{candidate['name']}"""

        # Follow-up Email
        materials[
            "followup_email"
        ] = f"""Subject: Following Up - {job['title']} Application

Hi [Hiring Manager],

I wanted to follow up on my application for the {job['title']} position submitted on [DATE].

I remain very interested in this opportunity and believe my experience with microservices architecture and cloud-native systems aligns well with {job['company']}'s technical challenges.

Would you be available for a brief conversation about the role?

Thank you,
{candidate['name']}"""

        # Networking Email
        materials[
            "networking_email"
        ] = f"""Subject: Exploring Opportunities at {job['company']}

Hi [Name],

I noticed you work at {job['company']} and have experience with [SKILL from their profile].

I'm exploring opportunities in cloud-native infrastructure and was impressed by {job['company']}'s work in this space. With {candidate['experience_years']} years of experience building scalable backend systems, I'm excited about the potential to contribute.

Would you be open to a brief 15-minute conversation about your experience at {job['company']} and the engineering culture there?

Thanks for considering!
{candidate['name']}"""

        return materials

    def _generate_complete_report(
        self,
        candidate: Dict,
        job: Dict,
        match_results: Dict,
        quality_gates: Dict,
        learning_plan: Dict,
        application_materials: Dict,
    ) -> str:
        """Generate comprehensive markdown report"""

        learning_plan_section = ""
        if learning_plan:
            learning_plan_section = f"""
**Total Duration:** {learning_plan['total_weeks']} weeks
**Total Study Time:** {learning_plan['total_hours']} hours
**Weekly Commitment:** {learning_plan['weekly_commitment']} hours/week

### Sprints

{chr(10).join(f"**Sprint {s['sprint']}** ({s['duration_weeks']} weeks): {s['skill']} - {s['estimated_hours']} hours" for s in learning_plan['sprints'])}
"""
        else:
            learning_plan_section = "No learning plan needed - all requirements met!"

        skill_gaps_section = ""
        if match_results["skill_gaps"]:
            skill_gaps_section = chr(10).join(
                f"- {g['skill']}: Current {g['actual']}/5, Target {g['required']}/5 (Gap: {g['gap']}, Priority: {g['priority']})"
                for g in match_results["skill_gaps"]
            )
        else:
            skill_gaps_section = "None - all requirements met!"

        report = f"""# Job Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analysis Engine:** Advanced Job Engine v2.0.0

---

## Executive Summary

### Overall Match Score: **{match_results['overall_score']}%**

**Recommendation:** {match_results['recommendation']}

---

## Position Details

**Role:** {job['title']}
**Company:** {job['company']}
**Location:** {job['location']}
**Salary Range:** {job['salary_range']}
**Experience Required:** {job['experience_required']}+ years

---

## Candidate Profile

**Name:** {candidate['name']}
**Current Role:** {candidate['current_role']} at {candidate['current_company']}
**Total Experience:** {candidate['experience_years']} years
**Skills Count:** {len(candidate['skills'])} technical skills
**Certifications:** {', '.join(candidate['certifications'])}

---

## Match Analysis

**Technical Skills:** {match_results['technical_score']}%
**Experience Match:** {match_results['experience_score']}%
**Required Skills Coverage:** {match_results['required_coverage']}%

### Matched Skills
{chr(10).join(f"- {m['skill']}: {m['actual']}/5 (required: {m['required']}/5)" for m in match_results['required_matches'])}

### Skills to Develop
{skill_gaps_section}

---

## Quality Gate Assessment

**Foundational Gate:** {"✓ PASSED" if quality_gates['foundational']['passed'] else "✗ FAILED"}
**Competitive Gate:** {"✓ PASSED" if quality_gates['competitive']['passed'] else "⚠ NEARLY PASSED"}
**Excellence Gate:** {"✓ PASSED" if quality_gates['excellence']['passed'] else "✗ NOT PASSED"}

---

## Learning Plan

{learning_plan_section}

---

## Next Steps

1. {'Review learning plan and begin skill development' if match_results['skill_gaps'] else 'Update resume with keyword optimization'}
2. Customize application materials
3. Research {job['company']} thoroughly
4. Apply with confidence
5. Prepare for interviews

---

*Generated by Advanced Job Engine*
"""

        return report

    def _save_results(self, export_dir: Path, results: Dict):
        """Save all results to export directory"""
        # Save markdown report
        with open(export_dir / "complete_report.md", "w") as f:
            f.write(results["report"])

        # Save JSON data
        with open(export_dir / "match_results.json", "w") as f:
            json.dump(results["match_results"], f, indent=2)

        with open(export_dir / "quality_gates.json", "w") as f:
            json.dump(results["quality_gates"], f, indent=2)

        if results["learning_plan"]:
            with open(export_dir / "learning_plan.json", "w") as f:
                json.dump(results["learning_plan"], f, indent=2)

        if results["application_materials"]:
            for material_type, content in results["application_materials"].items():
                with open(export_dir / f"{material_type}.txt", "w") as f:
                    f.write(content)

    def _load_config(self) -> Dict:
        """Load configuration"""
        config_path = self.data_dir / "config.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                return json.load(f)
        return {"version": "2.0.0"}


def main():
    """Run complete workflow demonstration"""
    engine = AdvancedJobEngine()

    # Example usage
    cv_path = "data/sample_cv.pdf"
    job_path = "data/sample_job.pdf"

    results = engine.run_complete_workflow(
        cv_path=cv_path, job_path=job_path, generate_materials=True, create_learning_plan=True
    )

    print("\n📈 Final Results:")
    print(f"Match Score: {results['match_score']}%")
    print(f"Recommendation: {results['recommendation']}")
    print(f"Export Location: {results['export_dir']}")

    if results["learning_plan"]:
        print(f"\nLearning Plan: {results['learning_plan']['total_weeks']} weeks")
        print(f"Study Time: {results['learning_plan']['total_hours']} hours")


if __name__ == "__main__":
    main()
