# made with o1! i don't use llms for the actual aoc code 😇

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors  # Import matplotlib.colors
import numpy as np
import copy
from tqdm import tqdm

# Global variables for controlling animation speed and durations
ANIMATION_INTERVAL = 60  # Time between frames in milliseconds
CELL_HIGHLIGHT_DURATION = 1  # Number of frames a cell remains highlighted when being checked
COLOR_HOLD_DURATION = 1  # Number of frames a color change lasts (e.g., red before fading)
FADE_DURATION = 10  # Number of frames over which the cell fades from color to white

def moore_neighbors():
    # Adjusted to search neighbors left-to-right, top-to-bottom
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if not (dx == 0 and dy == 0):  # Exclude the current cell (0, 0)
                yield dx, dy

def update_fading_cells(fading_cells):
    cells_to_remove = []
    for cell in fading_cells:
        initial_color, fade_time = fading_cells[cell]
        fade_time -= 1
        if fade_time <= 0:
            cells_to_remove.append(cell)
        else:
            fading_cells[cell] = (initial_color, fade_time)
    for cell in cells_to_remove:
        del fading_cells[cell]

def get_fade_color(initial_color, fade_time):
    fraction = fade_time / FADE_DURATION
    color_vec = np.array(mcolors.to_rgb(color_map[initial_color]))  # Use mcolors.to_rgb
    white_color = np.array([1, 1, 1])
    color = fraction * color_vec + (1 - fraction) * white_color
    return color

# Updated color map with "skyblue" for a slightly darker blue
color_map = {
    'skyblue': 'skyblue',
    'red': 'red',
    'yellow': 'yellow',
    'green': 'green',
    'white': 'white'
}

def search_around(idx, char, grid, current_seqs, frames, grid_colors, fading_cells):
    row, col = idx
    grid_shape = (len(grid), len(grid[0]))
    matches = []
    # Check the Moore neighborhood around the current idx for next char
    for dx, dy in moore_neighbors():
        i = row + dy
        j = col + dx
        if (0 <= i < grid_shape[0]) and (0 <= j < grid_shape[1]):
            # Skip cells already part of a sequence (green cells)
            if grid_colors.get((i, j)) == 'green':
                continue
            # Remove cell from fading_cells if it's there
            if (i, j) in fading_cells:
                del fading_cells[(i, j)]
            # Highlight the cell being checked
            grid_colors[(i, j)] = 'yellow'
            for _ in range(CELL_HIGHLIGHT_DURATION):
                update_fading_cells(fading_cells)
                frames.append({'grid_colors': copy.deepcopy(grid_colors),
                               'fading_cells': copy.deepcopy(fading_cells)})
            if grid[i][j] == char:
                matches.append((i, j))
                grid_colors[(i, j)] = 'green'  # Keep it green permanently
                # Remove from fading_cells to ensure green appears immediately
                if (i, j) in fading_cells:
                    del fading_cells[(i, j)]
                for _ in range(COLOR_HOLD_DURATION):
                    update_fading_cells(fading_cells)
                    frames.append({'grid_colors': copy.deepcopy(grid_colors),
                                   'fading_cells': copy.deepcopy(fading_cells)})
            else:
                # Immediately change to red
                grid_colors[(i, j)] = 'red'
                for _ in range(COLOR_HOLD_DURATION):
                    update_fading_cells(fading_cells)
                    frames.append({'grid_colors': copy.deepcopy(grid_colors),
                                   'fading_cells': copy.deepcopy(fading_cells)})
                # Start fading from red
                grid_colors.pop((i, j))
                fading_cells[(i, j)] = ('red', FADE_DURATION)
    return matches

def find_sequences(seqs, char, grid, frames, grid_colors, fading_cells):
    new_seqs = []
    for seq in seqs:
        matches = []
        # Find if char touches last idx in the sequence
        if len(seq) == 1:
            # In the case where we only have 'X', check all neighbors
            matches = search_around(seq[0], char, grid, set([idx for s in seqs for idx in s]),
                                    frames, grid_colors, fading_cells)
            for match in matches:
                new_seqs.append(seq + [match])
        else:
            # Otherwise, we need to check in the same direction
            penu_idx, final_idx = seq[-2:]  # Penultimate idx --> final idx
            dir_vec = [final_idx[i] - penu_idx[i] for i in (0, 1)]  # Direction vector
            i, j = [final_idx[i] + dir_vec[i] for i in (0, 1)]  # New idx
            if (0 <= i < len(grid)) and (0 <= j < len(grid[0])):
                # Skip cells already part of a sequence (green cells)
                if grid_colors.get((i, j)) == 'green':
                    continue
                # Remove cell from fading_cells if it's there
                if (i, j) in fading_cells:
                    del fading_cells[(i, j)]
                # Highlight the cell being checked
                grid_colors[(i, j)] = 'yellow'
                for _ in range(CELL_HIGHLIGHT_DURATION):
                    update_fading_cells(fading_cells)
                    frames.append({'grid_colors': copy.deepcopy(grid_colors),
                                   'fading_cells': copy.deepcopy(fading_cells)})
                if grid[i][j] == char:
                    matches = [(i, j)]  # There can only be one match in this direction
                    grid_colors[(i, j)] = 'green'  # Keep it green permanently
                    # Remove from fading_cells to ensure green appears immediately
                    if (i, j) in fading_cells:
                        del fading_cells[(i, j)]
                    for _ in range(COLOR_HOLD_DURATION):
                        update_fading_cells(fading_cells)
                        frames.append({'grid_colors': copy.deepcopy(grid_colors),
                                       'fading_cells': copy.deepcopy(fading_cells)})
                    new_seqs.append(seq + [(i, j)])
                else:
                    # Immediately change to red
                    grid_colors[(i, j)] = 'red'
                    for _ in range(COLOR_HOLD_DURATION):
                        update_fading_cells(fading_cells)
                        frames.append({'grid_colors': copy.deepcopy(grid_colors),
                                       'fading_cells': copy.deepcopy(fading_cells)})
                    # Start fading from red
                    grid_colors.pop((i, j))
                    fading_cells[(i, j)] = ('red', FADE_DURATION)
    return new_seqs

def visualize_search(grid, frames):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()
    plt.axis('off')

    rects = {}
    texts = {}

    # Draw the grid and store rectangle patches and texts
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            rect = patches.Rectangle((j, i), 1, 1, linewidth=1,
                                     edgecolor='black', facecolor='white')
            ax.add_patch(rect)
            rects[(i, j)] = rect
            text = ax.text(j + 0.5, i + 0.5, grid[i][j], fontsize=16,
                           ha='center', va='center', color='black')
            texts[(i, j)] = text

    ax.set_xlim(0, len(grid[0]))
    ax.set_ylim(0, len(grid))

    # Create a function to update the progress bar
    num_frames = len(frames)
    pbar = tqdm(total=num_frames, desc='Saving animation')

    def update(frame_index):
        frame = frames[frame_index]
        grid_colors = frame['grid_colors']
        fading_cells = frame['fading_cells']
        # Update cells based on priority
        for (i, j) in rects:
            if (i, j) in grid_colors:
                rects[(i, j)].set_facecolor(grid_colors[(i, j)])
            elif (i, j) in fading_cells:
                initial_color, fade_time = fading_cells[(i, j)]
                color = get_fade_color(initial_color, fade_time)
                rects[(i, j)].set_facecolor(color)
            else:
                rects[(i, j)].set_facecolor('white')
        pbar.update(1)
        return rects.values()

    ani = FuncAnimation(fig, update, frames=range(len(frames)), blit=False,
                        interval=ANIMATION_INTERVAL, repeat=False)

    # Save the animation as a video file
    ani.save('animation.mp4', writer='ffmpeg', fps=1000 // ANIMATION_INTERVAL)

    pbar.close()

def task_one_with_visualization(input_grid):
    """
    Given a crossword puzzle, find all instances
    of 'XMAS' horizontally, vertically, diagonally, backwards,
    and visualize the search process.
    """
    grid = [list(line) for line in input_grid]

    # Initialize grid colors
    grid_colors = {}  # Cells with permanent colors (e.g., 'green')

    # Prepare frames for animation
    frames = []

    # Initialize fading cells
    fading_cells = {}

    # Find all instances of 'X' and highlight them
    seqs = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # Remove cell from fading_cells if it's there
            if (i, j) in fading_cells:
                del fading_cells[(i, j)]
            # Highlight the cell being examined
            grid_colors[(i, j)] = 'skyblue'
            for _ in range(CELL_HIGHLIGHT_DURATION):
                update_fading_cells(fading_cells)
                frames.append({'grid_colors': copy.deepcopy(grid_colors),
                               'fading_cells': copy.deepcopy(fading_cells)})
            if grid[i][j] == "X":
                seqs.append([(i, j)])  # Add [idx1] to full list
                grid_colors[(i, j)] = 'green'  # Keep it green permanently
                # Remove from fading_cells to ensure green appears immediately
                if (i, j) in fading_cells:
                    del fading_cells[(i, j)]
                for _ in range(COLOR_HOLD_DURATION):
                    update_fading_cells(fading_cells)
                    frames.append({'grid_colors': copy.deepcopy(grid_colors),
                                   'fading_cells': copy.deepcopy(fading_cells)})
            else:
                # Start fading from skyblue
                grid_colors.pop((i, j))
                fading_cells[(i, j)] = ('skyblue', FADE_DURATION)
                update_fading_cells(fading_cells)
                frames.append({'grid_colors': copy.deepcopy(grid_colors),
                               'fading_cells': copy.deepcopy(fading_cells)})

    # After the initial search, ensure all non-'X' cells continue fading
    update_fading_cells(fading_cells)
    frames.append({'grid_colors': copy.deepcopy(grid_colors),
                   'fading_cells': copy.deepcopy(fading_cells)})

    # Search for 'M', 'A', 'S'
    for char in "MAS":
        seqs = find_sequences(seqs, char, grid, frames, grid_colors, fading_cells)

    # Visualize the search and save the animation
    visualize_search(grid, frames)

    return len(seqs)

if __name__ == "__main__":
    # Example puzzle
    grid = [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX"
    ]
    count = task_one_with_visualization(grid)
    print(f"Total sequences found: {count}")
