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
        arr_k = np.empty([2 * len(self._keys)], dtype=object)
        arr_v = np.empty([2 * len(self._vals)], dtype=object)
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
        mid = lo + int((high - lo) / 2)

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
                key_flag.append(lo + 1)
                return
            else:
                key_flag.append(True)
                key_flag.append(lo)
                return

        if key < arr[mid]:
            self._check_key(key_flag, key, arr, lo, mid - 1)
        elif key > arr[mid]:
            self._check_key(key_flag, key, arr, mid + 1, high)
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

        self._check_key(key_flag, key, self._keys, 0, self._size - 1)

        rank = key_flag[1]
        key_exists = key_flag[0]

        if key_exists:
            self._vals[rank] = val
        else:
            if len(self._keys) == self._size:
                self._resize()
            # move over to insert the key, value pair
            for k in range(self._size, rank, -1):
                self._keys[k] = self._keys[k - 1]
                self._vals[k] = self._vals[k - 1]
            # insert the key, value pair
            self._keys[rank] = key
            self._vals[rank] = val
            self._size += 1

    def _get(self, key):
        """ gets the value associated with the key
        If key is not there, returns None.
        """
        key_in_st = []
        self._check_key(key_in_st, key, self._keys, 0, self._size - 1)
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
        self._check_key(key_in_st, key, self._keys, 0, self._size - 1)
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


class BST(object):
    """Binary search tree using linked list. Balance is not guranteed,
    use with caution. For a general balanced BST, use the BBST.
    Definition : A BST is a binary tree where each node has a comparable
    key with the following property : a key in any node is larger than
    all the keys in its left subtree and smaller than all the keys in
    its right subtree. Thus,
    a BST is :
    a) either empty
    b) node that points to 2 BST -> left and right with the above property.
    """

    class _Node(object):
        """inner node class that contains the key, value, link to left
        subtree and a link to right subtree and the size of the tree
        rooted at this node which is size of left tree + size of
        right tree + 1
        """

        def __init__(self, key, val, left=None, right=None, size=0):
            self.key = key
            self.val = val
            self.left = left
            self.right = right
            self.size = size

    def __init__(self):
        """ construct a bst with a null root"""
        self._root = None

    def _put(self, put_node, key, val):
        """ recursively put a key value pair according to the following recipie:
        a) if put_node is None, then create a node object at put_node and
        return it
        b) else :
        if key < key at put_node, call the function with put_node.left,
        if key > key at put_node, call the function with put_node.right,
        else update the put_node.val = val
        """
        # write the base case first
        if put_node is None:
            put_node = BST._Node(key, val, size=1)
        elif key < put_node.key:
            put_node.left = self._put(put_node.left, key, val)
        elif key > put_node.key:
            put_node.right = self._put(put_node.right, key, val)
        else:
            put_node.val = val
        put_node.size = self._size(put_node.left) + \
            self._size(put_node.right) + 1
        return put_node

    def _get(self, key, start_node):
        """ returns the value associated with the key with a recursive
        search. If key is not found, return None.
        check if key is in the start node, if so return it. Else, if key is
        less than the key at the start_node check in the left subtree;
        otherwise check in the right subtree
        """

        # base case
        if start_node is None:
            return None

        if key < start_node.key:
            return self._get(key, start_node.left)
        elif key > start_node.key:
            return self._get(key, start_node.right)
        else:
            return start_node.val

    def _size(self, node):
        if node is None:
            return 0
        else:
            return node.size

    def _min(self, node):
        """ recursively search left to find the min """
        if node is None:
            return None
        if node.left is None:
            return node.key
        else:
            return self._min(node.left)

    def _max(self, node):
        """ recursively search right to find the max """
        if node is None:
            return None
        if node.right is None:
            return node.key
        else:
            return self._max(node.right)

    def _floor(self, key, node):
        """ returns the largest key in the bst that is smaller or equal
        than key. If node is None return None. If key is smaller than
        key at node, then floor must be in left subtree. If key is larger
        than the key at node, then floor could be in the right subtree
        provided there is a smaller key. If not, floor is the node.
        """

        if node is None:
            return None
        if key < node.key:
            return self._floor(key, node.left)
        if key > node.key:
            temp = self._floor(key, node.right)
            if temp is None:
                return node
            else:
                return temp
        if key == node.key:
            return node

    def _ceiling(self, key, node):
        """ returns the smallest key in the bst that is larger or equal
        than key. If node is None return None. If key is larger than
        key at node, then floor must be in right subtree. If key is smaller
        than the key at node, then ceiling could be in the left subtree
        provided there is a larger key. If not, floor is the node.
        """
        if node is None:
            return None
        if key > node.key:
            return self._ceiling(key, node.right)
        if key < node.key:
            temp = self._ceiling(key, node.left)
            if temp is None:
                return node
            else:
                return temp
        if key == node.key:
            return node

    def _select(self, rank, node):
        """ returns the key with the given rank, that is the the
        key with rank number of keys lower than it """

        if node is None:
            return None
        elif rank < self._size(node.left):
            return self._select(rank, node.left)
        elif rank > self._size(node.left):
            size_left = self._size(node.left)
            return self._select(rank - (size_left + 1), node.right)
        else:
            return node

    def _rank(self, key, node):
        """ return the rank of the key i.e the number of keys lesser than
        it in the bst """

        if node is None:
            return 0
        elif key < node.key:
            return self._rank(key, node.left)
        elif key > node.key:
            return self._rank(key, node.right) + 1 + self._size(node.left)
        else:
            return self._size(node.left)

    def _keys(self, iterable, node):
        if node is None:
            return
        self._keys(iterable, node.left)
        iterable.enqueue(node.key)
        self._keys(iterable, node.right)

    def __contains__(self, key):
        """ checks if key is in the search tree """
        if self._get(key, self._root) is None:
            return False
        else:
            return True

    def __setitem__(self, key, val):
        if not is_comparable(key):
            raise NotComparable("key is not comparable")
        self._root = self._put(self._root, key, val)

    def __getitem__(self, key):
        return self._get(key, self._root)

    def size(self):
        return self._size(self._root)

    def is_empty(self):
        return self.size() == 0

    def min(self):
        """ returns the min of the bst """
        return self._min(self._root)

    def max(self):
        """ returns the max of the bst """
        return self._max(self._root)

    def floor(self, key):
        """ returns the largest key in bst smaller than or equal
        to key
        """
        node = self._floor(key, self._root)
        if node is None:
            return None
        else:
            return node.key

    def ceiling(self, key):
        """ returns the smallest key in bst larger/equal to the
        key
        """
        node = self._ceiling(key, self._root)
        if node is None:
            return None
        else:
            return node.key

    def select(self, rank):
        """ returns they key of given rank """
        node = self._select(rank, self._root)
        if node is None:
            return None
        else:
            return node.key

    def rank(self, key):
        """ returns the rank of the given key """
        return self._rank(key, self._root)

    def keys(self):
        """ returns a queue of keys in sorted order """
        queue_of_keys = Queue()
        self._keys(queue_of_keys, self._root)
        return queue_of_keys



