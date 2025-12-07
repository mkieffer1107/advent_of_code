from itertools import product


def get_combos(values, n, current=[], depth=0):
    """
    Generate all possible combinations of length n from values in values list.
    """
    if depth == n:
        # return a single combination as a new list
        return [current[:]]  
    combinations = []
    for val in values:
        current.append(val)
        combinations.extend(get_combos(values, n, current, depth + 1))
        current.pop()  
    return combinations


def eval_equation(result, operands, values):
    num_ops = len(operands) - 1
    op_combos = get_combos(values=values, n=num_ops)
    # op_combos = list(product(values, repeat=num_ops))
    successful_combos = []
    
    # test all possible combinations
    for op_combo in op_combos:
        # since ops are from left to right, just sequentially apply
        # operators to a number aggregated into a single val, 
        # candidate_result, on the left side --> move left-to-right
        candidate_result = operands[0]
        for i in range(len(op_combo)):
            op = op_combo[i]
            num = operands[i+1]
            # apply the op to the aggregate result and next num in operands
            if op == "+":
                candidate_result += num
            elif op == "*":
                candidate_result *= num
            elif op == "||":
                # for a||b we make ab. the current result, a, gets pushed over to the
                # left -- so we need to multiply by a power of ten to account for this shift
                # by the number of digits of the displacer, b. then simply add b onto the 
                # result since it's the least significant part of the number
                candidate_result = candidate_result * (10 ** len(str(num))) + num
        # if this combinations of operations give the correct result, save it
        if candidate_result == result:
            successful_combos.append(op_combo)
            # optional end to save time once we find first working combo -- successful_combos list won't be complete
            # break 
    return successful_combos


def task_one(input):
    """
    Given a series of equations, figure out what combinations of operations of 
    addition and multiplication can be used to get the result. Then return the
    sum of the equations which are possible. Operators are always evaluated left-to-right!
    """
    # since there are two operators, + and *, there would be 2^(N-1) combinations
    # given there are N numbers in the sequence. this should be easy to solve
    # with a brute force solution since N ~ 10
    total = 0
    for line in input:
        lhs, rhs = line.split(":")
        result = int(lhs.strip())
        operands = list(map(int, rhs.strip().split(" ")))
        successful_combos = eval_equation(result, operands, values=["+", "*"])
        if len(successful_combos) > 0:
            total += result
    return total


def task_two(input):
    """
    Now include a concatenation operator, ||, that combines consecutive 
    values: 12||345 becomes 12345
    """
    total = 0

    # repeat task 1, but keep track of the lines that are
    # already clear so that we don't check them again with 
    # the new operator
    equation_satisfied = set()
    for i, line in enumerate(input):
        lhs, rhs = line.split(":")
        result = int(lhs.strip())
        operands = list(map(int, rhs.strip().split(" ")))
        successful_combos = eval_equation(result, operands, values=["+", "*"])
        if len(successful_combos) > 0:
            total += result
            equation_satisfied.add(i)

    # for task 2, do the same thing with another operator. this time since
    # we have 3 operations, there should be a total of 3^(N-1) combinations
    # to check per line. by checking them in task 1, which only has 2^(N-1)
    # combinations, we save time by not applying the new operator to 
    # equations that we already know are satisfied by some combination of the 
    # two previous operators
    for i, line in enumerate(input):
        if i in equation_satisfied:
            continue
        lhs, rhs = line.split(":")
        result = int(lhs.strip())
        operands = list(map(int, rhs.strip().split(" ")))
        successful_combos = eval_equation(result, operands, values=["+", "*", "||"])
        if len(successful_combos) > 0:
            total += result
    return total 


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")