import numpy as np

"""
start at 10
    move left -110
    land at 0 with -10
    get to 0 again with -100
so crossed 0 twice

start at 10
    move left -120
    land at 0 with -10
    get to -10 again with -110
so crossed 0 twice

start at 30
    move left -120
    land at 0 with -30
    get to -90 again with -90
so crossed 0 once
"""

def rotate(cmd: str, curr_pos: int, max_pos: int = 99) -> tuple[int, int]:
    """Rotate lock and return new position"""
    # parse 'Lxx' and 'Rxx' strings into -/+ rotations, respectively
    delta_pos = (1-2*int(cmd[0]=="L")) * int(cmd[1:])
    new_pos = curr_pos + delta_pos # update pos

    # count times exactly land on 0 _and_ when passed
    num_crossed = 0
    if delta_pos < 0:
        # new_pos < curr_pos when delta_pos < 0 (it could be negative or positive)
        # the total distance between curr_pos and new_pos is curr_pos-new_pos, which is the
        # same as (curr_pos-1)-(new_pos-1), where we can use -1 to get out of the case curr_pos or new_pos == 0.
        # we want to find out how many times we cycle over this distance, which is found with dist//(max_pos+1).
        # however, floor division isn't distributive, A//C - B//C != (A-B)//C, so we need to div each term individually and combine
        num_crossed = (curr_pos-1)//(max_pos+1) - (new_pos-1)//(max_pos+1)
    else:
        # positive start + postive delta = positive new position
        # can just use b = q*a + r, where q = floor(b/a) with a = max_pos+1
        num_crossed = abs(new_pos)//(max_pos+1)

    # it's not quite mod 99, because adding 1 to 99 gets you to 0.
    # so it's actually mod 100, or max_pos+1. if you did mod 99, then 
    # +1 from 99 would be 100 mod 99 = 1
    # if a < 0, then we can repeatedly add m to a, since m|(a+km) = m|a.
    # in our case, a+km < m. e.g., start at 0, move left 1. -1 mod 100 = 99 mod 100 = 99
    return new_pos % (max_pos+1), num_crossed # wrap around


def rotate_all(cmds: list[str], prev_pos: int, max_pos: int = 99):
    """motivated by this post https://x.com/jargnar/status/1995389674505060856?s=20"""
    # parse 'Lxx' and 'Rxx' strings into -/+ rotations, respectively
    deltas = [(1-2*int(cmd[0]=="R")) * int(cmd[1:]) for cmd in cmds]
    return ((50 + np.cumsum(deltas)) % (max_pos+1)==0).sum()


def task_one(input):
    """
    Given a series of rotations around a lock with 100 notches, in
    [0, 99], find how many times it returns to position 0.
    """
    count = 0
    curr_pos = 50
    for line in input:
        curr_pos, _ = rotate(line, curr_pos)
        if curr_pos == 0: count+=1
    return count


def task_two(input):
    """
    Given a series of rotations around a lock with 100 notches, in
    [0, 99], find how many times it crosses the position 0 in a single turn.
    So, if one rotation moves to 0, this doesn't count. If the next rotation 
    moves _from_ 0 it doesn't count. Only moving passed 0 in a single step counts.
    """
    count = 0
    curr_pos = 50
    for line in input:
        curr_pos, num_crossed = rotate(line, curr_pos)
        count += num_crossed
    return count


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")