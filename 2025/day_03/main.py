def n_largest_ordered(arr: list[int], n: int) -> list[int]:
    """
    Find the largest n-digit number possible by concatenating numbers
    in the order they appear in an array.
    """
    digits = []
    while len(digits) < n:
        if n - len(digits) == 1:
            # if there is only one spot left, use the largest num that remains
            digits.append(max(arr))
        else:
            # if we want the n largest items, we must leave at least
            # n spaces open to the very right to check later. because we'll be selecting
            # one now, we include an additional -1 term to leave enough room for the next step
            remaining = n - len(digits) - 1
            idx, left_max = max(enumerate(arr[:-remaining]), key = lambda x: x[1])
            digits.append(left_max)
            # now only look to the right of the left_max
            arr = arr[idx+1:] 
    return digits


def task_one(input):
    """
    Given a row of digits, select the two digits that make the largest number.
    For example, in 8111119 you would choose 8 and 9 to make 89. The order cannot be rearranged.
    This is the specific, hard-coded case n_largest_ordered(arr, 2)
    """
    total = 0
    for row in input:
        arr = [int(num) for num in list(row)]
        # search leftside for largest digit (excluding final item which can never be the first digit)
        idx, digit_1 = max(enumerate(arr[:-1]), key=lambda x: x[1]) # (idx, val), find max over first item, the vals
        # now search to the right of the first digit
        digit_2 = max(arr[idx+1:])
        total += 10 * digit_1 + digit_2
    return total


def task_two(input):
    """Same thing, except now we must select 12 digits"""
    total = 0
    for row in input:
        arr = [int(num) for num in list(row)]
        digits = n_largest_ordered(arr, 12)
        total += sum(digits[i] * 10**(len(digits)-1-i) for i in range(len(digits)))
    return total


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")