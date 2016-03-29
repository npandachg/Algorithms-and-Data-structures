# import numpy as np
""" BASIC data structures : Stack, Queue, Bag, Randomized Bag, Randomized
stack, Deque (double ended queue). All data structures are iterable.
"""


class NoSuchElement(Exception):
    """No such element exception class"""
    pass


class Stack(object):
    """Create a Stack data structure using linked list LIFO

    arguments: None
    attributes:
    1) push(item) -> pushes an item to stack
    2) pop()      -> (Object Type) removes the last added item
    3) peek()     -> (Object Type) returns the item that is currently at top
    4) is_empty() -> (Bool Type)   true if stack is empty, false otherwise
    5) size()     -> (Int Type)    returns the size of stack
    """

    class _Node(object):
        """Node Object"""

        def __init__(self, item, next=None):
            self.item = item
            self.next = next

    def __init__(self):
        """Creates an empty stack of objects"""
        self._head = None
        self._size = 0

    def __iter__(self):
        """ Make Stack iterable """
        return Stack._StackIterator(self)

    def is_empty(self):
        return self._size == 0

    def push(self, item):
        """ adds item to the stack at the top"""

        # save the head
        old_head = self._head
        # create a new head from item
        self._head = Stack._Node(item, old_head)
        # update the size of the stack
        self._size += 1

    def pop(self):
        """ removes the top most item on the stack """
        if self.is_empty():
            raise NoSuchElement("Removing from an empty stack")
        # get the item
        item = self._head.item
        # update new head to be the one next of old head
        self._head = self._head.next
        self._size -= 1
        return item

    def peek(self):
        return self._head.item

    def size(self):
        return self._size

    class _StackIterator(object):
        """docstring for _StackIterator"""

        def __init__(self, stackObj):
            self.current = stackObj._head

        def __iter__(self):
            return self

        def next(self):
            if self.current is None:
                raise StopIteration
            item = self.current.item
            self.current = self.current.next
            return item


class Queue(object):
    """Create a Queue data structure using linked list FIFO

    arguments: None
    attributes:
    1) enqueue(item) -> adds an item to queue
    2) pop()      -> (Object Type) removes the last added item
    3) peek()     -> (Object Type) returns the item that is currently at top
    4) is_empty() -> (Bool Type)   true if queue is empty, false otherwise
    5) size()     -> (Int Type)    returns the size of queue
    """

    class _Node(object):
        """Node Object"""

        def __init__(self, item, next=None):
            self.item = item
            self.next = next

    def __init__(self):
        """Creates an empty stack of objects"""
        self._head = None
        self._tail = None
        self._size = 0

    def __iter__(self):
        """ Make Stack iterable """
        return Queue._QueueIterator(self)

    def is_empty(self):
        return self._size == 0

    def enqueue(self, item):
        """ adds item to the end"""

        # save the tail
        old_tail = self._tail
        # create a new head from item
        self._tail = Stack._Node(item)
        # make old_tail point to new tail
        if self.is_empty():
            self._head = self._tail
        else:
            old_tail.next = self._tail
        # update the size of the stack
        self._size += 1

    def pop(self):
        """ removes the top most item on the queue """
        if self.is_empty():
            raise NoSuchElement("Removing from an empty queue")
        # get the item
        item = self._head.item
        # update new head to be the one next of old head
        self._head = self._head.next
        self._size -= 1
        return item

    def peek(self):
        return self._head.item

    def size(self):
        return self._size

    class _QueueIterator(object):
        """docstring for _StackIterator"""

        def __init__(self, queueObj):
            self.current = queueObj._head

        def __iter__(self):
            return self

        def next(self):
            if self.current is None:
                raise StopIteration
            item = self.current.item
            self.current = self.current.next
            return item


class Bag(object):
    """Create a Bag data structure using linked list

    arguments: None
    attributes:
    1) add(item) -> adds an item to Bag
    3) peek()     -> (Object Type) returns the item that is currently at top
    4) is_empty() -> (Bool Type)   true if Bag is empty, false otherwise
    5) size()     -> (Int Type)    returns the size of Bag
    """

    class _Node(object):
        """Node Object"""

        def __init__(self, item, next=None):
            self.item = item
            self.next = next

    def __init__(self):
        """Creates an empty Bag of objects"""
        self._head = None
        self._size = 0

    def __iter__(self):
        """ Make Bag iterable """
        return Bag._BagIterator(self)

    def is_empty(self):
        return self._size == 0

    def add(self, item):
        """ adds item to the Bag at the top"""

        # save the head
        old_head = self._head
        # create a new head from item
        self._head = Bag._Node(item, old_head)
        # update the size of the Bag
        self._size += 1

    def peek(self):
        return self._head.item

    def size(self):
        return self._size

    class _BagIterator(object):
        """docstring for _StackIterator"""

        def __init__(self, bagObj):
            self.current = bagObj._head

        def __iter__(self):
            return self

        def next(self):
            if self.current is None:
                raise StopIteration
            item = self.current.item
            self.current = self.current.next
            return item

