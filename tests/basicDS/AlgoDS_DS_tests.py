from nose.tools import *
from AlgoDS.basicDS import MaxPQ
from AlgoDS.basicDS import MinPQ
from AlgoDS.basicDS import UnionFind


def test_MaxPQ():
    """ Test the constructor
    """

    print "Testing the constructor\n"

    max_pq = MaxPQ()
    assert_equal(max_pq.size, 0)
    assert_equal(len(max_pq.pq), 2)


def test_MaxPQ_insert():
    """ Test the insert method
    """

    print "Testing the insert method\n"

    # since insert uses swim and resize we can
    # test them both.
    max_pq = MaxPQ()
    # add P
    max_pq.insert("P")
    assert_equal(max_pq.size, 1)
    assert_equal(len(max_pq.pq), 2)
    assert_equal(max_pq.pq[1], "P")
    # add Q
    max_pq.insert("Q")
    assert_equal(max_pq.size, 2)
    assert_equal(len(max_pq.pq), 3)
    assert_equal(max_pq.pq[1], "Q")
    assert_equal(max_pq.pq[2], "P")
    # add E
    max_pq.insert("E")
    assert_equal(max_pq.size, 3)
    assert_equal(len(max_pq.pq), 5)
    assert_equal(max_pq.pq[1], "Q")
    assert_equal(max_pq.pq[2], "P")
    assert_equal(max_pq.pq[3], "E")
    max_pq.insert("X")
    assert_equal(max_pq.size, 4)
    assert_equal(len(max_pq.pq), 5)
    assert_equal(len(max_pq.pq), 5)
    assert_equal(max_pq.pq[1], "X")
    assert_equal(max_pq.pq[2], "Q")
    assert_equal(max_pq.pq[3], "E")
    assert_equal(max_pq.pq[4], "P")
    max_pq.insert("A")
    assert_equal(max_pq.size, 5)
    assert_equal(len(max_pq.pq), 9)
    assert_equal(max_pq.pq[1], "X")
    assert_equal(max_pq.pq[2], "Q")
    assert_equal(max_pq.pq[3], "E")
    assert_equal(max_pq.pq[4], "P")
    assert_equal(max_pq.pq[5], "A")


def test_MaxPQ_deleteMax():
    """ Test the delete_max method
    """

    print "Testing the delete_max method\n"

    # since delete max uses sink and resize we can test
    # them both.
    max_pq = MaxPQ()
    # add P, Q, E
    max_pq.insert("P")
    max_pq.insert("Q")
    max_pq.insert("E")
    # remove max
    v = max_pq.delete_max()
    assert_equal(v, "Q")
    assert_equal(max_pq.size, 2)
    assert_equal(len(max_pq.pq), 5)


def test_MaxPQ_Main():
    """ Test the main method
    """
    print "Testing the MaxPQ method as a script\n"
    max_pq = MaxPQ()
    # add P, Q, E
    max_pq.insert("P")
    max_pq.insert("Q")
    max_pq.insert("E")
    # remove max
    max_pq.delete_max()
    for v in max_pq.pq:
        print v
    print "\n"
    # add X, A, M
    max_pq.insert("X")
    max_pq.insert("A")
    max_pq.insert("M")
    # remove max
    max_pq.delete_max()
    for v in max_pq.pq:
        print v
    print "\n"
    # add P, L, E
    max_pq.insert("P")
    max_pq.insert("L")
    max_pq.insert("E")
    print "\n"
    for v in max_pq.pq:
        print v

    # remove max
    max_pq.delete_max()

    # size should be 6, max at P with the heap
    assert_equal(max_pq.get_size(), 6)
    assert_equal(max_pq.max(), "P")
    # PMLAEE
    for v in max_pq.pq:
        print v


def test_MinPQ_Main():
    """ Test the MinPQ """

    print "Testing the MinPQ class as a script\n"
    min_pq = MinPQ()

    # add P, Q, E, X, A, M, P, L, E
    min_pq.insert("P")
    min_pq.insert("Q")
    min_pq.insert("E")
    min_pq.insert("X")
    min_pq.insert("A")
    min_pq.insert("M")
    min_pq.insert("P")
    min_pq.insert("L")
    min_pq.insert("E")

    for v in min_pq.pq:
        print v

    print min_pq.delete_min()
    print min_pq.delete_min()
    print min_pq.delete_min()
    print min_pq.delete_min()
    print min_pq.delete_min()
    print min_pq.delete_min()
    print min_pq.delete_min()
    print min_pq.delete_min()
    print min_pq.delete_min()


def test_UnionFind():
    """ test the constructor """
    print "testing the constructor for UnionFind\n"

    uf = UnionFind(10)
    assert_equal(uf.size, 10)
    pass


def test_UnionFind_Main():
    """ test UF as main """
    print "testing the UnionFind as main\n"
    uf = UnionFind(10)
    uf.union(4, 3)
    uf.union(3, 8)
    uf.union(6, 5)
    uf.union(9, 4)
    uf.union(2, 1)
    uf.union(8, 9)
    uf.union(5, 0)
    uf.union(7, 2)
    uf.union(6, 1)
    uf.union(1, 0)
    uf.union(6, 7)

    assert_equal(uf.id[4], 4)
    assert_equal(uf.id[3], 4)
    assert_equal(uf.id[8], 4)
    assert_equal(uf.id[9], 4)

    assert_equal(uf.id[6], 6)
    assert_equal(uf.id[0], 6)
    assert_equal(uf.id[2], 6)
    assert_equal(uf.id[5], 6)

    assert_equal(uf.id[1], 2)
    assert_equal(uf.id[7], 2)

