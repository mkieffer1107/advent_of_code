from functools import cache


def print_grid(grid: list[list]):
    print("\n".join("".join(row) for row in grid) + "\n")


def task_one(input):
    """
    Given a grid, a source point, and a downard moving beam, figure out how many
    times the beam is split by '^' chars. Upon being split the beam continues
    propagating down from the left and right of the splitter like '|^|'
    """
    grid = [list(row) for row in input]
    source_pos = [0, input[0].find("S")]
    # instead of updating entire grid, just keep track of latest beam front idxs
    beam_idxs = [[1, source_pos[1]]] # beam appears one below the source

    num_splits = 0
    while len(beam_idxs) > 0:
        # propagate beam down until it splits or leaves grid
        beam_i, beam_j = beam_idxs.pop()
        # print_grid(grid)

        # we also check that a beam hasn't been there yet, since we'd just be
        # following a previously charted path
        while beam_i < len(grid) and grid[beam_i][beam_j] != "^" and grid[beam_i][beam_j] != "|":
            grid[beam_i][beam_j] = "|"
            beam_i += 1
            
        # if beam leaves grid, we don't need to do anything with it
        # but we must add new beams upon a split
        if beam_i < len(grid) and grid[beam_i][beam_j] == "^":
            num_splits += 1
            beam_idxs.extend([[beam_i, beam_j+1], [beam_i, beam_j-1]])
    return num_splits 


def task_two(input):
    """
    Track the number of possible trajectories down.
    A trajectory is a unique set of left/right movements at splitters
    """
    grid = [list(row) for row in input]
    source_pos = [0, input[0].find("S")]
    beam_idx = (1, source_pos[1]) # beam appears one below the source

    # grid is list[list] can't be hashed for the cache... easiest to
    # throw the counting function inside here than figure that out :)
    @cache
    def count_trajectories(i: int, j: int) -> int:
        if i > len(grid[0]):
            # a beam has reached the bottom, counting as 1 trajectory
            return 1
        elif grid[i][j] == "^":
            # split the beam into two new trajectories
            return count_trajectories(i, j-1) + count_trajectories(i, j+1)
        # keep propagating down
        return count_trajectories(i+1, j)
    
    return count_trajectories(beam_idx[0], beam_idx[1])
    

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines() if line.strip()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")