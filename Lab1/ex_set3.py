import numpy as np


def f1_sol():
    array1 = np.empty([4, 2], dtype=np.uint16)
    print('Printing array')
    print(array1)
    print('\nPrinting numpy array attributes')
    print('1. Array Shape is', array1.shape )
    print('2.  Array dimensions are', array1.ndim )
    print('3.  Length of each element of array in bytes is', array1.itemsize )


def f2_sol():
    # Create a 5X2 integer array from a range between 100 to 200 such that the
    # difference between each element is 10
    array1 = np.arange(100, 200, 10).reshape(5, 2)
    print(array1)


def f3_sol():
    # return the array of items in the third column of each row
    array1 = np.array([[11, 22, 33], [44, 55, 66], [77, 88, 99]])
    new_array = array1[:, 2]
    print(new_array)


def f4_sol():
    # return the array of the odd rows and the even columns
    sample_array = np.array([[3, 6, 9, 12], [15, 18, 21, 24],
                             [27, 30, 33, 36], [39, 42, 45, 48], [51, 54, 57, 60]])

    print(sample_array)
    new_array = sample_array[::2, 1::2]
    print(new_array)


def f5_sol():
    array1 = np.array([[5, 6, 9], [21, 18, 27]])
    array2 = np.array([[15, 33, 24], [4, 7, 1]])
    result_array = array1 + array2

    print(result_array)
    for num in np.nditer(result_array, op_flags=['readwrite']):
        num[...] = np.sqrt(num)

    print(result_array)


def f6_sol():
        sample_array = np.array([[34, 43, 73], [82, 22, 12], [53, 94, 66]])
        print(sample_array)
        # ottenere i valori tutti su una riga
        line_array = sample_array.reshape(1, np.prod(sample_array.shape))
        print(line_array)
        # ordino
        sort_line_array = np.sort(line_array)
        print(sort_line_array)
        # trasformo di nuovo in una matrice
        sort_array = sort_line_array.reshape(sample_array.shape)
        print(sort_array)


def f7_sol():
    # print the max of axis 0 and the min of axis 1
    sample_array = np.array([[34, 43, 73], [82, 22, 12], [53, 94, 66]])
    print(sample_array)
    print()
    min_of_axis1 = np.amin(sample_array, 1)
    print(min_of_axis1)
    max_of_axis0 = np.amax(sample_array, 0)
    print(max_of_axis0)


def f8_sol():
    sample_array = np.array([[34, 43, 73], [82, 22, 12], [53, 94, 66]])
    print(sample_array)
    sample_array = np.delete(sample_array, 1, axis=1) # 1:seconda colonna
    print(sample_array)
    arr = np.array([[10, 10, 10]])
    sample_array = np.insert(sample_array, 1, arr, axis=1)
    print(sample_array)