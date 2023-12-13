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
         destination_range_start, source_range_start, range_length
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
    src is an int
    mapping is tuple (start_src, start_dest, start_length)
        - start_src:  start of the mapping interval
        - start_dest: start of the destination interval
        - start_length:  width of the interval

    mapping interval = [start_src, start_src + start_length)
    destination interval = [start_dest, start_dest + start_length)

    - if src is not in the mapping interval, then it maps to itself: src -> src

    - if src is in the mapping interval, then it should be mapped to the destination interval
    
        - but only the start and end of each interval is given, so to find out how far from
          the start of the destination interval src should be mapped, we must find its offset
          from the mapping interval

            offset = src - start_src (assuming src > start_src - logic below)
            dest_mapping = start_dest + offset
    
    ----------------------------------------------------        
    store the intervals -- like histogram binning
    then just add the offset of the selected key

    given an input, find the first src mapping key that is less than
    it, then check if the interval includes it

    if it does, find the difference between it and the src,
    add this to the dest start interval, and return that value
    
    if the inputted number does not lie within any interval
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

    # start_src, start_dest, start_length = mapping[start_idx]

    # if src < start_src + start_length:
    #     offset = src - start_src
    #     return start_dest + offset
    # else:
    #     return src
    
    # condensed
    for start_src, start_dest, start_length in mapping:
        if start_src <= src < start_src + start_length:
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
    Now, the seed lines give the start of interval and length, e.g.
    
        seeds: 79 14 55 13 --> seeds in intervals [79, 14) and [55, 13)

    Simple modification, but huge intervals. The key is parallelization or something...
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

    nice visualization:
        https://www.reddit.com/r/adventofcode/comments/18bq77i/2023_day_5_part_2_walkthrough_and_a_picture_to/?utm_source=share&utm_medium=web2x&context=3
    
    The input seeds' intervals and their subsequent transformations / mappings do not overlap. I initially tried
    to just map the start and end numbers for each interval, but found that this did not work because it did not
    account for the mapping of numbers within the interval, i.e., [start, inside1, inside2, ..., end). 

    The key is to remap / split intervals after each transformation if there is an intersection. 

    We are given a source interval S = [s1, s2), a mapping interval M = [m1, m2) (the range of numbers that are mapped 
    to some destination), and a map (maps intervals in the mapping interval to some destination interval D = [d1, d2))

        - if the source interval is outside of the mapping interval, then it maps to itself: 
                    
                    S !c M, so S -> S

        - if the source interval lies entirely inside the mapping interval, then it is shifted via the map by an offset:
            - but only the start and end of each interval is given (source S, mapping M, destination D), so to find 
              out how far from the start of the destination interval D[0] the source interval S should be mapped, we 
              must find its offset from the mapping interval M

                    a = S[0] - M[0] = s1 - m1                    (a is offset -- we assume s1 > m1 because S c M)
                    S c M, so map[S]-> [d1 + a, d2 + a) = D + a  (destination interval plus an offset)
                    
        - if part of the source interval lies within the mapping interval, and part of it lies outside of it, we
          must first split the source interval into the intesection of S and M, and to the difference of S and M 

                    some of S c M and some of S !c M

                    i = (S ∩ M) c M   (intersection)
                    b = (S - M) !c M  (difference)

         now we can map the intersection and difference separately

                    i c M, so map[i] -> D + a    (where a is offset)

                    b !c M, so b -> b
    
    This process is repeated for each map. After the final transformation, the lowest interval value is the smallest final 
    possible output, so it is the answer!
    
    '''
    seeds = input[0]
    mappings = input[1:]   

    # seeds come in pairs: range_start_1, range_len_1, range_start_2, range_len_2, ...
    seed_intervals = [(i, i+j) for i, j in list(zip(seeds, seeds[1:]))[::2]] # ha ha


    # the seeds are the initial intervals
    intervals = seed_intervals
    for mapping in mappings:

        # store the new intervals created for the current map   
        new_intervals = []

        # iterate over each mapping interval within the current map
        #   need to find all mappings within the current map, and then
        #   add them to the new_intervals list

        for start_src, start_dest, start_length in mapping:
            # interval of numbers that are transformed by the current map
            mapping_interval = (start_src, start_src + start_length)
            src_start, src_end = mapping_interval

            # store the mappings of each source interval to its destination
            # for the current mapping_interval within the current map
            dest_intervals = []
            
            while intervals:
                # remove and map each source interval in the list
                src_interval = intervals.pop()

                '''Approach 1'''
                # intersection = (max(src_interval[0], mapping_interval[0]), min(src_interval[1], mapping_interval[1]))
                # if intersection[0] < intersection[1]:
                #     offset = [bound - mapping_interval[0] for bound in intersection]
                #     new_intervals.append((start_dest + offset[0], start_dest + offset[1]) )
                
                # # valid case: src_interval[0]-- src_interval[1] -- mapping_interval[0]
                # left_interval = (src_interval[0], min(src_interval[1], mapping_interval[0]))
                # if left_interval[0] < left_interval[1]:
                #     dest_intervals.append(left_interval)  
                
                # # valid case: mapping_interval[1] -- src_interval[0] -- src_interval[1]                       
                # right_interval = (max(src_interval[0], mapping_interval[1]), src_interval[1])
                # if right_interval[0] < right_interval[1]:
                #     dest_intervals.append(right_interval)
                '''End approach 1'''        
        
                '''Approach 2'''
                # split src_interval if intersections between the src_interval and mapping_interval
                intersection = get_intersection(src_interval, mapping_interval)
                
                if intersection is None:
                    # if the intersection is invalid (start > end), then there is no intersection, so 
                    # src_interval is not within mapping_interval --> return src_interval
                    dest_intervals.append(src_interval)
                else:
                    # intersection exists - need to map this
                    # and then deal with the difference of src_interval and mapping_interval if they exist
                    if src_interval[0] < mapping_interval[0]:
                        # if the smallest value of the src_interval is smaller than the smallest value of the mapping_interval
                        # then there is a sub-interval to the left of the mapping_interval -- starting before the intersection
                        #   src_interval[0]-- src_interval[1] -- mapping_interval
                        left_interval = (src_interval[0], intersection[0]-1) # start at beginning of src and up to right before the intersection
                        dest_intervals.append(left_interval)

                    if mapping_interval[1] < src_interval[1]:
                        # if the largest value of the src_interval is larger than the largest value of the mapping_interval
                        # then there is a sub-interval to the right of the mapping_interval -- starting after the intersection
                        #   mapping_interval -- src_interval[0] -- src_interval[1]                    
                        right_interval = (intersection[1], src_interval[1]) # start right after intersection and go to end of src interval
                        dest_intervals.append(right_interval)               #  the end of intersection is not inclusive, so no +1
                    
                    # map the intersection interval 
                    # get the offset of the intersection start and end from the mapping interval start
                    offset = [bound - mapping_interval[0] for bound in intersection]
                    mapped_interval = (start_dest + offset[0], start_dest + offset[1]) 
                    # dest_intervals.append(mapped_interval)

                    # for the intersection, this interval is completely contained within one of the mapping intervals
                    #   therefore, it cannot be contained by another mapping interval within the current map
                    #   so we can go ahead and add it to the list of completed intervals for the entire map 
                    new_intervals.append(mapped_interval)
                '''End approach 2'''  

            # the new set of intervals is composed of those intervals that were not contained within the mapping_interval
            #   so they must be passed on to the next mapping_interval to be checked + split if necessary
            intervals = dest_intervals

        # the final set of intervals for the map contains those that were previously completed (new_intervals)
        #   plus the final output of the final mapping_interval (intervals)
        intervals = new_intervals + intervals

    # return the smallest starting value out of every interval
    return min(start for start, end in intervals)


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