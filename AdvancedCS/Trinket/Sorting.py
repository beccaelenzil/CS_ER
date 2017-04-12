def QuickSort(alist):
    pivot = alist[0]
    list = alist

    for i in len(list):
        if list[i] >= pivot:
            big_num = list[i]

            j = list[len(list)-1]
            while list[j] >= pivot:
                j -= 1

            list[i],list[j] = list[j],list[i]

    print list

def test():
    alist = [39, 30, 45, 33, 20, 61, 36, 5, 31, 64, 22, 10, 21, 25, 80, 86, 63, 27, 85, 2, 71, 4, 5]
    QuickSort(alist)
