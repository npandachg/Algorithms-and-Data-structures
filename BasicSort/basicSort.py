import numpy as np


def is_sortable(obj):
    return hasattr(obj, "__cmp__") or \
        hasattr(obj, "__lt__")


class IsNotSortable(Exception):
    """Not sortable exception class"""
    pass


class EmptyArray(Exception):
    """Empty Array exception class"""
    pass


class Selection(object):
    """Selection sort class. Only for array of objects that are sortable"""

    @staticmethod
    def sort(arr):
        if not arr:
            raise EmptyArray("Array is empty")
        elif not is_sortable(arr[0]):
            raise IsNotSortable("No order for the object defined")
        else:
            return Selection._sort(arr)

    @staticmethod
    def _sort(arr):
        """ Sort by looping through i from a[0] to a[size-1],
        and for each i, swap the smallest entry to the right of
        i with a[i]"""

        for i in range(len(arr)):
            min_pos = i
            for j in range(i+1, len(arr)):
                if arr[j] < arr[min_pos]:
                    min_pos = j
            Selection._swap(arr, i, min_pos)
        return arr

    @staticmethod
    def _swap(arr, i, j):
        """ swaps arr[i] and arr[j]"""
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp


class Insertion(object):
    """Insertion sort class for sortable objects"""

    @staticmethod
    def sort(arr):
        if not arr:
            raise EmptyArray("Array is empty")
        elif not is_sortable(arr[0]):
            raise IsNotSortable("No order for the object defined")
        else:
            return Insertion._sort(arr)

    @staticmethod
    def _sort(arr):
        """ Sort by looping through i from a[0] to a[size-1],
        and for each i, entries to the left of i are sorted, while to the
        right are not seen"""

        for i in range(1, len(arr)):
            for j in range(i, 0, -1):
                if arr[j] < arr[j-1]:
                    Insertion._swap(arr, j, j-1)
                else:
                    break
        return arr

    @staticmethod
    def _swap(arr, i, j):
        """ swaps arr[i] and arr[j]"""
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp


class MergeSort(object):
    """Merge Sort class for sortable objects. Sorts using divide and conquer"""
    @staticmethod
    def sort(arr):
        if not arr:
            raise EmptyArray("Array is empty")
        elif not is_sortable(arr[0]):
            raise IsNotSortable("No order for the object defined")
        else:
            aux = np.empty([len(arr)], dtype=object)
            # aux = MergeSort._copy(arr)
            lo = 0
            high = len(arr)
            mid = lo + int((high - lo)/2)
            return MergeSort._sort(arr, aux, lo, mid, high)

    @staticmethod
    def _sort(arr, aux, lo, mid, high):
        """ Sort recursively through divide and conquer
        left half is [a(lo), a(mid)) and right half is
        [a(mid), a(hight)). Return when lo = mid
        """

        if (lo == mid):
            return
        left_mid = lo + int((mid - lo)/2)
        right_mid = mid + int((high - mid)/2)
        # sort the left half [lo, mid)
        MergeSort._sort(arr, aux, lo, left_mid, mid)
        # sort the right half [mid, high)
        MergeSort._sort(arr, aux, mid, right_mid, high)
        # merge the result
        MergeSort._merge(arr, aux, lo, mid, high)

    @staticmethod
    def _merge(arr, aux, lo, mid, high):
        """ Merge left half with right half. This is the actual
        sorting algorithm. Use aux as an auxillary array"""

        aux[lo:high] = arr[lo:high]
        left_indx = lo
        right_indx = mid
        for k in range(lo, high):
            if left_indx == mid:
                arr[k] = aux[right_indx]
                right_indx += 1
            elif right_indx == high:
                arr[k] = aux[left_indx]
                left_indx += 1
            elif aux[left_indx] <= aux[right_indx]:
                arr[k] = aux[left_indx]
                left_indx += 1
            else:
                arr[k] = aux[right_indx]
                right_indx += 1

        return

    @staticmethod
    def _swap(arr, i, j):
        """ swaps arr[i] and arr[j]"""
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp

    @staticmethod
    def _copy(arr):
        a = []
        for i in range(len(arr)):
            a.append(arr[i])
        return a

