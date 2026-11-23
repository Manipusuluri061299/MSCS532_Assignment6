
"""Elementary data structures for MSCS-532 Assignment 6."""


class DynamicArray:
    """An array with indexed access, insertion, and deletion."""

    def __init__(self):
        self._items = []

    def insert(self, index, value):
        # Insert at a valid position and shift later elements right.
        if not 0 <= index <= len(self._items):
            raise IndexError("Array insertion index out of range")

        self._items.append(None)

        for position in range(len(self._items) - 1, index, -1):
            self._items[position] = self._items[position - 1]

        self._items[index] = value

    def append(self, value):
        self.insert(len(self._items), value)

    def access(self, index):
        if not 0 <= index < len(self._items):
            raise IndexError("Array index out of range")
        return self._items[index]

    def delete(self, index):
        if not 0 <= index < len(self._items):
            raise IndexError("Array deletion index out of range")

        removed = self._items[index]

        # Move later elements left to fill the deleted position.
        for position in range(index, len(self._items) - 1):
            self._items[position] = self._items[position + 1]

        self._items.pop()
        return removed

    def to_list(self):
        return self._items.copy()

    def __len__(self):
        return len(self._items)


class Matrix:
    """A fixed-size rectangular matrix using nested arrays."""

    def __init__(self, rows, columns, default=0):
        if type(rows) is not int or type(columns) is not int:
            raise TypeError("Matrix dimensions must be integers")

        if rows <= 0 or columns <= 0:
            raise ValueError("Matrix dimensions must be positive")

        self._rows = [
            [default for _ in range(columns)]
            for _ in range(rows)
        ]

    def _validate(self, row, column):
        if not (
            0 <= row < len(self._rows)
            and 0 <= column < len(self._rows[0])
        ):
            raise IndexError("Matrix index out of range")

    def access(self, row, column):
        self._validate(row, column)
        return self._rows[row][column]

    def insert(self, row, column, value):
        # In a fixed-size matrix, insertion means assigning
        # a value to an existing cell.
        self._validate(row, column)
        self._rows[row][column] = value

    def delete(self, row, column):
        # Clear a cell without changing the matrix dimensions.
        self._validate(row, column)
        removed = self._rows[row][column]
        self._rows[row][column] = 0
        return removed

    def to_list(self):
        return [row.copy() for row in self._rows]


class ArrayStack:
    """Last-in, first-out stack implemented using an array."""

    def __init__(self):
        self._items = []

    def push(self, value):
        self._items.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop an empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


class ArrayQueue:
    """First-in, first-out queue using a circular array."""

    def __init__(self, capacity=4):
        if type(capacity) is not int or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")

        self._items = [None] * capacity
        self._front = 0
        self._size = 0

    def _grow(self):
        # Copy elements in their logical FIFO order.
        new_items = [None] * (len(self._items) * 2)

        for index in range(self._size):
            old_index = (self._front + index) % len(self._items)
            new_items[index] = self._items[old_index]

        self._items = new_items
        self._front = 0

    def enqueue(self, value):
        if self._size == len(self._items):
            self._grow()

        # Modulo wraps the insertion position around the array.
        index = (self._front + self._size) % len(self._items)
        self._items[index] = value
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Cannot dequeue an empty queue")

        value = self._items[self._front]
        self._items[self._front] = None

        self._front = (self._front + 1) % len(self._items)
        self._size -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty queue")
        return self._items[self._front]

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size


class Node:
    """A node containing a value and a reference to the next node."""

    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    """A linked list supporting insertion, deletion, and traversal."""

    def __init__(self):
        self.head = None
        self._size = 0

    def prepend(self, value):
        # The new node becomes the first node in the list.
        node = Node(value)
        node.next = self.head
        self.head = node
        self._size += 1

    def append(self, value):
        node = Node(value)

        if self.head is None:
            self.head = node
        else:
            current = self.head

            # Follow node references until reaching the tail.
            while current.next is not None:
                current = current.next

            current.next = node

        self._size += 1

    def insert(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError("Linked list insertion index out of range")

        if index == 0:
            self.prepend(value)
            return

        current = self.head

        for _ in range(index - 1):
            current = current.next

        node = Node(value)
        node.next = current.next
        current.next = node
        self._size += 1

    def delete(self, value):
        # Delete the first node matching the requested value.
        if self.head is None:
            return False

        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head

        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return True

            current = current.next

        return False

    def search(self, value):
        current = self.head
        index = 0

        while current is not None:
            if current.value == value:
                return index

            current = current.next
            index += 1

        return -1

    def traverse(self):
        result = []
        current = self.head

        while current is not None:
            result.append(current.value)
            current = current.next

        return result

    def __len__(self):
        return self._size


if __name__ == "__main__":
    print("ELEMENTARY DATA STRUCTURES DEMONSTRATION")

    numbers = DynamicArray()
    numbers.append(10)
    numbers.append(30)
    numbers.insert(1, 20)
    print("Array:", numbers.to_list())
    print("Array access:", numbers.access(1))
    print("Array delete:", numbers.delete(0))

    matrix = Matrix(2, 2)
    matrix.insert(0, 1, 50)
    print("Matrix:", matrix.to_list())
    print("Matrix delete:", matrix.delete(0, 1))

    stack = ArrayStack()
    stack.push("First")
    stack.push("Second")
    print("Stack pop:", stack.pop())

    queue = ArrayQueue()
    queue.enqueue("First")
    queue.enqueue("Second")
    print("Queue dequeue:", queue.dequeue())

    linked = SinglyLinkedList()
    linked.append(10)
    linked.append(30)
    linked.insert(1, 20)
    print("Linked list:", linked.traverse())
    print("Linked list search:", linked.search(20))
    print("Linked list delete:", linked.delete(20))
    print("Linked list after deletion:", linked.traverse())
