def abs(x):
    '''Absolute value'''
    return -x if x < 0 else x

def task_one(input):
    '''
    Data consists of galaxies '#' and empty space '.'

    Find the sum of the lengths of the shortest path between every
    pair of galaxies once (so only [i, j] -- not both [i, j] and [j, i])

    Any row or column that contains no galaxies should be twice as big

    So what we can do is first find the number of empty rows / cols,
    which we can use later to offset the coordinates of the galaxies
    ''' 

    # store the i, j indexes of the empty space
    empty_rows = []
    empty_cols = []

    for i, row in enumerate(input):
        if all(char=="." for char in row):
            empty_rows.append(i)
        
    for j in range(len(input[0])):
        if all(input[i][j]=="." for i in range(len(input))):
            empty_cols.append(j)
    
    # next update the coordinate of each galaxy with its shift
    galaxy_coords = []
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == "#":
                # the galaxy is shifted by the number of empty rows / cols that come before it
                #   so we need to find the highest empty_row/col index before its coordinate (i, j)
                #   and then shift it by the number of indexes < that highest empty_row/col
                i_shift = len([row_idx for row_idx in empty_rows if row_idx < i])
                j_shift = len([col_idx for col_idx in empty_cols if col_idx < j])
                updated_i = i + i_shift
                updated_j = j + j_shift
                galaxy_coords.append((updated_i, updated_j))

    
    # now we need to find the Manhattan distance between each galaxy pair
    # (0, 1), (0, 2), ..., (1, 2), (1, 3), ..., (2, 3), (2, 4), ...
    # it is okay to pair an index with itself, e.g., (2, 2) because dist = 0
    total = 0
    for i in range(len(galaxy_coords)):
        for j in range(i, len(galaxy_coords)): # includes j=i
            galaxy_i = galaxy_coords[i]
            galaxy_j = galaxy_coords[j] 
            dist = abs(galaxy_i[0] - galaxy_j[0]) + abs(galaxy_i[1] - galaxy_j[1])
            total += dist
    return total




def task_two(input):
    '''
    This time, each empty row/col should be replaced with 1000000 empty rows/cols

    Well, 
        if you want to double a row, you have two, meaning you added one row
        if you want to triple a row, you have three, meaning you added two rows
        if you want to duplicate a row N times, you have N, meaning you added N-1 rows
    '''
    # store the i, j indexes of the empty space
    empty_rows = []
    empty_cols = []

    for i, row in enumerate(input):
        if all(char=="." for char in row):
            empty_rows.append(i)
        
    for j in range(len(input[0])):
        if all(input[i][j]=="." for i in range(len(input))):
            empty_cols.append(j)
    
    # next update the coordinate of each galaxy with its shift
    galaxy_coords = []
    multiplier = 1_000_000 
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == "#":
                # the galaxy is shifted by the number of empty rows / cols that come before it
                #   so we need to find the highest empty_row/col index before its coordinate (i, j)
                #   and then shift it by the number of indexes < that highest empty_row/col
                i_shift = len([row_idx for row_idx in empty_rows if row_idx < i])
                j_shift = len([col_idx for col_idx in empty_cols if col_idx < j])
                updated_i = i + i_shift * (multiplier-1)
                updated_j = j + j_shift * (multiplier-1)
                galaxy_coords.append((updated_i, updated_j))

    
    # now we need to find the Manhattan distance between each galaxy pair
    # (0, 1), (0, 2), ..., (1, 2), (1, 3), ..., (2, 3), (2, 4), ...
    # it is okay to pair an index with itself, e.g., (2, 2) because dist = 0
    total = 0
    for i in range(len(galaxy_coords)):
        for j in range(i, len(galaxy_coords)): # includes j=i
            galaxy_i = galaxy_coords[i]
            galaxy_j = galaxy_coords[j] 
            dist = abs(galaxy_i[0] - galaxy_j[0]) + abs(galaxy_i[1] - galaxy_j[1])
            total += dist
    return total

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")