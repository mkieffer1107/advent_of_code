def check_row(row, j, left_or_right):
    '''Return lowest/highest index of valid char in row'''
    assert left_or_right == -1 or left_or_right == 1 # move left == -1, move right == 1
    while (0<= j < len(row)) and row[j].isdigit():   # checks left-to-right, so can include boundary condition first
        j += left_or_right
    return j - left_or_right # increment / decrement to get last valid index

def task_one(input):
    '''
    Find the sum of all numbers adjacent to non-period characters (https://en.wikipedia.org/wiki/Moore_neighborhood)
    Numbers should only be counted once 
        - num may touch two special chars: '..*32*..'

    Could maybe do this by creating two grids: 
        - puzzle input 
        - 'hit' grid to indicate the position of valid numbers

    Or just extract valid numbers as they come and replace them with periods
    '''
    # create grid of chars from the input
    grid = []
    for line in input:
        grid.append([char for char in line])

    # iterate over grid
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # if non-numeric + non-period char found, check neighbors
            if grid[i][j] != "." and not grid[i][j].isdigit():
                for y in range(-1, 2): # range is [inclusive, exclusive)
                    for x in range(-1, 2):
                        if (0 <= i + y < len(grid)) and (0 <= j + x < len(grid[0])):
                            # if the char is a digit, find all adjacent digits in current row
                            # and replace them with periods, so they aren't counted again
                            if grid[i+y][j+x].isdigit():
                                # get index range for valid number string
                                low = check_row(grid[i+y], j+x, -1)                                
                                high = check_row(grid[i+y], j+x, 1)      
                                num = ""
                                # build the number
                                for k in range(low, high+1):
                                    num += grid[i+y][k]  # get all touching digit chars in row
                                    grid[i+y][k] = "."   # replace grid cells with periods
                                total += int(num)        # add the number to the total count
    return total                          
                                
def task_two(input):
    '''
    This time we need to find the sum of the product of numbers adjacent to '*' chars.

    For example: ..467*35... -> 467x35
    '''
    # create grid of chars from the input
    grid = []
    for line in input:
        grid.append([char for char in line])

    # iterate over grid
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # if on an asterisk *, check neighbors
            if grid[i][j] == "*":
                nums = [] # store numbers touching the asterisk
                for y in range(-1, 2): # range is [inclusive, exclusive)
                    for x in range(-1, 2):
                        if (0 <= i + y < len(grid)) and (0 <= j + x < len(grid[0])):
                            # if the char is a digit, find all adjacent digits in current row
                            # and replace them with periods, so they aren't counted again
                            if grid[i+y][j+x].isdigit():
                                # get index range for valid number string
                                low = check_row(grid[i+y], j+x, -1)                                
                                high = check_row(grid[i+y], j+x, 1)      
                                num = ""
                                # build the number
                                for k in range(low, high+1):
                                    num += grid[i+y][k]  # get all touching digit chars in row
                                    grid[i+y][k] = "."   # replace grid cells with periods
                                nums.append(int(num))    # store the number touching the asterisk
                if len(nums) == 2:
                    total += nums[0]*nums[1]
    return total            

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.rstrip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")

'''
35 and 467 should only be counted once -- they touch the same *, but also if they were touching 
separate chars

'''