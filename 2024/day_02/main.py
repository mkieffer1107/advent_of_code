import numpy as np

def task_one(input):
    """
    For each line, ensure that the sequence of numbers is
    monotonically changing with a difference of 1 to 3
    """
    total = 0
    for line in input:
        # take the differences of adjacent elements
        # [a, b, c, ...] --> [b-a, c-b, ...]
        arr = np.array([int(num) for num in line.split()])
        diffs = np.diff(arr)
        if (np.all(diffs > 0) or np.all(diffs < 0)) and np.all((1 <= np.abs(diffs)) & (np.abs(diffs) <= 3)):
            total += 1
    return total


def task_two(input):
    """
    Now a line counts if removing a single number in the sequence
    causes the condition above to be satisfied
    """
    total = 0

    def passes(arr):
        diffs = np.diff(arr)
        if (np.all(diffs > 0) or np.all(diffs < 0)) and np.all((1 <= np.abs(diffs)) & (np.abs(diffs) <= 3)):
            return True
        return False

    for line in input:
        arr = np.array([int(num) for num in line.split()])
        if passes(arr):
            total += 1
        else:
            # just brute force it :p
            for i in range(len(arr)):
                # if passes(list(arr)[:i] + list(arr)[i+1:]):
                if passes(np.delete(arr, i)):
                    total += 1
                    break

        # take the differences of adjacent elements
        # [a, b, c, ...] --> [b-a, c-b, ...]
        # arr = np.array([int(num) for num in line.split()])
        # diffs = np.diff(arr)

        # sum_of_diffs = diffs[:-1] + diffs[1:] # [a, b, c, d] --> [a, ..., c] + [b, ..., d]
        # if we add the diffs together, we can find the difference 
        # between elements two away from each other, as if the number
        # in between them was removed. 
        # diffs:     [a, b, c, d, ...] --> [b-a, c-b, d-c...]
        # sum diffs: [b-a, c-b, d-c...] --> [c-a, d-b]
    return total


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")