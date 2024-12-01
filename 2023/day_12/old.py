class Block:
    def __init__(self, size):
        self.size = size

    def is_valid(self, idx, row):
        '''
        Check whether the chunk below the block is valid
        Must be a contiguous block of either '#', '?', or a combination of the two
        '''
        print(idx*" " + row[idx:idx+self.size])
        print(row)
        for char in row[idx:idx+self.size]:
            if char not in ("#", "?"):
                return False
        return True
    
    def __str__(self):
        return f"Size: {self.size}"


def get_permutations(arr):
    # base case -- only one ordering
    if len(arr) == 1:
        return [arr]

    # recursive case 
    permutations = []
    for i in range(len(arr)):
        # remove the current element from the array
        curr = arr[i]
        remaining = arr[:i] + arr[i+1:] # slicing is [inclusive, exclusive) -- exclude i, include i+1

        # consider all of the permutations where curr is at index i in the permutation
        #   and then add curr back into the permutation
        for permutation in get_permutations(remaining):
            permutations.append([curr] + permutation)

    return permutations
 

def task_one(input):
    '''
    Each row contains spring records: 
        '.' means operational, 
        '#' means damaged, 
        '?' means unknown condition.

    After each row is a list of numbers for the size of 
    each contiguous group of damaged springs, e.g,
        #.#.### 1,1,3
        .??..??...?##. 1,1,3

    But of course, '?' might actually be a '#'. 

    Return the sum of different possible arrangements of each row.
    '''
    for line in input:
        record, nums = line.split()
        blocks = [Block(num) for num in map(int, nums.split(","))]
        
        # consider every ordering / permutation of the blocks
        block_permutations = get_permutations(blocks)

        # within each permutation, consider all shift distances without overlap
        for permutation in block_permutations:
            # start all blocks at the leftmost index available
            idxs = [0]                            # first block starts at idx = 0
            for i in range(len(permutation)-1):   # len(permutation)-1 because we are adding idx for NEXT block
                block = permutation[i]            
                idxs.append(idxs[i] + block.size) # next index starts at end of the current block

            # now consider all valid shifts 
            #   we will shift the rightmost block to the right first -- binary style
            for block, idx in zip(permutation, idxs):
                if block.is_valid(idx, record):
                    print(f"block {block.size} at idx {idx}")
                else:
                    print("invalid")
        break




def task_two(input):
    ...

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")