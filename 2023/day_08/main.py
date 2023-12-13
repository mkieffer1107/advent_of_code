def create_map(input):
    '''
    Return map of instructions in the form 

        {
            pnt: {"L": pnt, "R": pnt},
            pnt: {"L": pnt, "R": pnt},
            pnt: {"L": pnt, "R": pnt},
        }
    '''

    # TODO: is there a better way like regex to just extract elements
    #        RLK = (TMG, BMB) --> X = (Y, Z)
    mapping = {}
    for line in input:
        pos, next_pos = [x.strip() for x in line.split("=")]
        l_pos, r_pos = [x.strip() for x in next_pos.split(",")]
        l_pos = l_pos.replace("(", "")
        r_pos = r_pos.replace(")", "")
        mapping[pos] = {"L": l_pos, "R": r_pos}
    return mapping

def task_one(input):
    '''
    Find the number of steps required to move from point AAA to ZZZ.

    Given a string of directions

        LRRRLRLL ...

    and next steps, where you choose the left side if your direction is L, right otherwise.

        pnt = (L, R)
        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)

    If you run through the list of directions, just repeat them over again.
    '''
    directions = input[0]
    mapping = create_map(input[2:])    

    steps = 0
    pos = "AAA"
    while pos != "ZZZ":
        direction = directions[steps % len(directions)] # wrap around index
        pos = mapping[pos][direction]
        steps += 1
    return steps


def task_two_slow(input):
    '''
    Oh no! The map you were following is actually for ghosts 👻

    Now, you must start at all nodes that end with A, and navigate
    through all paths simultaneously until they all reach a node
    with a Z at the end -- at the same time. If any one of the nodes
    does not have a Z at the end, continue.
    '''
    directions = input[0]
    mapping = create_map(input[2:])    

    # starting positions are the set of strings of form xxA
    pos = [x for x in mapping.keys() if x[2] == "A"]
    # pos = [x for x in mapping.keys() if x.endswith("A")]
    steps = 0

    # end when all positions are in form xxZ
    # while len(pos) != len([x for x in pos if x[2] == "Z"]):
    while not all([x.endswith("Z") for x in pos]): 
        # move all positions
        for i, p in enumerate(pos):
            direction = directions[steps % len(directions)] # wrap around index
            pos[i] = mapping[p][direction]
        steps += 1
    return steps


def gcd(a, b):
    '''
        Euclidean algorithm for finding GCD(a, b) with b > a

                b = q_0 * a + r_0
                a = q_1 * r_0 + r_1
                r_0 = q_2 * r_1 + r_2
                r_1 = q_3 * r_2 + r_3
                    ...
                r_{N-2} = q_N * r_{N-1} + r_N

       GCD(b, a) = GCD(a, r0) = GCD(r0, r1) = ... = GCD(r_{N-2}, r_{N-1}) = r_{N-1}
    '''
    # make sure b >= a
    if a > b: 
        a, b = b, a

    # start with division algo to get integer quotient and remainder
    q = b//a       # floor div 
    r = b - q * a  # same as b mod a

    # if there is no remainder, then GCD(a, b) = a
    if r == 0:
        return a
    # otherwise, 
    else:
        return gcd(r, a)
    

def lcm_single(a, b):
    return (a*b) // gcd(a, b) # return as int


# could use math.lcm
def lcm(nums):
    '''The LCM of a list of nums must be the lcm of each element, so can do this iteratively'''
    curr_lcm = nums[0]
    for num in nums[1:]:
        curr_lcm = lcm_single(curr_lcm, num)
    return curr_lcm


def task_two(input):
    '''
    This quick approach uses LCMs to identify cycles.

    We can do this because xxZ maps you to the same position as the 
    starting xxA for a particular path. This means that the number of steps
    from xxA to xxZ is the same as going from xxZ back to xxZ again.

         0       1      ...      N
        xxA --> xxx --> ... --> xxZ
        xxZ --> xxx --> ... --> xxZ

    So we have a bunch of cycles that each have a constant number of steps.
    The LCM of all of these cycle steps is the minimum number of steps required 
    such that all paths simultaneously reach the end at xxZ.

    This is because finding the LCM of the number of steps for each path gives the
    smallest number of steps that they can all multiply to. The multiplier for each
    of these step numbers would then be the number of times required to repeat the particular 
    path such that it reaches xxZ at the same time as all the other paths. So 
        LCM(num_steps) / num_steps[i] = num_cycles[i]
    '''
    directions = input[0]
    mapping = create_map(input[2:])    

    # store the number of steps in a cycle for each path -- order doesn't matter
    num_steps = []
    start_pos = [x for x in mapping.keys() if x[2] == "A"]
    
    for pos in start_pos:
        steps = 0
        while not pos.endswith("Z"):
            direction = directions[steps % len(directions)] # wrap around index
            pos = mapping[pos][direction]
            steps += 1
        num_steps.append(steps)
    
    return lcm(num_steps)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.rstrip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")
