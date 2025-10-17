#!/usr/bin/env python3
"""
Benchmark script for CV-Job matching algorithm performance.

Tests matching speed, accuracy, and scalability across:
- Different match score ranges
- Various skill set sizes
- Multiple scoring configurations
- Batch processing scenarios

Usage:
    python benchmark_matching.py
    python benchmark_matching.py --iterations 100
    python benchmark_matching.py --batch-size 50
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


class MatchingBenchmark:
    """Benchmark suite for matching operations."""

    def __init__(self, iterations: int = 100):
        self.engine = AdvancedJobEngine()
        self.iterations = iterations
        self.results = {
            "single_match": [],
            "batch_match": [],
            "scoring_variants": [],
            "scalability": [],
            "summary": {},
        }

    def create_cv_variants(self) -> Dict[str, str]:
        """Create CV variants with different match levels."""
        base_skills = ["Python", "JavaScript", "Git", "Linux", "SQL"]

        variants = {
            "perfect_match": base_skills
            + [
                "React",
                "Node.js",
                "AWS",
                "Kubernetes",
                "CI/CD",
                "MongoDB",
                "Redis",
                "Microservices",
            ],
            "strong_match": base_skills + ["React", "Node.js", "AWS", "MongoDB"],
            "moderate_match": base_skills + ["React", "MongoDB"],
            "weak_match": base_skills,
            "poor_match": ["Python", "Git", "Linux"],
        }

        cvs = {}
        for variant_name, skills in variants.items():
            cv = f"""
John Doe
Senior Software Engineer
john.doe@email.com

PROFESSIONAL SUMMARY
Experienced software engineer with 5 years in full-stack development.

TECHNICAL SKILLS
{", ".join(skills)}

EXPERIENCE
Senior Software Engineer | TechCorp | 2020 - Present
- Led development of scalable systems
- Improved performance by 40%

Software Engineer | StartupXYZ | 2018 - 2020
- Built web applications
- Implemented CI/CD

EDUCATION
Bachelor of Science in Computer Science | 2018
"""
            cvs[variant_name] = cv

        return cvs

    def create_standard_job(self) -> str:
        """Create standard job description."""
        return """
Senior Full Stack Engineer

Company: TechCorp

REQUIREMENTS
- 5+ years software development
- Strong Python and JavaScript
- React and Node.js experience
- PostgreSQL and MongoDB
- Docker and Kubernetes
- AWS cloud platform
- CI/CD pipelines
- REST API design

PREFERRED
- Redis experience
- Microservices architecture
- Team leadership

RESPONSIBILITIES
- Design scalable systems
- Lead technical projects
- Mentor developers
"""

    def benchmark_single_match(self, cv_text: str, job_text: str, label: str) -> Dict:
        """Benchmark single CV-job matching."""
        times = []
        memories = []
        scores = []

        for i in range(self.iterations):
            # Start memory tracking
            tracemalloc.start()

            # Time the matching
            start_time = time.perf_counter()

            cv_data = self.engine.parse_cv(cv_text)
            job_data = self.engine.parse_job_description(job_text)
            score = self.engine.calculate_match_score(cv_data, job_data)

            end_time = time.perf_counter()

            # Get memory usage
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            times.append(end_time - start_time)
            memories.append(peak / 1024 / 1024)  # Convert to MB
            scores.append(score["total_score"])

        return {
            "label": label,
            "iterations": self.iterations,
            "avg_time_ms": sum(times) / len(times) * 1000,
            "min_time_ms": min(times) * 1000,
            "max_time_ms": max(times) * 1000,
            "avg_memory_mb": sum(memories) / len(memories),
            "avg_score": sum(scores) / len(scores),
            "score_variance": max(scores) - min(scores),
        }

    def benchmark_batch_matching(self, batch_size: int = 10) -> Dict:
        """Benchmark batch processing of multiple jobs."""
        cv_text = self.create_cv_variants()["strong_match"]
        job_text = self.create_standard_job()

        # Start memory tracking
        tracemalloc.start()

        # Time batch processing
        start_time = time.perf_counter()

        results = []
        for i in range(batch_size):
            cv_data = self.engine.parse_cv(cv_text)
            job_data = self.engine.parse_job_description(job_text)
            score = self.engine.calculate_match_score(cv_data, job_data)
            results.append(score["total_score"])

        end_time = time.perf_counter()

        # Get memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        total_time = end_time - start_time

        return {
            "batch_size": batch_size,
            "total_time_ms": total_time * 1000,
            "avg_time_per_match_ms": (total_time / batch_size) * 1000,
            "peak_memory_mb": peak / 1024 / 1024,
            "throughput_per_second": batch_size / total_time,
        }

    def benchmark_scoring_variants(self):
        """Benchmark different scoring weight configurations."""
        cv_text = self.create_cv_variants()["strong_match"]
        job_text = self.create_standard_job()

        weight_configs = {
            "default": {
                "required_skills": 0.35,
                "preferred_skills": 0.15,
                "experience": 0.20,
                "education": 0.10,
                "certifications": 0.05,
                "keywords": 0.15,
            },
            "skill_focused": {
                "required_skills": 0.50,
                "preferred_skills": 0.20,
                "experience": 0.15,
                "education": 0.05,
                "certifications": 0.05,
                "keywords": 0.05,
            },
            "experience_focused": {
                "required_skills": 0.25,
                "preferred_skills": 0.10,
                "experience": 0.40,
                "education": 0.15,
                "certifications": 0.05,
                "keywords": 0.05,
            },
            "balanced": {
                "required_skills": 0.30,
                "preferred_skills": 0.15,
                "experience": 0.25,
                "education": 0.15,
                "certifications": 0.05,
                "keywords": 0.10,
            },
        }

        results = []
        for config_name, weights in weight_configs.items():
            # Save original weights
            original_weights = self.engine.WEIGHTS.copy()

            # Set new weights
            self.engine.WEIGHTS = weights

            # Benchmark
            times = []
            scores = []

            for i in range(self.iterations):
                start_time = time.perf_counter()

                cv_data = self.engine.parse_cv(cv_text)
                job_data = self.engine.parse_job_description(job_text)
                score = self.engine.calculate_match_score(cv_data, job_data)

                end_time = time.perf_counter()

                times.append(end_time - start_time)
                scores.append(score["total_score"])

            results.append(
                {
                    "config": config_name,
                    "avg_time_ms": sum(times) / len(times) * 1000,
                    "avg_score": sum(scores) / len(scores),
                    "weights": weights,
                }
            )

            # Restore original weights
            self.engine.WEIGHTS = original_weights

        return results

    def benchmark_scalability(self):
        """Test performance scaling with different input sizes."""
        self.create_cv_variants()
        job_text = self.create_standard_job()

        skill_counts = [5, 10, 20, 30, 40]
        results = []

        for skill_count in skill_counts:
            # Generate CV with specific skill count
            skills = [f"Skill_{i}" for i in range(skill_count)]
            cv_text = f"""
John Doe
Engineer

SKILLS
{", ".join(skills)}

EXPERIENCE
Engineer | Company | 2020 - Present
- Work experience

EDUCATION
Bachelor's Degree | 2020
"""

            times = []
            for i in range(min(self.iterations, 50)):  # Limit iterations for large tests
                start_time = time.perf_counter()

                cv_data = self.engine.parse_cv(cv_text)
                job_data = self.engine.parse_job_description(job_text)
                self.engine.calculate_match_score(cv_data, job_data)

                end_time = time.perf_counter()
                times.append(end_time - start_time)

            results.append(
                {
                    "skill_count": skill_count,
                    "avg_time_ms": sum(times) / len(times) * 1000,
                    "min_time_ms": min(times) * 1000,
                    "max_time_ms": max(times) * 1000,
                }
            )

        return results

    def run_single_match_benchmarks(self):
        """Run single match benchmarks."""
        print("\n" + "=" * 70)
        print("SINGLE MATCH BENCHMARKS")
        print("=" * 70)

        cv_variants = self.create_cv_variants()
        job_text = self.create_standard_job()

        for variant_name, cv_text in cv_variants.items():
            print(f"\nBenchmarking {variant_name}...")
            result = self.benchmark_single_match(cv_text, job_text, variant_name)
            self.results["single_match"].append(result)

            print(f"  Average time: {result['avg_time_ms']:.2f}ms")
            print(f"  Average score: {result['avg_score']:.1f}%")
            print(f"  Score variance: {result['score_variance']:.2f}%")
            print(f"  Memory usage: {result['avg_memory_mb']:.2f}MB")

    def run_batch_benchmarks(self):
        """Run batch processing benchmarks."""
        print("\n" + "=" * 70)
        print("BATCH PROCESSING BENCHMARKS")
        print("=" * 70)

        batch_sizes = [10, 25, 50, 100]

        for batch_size in batch_sizes:
            print(f"\nBenchmarking batch size: {batch_size}...")
            result = self.benchmark_batch_matching(batch_size)
            self.results["batch_match"].append(result)

            print(f"  Total time: {result['total_time_ms']:.2f}ms")
            print(f"  Time per match: {result['avg_time_per_match_ms']:.2f}ms")
            print(f"  Throughput: {result['throughput_per_second']:.2f} matches/sec")
            print(f"  Peak memory: {result['peak_memory_mb']:.2f}MB")

    def run_scoring_benchmarks(self):
        """Run scoring variant benchmarks."""
        print("\n" + "=" * 70)
        print("SCORING CONFIGURATION BENCHMARKS")
        print("=" * 70)

        results = self.benchmark_scoring_variants()
        self.results["scoring_variants"] = results

        for result in results:
            print(f"\n{result['config']}:")
            print(f"  Average time: {result['avg_time_ms']:.2f}ms")
            print(f"  Average score: {result['avg_score']:.1f}%")

    def run_scalability_benchmarks(self):
        """Run scalability benchmarks."""
        print("\n" + "=" * 70)
        print("SCALABILITY BENCHMARKS")
        print("=" * 70)

        results = self.benchmark_scalability()
        self.results["scalability"] = results

        print("\nPerformance vs. Skill Count:")
        print(f"{'Skills':<10} {'Avg Time':<15} {'Min Time':<15} {'Max Time':<15}")
        print("-" * 55)

        for result in results:
            print(
                f"{result['skill_count']:<10} "
                f"{result['avg_time_ms']:<15.2f} "
                f"{result['min_time_ms']:<15.2f} "
                f"{result['max_time_ms']:<15.2f}"
            )

    def generate_summary(self):
        """Generate benchmark summary statistics."""
        single_times = [r["avg_time_ms"] for r in self.results["single_match"]]
        batch_throughputs = [r["throughput_per_second"] for r in self.results["batch_match"]]

        self.results["summary"] = {
            "total_tests": len(self.results["single_match"])
            + len(self.results["batch_match"])
            + len(self.results["scoring_variants"])
            + len(self.results["scalability"]),
            "single_match": {
                "avg_time_ms": sum(single_times) / len(single_times) if single_times else 0,
                "fastest_ms": min(single_times) if single_times else 0,
                "slowest_ms": max(single_times) if single_times else 0,
            },
            "batch_processing": {
                "max_throughput": max(batch_throughputs) if batch_throughputs else 0,
                "avg_throughput": (
                    sum(batch_throughputs) / len(batch_throughputs) if batch_throughputs else 0
                ),
            },
            "timestamp": datetime.now().isoformat(),
        }

    def print_summary(self):
        """Print benchmark summary."""
        print("\n" + "=" * 70)
        print("BENCHMARK SUMMARY")
        print("=" * 70)

        summary = self.results["summary"]

        print(f"\nTotal tests run: {summary['total_tests']}")

        print("\nSingle Match Performance:")
        print(f"  Average time: {summary['single_match']['avg_time_ms']:.2f}ms")
        print(f"  Fastest: {summary['single_match']['fastest_ms']:.2f}ms")
        print(f"  Slowest: {summary['single_match']['slowest_ms']:.2f}ms")

        print("\nBatch Processing:")
        print(f"  Max throughput: {summary['batch_processing']['max_throughput']:.2f} matches/sec")
        print(f"  Avg throughput: {summary['batch_processing']['avg_throughput']:.2f} matches/sec")

        print(f"\nTimestamp: {summary['timestamp']}")

    def save_results(self, output_dir: str = "benchmarks/results"):
        """Save benchmark results to JSON file."""
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"matching_benchmark_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✅ Results saved to: {filepath}")
        return filepath

    def compare_with_previous(self, previous_file: str = None):
        """Compare current results with previous benchmark."""
        results_dir = "benchmarks/results"

        if not previous_file:
            if not os.path.exists(results_dir):
                return

            # Find most recent previous file
            files = sorted(
                [
                    f
                    for f in os.listdir(results_dir)
                    if f.startswith("matching_benchmark_") and f.endswith(".json")
                ]
            )
            if len(files) < 2:
                return

            previous_file = os.path.join(results_dir, files[-2])

        try:
            with open(previous_file, "r") as f:
                previous = json.load(f)

            print("\n" + "=" * 70)
            print("COMPARISON WITH PREVIOUS BENCHMARK")
            print("=" * 70)

            previous_avg = previous["summary"]["single_match"]["avg_time_ms"]
            current_avg = self.results["summary"]["single_match"]["avg_time_ms"]

            improvement = ((previous_avg - current_avg) / previous_avg) * 100

            print("\nSingle Match Average Time:")
            print(f"  Previous: {previous_avg:.2f}ms")
            print(f"  Current:  {current_avg:.2f}ms")
            print(f"  Change:   {improvement:+.2f}%")

            if improvement > 0:
                print("  ✅ Performance improved!")
            elif improvement < -5:
                print("  ⚠️  Performance degraded!")
            else:
                print("  ➡️  Performance similar")

        except Exception as e:
            print(f"\n⚠️  Could not compare with previous: {e}")

    def run_all(self):
        """Run all benchmarks."""
        print("\n" + "=" * 70)
        print("ADVANCED JOB ENGINE - MATCHING BENCHMARKS")
        print("=" * 70)
        print(f"Iterations per test: {self.iterations}")

        self.run_single_match_benchmarks()
        self.run_batch_benchmarks()
        self.run_scoring_benchmarks()
        self.run_scalability_benchmarks()
        self.generate_summary()
        self.print_summary()
        self.save_results()
        self.compare_with_previous()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Benchmark CV-job matching algorithm performance")
    parser.add_argument(
        "--iterations", type=int, default=100, help="Number of iterations per test (default: 100)"
    )
    parser.add_argument(
        "--batch-size", type=int, default=50, help="Maximum batch size to test (default: 50)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="benchmarks/results",
        help="Output directory for results (default: benchmarks/results)",
    )
    parser.add_argument("--compare", type=str, help="Previous benchmark file to compare against")

    args = parser.parse_args()

    # Run benchmarks
    benchmark = MatchingBenchmark(iterations=args.iterations)
    benchmark.run_all()

    if args.output:
        benchmark.save_results(args.output)

    if args.compare:
        benchmark.compare_with_previous(args.compare)


if __name__ == "__main__":
    main()
