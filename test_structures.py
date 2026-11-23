
import unittest

from elementary_structures import (
    DynamicArray,
    Matrix,
    ArrayStack,
    ArrayQueue,
    SinglyLinkedList,
)


class TestDynamicArray(unittest.TestCase):

    def test_insert_and_access(self):
        array = DynamicArray()
        array.append(10)
        array.append(30)
        array.insert(1, 20)

        self.assertEqual(array.to_list(), [10, 20, 30])
        self.assertEqual(array.access(1), 20)

    def test_delete(self):
        array = DynamicArray()

        for value in (10, 20, 30):
            array.append(value)

        self.assertEqual(array.delete(1), 20)
        self.assertEqual(array.to_list(), [10, 30])
        self.assertEqual(len(array), 2)

    def test_invalid_index(self):
        array = DynamicArray()

        with self.assertRaises(IndexError):
            array.access(0)

        with self.assertRaises(IndexError):
            array.insert(2, 10)

        with self.assertRaises(IndexError):
            array.delete(0)


class TestMatrix(unittest.TestCase):

    def test_insert_and_access(self):
        matrix = Matrix(2, 3)
        matrix.insert(1, 2, 99)

        self.assertEqual(matrix.access(1, 2), 99)
        self.assertEqual(matrix.access(0, 0), 0)

    def test_delete(self):
        matrix = Matrix(2, 2)
        matrix.insert(0, 1, 15)

        self.assertEqual(matrix.delete(0, 1), 15)
        self.assertEqual(matrix.access(0, 1), 0)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            Matrix(0, 2)

        with self.assertRaises(ValueError):
            Matrix(2, -1)

    def test_invalid_position(self):
        matrix = Matrix(2, 2)

        with self.assertRaises(IndexError):
            matrix.access(3, 0)


class TestStack(unittest.TestCase):

    def test_lifo_order(self):
        stack = ArrayStack()

        for value in (10, 20, 30):
            stack.push(value)

        self.assertEqual(stack.pop(), 30)
        self.assertEqual(stack.pop(), 20)
        self.assertEqual(stack.pop(), 10)
        self.assertTrue(stack.is_empty())

    def test_peek(self):
        stack = ArrayStack()
        stack.push("A")
        stack.push("B")

        self.assertEqual(stack.peek(), "B")
        self.assertEqual(len(stack), 2)

    def test_empty_stack(self):
        stack = ArrayStack()

        with self.assertRaises(IndexError):
            stack.pop()

        with self.assertRaises(IndexError):
            stack.peek()


class TestQueue(unittest.TestCase):

    def test_fifo_order(self):
        queue = ArrayQueue()

        for value in (10, 20, 30):
            queue.enqueue(value)

        self.assertEqual(queue.dequeue(), 10)
        self.assertEqual(queue.dequeue(), 20)
        self.assertEqual(queue.dequeue(), 30)
        self.assertTrue(queue.is_empty())

    def test_circular_wraparound(self):
        queue = ArrayQueue(capacity=3)

        for value in (1, 2, 3):
            queue.enqueue(value)

        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)

        queue.enqueue(4)
        queue.enqueue(5)

        self.assertEqual(
            [queue.dequeue() for _ in range(3)],
            [3, 4, 5],
        )

    def test_dynamic_growth(self):
        queue = ArrayQueue(capacity=2)

        for value in range(20):
            queue.enqueue(value)

        self.assertEqual(
            [queue.dequeue() for _ in range(20)],
            list(range(20)),
        )

    def test_peek(self):
        queue = ArrayQueue()
        queue.enqueue("A")
        queue.enqueue("B")

        self.assertEqual(queue.peek(), "A")
        self.assertEqual(len(queue), 2)

    def test_empty_queue(self):
        queue = ArrayQueue()

        with self.assertRaises(IndexError):
            queue.dequeue()

        with self.assertRaises(IndexError):
            queue.peek()


class TestLinkedList(unittest.TestCase):

    def test_append_and_traverse(self):
        linked = SinglyLinkedList()
        linked.append(10)
        linked.append(20)

        self.assertEqual(linked.traverse(), [10, 20])

    def test_prepend(self):
        linked = SinglyLinkedList()
        linked.prepend(20)
        linked.prepend(10)

        self.assertEqual(linked.traverse(), [10, 20])

    def test_insert_middle(self):
        linked = SinglyLinkedList()
        linked.append(10)
        linked.append(30)
        linked.insert(1, 20)

        self.assertEqual(linked.traverse(), [10, 20, 30])

    def test_delete_head(self):
        linked = SinglyLinkedList()
        linked.append(10)
        linked.append(20)

        self.assertTrue(linked.delete(10))
        self.assertEqual(linked.traverse(), [20])

    def test_delete_middle(self):
        linked = SinglyLinkedList()

        for value in (10, 20, 30):
            linked.append(value)

        self.assertTrue(linked.delete(20))
        self.assertEqual(linked.traverse(), [10, 30])

    def test_delete_missing(self):
        linked = SinglyLinkedList()
        linked.append(10)

        self.assertFalse(linked.delete(99))
        self.assertEqual(len(linked), 1)

    def test_search(self):
        linked = SinglyLinkedList()

        for value in (10, 20, 30):
            linked.append(value)

        self.assertEqual(linked.search(20), 1)
        self.assertEqual(linked.search(99), -1)

    def test_invalid_insert(self):
        linked = SinglyLinkedList()

        with self.assertRaises(IndexError):
            linked.insert(2, 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
