def moore_neighbors():
    for i in range(-1, 2):
        for j in range(-1, 2):
            yield (i, j) # checking (0, 0) which is unnecessary


def search_around(idx, char, grid):
    # returns list of tuples of neighbors to idx with matching char
    row, col = idx
    grid_shape = (len(grid), len(grid[0]))
    matches = []
    # check the moore neighborhood around the current idx for next char
    for dx, dy in moore_neighbors():
        i = row + dy
        j = col + dx
        if (0 <= i < grid_shape[0]) and (0 <= j < grid_shape[1]):
            if grid[i][j] == char:
                matches.append((i, j))
    return matches


def find_sequences(seqs, char, grid):
    # return list of idx groups of sequences ('X', 'XM', ...)
    # seqs looks like: [(seq1), (seq2), ...] where seq_i looks like (idx1, idx2, ...) with idx_i (i, j)
    new_seqs = []
    for seq in seqs:
        matches = []
        
        # find if char touches last idx in the sequence
        if len(seq) == 1:
            # in the case where we only have X, check all neighbors
            matches = search_around(seq[0], char, grid)
        else:
            # otherwise, we need to check in the same direction, so words don't twist around 
            # direction will always be in {-1, 0, 1}. to find next char, just add direction 
            # vector onto the final index.
            penu_idx, final_idx = seq[-2:] # penultimate idx --> final idx 
            dir_vec = [final_idx[i] - penu_idx[i] for i in (0, 1)] # direction vector
            i, j = [final_idx[i] + dir_vec[i] for i in (0, 1)] # new idx
            # print(seq, dir_vec, (i, j))
            if (0 <= i < len(grid)) and (0 <= j < len(grid[0])) and grid[i][j] == char:
                # print("match!")
                matches = [(i, j)] # there can only possibly be one match in the direction
        # add all combinations of [idx, match] to list 
        # if len(matches) > 0:
        for match in matches:
            new_seqs.append(seq + [match])
            # print("new_seq:", new_seqs)
    return new_seqs


def print_seq(seq, grid):
    # prints out the sequence of chars
    seq_str = ""
    for (row, col) in seq:
        if (0 <= row < len(grid)) and (0 <= col < len(grid[0])):
            seq_str += grid[row][col]   
    print(seq_str)


def task_one(input):
    """
    Given a crossword puzzle, find all instances
    of 'XMAS' horizontally, vertically, diagonally, backwards
    """
    # first let's create an array
    grid = []
    for line in input:
        grid.append(line)

    # find all instances of X
    # store sequences as [[idx1, idx2, ...], [idx1, ...], ...]
    seqs = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "X":
                seqs.append([(i, j)]) # add [idx1] to full list

    # find all instances of M touching prev X seqs, then find
    # A touch prev M in same direction, S touching prev A in same dir
    for char in "MAS":
        seqs = find_sequences(seqs, char, grid)
    return len(seqs)


def task_two(input):
    """
    Now find two 'MAS' in the shape of an X
    """
    # first let's create an array -- padding is simpler than literal edge cases below 😅
    grid = []
    for line in input:
        grid.append("-" + line + "-")
    top_bottom = ["-" * len(grid[0])]
    grid = top_bottom + grid + top_bottom

    # find all instances of A
    # store sequences as [[idx1, idx2, ...], [idx1, ...], ...]
    a_idxs = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "A":
                a_idxs.append((i, j)) # add [idx1] to full list

    is_mas = lambda str: True if (str == "MAS" or str == "SAM") else False
    
    # now just check if the two diagonals around 'A' form some variation of 'MAS'
    count = 0
    for i, j in a_idxs:
        diag_1 = grid[i-1][j-1] + grid[i][j] + grid[i+1][j+1]  # up and to the right
        diag_2 = grid[i-1][j+1] + grid[i][j] + grid[i+1][j-1] # up and to the left
        if is_mas(diag_1) and is_mas(diag_2):
            count += 1
    return count
         

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")