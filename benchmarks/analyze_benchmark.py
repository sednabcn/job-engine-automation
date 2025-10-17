#!/usr/bin/env python3
"""
Analyze and aggregate benchmark results over time.

Provides insights into:
- Performance trends
- Regression detection
- Statistical analysis
- Comparison reports

Usage:
    python benchmarks/analyze_benchmarks.py
    python benchmarks/analyze_benchmarks.py --dir custom_results/
    python benchmarks/analyze_benchmarks.py --report html
"""

import argparse
import json
import os
from statistics import mean, median, stdev


class BenchmarkAnalyzer:
    """Analyze benchmark results over time."""

    def __init__(self, results_dir: str = "benchmarks/results"):
        self.results_dir = results_dir
        self.parsing_results = []
        self.matching_results = []

    def load_results(self):
        """Load all benchmark result files."""
        if not os.path.exists(self.results_dir):
            print(f"❌ Results directory not found: {self.results_dir}")
            return

        files = sorted(os.listdir(self.results_dir))

        for filename in files:
            filepath = os.path.join(self.results_dir, filename)

            try:
                with open(filepath, "r") as f:
                    data = json.load(f)

                if filename.startswith("parsing_benchmark_"):
                    self.parsing_results.append({"filename": filename, "data": data})
                elif filename.startswith("matching_benchmark_"):
                    self.matching_results.append({"filename": filename, "data": data})
            except Exception as e:
                print(f"⚠️  Could not load {filename}: {e}")

        print(f"\n✅ Loaded {len(self.parsing_results)} parsing results")
        print(f"✅ Loaded {len(self.matching_results)} matching results")

    def analyze_parsing_trends(self):
        """Analyze parsing performance trends."""
        if not self.parsing_results:
            print("\n⚠️  No parsing results to analyze")
            return

        print("\n" + "=" * 70)
        print("PARSING PERFORMANCE TRENDS")
        print("=" * 70)

        # Extract CV parsing times over time
        data = []
        timestamps = []
        cv_times = []
        job_times = []

        for result in self.parsing_results:
            data = result["data"]
            timestamp = data["summary"].get("timestamp", "")
            timestamps.append(timestamp)

            cv_avg = data["summary"]["cv_parsing"]["avg_time_ms"]
            job_avg = data["summary"]["job_parsing"]["avg_time_ms"]

            cv_times.append(cv_avg)
            job_times.append(job_avg)

        # Statistics
        print("\nCV Parsing Performance:")
        print(f"  Mean: {mean(cv_times):.2f}ms")
        print(f"  Median: {median(cv_times):.2f}ms")
        if len(cv_times) > 1:
            print(f"  Std Dev: {stdev(cv_times):.2f}ms")
        print(f"  Min: {min(cv_times):.2f}ms")
        print(f"  Max: {max(cv_times):.2f}ms")

        print("\nJob Parsing Performance:")
        print(f"  Mean: {mean(job_times):.2f}ms")
        print(f"  Median: {median(job_times):.2f}ms")
        if len(job_times) > 1:
            print(f"  Std Dev: {stdev(job_times):.2f}ms")
        print(f"  Min: {min(job_times):.2f}ms")
        print(f"  Max: {max(job_times):.2f}ms")

        # Trend analysis
        if len(cv_times) >= 2:
            cv_trend = cv_times[-1] - cv_times[0]
            job_trend = job_times[-1] - job_times[0]

            print("\nTrend (latest vs. earliest):")
            print(f"  CV Parsing: {cv_trend:+.2f}ms " f"({(cv_trend / cv_times[0] * 100):+.1f}%)")
            print(
                f"  Job Parsing: {job_trend:+.2f}ms " f"({(job_trend / job_times[0] * 100):+.1f}%)"
            )

            if cv_trend < -0.5 or job_trend < -0.5:
                print("  ✅ Performance improved!")
            elif cv_trend > 0.5 or job_trend > 0.5:
                print("  ⚠️  Performance regressed")
            else:
                print("  ➡️  Performance stable")

    def analyze_matching_trends(self):
        """Analyze matching performance trends."""
        if not self.matching_results:
            print("\n⚠️  No matching results to analyze")
            return

        print("\n" + "=" * 70)
        print("MATCHING PERFORMANCE TRENDS")
        print("=" * 70)

        # Extract matching times and throughput
        data = []
        timestamps = []
        match_times = []
        throughputs = []

        for result in self.matching_results:
            data = result["data"]
            timestamp = data["summary"].get("timestamp", "")
            timestamps.append(timestamp)

            match_avg = data["summary"]["single_match"]["avg_time_ms"]
            throughput = data["summary"]["batch_processing"]["max_throughput"]

            match_times.append(match_avg)
            throughputs.append(throughput)

        # Statistics
        print("\nSingle Match Performance:")
        print(f"  Mean: {mean(match_times):.2f}ms")
        print(f"  Median: {median(match_times):.2f}ms")
        if len(match_times) > 1:
            print(f"  Std Dev: {stdev(match_times):.2f}ms")
        print(f"  Min: {min(match_times):.2f}ms (fastest)")
        print(f"  Max: {max(match_times):.2f}ms (slowest)")

        print("\nBatch Processing Throughput:")
        print(f"  Mean: {mean(throughputs):.2f} matches/sec")
        print(f"  Median: {median(throughputs):.2f} matches/sec")
        if len(throughputs) > 1:
            print(f"  Std Dev: {stdev(throughputs):.2f}")
        print(f"  Max: {max(throughputs):.2f} matches/sec")
        print(f"  Min: {min(throughputs):.2f} matches/sec")

        # Trend analysis
        if len(match_times) >= 2:
            time_trend = match_times[-1] - match_times[0]
            throughput_trend = throughputs[-1] - throughputs[0]

            print("\nTrend (latest vs. earliest):")
            print(
                f"  Match Time: {time_trend:+.2f}ms "
                f"({(time_trend / match_times[0] * 100):+.1f}%)"
            )
            print(
                f"  Throughput: {throughput_trend:+.2f} matches/sec "
                f"({(throughput_trend / throughputs[0] * 100):+.1f}%)"
            )

            if time_trend < -0.5 and throughput_trend > 0:
                print("  ✅ Performance improved!")
            elif time_trend > 0.5 or throughput_trend < 0:
                print("  ⚠️  Performance regressed")
            else:
                print("  ➡️  Performance stable")

    def detect_regressions(self, threshold: float = 5.0):
        """Detect performance regressions."""
        print("\n" + "=" * 70)
        print("REGRESSION DETECTION")
        print("=" * 70)
        print(f"Threshold: {threshold}% degradation")

        regressions = []

        # Check parsing regressions
        if len(self.parsing_results) >= 2:
            latest = self.parsing_results[-1]["data"]
            baseline = self.parsing_results[0]["data"]

            cv_latest = latest["summary"]["cv_parsing"]["avg_time_ms"]
            cv_baseline = baseline["summary"]["cv_parsing"]["avg_time_ms"]
            cv_change = ((cv_latest - cv_baseline) / cv_baseline) * 100

            if cv_change > threshold:
                regressions.append(
                    {
                        "type": "CV Parsing",
                        "baseline": cv_baseline,
                        "current": cv_latest,
                        "change_pct": cv_change,
                    }
                )

            job_latest = latest["summary"]["job_parsing"]["avg_time_ms"]
            job_baseline = baseline["summary"]["job_parsing"]["avg_time_ms"]
            job_change = ((job_latest - job_baseline) / job_baseline) * 100

            if job_change > threshold:
                regressions.append(
                    {
                        "type": "Job Parsing",
                        "baseline": job_baseline,
                        "current": job_latest,
                        "change_pct": job_change,
                    }
                )

        # Check matching regressions
        if len(self.matching_results) >= 2:
            latest = self.matching_results[-1]["data"]
            baseline = self.matching_results[0]["data"]

            match_latest = latest["summary"]["single_match"]["avg_time_ms"]
            match_baseline = baseline["summary"]["single_match"]["avg_time_ms"]
            match_change = ((match_latest - match_baseline) / match_baseline) * 100

            if match_change > threshold:
                regressions.append(
                    {
                        "type": "Single Match",
                        "baseline": match_baseline,
                        "current": match_latest,
                        "change_pct": match_change,
                    }
                )

        # Report regressions
        if regressions:
            print(f"\n⚠️  Found {len(regressions)} regression(s):\n")
            for reg in regressions:
                print(f"  {reg['type']}:")
                print(f"    Baseline: {reg['baseline']:.2f}ms")
                print(f"    Current:  {reg['current']:.2f}ms")
                print(f"    Change:   {reg['change_pct']:+.1f}%")
                print()
        else:
            print("\n✅ No regressions detected!")

    def compare_latest_runs(self):
        """Compare the two most recent benchmark runs."""
        print("\n" + "=" * 70)
        print("LATEST RUN COMPARISON")
        print("=" * 70)

        # Compare parsing
        if len(self.parsing_results) >= 2:
            previous = self.parsing_results[-2]["data"]
            latest = self.parsing_results[-1]["data"]

            print("\nParsing Performance:")
            print(f"  {'Metric':<20} {'Previous':<15} {'Latest':<15} {'Change':<10}")
            print("  " + "-" * 60)

            cv_prev = previous["summary"]["cv_parsing"]["avg_time_ms"]
            cv_latest = latest["summary"]["cv_parsing"]["avg_time_ms"]
            cv_change = ((cv_latest - cv_prev) / cv_prev) * 100

            print(
                f"  {'CV Parsing':<20} {cv_prev:<15.2f} {cv_latest:<15.2f} " f"{cv_change:>+9.1f}%"
            )

            job_prev = previous["summary"]["job_parsing"]["avg_time_ms"]
            job_latest = latest["summary"]["job_parsing"]["avg_time_ms"]
            job_change = ((job_latest - job_prev) / job_prev) * 100

            print(
                f"  {'Job Parsing':<20} {job_prev:<15.2f} {job_latest:<15.2f} "
                f"{job_change:>+9.1f}%"
            )

        # Compare matching
        if len(self.matching_results) >= 2:
            previous = self.matching_results[-2]["data"]
            latest = self.matching_results[-1]["data"]

            print("\nMatching Performance:")
            print(f"  {'Metric':<20} {'Previous':<15} {'Latest':<15} {'Change':<10}")
            print("  " + "-" * 60)

            match_prev = previous["summary"]["single_match"]["avg_time_ms"]
            match_latest = latest["summary"]["single_match"]["avg_time_ms"]
            match_change = ((match_latest - match_prev) / match_prev) * 100

            print(
                f"  {'Single Match':<20} {match_prev:<15.2f} {match_latest:<15.2f} "
                f"{match_change:>+9.1f}%"
            )

            tp_prev = previous["summary"]["batch_processing"]["max_throughput"]
            tp_latest = latest["summary"]["batch_processing"]["max_throughput"]
            tp_change = ((tp_latest - tp_prev) / tp_prev) * 100

            print(
                f"  {'Max Throughput':<20} {tp_prev:<15.2f} {tp_latest:<15.2f} "
                f"{tp_change:>+9.1f}%"
            )

    def generate_summary_report(self):
        """Generate overall summary report."""
        print("\n" + "=" * 70)
        print("BENCHMARK SUMMARY REPORT")
        print("=" * 70)

        print(f"\nResults Directory: {self.results_dir}")
        print("Total Benchmark Files: " f"{len(self.parsing_results) + len(self.matching_results)}")

        if self.parsing_results:
            print(f"\nParsing Benchmarks: {len(self.parsing_results)}")
            print(
                "  Date Range: "
                f"{self.parsing_results[0]['filename'][18:26]} to "
                f"{self.parsing_results[-1]['filename'][18:26]}"
            )

        if self.matching_results:
            print(f"\nMatching Benchmarks: {len(self.matching_results)}")
            print(
                "  Date Range: "
                f"{self.matching_results[0]['filename'][19:27]} to "
                f"{self.matching_results[-1]['filename'][19:27]}"
            )

        # Overall best performance
        if self.matching_results:
            all_match_times = []
            all_throughputs = []

            for result in self.matching_results:
                all_match_times.append(result["data"]["summary"]["single_match"]["avg_time_ms"])
                all_throughputs.append(
                    result["data"]["summary"]["batch_processing"]["max_throughput"]
                )

            print("\nBest Recorded Performance:")
            print(f"  Fastest Match: {min(all_match_times):.2f}ms")
            print(f"  Highest Throughput: {max(all_throughputs):.2f} matches/sec")

    def run_analysis(self):
        """Run complete analysis."""
        self.load_results()

        if not self.parsing_results and not self.matching_results:
            print("\n❌ No benchmark results found!")
            print("   Run benchmarks first:")
            print("   python benchmarks/benchmark_parsing.py")
            print("   python benchmarks/benchmark_matching.py")
            return

        self.analyze_parsing_trends()
        self.analyze_matching_trends()
        self.compare_latest_runs()
        self.detect_regressions()
        self.generate_summary_report()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Analyze benchmark results over time")
    parser.add_argument(
        "--dir",
        type=str,
        default="benchmarks/results",
        help="Results directory to analyze (default: benchmarks/results)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=5.0,
        help="Regression detection threshold in percent (default: 5.0)",
    )

    args = parser.parse_args()

    # Run analysis
    analyzer = BenchmarkAnalyzer(results_dir=args.dir)
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
