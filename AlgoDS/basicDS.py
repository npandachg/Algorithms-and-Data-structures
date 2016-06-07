import numpy as np
""" BASIC data structures : Stack, Queue, Bag, Randomized Bag, Randomized
queue, Deque (double ended queue), Priority Queue and Union Find.
All data structures are iterable.
"""


class NoSuchElement(Exception):
    """No such element exception class"""
    pass


class IllegalArgument(Exception):
    """Illegal Argument exception class"""
    pass


class IndexOutOfBound(Exception):
    """Index out of bound exception class"""
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
    2) pop()      -> (Object Type) removes the first added item
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
        """docstring for _BagIterator"""

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


class PQ(object):
    """A priority queue implemented as a binary heap.
    In a max binary heap, the parent is larger than its two
    children, while in a min binary heap, the parent is smaller
    than its two childre.  A (binary heap) priority queue
    maintains this invariant.
    API:
    1) PQ(cmp=None, type)   -> constructor with an optional comparator, type
    2) insert(object v)     -> insert obj v to queue
    3) top()                -> return object at the top
    4) is_empty()           -> is PQ empty ?
    5) size()               -> number of objects in PQ
    """

    def __init__(self, type="max", cmp=None):
        """ Initialize a priority queue which keeps the highest
        priority of a max heap at the top and the lowest priority of a
        min heap at the top. The priority is decided by the user
        implementing __lt__ for the object or by providing a comparator
        object cmp, whose method compare takes (object a, object b)
        and returns -1, 0 or 1 if a < b, a = b and a > b respectively.
        Specifying the type = "max" or "min" determines the type of PQ.
        """
        self.cmp = cmp
        self.pq = np.empty([2], dtype=object)
        self.size = 0
        self.type = type

    def insert(self, v):
        # check if we are full
        if self.size >= len(self.pq) - 1:
            self._resize()

        # increase the size of array
        self.size += 1

        # add v to the pq array
        self.pq[self.size] = v

        # we probably violated the invariant, thus we need to swim up
        self._swim(self.size)

    def top(self):
        """ returns the top element: one with the highest priority
        in a max pq or one with lowest priority in a min pq.
        """
        if self.size == 0:
            return None

        return self.pq[1]

    def is_empty(self):
        """ is the PQ empty ?
        """
        return self.size == 0

    def get_size(self):
        return self.size

    def delete_top(self):
        """ delete the top item
        """

        # swap the 1st entry with the last entry
        self._swap(1, self.size)

        # get the top object and null it in the array
        top_obj = self.pq[self.size]
        self.pq[self.size] = None

        # decrease the size of pq
        self.size -= 1

        # we probably violated the invariant so, sink down
        self._sink(1)

        # resize the array if we are 1/4 full
        if self.size <= 0.25 * (len(self.pq) - 1):
            self._resize()

        # return the top object
        return top_obj

    def _resize(self):
        """ resize the array """
        # create temp arrays
        arr_temp = np.empty([2 * self.size + 1], dtype=object)
        # copy pq array to temp
        arr_temp[1:self.size + 1] = self.pq[1:self.size + 1]
        # update the pq array
        self.pq = arr_temp

    def _less_than(self, i, j):
        """ is key at i < key at j? """

        if self.cmp is None:
            return self.pq[i] < self.pq[j]
        else:
            return self.cmp.compare(self.pq[i], self.pq[j]) < 0

    def _greater_than(self, i, j):
        """ is  key at i > key at j ? """

        if self.cmp is None:
            return self.pq[j] < self.pq[i]
        else:
            return self.cmp.compare(self.pq[i], self.pq[j]) > 0

    def _swap(self, i, j):
        """ swap i and j elements in pq
        """
        temp = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = temp

    def _swim(self, indx):
        """ swim up from indx to maintain invariant property.
        For max PQ: while parent < child, replace parent with child.
        For min PQ: while parent > child, replace parent with child.
        """
        parent_id = int(indx / 2)
        child_id = indx
        if parent_id < 1:
            return

        if self.type == "max":
                while (self._less_than(parent_id, child_id)):
                    # swap parent with child
                    self._swap(parent_id, child_id)

                    # update the parent_id and the child_id
                    child_id = parent_id
                    parent_id = int(child_id / 2)
                    if parent_id < 1:
                        break

        if self.type == "min":
                while (self._greater_than(parent_id, child_id)):
                    # swap parent with child
                    self._swap(parent_id, child_id)

                    # update the parent_id and the child_id
                    child_id = parent_id
                    parent_id = int(child_id / 2)
                    if parent_id < 1:
                        break

    def _sink(self, indx):
        """ sink down from indx to maintain invariant property.
        For max PQ : while parent < child, replace parent with the
        max child.
        For min PQ : while parent > child, replace parent with the
        min chld.
        """

        parent_id = indx
        # check if child exists
        if 2 * parent_id > self.size:
            return

        if self.type == "max":
            # get child id
            if 2 * parent_id + 1 > self.size:
                child_id = 2 * parent_id
            elif self._less_than(2 * parent_id, 2 * parent_id + 1):
                child_id = 2 * parent_id + 1
            else:
                child_id = 2 * parent_id

            while (self._less_than(parent_id, child_id)):

                # swap parent with child
                self._swap(parent_id, child_id)

                # get the child_id and update the parent id
                parent_id = child_id

                # we have no children
                if 2 * parent_id > self.size:
                    break

                if 2 * parent_id + 1 > self.size:
                    child_id = 2 * parent_id
                elif self._less_than(2 * parent_id, 2 * parent_id + 1):
                    child_id = 2 * parent_id + 1
                else:
                    child_id = 2 * parent_id

        if self.type == "min":
            # get child id
            if 2 * parent_id + 1 > self.size:
                child_id = 2 * parent_id
            elif self._less_than(2 * parent_id, 2 * parent_id + 1):
                child_id = 2 * parent_id
            else:
                child_id = 2 * parent_id + 1

            while (self._greater_than(parent_id, child_id)):
                # swap parent with child
                self._swap(parent_id, child_id)

                # get the child_id and update the parent id
                parent_id = child_id

                # we have no children
                if 2 * parent_id > self.size:
                    break

                if 2 * parent_id + 1 > self.size:
                    child_id = 2 * parent_id
                elif self._less_than(2 * parent_id, 2 * parent_id + 1):
                    child_id = 2 * parent_id
                else:
                    child_id = 2 * parent_id + 1


class MaxPQ(PQ):
    """A priority queue implemented as a binary heap.
    In a (max)binary heap, the parent is larger than its two
    children. A (binary) max priority queue maintains this invariant.
    API:
    1) MaxPQ(cmp=None)          -> constructor with an optional comparator
    2) insert(object v)         -> insert obj v to queue
    3) max()                    -> return object with largest priority
    4) is_empty()                -> is PQ empty ?
    5) get_size()                   -> number of objects in PQ
    """
    def __init__(self, cmp=None):
        """ Initialize a max priority queue which keeps the highest
        priority at the top. The priority is decided by the user
        implementing __lt__ for the object or by providing a comparator
        object cmp, whose method compare takes (object a, object b)
        and returns -1, 0 or 1 if a < b, a = b and a > b respectively
        """
        super(MaxPQ, self).__init__(cmp=cmp, type="max")

    def max(self):
        return self.top()

    def delete_max(self):
        return self.delete_top()


class MinPQ(PQ):
    """A priority queue implemented as a binary heap.
    In a (min)binary heap, the parent is smaller than its two
    children. A (binary) min priority queue maintains this invariant.
    API:
    1) MinPQ(cmp=None)          -> constructor with an optional comparator
    2) insert(object v)         -> insert obj v to queue
    3) min()                    -> return object with smallest priority
    4) is_empty()               -> is PQ empty ?
    5) get_size()               -> number of objects in PQ
    """
    def __init__(self, cmp=None):
        super(MinPQ, self).__init__(cmp=cmp, type="min")

    def min(self):
        return self.top()

    def delete_min(self):
        return self.delete_top()


class IndexPQ(object):
    """Refer to items in a PQ by associating a unique integer
    with the PQ object. Comes in handy when we need to change the
    priority of the object. Here the identifier index is fixed
    within a range [0, max_n).
    API:
    1) IndexPQ(max_size, cmp=None, type="max") -> constructor
    2) insert(int index, object v)   -> insert v associated with index
    3) change_key(int i, object v)   -> change the key with index i to v
    4) contains(int i)               -> is index i associated with some key?
    5) delete(int i)                 -> delete index i and its key
    6) top_key()                     -> return the key at the top of the heap
    7) top_index()
    """
    def __init__(self, max_size, cmp=None, type="max"):
        """ pq[0..max+1] starts at 1. qp[index] = location of
        the key associated with the index in pq. Thus
        pq[qp[index]] = j tells us that key associated with index
        is in position j in the PQ """
        self.cmp = cmp
        self.pq = np.zeros([max_size + 1], dtype=int)
        self.qp = -1 * np.ones([max_size], dtype=int)
        self.keys = np.empty([max_size], dtype=object)
        self.size = 0
        self.max = max_size
        self.type = type

    def is_empty(self):
        return self.size == 0

    def contains(self, i):
        if i not in range(self.max):
            return False
        return self.qp[i] != -1

    def insert(self, index, k):
        """ insert key with the corresponding index """
        # check if index is valid
        if index not in range(self.max):
            raise IndexOutOfBound("index out of range: 0 < index < max")
        # check if key associated with index already exists
        if self.contains(index):
            raise IllegalArgument("index is already in PQ")

        # increase size (do this here since we start from 1)
        self.size += 1

        # add index to the end of pq and modify qp
        self.pq[self.size] = index
        self.qp[index] = self.size
        # add key to keys array with the corresponding index
        self.keys[index] = k
        # swim up, we may have violated the heap condition
        self._swim(self.size)
        pass

    def delete(self, i):
        """ delete key associated with the index i """
        # check if i is a valid index
        if i not in range(self.max):
            raise IndexOutOfBound("i out of range: 0 < i < max")
        # check if key associated with index already exists
        if not self.contains(i):
            raise IllegalArgument("index is not in PQ")

        # where is i in PQ?
        loc_i = self.qp[i]

        # swap loc_i with the last element
        self._swap(loc_i, self.size)

        # decrease the size of PQ by 1
        self.size -= 1

        # swim and sink at loc_i
        self._swim(loc_i)
        self._sink(loc_i)

        # make key associated with i a null object
        self.keys[i] = None
        self.qp[i] = -1

    def delete_top(self):
        """ delete the top key and return the index associated with
        the key.
        """
        if self.size == 0:
            raise NoSuchElement(" PQ is empty")
        # top is at pq[1]
        top_index = self.pq[1]

        # swap the top element with last element
        self._swap(1, self.size)

        # decrease the size of PQ by 1
        self.size -= 1

        # sink at 1
        self._sink(1)

        # make key associated with top_index a null object
        self.keys[top_index] = None
        self.qp[top_index] = -1

        # return the top_index
        return top_index

    def change_key(self, i, key):
        """ change the key at i """
        # check if i is a valid index
        if i not in range(self.max):
            raise IndexOutOfBound("i out of range: 0 < i < max")
        # check if key associated with index already exists
        if not self.contains(i):
            raise IllegalArgument("index is not in PQ")

        # change key associated with i
        self.keys[i] = key

        # where is i in PQ?
        loc_i = self.qp[i]

        # sink, swim at loc_i
        self._swim(loc_i)
        self._sink(loc_i)

    def top_index(self):
        """ return the index associated with the top key """
        if self.size == 0:
            raise NoSuchElement(" PQ is empty")
        return self.pq[1]

    def top_key(self):
        """ returns the top key """
        if self.size == 0:
            raise NoSuchElement(" PQ is empty")
        return self.keys[self.pq[1]]

    def _less_than(self, i, j):
        """ is key at i in pq < key at j in pq? """

        if self.cmp is None:
            return self.keys[self.pq[i]] < self.keys[self.pq[j]]
        else:
            return self.cmp.compare(self.keys[self.pq[i]],
                                    self.keys[self.pq[j]]) < 0

    def _greater_than(self, i, j):
        """ is  key at i in pq > key at j in pq ? """

        if self.cmp is None:
            return self.keys[self.pq[j]] < self.keys[self.pq[i]]
        else:
            return self.cmp.compare(self.keys[self.pq[i]],
                                    self.keys[self.pq[j]]) > 0

    def _swap(self, i, j):
        """ swap i and j elements in pq. Modify qp
        """
        temp = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = temp
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j

    def _swim(self, indx):
        """ swim up from indx to maintain invariant property.
        For max PQ: while parent < child, replace parent with child.
        For min PQ: while parent > child, replace parent with child.
        """
        parent_id = int(indx / 2)
        child_id = indx
        if parent_id < 1:
            return

        if self.type == "max":
                while (self._less_than(parent_id, child_id)):
                    # swap parent with child
                    self._swap(parent_id, child_id)

                    # update the parent_id and the child_id
                    child_id = parent_id
                    parent_id = int(child_id / 2)
                    if parent_id < 1:
                        break

        if self.type == "min":
                while (self._greater_than(parent_id, child_id)):
                    # swap parent with child
                    self._swap(parent_id, child_id)

                    # update the parent_id and the child_id
                    child_id = parent_id
                    parent_id = int(child_id / 2)
                    if parent_id < 1:
                        break

    def _sink(self, indx):
        """ sink down from indx to maintain invariant property.
        For max PQ : while parent < child, replace parent with the
        max child.
        For min PQ : while parent > child, replace parent with the
        min chld.
        """

        parent_id = indx
        # check if child exists
        if 2 * parent_id > self.size:
            return

        if self.type == "max":
            # get child id
            if 2 * parent_id + 1 > self.size:
                child_id = 2 * parent_id
            elif self._less_than(2 * parent_id, 2 * parent_id + 1):
                child_id = 2 * parent_id + 1
            else:
                child_id = 2 * parent_id

            while (self._less_than(parent_id, child_id)):

                # swap parent with child
                self._swap(parent_id, child_id)

                # get the child_id and update the parent id
                parent_id = child_id

                # we have no children
                if 2 * parent_id > self.size:
                    break

                if 2 * parent_id + 1 > self.size:
                    child_id = 2 * parent_id
                elif self._less_than(2 * parent_id, 2 * parent_id + 1):
                    child_id = 2 * parent_id + 1
                else:
                    child_id = 2 * parent_id

        if self.type == "min":
            # get child id
            if 2 * parent_id + 1 > self.size:
                child_id = 2 * parent_id
            elif self._less_than(2 * parent_id, 2 * parent_id + 1):
                child_id = 2 * parent_id
            else:
                child_id = 2 * parent_id + 1

            while (self._greater_than(parent_id, child_id)):
                # swap parent with child
                self._swap(parent_id, child_id)

                # get the child_id and update the parent id
                parent_id = child_id

                # we have no children
                if 2 * parent_id > self.size:
                    break

                if 2 * parent_id + 1 > self.size:
                    child_id = 2 * parent_id
                elif self._less_than(2 * parent_id, 2 * parent_id + 1):
                    child_id = 2 * parent_id
                else:
                    child_id = 2 * parent_id + 1


class IndexMaxPQ(IndexPQ):
    """An index priority queue of fixed size implemented as a binary heap.
    In a (max)binary heap, the parent is larger than its two
    children. A (binary) max priority queue maintains this invariant.
    API:
    1) MaxPQ(cmp=None)          -> constructor with an optional comparator
    2) insert(object v)         -> insert obj v to queue
    3) max()                    -> return object with largest priority
    4) is_empty()                -> is PQ empty ?
    5) get_size()                   -> number of objects in PQ
    """
    def __init__(self, max_size, cmp=None):
        """ Initialize a max priority queue which keeps the highest
        priority at the top. The priority is decided by the user
        implementing __lt__ for the object or by providing a comparator
        object cmp, whose method compare takes (object a, object b)
        and returns -1, 0 or 1 if a < b, a = b and a > b respectively
        """
        super(IndexMaxPQ, self).__init__(max_size, cmp=cmp, type="max")

    def max(self):
        return self.top_key()

    def max_index(self):
        return self.top_index()

    def delete_max(self):
        return self.delete_top()


class IndexMinPQ(IndexPQ):
    """An index priority queue of fixed size implemented as a binary heap.
    In a (min)binary heap, the parent is smaller than its two
    children. A (binary) min priority queue maintains this invariant.
    API:
    1) MinPQ(cmp=None)          -> constructor with an optional comparator
    2) insert(object v)         -> insert obj v to queue
    3) min()                    -> return object with smallest priority
    4) is_empty()               -> is PQ empty ?
    5) get_size()               -> number of objects in PQ
    """
    def __init__(self, max_size, cmp=None):
        super(IndexMinPQ, self).__init__(max_size, cmp=cmp, type="min")

    def min(self):
        return self.top_key()

    def min_index(self):
        return self.top_index()

    def delete_min(self):
        return self.delete_top()


class UnionFind(object):
    """A union find class for generating partition.
    N sites are indexed 0..N-1. Union(a, b) puts a and b
    in the same equivalence class.
    API:
    1) UnionFind(size)           -> construct UF object of given size
    2) get_connected_components()-> distinct connected objects
    3) are_connected(p, q)       -> are p, q connected ?
    4) find(p)                   -> find root of p
    5) union(p, q)               -> put p, q in same class.
    """
    def __init__(self, size):
        # id[i] is the parent of the site i
        # sz[i] is the number of sites rooted at i
        # cc is the number of connected components
        self.size = size
        self.cc = size
        self.id = np.zeros([self.size], dtype=int)
        self.sz = np.ones([self.size], dtype=int)
        for i in range(self.size):
            self.id[i] = i

    def get_connected_components(self):
        return self.cc

    def are_connected(self, p, q):
        """ are p, q in the same equivalence class """
        # connected if they have same parent
        return self.id[p] == self.id[q]

    def find(self, p):
        """ find the root of p """
        while p != self.id[p]:
            p = self.id[p]

        return p

    def union(self, p, q):
        """ put p, q in the same equivalence class """
        """ i : root of p
        j : root of q
        if sz[i] < sz[j] make j the parent of i, update size
        else make i the parent of j and update size
        """

        i = self.find(p)
        j = self.find(q)

        if i == j:
            return

        if self.sz[i] < self.sz[j]:
            self.id[i] = j
            self.sz[j] += self.sz[i]

        else:
            self.id[j] = i
            self.sz[i] += self.sz[j]

        self.cc -= 1









