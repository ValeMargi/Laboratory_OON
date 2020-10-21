import numpy as np


def f1_my(val1, val2):
    prod = val1 * val2
    if prod > 1000:
        return val1 + val2
    else:
        return prod


def f1_sol():
    num1 = int(input(" Enter first number : "))
    num2 = int(input(" Enter second number : "))
    product = num1 * num2
    if product <= 1000:
        result = product
    else:
        result = num1 + num2
    print("The result is", result)


def f2_my(i):
    for i in range(10):
        print(i + (i - 1))


def f2_sol():
    num = 10
    print(" Printing current and previous number sum in a given range ")
    prev = 0
    for curr in range(num):
        tot = curr + prev
        print('Sum: ', tot)
        prev = curr


def f3_my():
    list1 = [1, 2, 3, 4, 5]
    if list1[0] == list1[-1]:
        result = True
    else:
        result = False
    print(result)


def f3_sol():
    num_list = [10, 20, 30, 40, 10]  # Arbitrary list
    first_element = num_list[0]
    last_element = num_list[-1]
    if first_element == last_element:
        result = True
    else:
        result = False
    print(result)


def f4_my():
    list1 = [10, 2, 3, 4, 5]
    for i in list1:
        if i % 5 == 0:
            print(i)


def f5_sol():
    str = "Emma is a good developer.  Emma is also a writer"
    count = 0
    for i in range(len(str) - 1):
        count += str[i:i + 4] == 'Emma'
        print(str[i:i + 4])

    print(count)


def f6_sol():
    list1 = [1, 2, 3, 4, 5]
    list2 = [1, 2, 3, 4, 5]
    list3 = []
    for num in list1:
        if num % 2 != 0:
            list3.append(num)
    for num in list2:
        if num % 2 == 0:
            list3.append(num)

    print(list3)


def f7_sol():
    s1 = 'OpenNets'
    s2 = 'Optical'
    middle_index = int(len(s1) / 2)
    middle_three = s1[: middle_index] + s2 + s1[middle_index:]
    print(middle_three)


def f8_sol():
    s1 = 'America'
    s2 = 'Japan'
    s3 = s1[:1] + s2[:1] + s1[int(len(s1) / 2): int(len(s1) / 2) + 1] + s2[int(len(s2) / 2): int(len(s2) / 2) + 1] + s1[
        len(s1) - 1] + s2[len(s2) - 1]
    s4 = s1[0] + s1[int(len(s1) / 2)] + s1[-1] + s2[0] + s2[int(len(s2) / 2)] + s2[-1]
    print(s3)
    print(s4)


def f9_sol():
    input_string = 'P @  # yn26at ^& i5veì'
    char_count = 0
    digit_count = 0
    symbol_count = 0
    for char in input_string:
        if char.islower() or char.isupper():
            char_count += 1
        elif char.isnumeric():
            digit_count += 1
        else:
            symbol_count += 1
    print(f'Chars = {char_count}\t tDigits = {digit_count}\t Symbols = {symbol_count}')


def f10_sol():
    str = 'USAusausaUsA'
    substring = 'USA'
    temp_string = str.lower()
    count = temp_string.count(substring.lower())
    print(count)


def f11_sol():
    input_str = 'English = 78 Science = 83  Math = 68 History = 65'
    words = input_str.split()
    mark_list = [int(num) for num in words if num.isnumeric()]
    total_marks = sum(mark_list)
    percentage = total_marks / len(mark_list)
    print(f'Mark total is {total_marks}\tAverage is {percentage}')


def f12_sol():
    input_str = 'pynativepynvepynative'
    count_dict = dict()
    for char in input_str:
        count = input_str.count(char)
        count_dict[char] = count
    print(count_dict)