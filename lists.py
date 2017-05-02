# File: Sorting.py
# Versions: Python 2.7.13
# Name: Ezra Robinson
# Date: 4/25/17
# Desc: list comprehensions practice

listA = [i for i in range(10,20)]  # [10,11,12,13,14,15,16,17,18,19]
listB = [i for i in reversed(range(-10,-4))]  # [-5,-6,-7,-8,-9,-10]

print listA
print listB

listA = [i for i in range(0, 13, 3)]  # [0,3,6,9,12]
listB = [i for i in reversed(range(0,11,2))]  # [10,8,6,4,2,0]
listC = [i for i in reversed(range(-5,1))]  # [0,-1,-2,-3,-4,-5]

print listA
print listB
print listC

print "yaya hooraaaaaay"
