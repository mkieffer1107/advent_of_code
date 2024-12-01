'''
I originally tried to place different permutations of blocks manually, 
but found that overcomplicated things... So I followed this tutorial instead:

    https://www.reddit.com/r/adventofcode/comments/18hg99r/2023_day_12_simple_tutorial_with_memoization/
    another: https://www.reddit.com/r/adventofcode/comments/18hbbxe/2023_day_12python_stepbystep_tutorial_with_bonus/

This helped me learn some dynamic programming!

For a record string "??#???#?????.? 5,1,1" with groups [5,1,1], we can create a memoization table
that records the number of arrangements at each index based on the number of remaining groups.
Memoization is a technique where we store the results of expensive function calls and return the cached result when the same inputs occur again. 

        +-------------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
        | Rem. Groups | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13|     example arrangements
        +-------------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
        |           0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | []
        +-------------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
        |           1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 4 | 3 | 2 | 0 | 1 | [5], [1]
        +-------------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
        |           2 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 7 | 4 | 2 | 1 | 0 | 0 | [5,1], [1,5], [1,1]
        +-------------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
        |           3 |12 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | [5, 1, 1], ... 
        +-------------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

The y-axis gives the number of remaining groups. Because there are 3 groups in [5,1,1], the y-axis has a max of 3.
At index 9 with 2 groups (1, 1) remaining, there are 4 possible arrangements:

                                #.#..
                                #...#
                                .#..#
                                ..#.#

Notice how this is laid out:
    - for 0 remaining groups, there are no possible arrangements of springs possible -- because there are none left!
    
So how do we fill in a position for a given index and number of remaining groups:                                
    - at index i, we can either:
        1) place one of the groups down, and then move up in the y-axis since we have one less group remaining
            -   rem. groups: y -> y-1
            - and then advance the index position i by (1 + groupsize), where groupsize is the size of the remaining group we just placed
            -   index: i -> i + groupsize + 1      
            -   (we add groupsize because the spring occupies this part of the string, and +1 because there is at least one space between spring groups)
        2) or not place anything at index i, and instead advance to the index position (i+1) and repeat either (1) or (2)

Placing a spring down is of course contingent on there being either '#' or '?' chars in all positions record[i:i+groupsize] for a particular group at index i

----------------------------------------------------
Example:

Suppose we want to find the number of possible arrangements at index i = 8 with groups [5, 1, 1].

We are assuming that the number of remaining groups is two, so we start at y=2, x=8

1) assuming that 5 has been placed, leaving us with [1, 1]
    1) Place a group at index i = 8 and then calculate arrangements for subsequent indexes
        - place group 1 from [1, 1], and then advance idx i -> i + groupsize + 1 = 8 + 1 + 1 = 10
        - so 
            -   y -> y-1 -> 2-1 -> y = 1 
            -   x -> x+1+1 ->      x = 10
        - we can look at how many ways there are to place a group of size 1 in the remaining substring after idx i = 10
        -   "??#???#?????.?"[10:] -> "??.?"
        - the group of size 1 can be placed at any of the 3 '?'s, so memotable[1, 10] = 3

    2) Place a group at index i + 1 = 8 + 1 = 9
        - same deal: how many ways are there to fit a group of size 1 in the substring starting at idx i = 9:
            - "??#???#?????.?"[9:] -> "???.?"
        - we place a group down, so y decrements to y=1 and x=9
        -   there are 4 ways to fit the group of size 1, so memotable[1, 9] = 4

    Thus, there are a total of 3 + 4 = 7 ways if we place down a group of size 1.

2) assuming that 1 has been placed, leaving us with [5, 1]
    1) Place a group at index i = 8 and then calculate arrangements for subsequent indexes
        - place group 5 from [5, 1], and then advance idx i -> i + groupsize + 1 = 8 + 5 + 1 = 14
        - index i = 14 is out of bounds, so we must place down group of size 1
            - in this case, we are repeating the steps from above, but with only a single group instead of two ones
'''

def solve(record, groups, cache, idx):
    '''
        record: str of spring states
        groups: list containing possible spring sizes
        cache:  memoization table of possible arrangements
        idx:    current index in record str being considered
    '''
    # if no groups left
    if len(groups) == 0:       
        if idx < len(record) and "#" in record[idx:]:
            # no more groups to place, but there is still an actual spring '#'
            return 0
        else:
            # no more groups to place, and there are no more actual springs '#' 
            return 1
    
    # advance i to next available '?' or '#' in record
    while idx < len(record) and record[idx] not in ["?", "#"]:
    # for char in (record[idx:]):
        idx += 1
        # if not found, then i will be out of range for record str
        # if char in ["?", "#"]:
        #     break 

    # if have advanced i to the end of the string -- no more '?' or '#'
    if idx >= len(record):
        return 0
    
    # if we have already found this spring state
    if (idx, len(groups)) in cache:
        return cache[(idx, len(groups))]

    # base cases finished

    # store the number of ways to arrange the groups for a given record
    num_arrangements = 0

    # try to place the first group down at the current index i
    # check that all chars are (potential) springs starting at curr idx where the group will lie
    groupsize = groups[0]
    if (idx + groupsize < len(record)) and all(char in ["?", "#"] for char in record[idx:idx+groupsize]) \
    and record[idx+groupsize] != "#":
    # if can_fit(record, idx, idx + groupsize):
        # if idx + groupsize + 1 < len(record) and record[idx+groupsize+1] != "#":
        new_groups = groups[1:]        # remove first group from list
        new_idx = idx + groupsize + 1  # increment idx by groupsize and min spacing between groups of 1
        num_arrangements += solve(record, new_groups, cache, new_idx)


    # if the first group doesn't fit, then try the next index: idx -> idx+1 with current set of groups
    # try al permutations with the mystery char
    if record[idx] == "?":
        new_idx = idx + 1
        num_arrangements += solve(record, groups, cache, new_idx)

    # store the number of arrangements to the memoization table
    cache[(idx, len(groups))] = num_arrangements
    return num_arrangements

# def can_fit(springs, start, end):
#     # Ensure the range's end fits into the springs string
#     if end > len(springs):
#         return False
#     # Ensure all chars in range are either '?' or '#', not '.'
#     if any(x == '.' for x in springs[start:end]):
#         return False
#     # Make sure the next char is out of bounds, '.', or '?', not '#'
#     if end < len(springs) and springs[end] == '#':
#         return False
#     return True


def task_one(input):
    '''
    Each row contains spring records: 
        '.' means operational, 
        '#' means damaged, 
        '?' means unknown condition.

    After each row is a list of numbers for the size of 
    each contiguous group of damaged springs, e.g,
        #.#.### 1,1,3
        .??..??...?##. 1,1,3

    But of course, '?' might actually be a '#'. 

    Importantly, groups are always separated by at least one operational spring: #### would always be (4), never (2,2).

    Return the sum of different possible arrangements of each row: 
    '''
    num_arrangements = 0
    for line in input:
        record, groups = line.split()
        groups = list(map(int, groups.split(",")))
        num_arrangements += solve(record, groups, {}, 0) # start with empty cache={} and idx=0
        # print(solve(record, groups, {}, 0))
    return num_arrangements

def task_two(input):
    ...

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")