def task_one(input):
    """
    Given a series of inclusive ranges, [start, end], and newline-delimited
    numbers, figure out how many numbers are out of range.
    """
    ranges = []
    nums = []
    for line in input:
        if "-" in line:
            ranges.append(list(map(int, line.split("-"))))
        else:
            nums.append(int(line))

    # count = 0
    # for num in nums:
    #     for _range in ranges:
    #         if _range[0] <= num <= _range[1]:
    #             count += 1
    #             break # break to guard from overlapping ranges
    # return count

    # check if each num falls into _any_ range
    return sum(
        any(_range[0] <= num <= _range[1] for _range in ranges)
        for num in nums
    )

"""
intersection example:
    [a1, ..., |b1, ..., a2|, ..., b2]
        max(a1, b1) = b1 = start
        min(a2, b2) = a2 = end
    where 
        a1 <= start < end <= b2 

no intersection case:
    [a1, a2, ..., b1, b2]
        max(a1, b1) = b1 = start
        min(a2, b2) = a2 = end
    where 
        start = b1 > a2 = end
"""

def get_intersection(a: list[int], b: list[int]) -> list[int]:
    """Return the intersection between intervals [start, end]"""
    a1, a2 = a
    b1, b2 = b
    # get the tightest intersection between intervals
    start, end = max(a1, b1), min(a2, b2) 
    if start > end: 
        # not >= because we want to capture [10, 14] and [14, 18]
        # as well, which would return [14, 14]
        return None
    else:
        return [start, end]


def overlap(a: list[int], b: list[int]) -> bool:
    """Return the overlap between two intervals [start, end]"""
    a1, a2 = a
    b1, b2 = b
    intersect = get_intersection(a, b)
    adjacent = (a2 == b1-1) or (b2 == a1-1) # e.g., [10, 14] and [15, 20]
    if intersect or adjacent:
        return True
    return False


def task_two(input):
    """Now just find out how many numbers are in the overlapping ranges"""
    ranges = [list(map(int, line.split("-"))) for line in input if "-" in line]
    ranges.sort() # sort in ascending order by interval start

    # ranges is sorted in ascending order by the start of the interval.
    # so we only need to check if the last merged range's interval overlaps
    # with the new range.
    merged_ranges = [ranges[0]]
    for _range in ranges[1:]:
        # we know that _range[i][0] < _range[i+1][0] < ...
        # because ranges is sorted in ascending order by interval start.
        # so we need to check if _range[i][0] < merged_ranges[-1][1].
        # in other words, if the end of the merged range overlaps with the 
        # beginning of the new range
        if overlap(_range, merged_ranges[-1]):
            # if the ranges intersect, merge them!
            # merged_range start should be lower because it comes from previous _range, which are sorted
            new_start = min(_range[0], merged_ranges[-1][0])   
            new_end = max(_range[1], merged_ranges[-1][1])
            merged_ranges[-1] = [new_start, new_end]
        else:
            # otherwise, the new range must have a higher lower bound,
            # merged_range_end < _range_start, since we know merged_range_start < _range_start
            merged_ranges.append(_range)

    # +1 to count first num in range as well
    return sum(1 + end-start for start, end in merged_ranges)

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines() if line.strip()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")