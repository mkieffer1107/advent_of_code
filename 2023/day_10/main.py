import numpy as np
from collections import deque
import matplotlib.pyplot as plt


# define directions in pixel map in format (dx, dy) --> (i + dy, j + dx)
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


# valid directions for a given pipe 
pipe2directions = {
	"|": (up, down),
	"-": (left, right),
	"L": (up, right),
	"J": (up, left),
	"7": (down, left),
	"F": (down, right),
    "S": (up, down, left, right),
	".": (),
}


def bfs(graph, start_idx):
    # store both the idx of node and its distance from start
    queue = deque([(start_idx, 0)])
    visited = {start_idx} # do not store (idx, count) because count increments -- so will always be unique elements
    
    # keep track of the max_dist (dists grid for fun)
    # actually the dists grid can be used to calculate the number of points within the loop
    dists = [[-1 for _ in range(len(graph[0]))] for _ in range(len(graph))] 
    max_dist = 0

    while queue:
        # get first index in queue (FIFO)
        (i, j), dist = queue.popleft()

        # update distances
        if dist > max_dist:
            max_dist = dist
        dists[i][j] = dist

        # get the pipe and the directions it can travel
        pipe = graph[i][j]
        valid_dirs = pipe2directions[pipe]

        # check neighbor pipes for valid movements
        for dx, dy in valid_dirs:
            next_i, next_j = i + dy, j + dx
            if (0 <= next_i < len(graph)) and (0 <= next_j < len(graph[0])):
                if (next_i, next_j) not in visited:
                    # if the index is valid, check if the next pipe connects to the current pipe
                    #   e.g., if the current pipe direction goes up, the next pipe must have a down
                    #   we can check if this is included if the negative of (dx, dy) is in the
                    #   set of possible movements of the next pipe
                    next_pipe = graph[next_i][next_j]
                    next_dirs = pipe2directions[next_pipe]
                    if (-dx, -dy) in next_dirs:
                        # print(graph[next_i][next_j])
                        next_node = ((next_i, next_j), dist+1)
                        queue.append(next_node)
                        visited.add((next_i, next_j)) # only add visited when here when we actually move into it -- another pipe orientation might work
    return max_dist, dists
        

def task_one(input):
    '''
    Given an input map, find the loop with the starting S, and then find the node
    on the loop that is farthest away from the S (along the loop).

    We can consider S to be our starting node, and then use BFS to explore
    adjacent nodes that are valid, meaning that they connect together in the pipe (valid adjacent chars)
    '''
    max_dist, dists = bfs(*input)
    # display_graph(dists, input[1])
    return max_dist


def inside_loop(i, j, graph, dists):
    '''
    if num_intersections is:
        - odd:  point is inside loop
        - even: point is outside of loop
    and
        (odd mod 2) = 1 = True (inside loop!)
    '''
    num_intersections = 0

    # these chars include up directions
    # vertical_boundaries = ("|", "L", "J", "S")
    vertical_boundaries = [char for char, dirs in pipe2directions.items() if up in dirs]

    # iterate over the columns (j) until we hit the end of the graph 
    while j < len(graph[0]):
        # check if the current pipe in a vertical boundary
        # and that it is part of the loop (dist >= 0)
        if graph[i][j] in vertical_boundaries and dists[i][j] >= 0:
            num_intersections += 1
        j += 1

    return num_intersections % 2


def task_two(input):
    '''
    Now we need to find the number of nodes within the loop!

    We can use the distances grid (which stores distances from the start) to help us.
    All distances in the matrix are initialized as -1. So nodes that were not traversed
    will have a distance less than 0. If the node was not traversed, then it is not
    included on the loop, and we must determine whether it is inside the loop.
    
    We can figure out if a point not traversed to is inside or outside using this trick:
        https://www.reddit.com/r/adventofcode/comments/18fgddy/2023_day_10_part_2_using_a_rendering_algorithm_to/
    
    Consider some point on the grid. Draw a ray in some direction (x, y, diagonal, etc... (will use x direction in code)):
        - if the ray intersects the loop an odd number of times, then it is inside the loop
        - if the ray intersects the loop an even number of times, then it is outside the loop
    '''
    _, dists = bfs(*input)
    graph = input[0]

    num_inside = 0

    for i in range(len(graph)):
        for j in range(len(graph[0])):
            # node not traversed -- so it is not on the loop
            if dists[i][j] < 0:
                num_inside += inside_loop(i, j, graph, dists)
    return num_inside


def display_graph(dists, start_idx):
    # unreachable nodes have dist = -1, change them to nan to change color
    dists = np.array(dists, dtype=float)
    dists[dists == -1] = np.nan

    plt.imshow(dists, cmap="viridis")  # Choose a colormap
    plt.colorbar()
    plt.title(f"distances to reachable nodes from start_idx {start_idx}")
    plt.grid(False)  
    plt.text(start_idx[1], start_idx[0], "X", color="red", fontsize=15, ha="center", va="center")
    plt.show()


def build_graph(input):
    graph = []
    start_idx = None
    for i, line in enumerate(input):
        row = []
        for j, char in enumerate(line):
            row.append(char)
            if char == "S":
                start_idx = (i, j)
        graph.append(row)
    return (graph, start_idx)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    input = build_graph(input)

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")