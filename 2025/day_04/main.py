import numpy as np
from scipy.ndimage import convolve


def build_grid(input: list[str]) -> np.array:
    char_map = {".": 0, "@": 1}
    return np.array([[char_map[char] for char in row] for row in input])
            

def task_one(input):
    """
    Given a grid of empty, '.', and filled, '@', cells, figure
    out how many filled cells have less than 4 adjacent, filled neighbors.
    """
    grid = build_grid(input)
    kernel = np.ones((3,3))
    kernel[1,1] = 0 # don't count the filled cell

    neighbor_counts = convolve(grid, kernel, mode="constant", cval=0) # pad outside with 0
    filled_mask = (grid == 1) # empty == 0, filled == 1
    return np.sum((neighbor_counts < 4) & filled_mask)


def task_two(input):
    """
    Filled cells with less than 4 filled neighbors can be removed.
    Figure out how many total filled cells can be removed
    """
    grid = build_grid(input)
    grid_copy = grid.copy()
    kernel = np.ones((3,3))
    kernel[1,1] = 0 # don't count the filled cell

    remove_mask = np.empty((1))
    
    while remove_mask.sum() > 0:
        neighbor_counts = convolve(grid, kernel, mode="constant", cval=0) # pad outside with 0
        filled_mask = (grid == 1) # empty == 0, filled == 1
        remove_mask = (neighbor_counts < 4) & filled_mask
        grid[remove_mask] = 0
    return np.sum(grid_copy - grid)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")