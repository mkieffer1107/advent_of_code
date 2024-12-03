import re


def mul(input: str) -> int:
    """Given 'mul(X,Y)', return X*Y"""
    X, Y = map(int, input[4:-1].split(","))
    return X * Y


def task_one(input):
    """
    Given a string, find all the 'mul(X,Y)' substrings, where X and Y
    are 1-3 digit numbers, perform the operation, and sum the total
    """
    pattern = r"mul\(\d{1,3},\d{1,3}\)"

    # pattern = r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)" # this returns tuples of numbers -- simpler parsing
    
    # total = 0
    # for line in input:
    #     total += sum(map(mul, re.findall(pattern, line)))
    # return total
    
    # could even wrap the outer loop in list comp with sum if we're crazy 🤪
    # return sum((sum(map(mul, re.findall(pattern, line))) for line in input))
    
    # too far?
    # return sum((sum(map(lambda x: map(lambda a, b: a*b, x[4:-1].split(",")), re.findall(r"mul\(\d{1,3},\d{1,3}\)", line))) for line in input))
    return sum((sum(map(lambda str_op: sum(X*Y for X,Y in [map(int, str_op[4:-1].split(","))]), re.findall(r"mul\(\d{1,3},\d{1,3}\)", line))) for line in input))


def task_two(input):
    """
    Now we also check for `do()` and `don't()` commands. if `don't()` comes somewhere
    before the 'mul(X,Y)' operation, then it isn't executed. basically the do and don'ts
    switch on and off subsequent operations
    """
    # we can just find patterns with a `do()` string before them 
    # and no `don't()` strings with any chars between them.
    # use the carrot ^ to indicate the lack of don't strs
    # pattern = r"[do\(\)][\s\d\w]*^[don't\(\)][\s\d\w]*(mul\(\d{1,3},\d{1,3}\))"
    # for line in input:
    #     matches = re.findall(pattern, line)
    #     print(matches)
    # return sum((sum(map(mul, re.findall(pattern, line))) for line in input))

    # treat it as a stream of inputs, using a flag when scanning across the string 
    # to determine whether or not to execute an operation
    pattern = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"

    total = 0
    active = True  
    for line in input:
        instructions = re.findall(pattern, line)
        # print(instructions)
        for instruction in instructions:
            if instruction == "do()":
                active = True
            elif instruction == "don't()":
                active = False
            else:
                total += mul(instruction) if active else 0
            # print(instruction, active)
    return total


def task_two_fast(input):
    pattern = re.compile(r"(do\(\))|(don't\(\))|mul\((\d{1,3}),(\d{1,3})\)")
    total = 0
    active = True
    for line in input:
        for match in pattern.finditer(line):
            if match.group(1):
                # do()
                active = True
            elif match.group(2):
                # don't()
                active = False
            elif active:
                a = int(match.group(3))
                b = int(match.group(4))
                total += a * b
    return total
    
    
if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")
