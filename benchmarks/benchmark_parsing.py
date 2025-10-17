#!/usr/bin/env python3
"""
Benchmark script for CV and Job Description parsing performance.

Tests parsing speed, accuracy, and resource usage across different:
- File sizes
- File formats (.txt, .pdf, .docx)
- Content complexity
- Number of skills/keywords

Usage:
    python benchmark_parsing.py
    python benchmark_parsing.py --format pdf
    python benchmark_parsing.py --iterations 100
"""

import argparse
import json
import os
import sys
import time
import tracemalloc
from datetime import datetime
from typing import Dict

from src.python_advanced_job_engine import AdvancedJobEngine

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class ParsingBenchmark:
    """Benchmark suite for parsing operations."""

    def __init__(self, iterations: int = 50):
        self.engine = AdvancedJobEngine()
        self.iterations = iterations
        self.results = {"cv_parsing": [], "job_parsing": [], "summary": {}}

    def generate_sample_cv(self, complexity: str = "medium") -> str:
        """Generate sample CV with varying complexity."""

        base_cv = """
John Doe
Senior Software Engineer
john.doe@email.com | +1-555-0123 | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with {exp_years} years in full-stack development.

TECHNICAL SKILLS
"""

        skill_sets = {
            "simple": ["Python", "JavaScript", "HTML", "CSS", "Git"],
            "medium": [
                "Python",
                "JavaScript",
                "TypeScript",
                "React",
                "Node.js",
                "Django",
                "Flask",
                "PostgreSQL",
                "MongoDB",
                "Docker",
                "Git",
                "AWS",
                "Linux",
                "REST APIs",
                "GraphQL",
            ],
            "complex": [
                "Python",
                "JavaScript",
                "TypeScript",
                "Go",
                "Rust",
                "React",
                "Vue.js",
                "Angular",
                "Next.js",
                "Node.js",
                "Django",
                "Flask",
                "FastAPI",
                "Express",
                "NestJS",
                "PostgreSQL",
                "MongoDB",
                "Redis",
                "Elasticsearch",
                "Docker",
                "Kubernetes",
                "Terraform",
                "Jenkins",
                "AWS",
                "Azure",
                "GCP",
                "Git",
                "GitHub Actions",
                "Linux",
                "Nginx",
                "REST APIs",
                "GraphQL",
                "gRPC",
                "Microservices",
                "CI/CD",
                "TDD",
                "Agile",
                "Scrum",
            ],
        }

        experiences = {"simple": 3, "medium": 5, "complex": 8}

        exp_years = experiences.get(complexity, 5)
        skills = skill_sets.get(complexity, skill_sets["medium"])

        cv = base_cv.format(exp_years=exp_years)
        cv += "- " + ", ".join(skills) + "\n\n"

        cv += """
EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2020 - Present
- Led development of microservices architecture
- Improved system performance by 40%
- Mentored team of 5 junior developers

Software Engineer | StartupXYZ | 2018 - 2020
- Built full-stack web applications
- Implemented CI/CD pipelines
- Collaborated with cross-functional teams

EDUCATION
Bachelor of Science in Computer Science | Tech University | 2018

CERTIFICATIONS
- AWS Certified Solutions Architect
- Certified Kubernetes Administrator
"""
        return cv

    def generate_sample_job(self, complexity: str = "medium") -> str:
        """Generate sample job description with varying complexity."""

        base_job = """
Senior Full Stack Engineer

Company: Innovation Labs

ABOUT THE ROLE
We are seeking a talented engineer to join our team.

REQUIREMENTS
"""

        requirement_sets = {
            "simple": [
                "3+ years experience",
                "Python or JavaScript",
                "Database experience",
                "Git version control",
            ],
            "medium": [
                "5+ years software development experience",
                "Strong proficiency in Python and JavaScript",
                "Experience with React and Node.js",
                "Database design (SQL and NoSQL)",
                "Docker and container orchestration",
                "Cloud platforms (AWS/Azure/GCP)",
                "RESTful API design",
                "Agile methodologies",
            ],
            "complex": [
                "7+ years full-stack development experience",
                "Expert-level Python, JavaScript/TypeScript",
                "Modern frontend frameworks (React, Vue, Angular)",
                "Backend frameworks (Django, Flask, FastAPI, Node.js)",
                "Microservices architecture and design patterns",
                "Container orchestration (Kubernetes, Docker Swarm)",
                "Cloud-native development (AWS, Azure, GCP)",
                "Database optimization (PostgreSQL, MongoDB, Redis)",
                "Message queues (RabbitMQ, Kafka)",
                "CI/CD pipelines and DevOps practices",
                "Infrastructure as Code (Terraform, CloudFormation)",
                "Security best practices and OWASP guidelines",
                "Performance optimization and scalability",
                "Technical leadership and mentoring",
                "System design and architecture",
            ],
        }

        requirements = requirement_sets.get(complexity, requirement_sets["medium"])
        job = base_job

        for req in requirements:
            job += f"- {req}\n"

        job += """
PREFERRED QUALIFICATIONS
- Master's degree in Computer Science
- Open source contributions
- Conference speaking experience

RESPONSIBILITIES
- Design and implement scalable systems
- Lead technical decisions
- Mentor junior developers
- Collaborate with product team
"""
        return job

    def benchmark_cv_parsing(self, text: str, label: str) -> Dict:
        """Benchmark CV parsing performance."""
        times = []
        memories = []
        result = None

        for i in range(self.iterations):
            # Start memory tracking
            tracemalloc.start()

            # Time the parsing
            start_time = time.perf_counter()
            result = self.engine.parse_cv(text)
            end_time = time.perf_counter()

            # Get memory usage
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            times.append(end_time - start_time)
            memories.append(peak / 1024 / 1024)  # Convert to MB

        return {
            "label": label,
            "iterations": self.iterations,
            "avg_time_ms": sum(times) / len(times) * 1000,
            "min_time_ms": min(times) * 1000,
            "max_time_ms": max(times) * 1000,
            "avg_memory_mb": sum(memories) / len(memories),
            "skills_extracted": len(result.get("skills", [])),
            "experience_years": result.get("experience_years", 0),
        }

    def benchmark_job_parsing(self, text: str, label: str) -> Dict:
        """Benchmark job description parsing performance."""
        times = []
        memories = []
        result = None

        for i in range(self.iterations):
            # Start memory tracking
            tracemalloc.start()

            # Time the parsing
            start_time = time.perf_counter()
            result = self.engine.parse_job_description(text)
            end_time = time.perf_counter()

            # Get memory usage
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            times.append(end_time - start_time)
            memories.append(peak / 1024 / 1024)  # Convert to MB

        return {
            "label": label,
            "iterations": self.iterations,
            "avg_time_ms": sum(times) / len(times) * 1000,
            "min_time_ms": min(times) * 1000,
            "max_time_ms": max(times) * 1000,
            "avg_memory_mb": sum(memories) / len(memories),
            "required_skills": len(result.get("required_skills", [])),
            "preferred_skills": len(result.get("preferred_skills", [])),
        }

    def run_cv_benchmarks(self):
        """Run all CV parsing benchmarks."""
        print("\n" + "=" * 70)
        print("CV PARSING BENCHMARKS")
        print("=" * 70)

        complexities = ["simple", "medium", "complex"]

        for complexity in complexities:
            print(f"\nBenchmarking CV parsing ({complexity} complexity)...")
            cv_text = self.generate_sample_cv(complexity)
            result = self.benchmark_cv_parsing(cv_text, f"CV_{complexity}")
            self.results["cv_parsing"].append(result)

            print(f"  Average time: {result['avg_time_ms']:.2f}ms")
            print(f"  Min time: {result['min_time_ms']:.2f}ms")
            print(f"  Max time: {result['max_time_ms']:.2f}ms")
            print(f"  Avg memory: {result['avg_memory_mb']:.2f}MB")
            print(f"  Skills extracted: {result['skills_extracted']}")
            print(f"  Experience years: {result['experience_years']}")

    def run_job_benchmarks(self):
        """Run all job parsing benchmarks."""
        print("\n" + "=" * 70)
        print("JOB DESCRIPTION PARSING BENCHMARKS")
        print("=" * 70)

        complexities = ["simple", "medium", "complex"]

        for complexity in complexities:
            print(f"\nBenchmarking job parsing ({complexity} complexity)...")
            job_text = self.generate_sample_job(complexity)
            result = self.benchmark_job_parsing(job_text, f"Job_{complexity}")
            self.results["job_parsing"].append(result)

            print(f"  Average time: {result['avg_time_ms']:.2f}ms")
            print(f"  Min time: {result['min_time_ms']:.2f}ms")
            print(f"  Max time: {result['max_time_ms']:.2f}ms")
            print(f"  Avg memory: {result['avg_memory_mb']:.2f}MB")
            print(f"  Required skills: {result['required_skills']}")
            print(f"  Preferred skills: {result['preferred_skills']}")

    def generate_summary(self):
        """Generate benchmark summary statistics."""
        cv_times = [r["avg_time_ms"] for r in self.results["cv_parsing"]]
        job_times = [r["avg_time_ms"] for r in self.results["job_parsing"]]

        self.results["summary"] = {
            "total_iterations": self.iterations
            * (len(self.results["cv_parsing"]) + len(self.results["job_parsing"])),
            "cv_parsing": {
                "avg_time_ms": sum(cv_times) / len(cv_times) if cv_times else 0,
                "total_tests": len(self.results["cv_parsing"]),
            },
            "job_parsing": {
                "avg_time_ms": sum(job_times) / len(job_times) if job_times else 0,
                "total_tests": len(self.results["job_parsing"]),
            },
            "timestamp": datetime.now().isoformat(),
        }

    def print_summary(self):
        """Print benchmark summary."""
        print("\n" + "=" * 70)
        print("BENCHMARK SUMMARY")
        print("=" * 70)

        summary = self.results["summary"]
        print(f"\nTotal iterations: {summary['total_iterations']}")
        print("\nCV Parsing:")
        print(f"  Tests run: {summary['cv_parsing']['total_tests']}")
        print(f"  Average time: {summary['cv_parsing']['avg_time_ms']:.2f}ms")

        print("\nJob Parsing:")
        print(f"  Tests run: {summary['job_parsing']['total_tests']}")
        print(f"  Average time: {summary['job_parsing']['avg_time_ms']:.2f}ms")

        print(f"\nTimestamp: {summary['timestamp']}")

    def save_results(self, output_dir: str = "benchmarks/results"):
        """Save benchmark results to JSON file."""
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"parsing_benchmark_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✅ Results saved to: {filepath}")
        return filepath

    def run_all(self):
        """Run all benchmarks."""
        print("\n" + "=" * 70)
        print("ADVANCED JOB ENGINE - PARSING BENCHMARKS")
        print("=" * 70)
        print(f"Iterations per test: {self.iterations}")

        self.run_cv_benchmarks()
        self.run_job_benchmarks()
        self.generate_summary()
        self.print_summary()
        self.save_results()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Benchmark CV and job description parsing performance"
    )
    parser.add_argument(
        "--iterations", type=int, default=50, help="Number of iterations per test (default: 50)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="benchmarks/results",
        help="Output directory for results (default: benchmarks/results)",
    )

    args = parser.parse_args()

    # Run benchmarks
    benchmark = ParsingBenchmark(iterations=args.iterations)
    benchmark.run_all()

    if args.output:
        benchmark.save_results(args.output)


if __name__ == "__main__":
    main()
