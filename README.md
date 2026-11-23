
# Assignment 6: Medians, Order Statistics, and Elementary Data Structures

**Course:** MSCS-532 Algorithms and Data Structures  
**Student:** Mani Deep Kumar Pusuluri

## Overview
This assignment implements and analyzes two selection algorithms
and five elementary data structures using Python 3.10.

## Part 1: Selection Algorithms
- Deterministic Median of Medians: O(n) worst-case time
- Randomized Quickselect: O(n) expected time, O(n²) worst case
- Both support duplicate and negative integer values.
- The kth smallest element uses 1-based indexing.

## Part 2: Elementary Data Structures
- Dynamic array: insertion, deletion, and indexed access
- Fixed-size matrix: cell assignment, clearing, and access
- Array-based stack: push, pop, and peek
- Circular array queue: enqueue, dequeue, and peek
- Singly linked list: insertion, deletion, search, and traversal

## Run the Code
```powershell
python selection_algorithms.py
python elementary_structures.py
python -m unittest discover -v
python benchmark.py
```

## Testing
All 42 automated tests passed.

## Benchmark Methodology
The selection algorithms were compared using random, sorted,
and reverse-sorted inputs containing 100, 1000, 5000, and
10000 elements.

Each algorithm was measured seven times per scenario using
time.perf_counter(). The median runtime was recorded in
milliseconds.

The benchmark validates correctness against Python's sorted()
result and excludes reference sorting and dataset generation
from the timed measurements.

## Results
The benchmark produced 12 scenarios and 168 timed executions.

For random inputs with 10000 elements:
- Median of Medians: 8.5288 ms
- Randomized Quickselect: 4.4855 ms

For sorted inputs with 10000 elements:
- Median of Medians: 4.5079 ms
- Randomized Quickselect: 6.0177 ms

Results depend on the dataset, runtime environment, and
random pivot choices.

## Files
- selection_algorithms.py
- elementary_structures.py
- test_selection.py
- test_structures.py
- benchmark.py
- benchmark_results.csv
- assignment6_random_chart.png
- assignment6_sorted_chart.png
- assignment6_reverse_sorted_chart.png
- Assignment6_Report.pdf

## Limitations
The selection implementations support integer lists.
The deterministic implementation allocates temporary lists.
The matrix uses fixed dimensions, and the singly linked list
does not maintain a tail pointer.
