# File: Sorting.py
# Versions: Python 2.7.13
# Name: Ezra Robinson
# Date: 4/25/17
# Desc: various sorting methods


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

    return alist


def ShellSort(alist, gap):
    for i in range(gap):  # for each inner list we will create
        newList = []  # create empty list
        for j in range(i, len(alist), gap):  # add vals of inner list to newList
            newList.append(alist[j])

        print newList

        newList = InsertionSort(newList)  # insertion sort the newList

        print newList

        k = 0
        for j in range(i, len(alist), gap):  #
            alist[j] = newList[k]
            k += 1
        print alist

    return InsertionSort(alist)


def BubbleSort(alist):
    done = False
    while not done:
        done = True
        for i in range(len(alist) - 1):
            if alist[i] > alist[i + 1]:
                alist[i], alist[i + 1] = alist[i + 1], alist[i]
                done = False
        print alist
    return alist


def MergeSort(alist):

    if len(alist) > 1:
        midpoint = len(alist)//2  # find center of list
        leftList = alist[:midpoint]  # split in two
        rightList = alist[midpoint:]

        MergeSort(leftList)  # then recurse
        MergeSort(rightList)

        leftPos = 0
        rightPos = 0
        finalPos = 0
        while leftPos < len(leftList) and rightPos < len(rightList):
            if leftList[leftPos] <= rightList[rightPos]:
                alist[finalPos] = leftList[leftPos]
                leftPos += 1
            else:
                alist[finalPos] = rightList[rightPos]
                rightPos += 1
            finalPos += 1

        while leftPos < len(leftList):
            alist[finalPos] = leftList[leftPos]
            leftPos += 1
            finalPos += 1

        while rightPos < len(rightList):
            alist[finalPos] = rightList[rightPos]
            rightPos += 1
            finalPos += 1

    print alist
    return alist


def test():
    alist = [39, 30, 45, 33, 20, 61, 36, 5, 31, 64, 22, 10, 21, 25, 80, 86, 63, 27, 85, 2, 71, 4, 5]
    MergeSort(alist)
