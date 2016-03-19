from nose.tools import *
from AlgoDS.treeDS import BST


def test_treeDS_bst():
    """ test the constructor """
    st = BST()
    assert_equal(st._root, None)


def test_treeDS_bst_put():
    """ test the put (insert key, val) method """

    st = BST()
    st._root = st._put(st._root, "S", 1)
    st._root = st._put(st._root, "E", 2)
    st._root = st._put(st._root, "W", 3)
    st._root = st._put(st._root, "S", 4)
    st._root = st._put(st._root, "A", 5)
    assert_equal(st._root.key, "S")
    assert_equal(st._root.val, 4)
    assert_equal(st._root.left.key, "E")
    assert_equal(st._root.left.val, 2)
    assert_equal(st._root.right.key, "W")
    assert_equal(st._root.right.val, 3)
    assert_equal(st._root.left.left.key, "A")
    assert_equal(st._root.left.left.val, 5)


def test_treeDS_bst_get():
    """ test the get method """

    st = BST()
    assert_equal(st._get("S", st._root), None)
    st._root = st._put(st._root, "S", 1)
    st._root = st._put(st._root, "E", 2)
    st._root = st._put(st._root, "W", 3)
    st._root = st._put(st._root, "S", 4)
    st._root = st._put(st._root, "A", 5)
    assert_equal(st._get("S", st._root), 4)
    assert_equal(st._get("E", st._root), 2)
    assert_equal(st._get("W", st._root), 3)
    assert_equal(st._get("A", st._root), 5)
    assert_equal(st._get("X", st._root), None)


def test_treeDS_bst_contains():
    """ test the contains method """
    st = BST()
    assert_equal("S" in st, False)
    st._root = st._put(st._root, "S", 1)
    st._root = st._put(st._root, "E", 2)
    st._root = st._put(st._root, "W", 3)
    st._root = st._put(st._root, "S", 4)
    st._root = st._put(st._root, "A", 5)
    assert_equal("E" in st, True)
    assert_equal("W" in st, True)
    assert_equal("A" in st, True)
    assert_equal("S" in st, True)
    assert_equal("X" in st, False)


def test_treeDS_bst_setitem():
    """ test the setitem and getitem methods"""
    st = BST()
    assert_equal(st["S"], None)
    st["S"] = 1
    st["S"] = 4
    assert_equal(st["S"], 4)



