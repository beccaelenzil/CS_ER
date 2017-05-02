# File: Sorting.py
# Versions: Python 2.7.13
# Name: Ezra Robinson
# Date: 4/20/17
# Desc: various search methods


def sequentialSearch(alist, item):
    found = False
    i = 0
    while i < len(alist) and not found:
        if i == item:
            found = True
        i += 1
    return found

# Number of Operations:
# Best Case: 1
# Worst Case: len(alist)
# Average Case: len(alist)/2


def binarySearch(alist, item):
    found = False
    midpoint = len(alist)//2
    if alist[midpoint] == item:
        found = True
    elif alist[midpoint] > item:
        newList = alist[:midpoint]
    else:
        newList = alist[midpoint:]

    if not found and len(newList) > 1:
        print newList
        found = binarySearch(newList, item)

    print found
    return found


def test():
    alist = [2, 4, 5, 5, 10, 20, 21, 22, 25, 27, 30, 31, 33, 36, 39, 45, 61, 63, 64, 71, 80, 85, 86]
    binarySearch(alist, 67)
