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
    assert_equal(st.size(), 4)
    assert_equal(st._size(st._root.left), 2)
    assert_equal(st._size(st._root.right), 1)


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


def test_treeDS_bst_min_max():
    """ test the min and max method """
    st = BST()
    assert_equal(st.min(), None)
    st._root = st._put(st._root, "S", 1)
    st._root = st._put(st._root, "E", 2)
    st._root = st._put(st._root, "W", 3)
    st._root = st._put(st._root, "S", 4)
    st._root = st._put(st._root, "A", 5)
    st._root = st._put(st._root, "F", 6)
    assert_equal(st.min(), "A")
    assert_equal(st.max(), "W")
    assert_equal(st._min(st._root.right), "W")
    assert_equal(st._max(st._root.left), "F")


def test_treeDS_bst_floor():
    """ test the floor method """
    st = BST()
    st["D"] = 1
    st["A"] = 2
    st["X"] = 3
    st["E"] = 4

    assert_equal(st.floor("F"), "E")
    st["F"] = 5
    assert_equal(st.floor("F"), "F")
    pass


def test_treeDS_bst_ceiling():
    """ test the floor method """
    st = BST()
    st["D"] = 1
    st["A"] = 2
    st["X"] = 3
    st["E"] = 4

    assert_equal(st.ceiling("F"), "X")
    st["F"] = 5
    assert_equal(st.ceiling("F"), "F")
    pass


def test_treeDS_bst_select():
    """ test the select method """
    st = BST()
    st["S"] = 1
    st["E"] = 2
    st["A"] = 3
    st["R"] = 4
    st["C"] = 5
    st["H"] = 6
    st["E"] = 7
    st["X"] = 8
    st["A"] = 9
    st["M"] = 10
    st["P"] = 11
    st["L"] = 12
    st["E"] = 13

    assert_equal(st.select(3), "H")
    assert_equal(st.select(13), None)


def test_treeDS_bst_rank():
    """ test the rank method """
    st = BST()
    st["S"] = 1
    st["E"] = 2
    st["A"] = 3
    st["R"] = 4
    st["C"] = 5
    st["H"] = 6
    st["E"] = 7
    st["X"] = 8
    st["A"] = 9
    st["M"] = 10
    st["P"] = 11
    st["L"] = 12
    st["E"] = 13

    assert_equal(st.rank("H"), 3)
    assert_equal(st.rank("X"), st.size() - 1)


def test_treeDS_bst_keys():
    """ test the keys method """
    st = BST()
    st["S"] = 1
    st["E"] = 2
    st["A"] = 3
    st["R"] = 4
    st["C"] = 5
    st["H"] = 6
    st["E"] = 7
    st["X"] = 8
    st["A"] = 9
    st["M"] = 10
    st["P"] = 11
    st["L"] = 12
    st["E"] = 13

    keys = st.keys()
    assert_equal(keys.peek(), st.min())
    for key in keys:
        print key






