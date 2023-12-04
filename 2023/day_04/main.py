def task_one(input):
    '''
    Given a set of cards, determine the total number of points. The format is

        Card #: winning nums | card nums

    The winning numbers on the left tell which numbers in the card on the right win.
    The first match awards one point, the rest double the amount
    '''
    total = 0
    for line in input:
        card_id, card_vals = line.split(":")
        winning_nums_str, card_nums_str = card_vals.split("|")
        
        # convert the string nums into a set of ints
        winning_nums = set([int(num) for num in winning_nums_str.split()])
        card_nums = set([int(num) for num in card_nums_str.split()])
        matches = winning_nums.intersection(card_nums)

        # first match awards one point, the rest double this 
        # so double 1 len(matches)-1 times as long as there is a match
        if len(matches) > 0:
            total += 2**(len(matches)-1)

    return total

def task_two_slow(input):
    '''
    This time, matches earn cards. If card 1 has 4 matches, then you get additional copies
    of the 4 cards below, i.e., an extra copy of cards 2, 3, 4, and 5. Return the total
    number of cards 

    Count the number of matches for each card first, and then increment the card counts below

    This can totally be optimized with recursively / with dynamic programming...
    '''
    # record the number of copies of each card number
    # num_copies = [1 for card in range(len(input))]
    num_copies = [1] * len(input)   # the number of copies of each card
    num_matches = [0] * len(input)  # the number of matches each card has

    for i, line in enumerate(input):
        # get the card number
        card_id, card_vals = line.split(":")
        # convert the string nums into a set of ints
        winning_nums_str, card_nums_str = card_vals.split("|")
        winning_nums = {int(num) for num in winning_nums_str.split()}
        card_nums = {int(num) for num in card_nums_str.split()}

        # store the number of matches the current card has
        num_matches[i] = len(winning_nums.intersection(card_nums))

    # iterate over card id
    for i in range(len(input)):
        # get new cards for each copy of the current card
        for _ in range(num_copies[i]):
            for j in range(1, num_matches[i] + 1):
                # increment the count of the cards below current card for each match
                #   i: the current card
                #   j: idx of next cards
                # j starts at 0, or just i + 0 = i, so use (j+1) instead
                # or can do range(1, len(matches)+1) to use j instead of (j+1)
                num_copies[i + j] += 1

    return sum(num_copies)

def task_two(input):
    '''
    this line 
        'for _ in range(num_copies[i]):'
    above is unecessary and slows the code down

    we can remove that line by changing
        num_copies[i + j] += 1
    to 
        num_copies[i + j] += num_copies[i]

    so we add all copies at once instead of using an extra for loop
    which added a single value at a time
    '''
    # record the number of copies of each card number
    # num_copies = [1 for card in range(len(input))]
    num_copies = [1] * len(input)   # the number of copies of each card
    num_matches = [0] * len(input)  # the number of matches each card has

    for i, line in enumerate(input):
        # get the card number
        card_id, card_vals = line.split(":")
        # convert the string nums into a set of ints
        winning_nums_str, card_nums_str = card_vals.split("|")
        winning_nums = {int(num) for num in winning_nums_str.split()}
        card_nums = {int(num) for num in card_nums_str.split()}

        # store the number of matches the current card has
        num_matches[i] = len(winning_nums.intersection(card_nums))

    # iterate over card id
    for i in range(len(input)):
        # increment the count of the cards below current card for each match
        for j in range(1, num_matches[i] + 1):
            # increment the count of the cards below current card for each match
            #   i: the current card
            #   j: idx of next cards
            # j starts at 0, or just i + 0 = i, so use (j+1) instead
            # or can do range(1, len(matches)+1) to use j instead of (j+1)
            num_copies[i + j] += num_copies[i]

    return sum(num_copies)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.rstrip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")