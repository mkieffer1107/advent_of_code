def task_one(input):
    """
    Given two columns of numbers, find the difference between 
    each next smallest number in the cols.
    """
    # first store the columns of numbers in order
    llist, rlist = [], []
    for line in input:
        num1, num2 = map(int, line.split())
        llist.append(num1)
        rlist.append(num2)
    rlist = sorted(rlist)
    llist = sorted(llist)

    # now find the differences
    total_diff = 0
    for num1, num2 in zip(rlist,llist):
        diff = num1 - num2
        diff = diff * -1 if diff < 0 else diff
        total_diff += diff
    return total_diff


def task_two(input):
    """
    This time, find out how many times each number from the
    left list appears in the right list. Then the similarity
    score is calculated as left_num * freq_in_right_list
    """
    # this time we'll use a dict to keep tabs on freqs
    nums, freqs = list(), dict()
    for line in input:
        num1, num2 = map(int, line.split())
        # need unique nums only in leftl list
        if num1 not in nums:
            nums.append(num1) # could use a set here
        freqs[num2] = freqs.get(num2, 0) + 1
    
    total = 0
    for num in nums:
        total += num * freqs.get(num, 0)
    return total

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")
