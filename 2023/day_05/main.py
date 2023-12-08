def parse_input(input):
    '''Return a list of lists that stores the seed numbers and mappings in order'''
    # header line stores seeds
    seeds_str = input[0].split(":")[1]
    seeds = list(map(int, seeds_str.split()))
    # seeds = [int(seed.strip()) for seed in seeds_str.split()]

    # store the seeds and mappings in order 
    out = [seeds]

    # input.pop(0) # remove first line -- can actually keep this, as it will be skipped 
    #                                     since words and nums are on the same line
    
    # cache to store lines for each map
    mapping_lines = []

    # include a final string in the input lines in order to create the final map because
    # the previous map from lines above is created when new string is reached
    for line in input + ["eof"]:
        # if the first char is a letter (name of map)
        # then create a map of the stuff above it, and flush the cache
        if line[0].isalpha():
            if len(mapping_lines) > 0:
                out.append(create_map(mapping_lines))
                mapping_lines.clear()
        # otherwise, store the lines for the new map
        elif line[0].isdigit():
            mapping_lines.append(line)
        
    return out


def create_map(mapping_lines):
    '''
    Convert text to dictionaries. Text mappings have format:
         destination range start, source range start, range length
    Return a dictionary in the form
        source, destination 
    If a source num is not given, then its mapping is itself, e.g.,
        10 -> 10
    '''
    # split by newline -- conditional filters out whitespace char only lines
    # same as doing 'if not line == ""'
    mapping = []
    for line in mapping_lines:
        # quick way to convert all str to int during split
        dest, src, ran = map(int, line.split())
        mapping.append((src, dest, ran))

    # sort in ascending order by src
    return sorted(mapping, key=lambda x: x[0])


def get_mapping(src, mapping):
    '''
    store the ranges -- like histogram binning
    then just add the offset of the selected key

    given an input, find the first src mapping key that is less than
    it, then check if the range includes it

    if it does, find the difference between it and the src,
    add this to the dest start range, and return that value
    
    if the inputted number does not lie within any range
    in the mapping dict, just return itself    
    '''
    # start_idx = None
    # for i in range(len(mapping)):
    #     key = mapping[i][0]
    #     if src < key:
    #         # first key smaller than the src input
    #         start_idx = i-1
    #         break
    
    # # case where src is larger than all keys
    # # set the start_idx to be the last idx in the list
    # if start_idx is None:
    #     start_idx = len(mapping) - 1

    # start_src, start_dest, start_ran = mapping[start_idx]

    # if src < start_src + start_ran:
    #     offset = src - start_src
    #     return start_dest + offset
    # else:
    #     return src
    
    # condensed
    for start_src, start_dest, start_ran in mapping:
        if start_src <= src < start_src + start_ran:
            offset = src - start_src
            return start_dest + offset
    return src
    
def task_one(input):
    '''
    Given a bunch of mappings with an input of a seed number, return the smallest
    location mapping from the initial seed values.
    '''
    seeds = input[0]
    mappings = input[1:]
    outs = []

    for x in seeds:
        for mapping in mappings:
            x = get_mapping(x, mapping)
        outs.append(x)
    return min(outs)

    
def task_two_slow(input):
    '''
    Now, the seed lines give the start of range and length, e.g.
    
        seeds: 79 14 55 13 --> seeds in range [79, 14) and [55, 13)

    Simple modification, but huge ranges. The key is parallelization or something...
    '''
    seeds = input[0]
    mappings = input[1:]
    outs = []

    # seeds come in pairs: range_start_1, range_len_1, range_start_2, range_len_2, ...
    ranges = [(i, i+j) for i, j in list(zip(seeds, seeds[1:]))[::2]] # ha ha

    for i, j in ranges:
        for x in range(i, j):
            for mapping in mappings:
                x = get_mapping(x, mapping)
            outs.append(x)

    return min(outs)



def get_intersection(r1, r2):
    '''r1 and r2 are intervals of form [start, end)'''
    start1, end1 = r1   # s1 -- e1
    start2, end2 = r2   # s2 -- e2

    new_start = max(start1, start2) 
    new_end = min(end1, end2)

    if new_end <= new_start:
        return None
    else:
        return (new_start, new_end)


def task_two(input):
    '''
    Everything above was too slow for part 2 :(
    I decided to see how some of the people on the leaderboard solved it:

        https://github.com/Kroppeb/AdventOfCodeSolutions2/blob/master/solutions/src/solutions/y2023/day%205%20fixed.kt
        https://github.com/mrphlip/aoc/blob/master/2023/05.md
    
    The input seeds' ranges do not overlap. However, the ranges of
    their output mappings do overlap. I thought this might be the case, but initially tried it anyway
    because I knew it would offer a significant speedup.

    The key is to remap intervals after each transformation. During each mapping, check for intersections 
    between the ranges. If intersections exist, the ranges might need to be split into several sub-ranges.

    This will automatically
    '''
    seeds = input[0]
    mappings = input[1:]
    outs = []

    # seeds come in pairs: range_start_1, range_len_1, range_start_2, range_len_2, ...
    seed_ranges = [(i, i+j) for i, j in list(zip(seeds, seeds[1:]))[::2]] # ha ha

    for seed_range in seed_ranges:
        for start_src, start_dest, start_ran in mappings:
            map_range = (start_src, start_dest + start_ran)
            new_range = get_intersection(seed_range, map_range)
            
            if new_range is None:
                ...



    return min(outs)






if __name__ == "__main__":
    with open("input.txt", "r") as f:
        # input = parse_input(f.read())
        # skip empty lines
        input = [line.strip() for line in f.readlines() if line.strip()]

    input = parse_input(input)


    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")

