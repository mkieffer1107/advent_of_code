import re
import numpy as np

def task_one(input):
    '''
    Find the sum of the game IDs that have a valid number of cubes. Games are stored in the format

            Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

    Where the game ID is followed by three sets of draws from the bag (with replacement)
    '''
    max_rgb = (12, 13, 14)

    # one or more digits followed by one or more whitespace chars
    r = r"(\d+)\s+red"
    g = r"(\d+)\s+green"
    b = r"(\d+)\s+blue"

    total = 0
    for line in input:
        # get the id number
        game_id, content = line.split(":")  # ['Game id', 'content']
        id = int(game_id.split()[1])        # ['Game', 'id']

        # get a boolean mask to check for invalid numbers (greater than the max)
        r_mask = np.array([int(num) for num in re.findall(r, line)]) > max_rgb[0]
        g_mask = np.array([int(num) for num in re.findall(g, line)]) > max_rgb[1]
        b_mask = np.array([int(num) for num in re.findall(b, line)]) > max_rgb[2]
        all_masks = np.concatenate([r_mask, g_mask, b_mask])
        
        # if the game is valid, add the id
        if not np.any(all_masks):
            total += id

        # this one also works!
        # sets = [set.strip() for set in game.split(";")]
        # #  3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        # invalid = False
        # for set in sets:
        #     #  3 blue
        #     for color in set.split(","):
        #         # print(color)
        #         if "red" in color:
        #             if int(color.split()[0]) > max_rgb[0]: invalid = True; break
        #         if "green" in color:
        #             if int(color.split()[0]) > max_rgb[1]: invalid = True; break
        #         if "blue" in color:
        #             if int(color.split()[0]) > max_rgb[2]: invalid = True; break
        # if not invalid:
        #     total += id
            
    return total

def task_two(input):
    '''
    Find the minimum number of cubes of each color per game and sum their product. For example, given

            Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

    The minimum required cubes of each color are:
        red:    4
        green:  2
        blue:   6

    Because they are the highest counts of each color out of all sets
    '''
    # one or more digits followed by one or more whitespace chars
    r = r"(\d+)\s+red"
    g = r"(\d+)\s+green"
    b = r"(\d+)\s+blue"

    total = 0
    for line in input:
        # get the id number
        game_id, game = line.split(":")  # 'Game #'
        id = int(game_id.split()[1])     # '#'

        # get the number of cubes of each color drawn in each set
        r_num = np.array([int(num) for num in re.findall(r, line)])
        g_num = np.array([int(num) for num in re.findall(g, line)])
        b_num = np.array([int(num) for num in re.findall(b, line)])
        
        # multiply the min required values together (the max out of all sets)
        total += max(r_num) * max(g_num) * max(b_num)
        
    return total

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.rstrip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")