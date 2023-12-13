#!/bin/bash

# day number arg required
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <day_number>"
    exit 1
fi

# add leading 0 if single digit day: 3 -> 03, 12 -> 12
DAY=$(printf "%02d" $1)

# create the directory
DIR="day_$DAY"
mkdir -p "$DIR"

# fill main.py with skeleton code
cat <<EOF >"$DIR/main.py"
def task_one(input):
    ...

def task_two(input):
    ...

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")
EOF

# create puzzle input file
touch "$DIR/input.txt"