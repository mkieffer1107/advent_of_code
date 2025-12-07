def repeating_pattern_slow1(num: int) -> bool:
    """
    Just roll/wrap the digits around. There will be some repetition frequency where subtracting
    the shifted digits from the original will give all zeros. If the period of repetition, 
    which is the number of shifts to a repeat, is equal to len(num), then the number has no repetitions.
    """
    digits = list(map(int, list(str(num))))
    digits_copy = digits.copy()
    
    # iterate over len-1, because len would be one full wrap, returning to the original state
    for i in range(len(digits)-1):
        # wrap the number around
        digits[:-1], digits[-1] = digits[1:], digits[0]
        # if all are 0, we have reached the period of repetetion!
        if all((a-b)==0 for a,b in zip(digits, digits_copy)):
            return True
    return False

def repeating_pattern_slow2(num: int) -> bool:
    """
    Just roll/wrap the digits around. There will be some repetition frequency where subtracting
    the shifted digits from the original will give all zeros. If the period of repetition, 
    which is the number of shifts to a repeat, is equal to len(num), then the number has no repetitions.
    """
    digits = list(map(int, list(str(num))))
    
    # iterate over full range this time
    for i in range(1,len(digits)):
        # just move a window around that accesses slices, instead of rearranging them
        digits_shifted = digits[i:] + digits[:i]
        # if all are 0, we have reached the period of repetetion!
        if all((a-b)==0 for a,b in zip(digits, digits_shifted)):
            return True
    return False


def repeating_pattern(num: int) -> bool:
    """Check if 'digit' is repeated in 'igitdigi'"""
    s = str(num)
    return s in (s + s)[1:-1]


def task_one(input):
    """
    Given a series of ranges, '11-22,95-115,998-1012', find all numbers
    with two repeating digits, e.g., 55, 6464, 123123, and take their sum

    link: https://www.tldraw.com/f/5teYRL_fNL7zrl0KkLzvT?d=v581.-1878.2251.1818.CTny6d-YpmWydGO1gXU4N
    """
    # pop the single str out of the list, split into ranges, and map each range to ints
    ranges = [list(map(int, pair.split("-"))) for pair in list(map(str, input[0].split(",")))]

    # populate endpoint inclusive ranges as a single list of values
    nums = [num for (start, end) in ranges for num in range(start, end+1)]

    total = 0
    for num in nums:
        str_num = str(num)
        if str_num[len(str_num)//2:] == str_num[:len(str_num)//2]:
            total += num

    return total


def task_two(input):
    # pop the single str out of the list, split into ranges, and map each range to ints
    ranges = [list(map(int, pair.split("-"))) for pair in list(map(str, input[0].split(",")))]

    # populate endpoint inclusive ranges as a single list of values
    nums = [num for (start, end) in ranges for num in range(start, end+1)]

    total = 0
    for num in nums:
        if repeating_pattern(num):
            total += num
    return total


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")