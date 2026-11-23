
"""Benchmark deterministic and randomized selection algorithms.

The benchmark compares both algorithms using identical datasets,
multiple input sizes, and repeatable random seeds.
"""

import csv
import random
import statistics
import time

from selection_algorithms import (
    deterministic_select,
    randomized_select,
)


# Test progressively larger inputs to examine scalability.
INPUT_SIZES = [100, 1000, 5000, 10000]
DISTRIBUTIONS = ["Random", "Sorted", "Reverse Sorted"]
REPEATS = 7
OUTPUT_FILE = "benchmark_results.csv"


def create_dataset(size, distribution):
    """Create repeatable data for a particular test scenario."""

    generator = random.Random(2026 + size)

    # Use a broad integer range and allow duplicate values.
    values = [
        generator.randint(-size * 5, size * 5)
        for _ in range(size)
    ]

    if distribution == "Sorted":
        return sorted(values)

    if distribution == "Reverse Sorted":
        return sorted(values, reverse=True)

    return values


def measure_algorithm(algorithm, values, k):
    """Measure execution time while checking correctness."""

    # Calculate the correct answer outside the timed section.
    expected = sorted(values)[k - 1]

    # Warm up the function before collecting measurements.
    if algorithm == randomized_select:
        result = algorithm(values, k, random.Random(42))
    else:
        result = algorithm(values, k)

    if result != expected:
        raise AssertionError("Warm-up produced an incorrect result")

    timings = []

    for repetition in range(REPEATS):
        # Start the timer immediately before calling the algorithm.
        start = time.perf_counter()

        if algorithm == randomized_select:
            # Different repeatable seeds provide varied pivots.
            result = algorithm(
                values,
                k,
                random.Random(1000 + repetition),
            )
        else:
            result = algorithm(values, k)

        elapsed = time.perf_counter() - start

        # A benchmark result is valid only if the answer is correct.
        if result != expected:
            raise AssertionError(
                f"{algorithm.__name__} returned an incorrect result"
            )

        # Convert seconds to milliseconds for easier comparison.
        timings.append(elapsed * 1000)

    return statistics.median(timings)


def run_benchmarks():
    """Run every scenario and save results to a CSV file."""

    results = []

    print("ASSIGNMENT 6 - SELECTION ALGORITHM BENCHMARK")
    print(f"Measurements per algorithm: {REPEATS}")
    print("-" * 75)

    for distribution in DISTRIBUTIONS:
        for size in INPUT_SIZES:
            values = create_dataset(size, distribution)

            # Select the middle-ranked element.
            k = (size + 1) // 2

            deterministic_ms = measure_algorithm(
                deterministic_select, values, k
            )

            randomized_ms = measure_algorithm(
                randomized_select, values, k
            )

            # A ratio above 1 indicates Randomized Quickselect
            # was faster in this particular measurement.
            ratio = (
                deterministic_ms / randomized_ms
                if randomized_ms > 0
                else 0
            )

            results.append({
                "distribution": distribution,
                "size": size,
                "deterministic_ms": round(deterministic_ms, 6),
                "randomized_ms": round(randomized_ms, 6),
                "deterministic_to_randomized_ratio": round(ratio, 3),
            })

            print(
                f"{distribution:15} | "
                f"n={size:6} | "
                f"Deterministic={deterministic_ms:10.4f} ms | "
                f"Randomized={randomized_ms:10.4f} ms | "
                f"Ratio={ratio:.2f}"
            )

    # Store measured values so the report can use real data.
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "distribution",
                "size",
                "deterministic_ms",
                "randomized_ms",
                "deterministic_to_randomized_ratio",
            ],
        )

        writer.writeheader()
        writer.writerows(results)

    print("-" * 75)
    print(f"Completed {len(results)} benchmark scenarios.")
    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_benchmarks()
