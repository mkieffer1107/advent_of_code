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
    if (idx + groupsize < len(record)) and all(char in ["?", "#"] for char in record[idx:idx+groupsize]):
    # and record[idx+groupsize] != "#":
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