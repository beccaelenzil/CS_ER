# File: Sorting.py
# Versions: Python 2.7.13
# Name: Ezra Robinson
# Date: 4/20/17
# Desc: various sorting methods
# Usage:

import random


# creates a list of numbers between 0 and listRange and lenght listLength
def makeList(listLength, listRange):
    return random.sample(range(0, listRange+1), listLength)


# sorts alist using quick sort algorithm
def QuickSort(alist):
    currentList = alist
    pivotVal = 0
    while currentList[pivotVal] == min(currentList):
        pivotVal += 1
    pivot = currentList[pivotVal]

    for i in range(len(currentList) - 1):
        if currentList[i] >= pivot:

            j = len(currentList) - 1
            while currentList[j] >= pivot and j >= i:
                j -= 1

            if j > i:
                currentList[i],currentList[j] = currentList[j],currentList[i]

        print currentList

    alist = currentList

    midpoint = 0
    for item in currentList:
        if item < pivot:
            midpoint += 1

    newList = alist[:midpoint]  # take first half of list and if longer than 1 item, quicksort
    if len(newList) > 2 or len(newList) == 2 and newList[0] != min(newList):
        QuickSort(newList)
        for i in range(len(newList)):
            alist[i] = newList[i]

    newList = alist[midpoint:]  # take second half of list and if longer than 1 item, quicksort
    if len(newList) > 2 or len(newList) == 2 and newList[0] != min(newList):
        QuickSort(newList)
        for i in range(len(newList)):
                alist[midpoint + i] = newList[i]

    print alist


def InsertionSort(alist):

    workingList = alist  # create temp list

    for i in range(1, len(workingList)):
        pos = i

        while workingList[pos] < workingList[pos-1] and pos > 0:
            workingList[pos], workingList[pos-1] = workingList[pos-1], workingList[pos]
            pos -= 1
            print workingList

    alist = workingList
    return alist


def SelectionSort(alist):

    for i in range(len(alist)):
        lowVal = i
        for j in range(i + 1, len(alist)):
            if alist[lowVal] > alist[j]:
                lowVal = j

        alist[i], alist[lowVal] = alist[lowVal], alist[i]
        print alist

    return alist


def test():
    alist = [39, 30, 45, 33, 20, 61, 36, 5, 31, 64, 22, 10, 21, 25, 80, 86, 63, 27, 85, 2, 71, 4, 5]
    SelectionSort(alist)
