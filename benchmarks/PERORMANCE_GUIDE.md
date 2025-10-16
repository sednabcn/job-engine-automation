# Performance Testing Guide

Complete guide for performance testing, optimization, and benchmarking.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Understanding Benchmarks](#understanding-benchmarks)
- [Running Benchmarks](#running-benchmarks)
- [Interpreting Results](#interpreting-results)
- [Optimization Tips](#optimization-tips)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Run All Benchmarks

```bash
# Simple run
bash benchmarks/run_all_benchmarks.sh

# With custom iterations
bash benchmarks/run_all_benchmarks.sh 200

# Or run individually
python benchmarks/benchmark_parsing.py
python benchmarks/benchmark_matching.py
python benchmarks/analyze_benchmarks.py
```

### Expected Output

```
PARSING PERFORMANCE TRENDS
==========================
CV Parsing Performance:
  Mean: 3.45ms
  Median: 3.42ms
  Min: 3.12ms
  Max: 4.89ms

✅ No regressions detected!
```

---

## 📊 Understanding Benchmarks

### What Gets Measured

#### 1. **Parsing Performance**
- **Time**: How long to extract data from CVs/jobs
- **Memory**: RAM usage during parsing
- **Accuracy**: Number of skills/requirements extracted

#### 2. **Matching Performance**
- **Time**: How long to calculate match scores
- **Throughput**: Matches processed per second
- **Consistency**: Score variance across runs

#### 3. **Scalability**
- Performance with different input sizes
- Memory usage growth
- Degradation patterns

### Performance Targets

| Operation | Target | Good | Acceptable | Poor |
|-----------|--------|------|------------|------|
| CV Parsing | <3ms | 3-5ms | 5-10ms | >10ms |
| Job Parsing | <4ms | 4-6ms | 6-12ms | >12ms |
| Single Match | <5ms | 5-8ms | 8-15ms | >15ms |
| Batch (100) | <2s | 2-4s | 4-8s | >8s |
| Memory/Match | <2MB | 2-5MB | 5-10MB | >10MB |

---

## 🏃 Running Benchmarks

### Basic Runs

```bash
# Quick test (10 iterations)
python benchmarks/benchmark_parsing.py --iterations 10

# Standard test (50 iterations)
python benchmarks/benchmark_parsing.py --iterations 50

# Production test (500 iterations)
python benchmarks/benchmark_parsing.py --iterations 500
```

### Targeted Testing

```bash
# Test only parsing
python benchmarks/benchmark_parsing.py

# Test only matching
python benchmarks/benchmark_matching.py

# Test specific batch size
python benchmarks/benchmark_matching.py --batch-size 200

# Custom output location
python benchmarks/benchmark_parsing.py --output my_results/
```

### Comparative Testing

```bash
# Run baseline
python benchmarks/benchmark_matching.py

# Make code changes
# ...

# Run comparison
python benchmarks/benchmark_matching.py --compare benchmarks/results/matching_benchmark_*.json
```

---

## 📈 Interpreting Results

### Reading Output

#### Parsing Benchmark Output

```
CV PARSING BENCHMARKS
=====================
Benchmarking CV parsing (medium complexity)...
  Average time: 3.67ms      ← Main metric
  Min time: 3.21ms          ← Best case
  Max time: 5.12ms          ← Worst case
  Avg memory: 1.56MB        ← Memory usage
  Skills extracted: 15      ← Accuracy check
```

**What to look for:**
- ✅ Average time < 5ms
- ✅ Small gap between min/max (consistent)
- ✅ Memory usage < 5MB
- ✅ Correct number of skills extracted

#### Matching Benchmark Output

```
SINGLE MATCH BENCHMARKS
=======================
Benchmarking perfect_match...
  Average time: 5.23ms      ← Main metric
  Average score: 92.5%      ← Expected score
  Score variance: 0.03%     ← Consistency
  Memory usage: 2.34MB      ← Memory per match
```

**What to look for:**
- ✅ Average time < 8ms
- ✅ Score matches expectations
- ✅ Low variance (<1%)
- ✅ Memory < 5MB

#### Batch Processing Output

```
BATCH PROCESSING BENCHMARKS
============================
Benchmarking batch size: 50...
  Total time: 245.67ms
  Time per match: 4.91ms            ← Efficiency
  Throughput: 203.52 matches/sec    ← Speed metric
  Peak memory: 12.45MB              ← Total memory
```

**What to look for:**
- ✅ Throughput > 150 matches/sec
- ✅ Time per match similar to single match
- ✅ Linear memory growth

### Analysis Report

```
REGRESSION DETECTION
====================
Threshold: 5.0% degradation

⚠️  Found 1 regression(s):

  Single Match:
    Baseline: 5.23ms
    Current:  6.12ms
    Change:   +17.0%
```

**Action items:**
- 🔍 Investigate what changed
- 🔄 Profile the code
- 📊 Check if it's acceptable
- ⏪ Consider reverting changes

---

## ⚡ Optimization Tips

### Common Bottlenecks

#### 1. **Slow Parsing**

**Symptoms:**
- Parsing time >10ms
- High memory usage

**Solutions:**
```python
# Use compiled regex (faster)
import re
SKILL_PATTERN = re.compile(r'\b(python|javascript|docker)\b', re.IGNORECASE)

# Cache parsed results
from functools import lru_cache

@lru_cache(maxsize=128)
def parse_cv(cv_text: str):
    # Parsing logic
    pass

# Use faster PDF libraries
# Replace PyPDF2 with pdfplumber or PyMuPDF
```

#### 2. **Slow Matching**

**Symptoms:**
- Match calculation >15ms
- Low batch throughput

**Solutions:**
```python
# Pre-compile skill sets
def __init__(self):
    self.skill_set = set(COMMON_SKILLS)  # O(1) lookup

# Avoid repeated calculations
def calculate_match_score(self, cv_data, job_data):
    # Cache intermediate results
    cv_skills_set = set(cv_data['skills'])
    job_skills_set = set(job_data['required_skills'])
    
    # Set intersection is faster than loops
    matched_skills = cv_skills_set & job_skills_set

# Use numpy for numerical operations
import numpy as np
weights = np.array([0.35, 0.15, 0.20, 0.10, 0.05, 0.15])
scores = np.array([skill_score, pref_score, ...])
total = np.dot(weights, scores)
```

#### 3. **Memory Issues**

**Symptoms:**
- Memory usage >10MB per match
- Growing memory in batch processing

**Solutions:**
```python
# Clear intermediate data
def calculate_match_score(self, cv_data, job_data):
    result = self._calculate(cv_data, job_data)
    # Don't keep references to large objects
    return result

# Use generators for batch processing
def batch_analyze(self, jobs):
    for job in jobs:
        yield self.analyze(job)
        # Memory freed after each yield

# Limit string operations
# Use string slicing instead of concatenation
text = text[:1000]  # Faster than text = text + more_text
```

### Profiling

#### Time Profiling

```bash
# Profile a benchmark
python -m cProfile -o profile.stats benchmarks/benchmark_matching.py

# View results
python -m pstats profile.stats
>>> sort cumtime
>>> stats 20
```

#### Memory Profiling

```bash
# Install memory profiler
pip install memory_profiler

# Profile memory
python -m memory_profiler benchmarks/benchmark_matching.py

# Or use tracemalloc (built-in)
import tracemalloc
tracemalloc.start()
# ... your code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

#### Line-by-Line Profiling

```bash
# Install line_profiler
pip install line_profiler

# Add @profile decorator to function
@profile
def calculate_match_score(self, cv_data, job_data):
    # Your code

# Run profiler
kernprof -l -v benchmarks/benchmark_matching.py
```

---

## 🎯 Best Practices

### Before Benchmarking

1. **Close unnecessary programs**
   - Free up CPU and memory
   - Disable background tasks

2. **Use consistent hardware**
   - Same machine for comparisons
   - Note hardware specs

3. **Warm up runs**
   - First run may be slower (cold start)
   - Discard first result

4. **Multiple iterations**
   - Minimum 50 iterations
   - 100+ for production benchmarks
   - 500+ for release testing

### During Development

1. **Baseline first**
   ```bash
   # Run before changes
   python benchmarks/benchmark_matching.py
   git commit -m "Baseline benchmark"
   ```

2. **Iterative testing**
   ```bash
   # After each optimization
   python benchmarks/benchmark_matching.py --iterations 50
   # Compare results
   ```

3. **Document changes**
   ```bash
   # Keep notes
   echo "Optimized regex compilation: -15% time" >> benchmarks/optimization_log.txt
   ```

### For CI/CD

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on: [pull_request]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Baseline benchmark
        run: |
          git checkout main
          python benchmarks/benchmark_matching.py
          mv benchmarks/results results_baseline
      
      - name: Current benchmark
        run: |
          git checkout ${{ github.head_ref }}
          python benchmarks/benchmark_matching.py
      
      - name: Compare
        run: |
          python benchmarks/analyze_benchmarks.py
          # Fail if >10% regression
```

---

## 🛠️ Troubleshooting

### Inconsistent Results

**Problem:** Results vary wildly between runs

**Solutions:**
- Increase iterations (100+)
- Close background programs
- Check system load
- Run on dedicated hardware
- Use median instead of mean

### Slow Benchmarks

**Problem:** Benchmarks take too long

**Solutions:**
```bash
# Reduce iterations for quick tests
python benchmarks/benchmark_parsing.py --iterations 10

# Test subset
python benchmarks/benchmark_matching.py --batch-size 10

# Skip heavy tests (modify script)
```

### Out of Memory

**Problem:** Benchmarks crash with memory errors

**Solutions:**
```bash
# Reduce batch size
python benchmarks/benchmark_matching.py --batch-size 25

# Monitor memory
python -m memory_profiler benchmarks/benchmark_matching.py

# Find memory leaks
import tracemalloc
# ... add to script ...
```

### Regression False Positives

**Problem:** Detected regression isn't real

**Solutions:**
- Check if it's within noise (±2%)
- Run multiple times for confirmation
- Adjust threshold: `--threshold 10.0`
- Compare on same hardware
- Verify code changes actually affect performance

---

## 📊 Benchmark Metrics Explained

### Time Metrics

| Metric | Meaning | Good Value |
|--------|---------|------------|
| **Average** | Mean time across iterations | Use for trends |
| **Median** | Middle value (robust to outliers) | Most reliable |
| **Min** | Best case performance | Theoretical limit |
| **Max** | Worst case performance | Outlier detection |
| **Std Dev** | Consistency measure | Lower is better |

### Memory Metrics

| Metric | Meaning | Impact |
|--------|---------|--------|
| **Average** | Typical memory usage | Scaling indicator |
| **Peak** | Maximum memory reached | System requirements |
| **Per-operation** | Memory per match/parse | Efficiency measure |

### Throughput Metrics

| Metric | Meaning | Use Case |
|--------|---------|----------|
| **Matches/sec** | Processing speed | Batch performance |
| **Operations/sec** | Generic throughput | Overall speed |
| **Latency** | Time per operation | User experience |

---

## 📝 Reporting

### Generate Report

```bash
# Run full analysis
python benchmarks/analyze_benchmarks.py > performance_report.txt

# Include in documentation
cat performance_report.txt
```

### Report Template

```markdown
## Performance Report - [Date]

### System Info
- CPU: Intel i7-9700K
- RAM: 16GB
- Python: 3.10.5

### Results Summary
- CV Parsing: 3.45ms (target: <5ms) ✅
- Job Parsing: 4.12ms (target: <6ms) ✅
- Single Match: 6.23ms (target: <8ms) ✅
- Batch Throughput: 198 matches/sec (target: >150) ✅

### Compared to Previous
- CV Parsing: +2.3% (acceptable)
- Matching: -5.1% (improved!)

### Recommendations
- Consider caching for repeated jobs
- Optimize skill pattern matching
- Monitor memory growth in production
```

---

## 🎓 Advanced Topics

### Statistical Analysis

```python
from scipy import stats

# T-test for significant difference
t_stat, p_value = stats.ttest_ind(baseline_times, current_times)
if p_value < 0.05:
    print("Statistically significant change")

# Confidence intervals
import numpy as np
ci = stats.t.interval(0.95, len(times)-1,
                      loc=np.mean(times),
                      scale=stats.sem(times))
```

### Continuous Monitoring

```python
# Track performance over time
import matplotlib.pyplot as plt

dates = [...]
times = [...]

plt.plot(dates, times)
plt.axhline(y=5.0, color='r', linestyle='--', label='Target')
plt.title('Matching Performance Over Time')
plt.xlabel('Date')
plt.ylabel('Time (ms)')
plt.legend()
plt.savefig('performance_trend.png')
```

### A/B Testing

```python
# Compare two implementations
def benchmark_comparison(impl_a, impl_b, iterations=100):
    times_a = [benchmark(impl_a) for _ in range(iterations)]
    times_b = [benchmark(impl_b) for _ in range(iterations)]
    
    print(f"Implementation A: {mean(times_a):.2f}ms")
    print(f"Implementation B: {mean(times_b):.2f}ms")
    print(f"Improvement: {((mean(times_a)-mean(times_b))/mean(times_a)*100):.1f}%")
```

---

<div align="center">

## 📚 Additional Resources

[Main README](../README.md) | [Benchmarks README](README.md) | [Contributing](../CONTRIBUTING.md)

**Need help with performance?**

[💬 Discussions](https://github.com/yourusername/advanced-job-engine/discussions) | [🐛 Issues](https://github.com/yourusername/advanced-job-engine/issues)

</div>