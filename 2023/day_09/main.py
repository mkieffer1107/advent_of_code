def task_one(input):
    '''
    Each line is a sequence of ints. For each sequence, take the difference between successive
    numbers until the entire line is 0. Use this to predict the next number. Return the sum of these predictions.

    Example:

    The third history requires even more sequences, but its next value can be found the same way:

            10  13  16  21  30  45  68
              3   3   5   9  15  23
                0   2   4   6   8
                  2   2   2   2
                    0   0   0

    To predict the next number in the sequences going from bottom-to-top, take the last number in a lower
    sequence and add it to the final number in the sequence above.                    
    '''
    total = 0
    for line in input:
        # get the sequence of integers
        seq = list(map(int, line.split()))

        # continue subtraction until the current sequence is all zeroes        
        seqs = [seq]
        while sum(seqs[-1]) != 0:  # FIXME: there are negative numbers -- turns out not to be a problem!
            prev_seq = seqs[-1]
            new_seq = [j-i for i, j in zip(prev_seq, prev_seq[1:])]
            seqs.append(new_seq)

        # get the elements in the last "column" and add them together to make prediction
        prediction = sum([seq[-1] for seq in seqs])
        total += prediction

    return total


def task_two(input):
    '''
    Now do the same thing, but in reverse -- predict a new first value!
    '''
    total = 0
    for line in input:
        # get the sequence of integers
        seq = list(map(int, line.split()))

        # reverse the order of the sequence
        seq.reverse()
        # seq = seq[::-1] # same thing

        # continue subtraction until the current sequence is all zeroes        
        seqs = [seq]
        while sum(seqs[-1]) != 0:  # FIXME: there are negative numbers -- turns out not to be a problem!
            prev_seq = seqs[-1]
            new_seq = []
            new_seq = [j-i for i, j in zip(prev_seq, prev_seq[1:])]
            seqs.append(new_seq)

        # get the elements in the last "column" and add them together to make prediction
        prediction = sum([seq[-1] for seq in seqs])
        total += prediction

    return total


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.rstrip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")
