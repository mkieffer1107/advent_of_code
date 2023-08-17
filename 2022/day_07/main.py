'''
     --- Day 7: No Space Left On Device ---

'''


def read_input(path):
    with open(path, 'r') as f:
        lines = []
        for line in f.readlines():
            lines.append(line.rstrip())
    return lines

def task_one(input):
    for line in input:
        parsed = line.split()

        if parsed[0] == '$':
            print("command")
        





def task_two(input):
    pass

if __name__ == '__main__':
    input = read_input("input.txt")

    task_one(input)
    # print(f"task 1: {task_one(input)}")
    # print(f"task 2: {task_two(input)}")
