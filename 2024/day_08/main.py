def get_pairs(arr):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)): # for j > i to exclude (i,i)
            yield (arr[i], arr[j])


def in_bounds(pos, grid):
    if 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]): 
        return True
    return False


def get_antinodes(pos1, pos2):
    """Get the first anti-nodes at either side of the antennas"""
    # in our case, we'll just define the distance
    # as the x and ys

    # we can just add the displacements onto each
    # antenna location, in opposite directions. this
    # will give us the spot on either side where one
    # antenna is 2x farther away than the other
    disps = tuple(pos2[i]-pos1[i] for i in range(2))

    # we could try adding both directions, if it lands
    # on the other antenna location, don't count it
    # pos1_a = tuple(pos1[i]-disps[i] for i in range(2))
    # pos1_b = tuple(pos1[i]+disps[i] for i in range(2))
    # print("pos1", pos1_a, pos1_b)
    # if pos1_a != pos2:
    #     antinode_1 = pos1_a
    # else:
    #     antinode_1 = pos1_b
    # pos2_a = tuple(pos2[i]-disps[i] for i in range(2))
    # pos2_b = tuple(pos2[i]+disps[i] for i in range(2))
    # print("pos2", pos2_a, pos2_b)
    # if pos2_a != pos1:
    #     antinode_2 = pos2_a
    # else:
    #     antinode_2 = pos2_b
    
    # after looking at prints, we can condense it to this
    antinode_1 = tuple(pos1[i] - disps[i] for i in range(2))
    antinode_2 = tuple(pos2[i] + disps[i] for i in range(2))
    return tuple(antinode_1), tuple(antinode_2)


def get_all_antinodes(pos1, pos2, grid):
    """Get all anti-nodes at either side of the antennas"""
    # now continue moving in either direction away from the antennas,
    # adding anti-nodes until we're out of bounds
    antinodes = []
    disps = tuple(pos2[i]-pos1[i] for i in range(2))

    # we include the initial pos1 and pos2 as candidate locations as well
    while(in_bounds(pos1, grid)):
        antinodes.append(pos1)
        pos1 = tuple(pos1[i] - disps[i] for i in range(2))
    while(in_bounds(pos2, grid)):
        antinodes.append(pos2)
        pos2 = tuple(pos2[i] + disps[i] for i in range(2))
    return antinodes
    

def print_grid(grid, antinode_positions):
    new_grid = [list(row) for row in grid]

    # place # at the anti-node pos if it is empty (keep antennas on grid!)
    for row, col in antinode_positions:
        if in_bounds((row, col), new_grid) and new_grid[row][col] == ".":
            new_grid[row][col] = "#"

    for row in new_grid:
        print("".join(row))


def task_one(input):
    """
    Given a grid with antennas on it, find all unique anti-node
    positions, return the count. Anti-nodes appear at locations
    where the distance from one node to it is exactly twice as 
    far away as a second. This means that there are two: one on
    either side. Anti-nodes only occur for waves of the same frequency
    """
    # store a list of all antenna positions by frequency
    antenna_pos = dict()  # {antenna_freq: [pos tuples]}
    for i, line in enumerate(input):
        for j, spot in enumerate(line):
            if spot != ".":
                # this spot holds an antenna
                antenna_freq = spot
                if antenna_freq in antenna_pos:
                    antenna_pos[antenna_freq].append((i, j))
                else:
                    antenna_pos[antenna_freq] = [(i, j)]

    # now find the two anti-nodes for each pair of antennas in same frequency
    antinode_pos = set() # store only unique locations
    for pos in antenna_pos.values():
        for antenna1, antenna2 in get_pairs(pos):
            antinode1, antinode2 = get_antinodes(antenna1, antenna2)
            if in_bounds(antinode1, input):
                antinode_pos.add(antinode1)
            if in_bounds(antinode2, input):
                antinode_pos.add(antinode2)

    # print_grid(input, antinode_pos)
    return len(list(antinode_pos))


def task_two(input):
    """
    Now it turns out that anti-nodes occur anywhere in line
    with two antennas, repeated at a distance of the spacing
    between the antennas until going out of bounds
    """
    # store a list of all antenna positions by frequency
    antenna_pos = dict()  # {antenna_freq: [pos tuples]}
    for i, line in enumerate(input):
        for j, spot in enumerate(line):
            if spot != ".":
                # this spot holds an antenna
                antenna_freq = spot
                if antenna_freq in antenna_pos:
                    antenna_pos[antenna_freq].append((i, j))
                else:
                    antenna_pos[antenna_freq] = [(i, j)]

    # now find the two anti-nodes for each pair of antennas in same frequency
    antinode_pos = set() # store only unique locations
    for pos in antenna_pos.values():
        for antenna1, antenna2 in get_pairs(pos):
            # we check that anti-nodes are in bounds in the function
            antinodes = get_all_antinodes(antenna1, antenna2, input)
            antinode_pos.update(antinodes) # update instead of add to add whole list

    # print_grid(input, antinode_pos)
    return len(list(antinode_pos))


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")