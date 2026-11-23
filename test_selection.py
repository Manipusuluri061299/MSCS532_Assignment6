
import random
import unittest

from selection_algorithms import (
    deterministic_select,
    randomized_select,
)


class TestSelectionAlgorithms(unittest.TestCase):

    def check_both(self, values, k):
        """Compare both selection methods with Python's sorted result."""

        original = values.copy()
        expected = sorted(values)[k - 1]

        # Both implementations should return the same kth value.
        self.assertEqual(deterministic_select(values, k), expected)
        self.assertEqual(
            randomized_select(values, k, random.Random(42)),
            expected,
        )

        # Neither implementation should change the original list.
        self.assertEqual(values, original)

    def test_single_element(self):
        self.check_both([9], 1)

    def test_smallest_element(self):
        self.check_both([8, 3, 5, 1, 9], 1)

    def test_largest_element(self):
        self.check_both([8, 3, 5, 1, 9], 5)

    def test_middle_element(self):
        self.check_both([12, 3, 5, 7, 4, 19, 26, 5], 4)

    def test_duplicate_elements(self):
        self.check_both([4, 2, 4, 1, 2, 4, 3], 5)

    def test_all_equal(self):
        self.check_both([7, 7, 7, 7, 7, 7], 3)

    def test_negative_numbers(self):
        self.check_both([-5, 0, -12, 9, -1], 2)

    def test_sorted_input(self):
        self.check_both(list(range(100)), 50)

    def test_reverse_sorted_input(self):
        self.check_both(list(range(100, 0, -1)), 50)

    def test_random_input(self):
        generator = random.Random(123)
        values = [generator.randint(-100, 100) for _ in range(200)]
        self.check_both(values, 75)

    def test_many_duplicates(self):
        values = [3] * 60 + [1] * 30 + [8] * 40
        self.check_both(values, 80)

    def test_empty_input(self):
        for algorithm in (deterministic_select, randomized_select):
            with self.subTest(algorithm=algorithm.__name__):
                with self.assertRaises(ValueError):
                    algorithm([], 1)

    def test_invalid_k_zero(self):
        for algorithm in (deterministic_select, randomized_select):
            with self.subTest(algorithm=algorithm.__name__):
                with self.assertRaises(ValueError):
                    algorithm([1, 2, 3], 0)

    def test_invalid_k_too_large(self):
        for algorithm in (deterministic_select, randomized_select):
            with self.subTest(algorithm=algorithm.__name__):
                with self.assertRaises(ValueError):
                    algorithm([1, 2, 3], 4)

    def test_invalid_k_type(self):
        for algorithm in (deterministic_select, randomized_select):
            with self.subTest(algorithm=algorithm.__name__):
                with self.assertRaises(TypeError):
                    algorithm([1, 2, 3], True)

    def test_non_integer_element(self):
        for algorithm in (deterministic_select, randomized_select):
            with self.subTest(algorithm=algorithm.__name__):
                with self.assertRaises(TypeError):
                    algorithm([1, "2", 3], 2)

    def test_non_list_input(self):
        for algorithm in (deterministic_select, randomized_select):
            with self.subTest(algorithm=algorithm.__name__):
                with self.assertRaises(TypeError):
                    algorithm((1, 2, 3), 2)

    def test_randomized_multiple_seeds(self):
        values = [9, 2, 6, 2, 8, 1, 5, 3, 7]

        # A correct selection result must not depend on which
        # random pivot choices happen during execution.
        for seed in range(20):
            with self.subTest(seed=seed):
                self.assertEqual(
                    randomized_select(values, 5, random.Random(seed)),
                    5,
                )

    def test_multiple_sizes_and_ranks(self):
        generator = random.Random(2026)

        # Test every valid rank on several small and medium
        # datasets to catch partition-boundary errors.
        for size in (2, 5, 6, 10, 25, 50):
            values = [
                generator.randint(-20, 20)
                for _ in range(size)
            ]

            for k in range(1, size + 1):
                with self.subTest(size=size, k=k):
                    self.check_both(values, k)


if __name__ == "__main__":
    unittest.main(verbosity=2)
