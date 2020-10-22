import pandas as pd
import  numpy as np


def f1_sol():
    list1 = [3, 6, 9, 12, 15, 18, 21]
    list2 = [4, 8, 12, 16, 20, 24, 28]
    list3 = list()
    odd_elements = list1[1::2]
    print(odd_elements)
    even_element = list2[0::2]
    print(even_element)
    list3.extend(odd_elements)
    list3.extend(even_element)
    print(list3)


def f2_sol():
    sample_list = [34, 54, 67, 89, 11, 43, 94]
    element = sample_list.pop(4)
    sample_list.insert(1, element)
    sample_list.append(element)
    print(sample_list)


def f3_sol():
    sampleList = [11, 45, 8, 23, 14, 12, 78, 45, 89]
    #slice_obj = slice(0, -1, 3)
    #print(sampleList[slice_obj])


    length = len(sampleList)
    chunk_size = int(length/3)
    start = 0
    end = chunk_size

    for i in range(1, chunk_size+1):
        indexes = slice(start, end, 1)
        list_chunk = sampleList[indexes]
        print('Chunk', i, list_chunk)
        print('Reversed', list(reversed(list_chunk)))
        start = end
        if i < chunk_size:
            end += chunk_size
        else:
            end += length - chunk_size


def f4_sol():
    sampleList = [11, 45, 8, 11, 23, 45, 23, 45, 89]
    count_dict = dict()
    for value in sampleList:
        count = sampleList.count(value)
        count_dict[value] = count
    print(count_dict)


def f5_sol():
    list1 = [2, 3, 4, 5, 6, 7, 8]
    list2 = [4, 9, 16, 25, 36, 49, 64]
    result = zip(list1, list2)
    print(result)
    result_set = set(result)
    print(result_set)


def f6_sol():
    firstSet = {23, 42, 65, 57, 78, 83, 29}
    secondSet = {57, 83, 29, 67, 73, 43, 48}
    intersection = firstSet.intersection(secondSet)
    print(intersection)
    firstSet.difference_update(intersection)
    print(firstSet)


def f7_sol():
    firstSet = {57, 83, 29}
    secondSet = {57, 83, 29, 67, 73, 43, 48}
    if firstSet.issubset(secondSet):
        firstSet.clear()
    if secondSet.issubset(firstSet):
        secondSet.clear()
    print(firstSet)
    print(secondSet)


def f8_sol():
    rollNumber = [47, 64, 69, 37, 76, 83, 95, 97]
    sampleDict = {'Jhon':47, 'Emma':69, 'Kelly':76, 'Jason':97}

    #shallow copy
    rollNumber[:] = [item for item in rollNumber if item in sampleDict.values()]
    print(rollNumber)


def f9_sol():
    speed = {'Jan': 47, 'Feb' :52, 'March': 47, 'April':44, 'May':52, 'June': 53, 'July': 54, 'Aug ':44, 'Sept': 54}

    list_ = list()

    for value in speed.values():
        if value not in list_:
            list_.append(value)

    print(list_)


def f10_sol():
    sampleList = [87, 52, 44, 53, 54, 87, 52, 53]
    #remove duplicate -> set
    sampleList = list(set(sampleList))
    print('Unique list', sampleList)
    tup = tuple(sampleList)
    print('min', min(tup),' max', max(tup))
    

