##############################################
# wow! you can zip an unpacked array to get its cols
import numpy as np
arr = np.arange(12).reshape(3, 4).tolist()
cols = [[row[i] for row in arr] for i in range(len(arr[0]))]
cols = list(zip(*arr))
# print(arr)
# print(*arr) # tuple of the rows. zipping this groups items i, the cols, across rows and so on

##############################################
from math import prod


def transpose(arr: list) -> list:
    # would be easier with np... but why not???
    shape = (len(arr), len(arr[0]))
    arr_T = [[0 for _ in range(shape[0])] for _ in range(shape[1])]
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            arr_T[j][i] = arr[i][j]
    return arr_T


def task_one(input):
    """
    Numbers are arranged in columns, with an operation
    to perform at the bottom.
    """
    arr = [list(map(int, line.split())) for line in input[:-1]]
    ops = input[-1].split()
    # results = [1 if op == "*" else 0 for op in ops]
    # for row in arr:
    #     for j, col in enumerate(row):
    #         if ops[j] == "*":
    #             results[j] *= col 
    #         else:
    #             results[j] += col
    # return sum(results)

    # or we can just transpose so that the columns are rows, which can be summed/multiplied easier
    # return sum(prod(row) if op=="*" else sum(row) for row, op in zip(transpose(arr), ops))

    # without transpose -- shortest! we iterate over the cols with zip(*arr) instead of transposing arr first
    return sum(prod(row) if op=="*" else sum(row) for row, op in zip(zip(*arr), ops))


def task_two(input):
    """
    This time we read right-to-left, one col at a time.
    So, 
        64 + 23 + 314
    becomes 
        4 + 431 + 623
    like
                64       64-
                23  -->  23-
                314      314 
                +        +
    """
    total = 0
    to_num = lambda digits: sum(int(digits[i])*10**(len(digits)-1-i) for i in range(len(digits)))
    ops = input[-1].split()[::-1] # reverse the order of ops so we can pop to get the next one
    nums = [] # nums for current problem, linked with an op
    for col in list(zip(*input[:-1])):
        digits = "".join(col)
        if digits.isspace():
            # if the entire column is empty, we move on to the next problem.
            # perform the op on the current nums and flush the list
            total += prod(nums) if ops.pop() == "*" else sum(nums)
            nums = []
        else:
            # remove any whitespace from the str repr of the digit
            nums.append(to_num(digits.strip()))
    return total


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        # do not strip the line this time!!!
        input = [line for line in f.readlines() if line.strip()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")