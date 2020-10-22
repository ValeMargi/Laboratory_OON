import numpy as np


def f1_sol():
    array1 = np.empty([4, 2], dtype=np.uint16)
    print('Printing array')
    print(array1)
    print('\nPrinting numpy array attributes')
    print('1. Array Shape is', array1.shape )
    print('2.  Array dimensions are', array1.ndim )
    print('3.  Length of each element of array in bytes is', array1.itemsize )
