import math

def task_one(input):
    '''
    Determine the number of ways you can win each race, and take their product.

    Input:
        Time:        60     94     78     82
        Distance:   475   2138   1015   1650
    
    Time is the total amount of time per race, and distance is the distance to beat.
    For each millisecond the boat is charged, it will move an extra one millimeter per millisecond
    for the remaining duration of time.
    '''
    # map each num to an int, and convert to list
    times = list(map(int, input[0].split()[1:]))
    distances = list(map(int, input[1].split()[1:]))

    # count the number of ways to win for each race
    # ways_to_win = [] 
    ways_to_win = 1
    for time, distance in zip(times, distances):
        num_wins = 0
        # check each charge duration t
        for t in range(time):
            speed = 1 * t
            remaining_time = time - t
            total_distance = speed * remaining_time
            if total_distance > distance:
                num_wins += 1
        # ways_to_win.append(num_wins)
        ways_to_win *= num_wins
    
    return ways_to_win


def task_two(input):
    '''
    Slowest. Brute force.

    Actually these are all one race!

        Input:
        Time:        60     94     78     82   --> 60,947,882 
        Distance:   475   2138   1015   1650   --> 475,213,810,151,650 
    '''
    # map each num to an int, and convert to list
    time = int("".join(input[0].split()[1:]))
    distance = int("".join(input[1].split()[1:]))

    # count the number of ways to win for each race
    ways_to_win = 0

    # check each charge duration t
    for t in range(time):
        speed = 1 * t
        remaining_time = time - t
        total_distance = speed * remaining_time  
        if total_distance > distance:
            ways_to_win += 1
    
    return ways_to_win


def task_two(input):
    '''
    Mid 

    This solution uses binary search. The trick here is to realize that there is 
    a lower and upper threshold time t within which you win the race. If you are
    outside these boundaries, then you will lose. 

    Recall that the charge time t gives the speed. So one unit of time t give 
    one unit of speed. 

    Then the lower threshold needs to be the minimum amount of charge time
    required to get enough speed to complete the course. So

        lower = distance / time

    where distance is the record distance to travel, and time is the alloted
    time to complete the race in.

    The upper bound is if you were to charge for half of the time, and then 
    race for the latter half

        upper = time / 2

    '''
    # map each num to an int, and convert to list
    time = int("".join(input[0].split()[1:]))
    distance = int("".join(input[1].split()[1:]))

    # boundaries
    lower = distance / time
    upper = time / 2

    while upper - lower > 1:
        t = math.floor((upper + lower) / 2)
        speed = t
        remaining_time = time - t
        if speed * remaining_time > distance:
            upper = t
        else:
            lower = t

    total_losing_ts = lower * 2 + 1
    return time - total_losing_ts


def task_two(input):
    '''
    Fastest

    This solution uses the quadratic formula. The original solution was

        for t in range(time):
            speed = 1 * t
            remaining_time = time - t
            total_distance = speed * remaining_time  
            if total_distance > distance:
            
    where t is the minimum charge time tested. We can write

        speed = t
        remaining_time = time - t
        total_distance = speed * remaining_time = t * (time - t)

    with condition

        total_distance > distance

        t * (time - t) > distance

        t * (time - t) - distance > 0

    by setting this equal to 0, we find the minimum time t that will cause a loss

        -t^2 + time * t - distance = 0

    solve for t:

        x = (-b +/- sqrt(b^2 - 4ac))/2a

    with

        x = t

        a = -1

        b = time

        c = - distance

    Solving for t gives the minimum charge time that gives a loss, meaning
    there isn't enough speed to beat the distance score in the given duration.
    '''

    # map each num to an int, and convert to list
    time = int("".join(input[0].split()[1:]))
    distance = int("".join(input[1].split()[1:]))

    # get the positive root
    t1 = (-time + math.sqrt(time**2 - 4 * (-1) * (-distance))) / -2
    t2 = (-time - math.sqrt(time**2 - 4 * (-1) * (-distance))) / -2
    t = t1 if t1 >= 0 else t2

    # t is the minimum charge time that results in a loss
    # need to floor to deal with ints
    min_lose_t = math.floor(t)

    # multiply by 2 to account for loss at time t=t and t=(time-t)
    #   if time = 10, you might lose at the ends, t=3 and t=10-3=7
    #   there is a threshold above which you win
    # add 1 to account for time t=0
    total_losing_ts = min_lose_t * 2 + 1 

    return time - total_losing_ts


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.rstrip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")