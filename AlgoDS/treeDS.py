""" Search tree implementation. Requires the key to be comparable, thus
keys must have __cmp__ or __lt__ and __eq__ impelemented.
"""
from AlgoDS.basicDS import Stack
from AlgoDS.basicDS import Queue
import numpy as np


def is_comparable(obj):
    return hasattr(obj, "__cmp__") or \
        (hasattr(obj, "__lt__") and hasattr(obj, "__eq__"))


class NotComparable(Exception):
    """elements not comparable"""
    pass


class UnOrderedSeqST(object):
    """sequential (unordered) symbol table using linked list for
    illustrative purpose as an associative array
    [key, value] ST[key] = value. When adding a key value pair to ST with
    pre-existing key, the value of the key is updated. Hence no duplicate keys.

    arguments: None
    attributes:
    1) __setitem__(key, value) -> adds key,value pair to the ST.
    2) __getitem__(key)        -> returns value associated with the key.
    3) __contains__(key)       -> checks to see if key is in the ST.
    4) size()                  -> get size of ST.
    """
    class _Node(object):
        """inner node class"""

        def __init__(self, key, value, next=None):
            self.key = key
            self.value = value
            self.next = next

    def __init__(self):
        self._head = None
        self._size = 0

    def _put(self, key, value):
            """ puts the key value pair. If key is in the ST, replace
            its value, otherwise add it to the head
            """
            node_with_key = self._check_key(key, self._head)
            if node_with_key is None:
                # add a new key value pair
                old_head = self._head
                self._head = UnOrderedSeqST._Node(key, value, old_head)
            else:
                # update the key with new value
                node_with_key.value = value
            # update size
            self._size += 1

    def _get(self, key):
        """ returns the value associated with the key. if key does not
        exist, returns none
        """

        node_with_key = self._check_key(key, self._head)
        if node_with_key is None:
            return None
        else:
            return node_with_key.value

    def _check_key(self, key, head):
        """ checks recursively if key is in the ST. if not returns
        None link, if yes returns the link"""
        if head is None:
            return head
        else:
            if head.key == key:
                return head
            else:
                return UnOrderedSeqST._check_key(self, key, head.next)

    def __setitem__(self, key, value):
        self._put(key, value)

    def __getitem__(self, key):
        return self._get(key)

    def __contains__(self, key):
        if self._get(key):
            return True
        else:
            return False

    def keys(self):
        "returns the key in a stack"
        stack_of_keys = Stack()
        indx = self._head
        while (indx is not None):
            stack_of_keys.push(indx.key)
            indx = indx.next

        return stack_of_keys

    def size(self):
        "returns size of the ST"
        return self._size


class BinarySearchST(object):
    """Ordered symbol table using resizing arrays for both keys and values.
    search is done through a binary search algorithm.
    [key, value] ST[key] = value. When adding a key value pair to ST with
    pre-existing key, the value of the key is updated. Hence no duplicate keys.

    arguments: None
    attributes:
    1) __setitem__(key, value) -> adds key,value pair to the ST.
    2) __getitem__(key)        -> returns value associated with the key.
    3) __contains__(key)       -> checks to see if key is in the ST.
    4) size()                  -> returns size of ST
    """
    def __init__(self):
        self._keys = np.empty([1], dtype=object)
        self._vals = np.empty([1], dtype=object)
        self._size = 0

    def _resize(self):
        # create temp arrays
        arr_k = np.empty([2*len(self._keys)], dtype=object)
        arr_v = np.empty([2*len(self._vals)], dtype=object)
        # copy key, val arrays
        arr_k[0:len(self._keys)] = self._keys
        arr_v[0:len(self._vals)] = self._vals
        # update key, val array
        self._keys = arr_k
        self._vals = arr_v

    def _check_key(self, key_flag, key, arr, lo, high):
        """ Recursively checks if key is in the array and modifies a
        list key_flag, where key_flag[0] is a boolean : True if
        key was in the list and false otherwise and key_flag[1] is an index
        which is the index of the array if the key is in the array and if not
        then it is the rank of the key """

        """ check recuresively through binary search by the following
        partition [lo mid-1] mid [mid+1, high]. For a full search
        lo = 0, high = size-1
        """
        mid = lo + int((high - lo)/2)

        # base case
        if high <= lo:
            # we have an array of one element arr[lo]
            # compare
            if key < arr[lo]:
                key_flag.append(False)
                key_flag.append(lo)
                return
            elif key > arr[lo]:
                key_flag.append(False)
                key_flag.append(lo+1)
                return
            else:
                key_flag.append(True)
                key_flag.append(lo)
                return

        if key < arr[mid]:
            self._check_key(key_flag, key, arr, lo, mid-1)
        elif key > arr[mid]:
            self._check_key(key_flag, key, arr, mid+1, high)
        else:
            key_flag.append(True)
            key_flag.append(mid)
            return

    def _put(self, key, val):
        """ adds the key value pair. If key is in the ST, then update the
        value, otherwise add the key, value pair
        """
        if self._size == 0:
            self._keys[0] = key
            self._vals[0] = val
            self._size += 1
            return

        key_flag = []

        self._check_key(key_flag, key, self._keys, 0, self._size-1)

        rank = key_flag[1]
        key_exists = key_flag[0]

        if key_exists:
            self._vals[rank] = val
        else:
            if len(self._keys) == self._size:
                self._resize()
            # move over to insert the key, value pair
            for k in range(self._size, rank, -1):
                self._keys[k] = self._keys[k-1]
                self._vals[k] = self._vals[k-1]
            # insert the key, value pair
            self._keys[rank] = key
            self._vals[rank] = val
            self._size += 1

    def _get(self, key):
        """ gets the value associated with the key
        If key is not there, returns None.
        """
        key_in_st = []
        self._check_key(key_in_st, key, self._keys, 0, self._size-1)
        if key_in_st[0]:
            return self._vals[key_in_st[1]]
        else:
            return None

    def __setitem__(self, key, val):
        if not is_comparable(key):
            raise NotComparable("key must be comparable : i.e must\
                have __lt__ and __eq__")
        self._put(key, val)

    def __getitem__(self, key):
        return self._get(key)

    def __contains__(self, key):
        key_in_st = []
        self._check_key(key_in_st, key, self._keys, 0, self._size-1)
        return key_in_st[0]

    def keys(self):
        """ Returns keys in a queue """
        queue_of_keys = Queue()
        for indx in range(self._size):
            queue_of_keys.enqueue(self._keys[indx])
        return queue_of_keys

    def size(self):
        """ Returns the size of ST """
        return self._size









