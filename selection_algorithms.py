
import random


def validate_selection(values, k):
    """Check the input before attempting to find an order statistic."""

    # Both algorithms expect a list of integers. Checking this
    # first makes invalid input easier to identify and debug.
    if not isinstance(values, list):
        raise TypeError("Input must be a list")

    if not values:
        raise ValueError("Cannot select from an empty list")

    # Boolean values are excluded because Python treats them
    # as integers, even though they are not meaningful here.
    if any(type(value) is not int for value in values):
        raise TypeError("All elements must be integers")

    # We use 1-based indexing for k: k=1 means the smallest
    # element, while k=len(values) means the largest.
    if type(k) is not int:
        raise TypeError("k must be an integer")

    if not 1 <= k <= len(values):
        raise ValueError("k is outside the valid range")


def deterministic_select(values, k):
    """Find the kth smallest value using Median of Medians."""

    validate_selection(values, k)

    # Work with a copy so the original list is not modified.
    data = values.copy()

    def select(items, position):
        # Sorting a group of at most five elements is inexpensive.
        # It also provides the base case for our recursive method.
        if len(items) <= 5:
            return sorted(items)[position - 1]

        # Divide the current input into groups of five.
        # The final group may contain fewer than five elements.
        groups = [
            items[index:index + 5]
            for index in range(0, len(items), 5)
        ]

        # Sort each small group and collect its middle value.
        # These medians help us choose a reasonably balanced pivot.
        medians = [
            sorted(group)[len(group) // 2]
            for group in groups
        ]

        # Recursively select the median of the group medians.
        # This pivot choice gives the algorithm its worst-case
        # linear-time guarantee.
        pivot = select(medians, (len(medians) + 1) // 2)

        # Separate values into three groups. The equal group
        # handles duplicates without repeatedly processing them.
        smaller = [value for value in items if value < pivot]
        equal = [value for value in items if value == pivot]
        larger = [value for value in items if value > pivot]

        # If the requested position is in the smaller group,
        # continue searching only within that group.
        if position <= len(smaller):
            return select(smaller, position)

        # Positions covered by the equal group all contain
        # the pivot, so no additional recursion is necessary.
        if position <= len(smaller) + len(equal):
            return pivot

        # Skip the smaller and equal groups when searching
        # the larger group, adjusting the requested position.
        new_position = position - len(smaller) - len(equal)
        return select(larger, new_position)

    return select(data, k)


def randomized_select(values, k, rng=None):
    """Find the kth smallest value using Randomized Quickselect."""

    validate_selection(values, k)

    # Copy the input to preserve the caller's original list.
    data = values.copy()

    # Allow a seeded generator for repeatable testing.
    # Normal usage creates a generator automatically.
    if rng is None:
        rng = random.Random()

    # Convert the requested rank into a zero-based index.
    target = k - 1
    low = 0
    high = len(data) - 1

    while low <= high:
        # Choose a random pivot from the active search range.
        # Randomization reduces the likelihood of consistently
        # choosing poor pivots for sorted or reverse-sorted data.
        pivot = data[rng.randint(low, high)]

        # Three-way partitioning groups smaller, equal, and
        # larger values together in the same list.
        left = low
        current = low
        right = high

        while current <= right:
            if data[current] < pivot:
                data[left], data[current] = data[current], data[left]
                left += 1
                current += 1

            elif data[current] > pivot:
                data[current], data[right] = data[right], data[current]
                right -= 1

            else:
                current += 1

        # After partitioning, indices before left are smaller
        # than the pivot and indices after right are larger.
        if target < left:
            high = left - 1

        elif target > right:
            low = right + 1

        else:
            return pivot

    # Valid input should always return from the loop.
    raise RuntimeError("Selection failed unexpectedly")


if __name__ == "__main__":
    sample = [12, 3, 5, 7, 4, 19, 26, 5]
    k = 4

    print("Original:", sample)
    print("Requested rank:", k)
    print("Expected value:", sorted(sample)[k - 1])
    print("Deterministic:", deterministic_select(sample, k))
    print("Randomized:", randomized_select(sample, k))
