def task_one(lines):
    '''
    Given lines of text, sum the first and last digits
    that appear in each line. Double up single digits: 7 -> 77
    '''
    total = 0
    for line in lines:
        nums = []
        for char in line:
            if char.isdigit():
                nums.append(char)
                if len(nums) > 2:
                    nums.pop(1)
        num = "".join(nums)
        num = 2*num if len(num)==1 else num

        # print(num, line)
        total += int(num)
    return total


def task_two(lines):
    '''
    Now include words as well. Must read + replace left-to-right. For example,
        eightwothree -> 8wothree -> 8wo3
    Actually this is wrong! Helpful meme: https://www.reddit.com/r/adventofcode/comments/188wjj8/2023_day_1_did_not_see_this_coming/
    
    This should still be intepreted as
        eightwothree -> 823
    So we can just replace the word with its corresponding digit + last letter
        eightwothree -> 8twothree -> 82othree -> 823

    '''
    word2num = {"one": "1", 
                "two": "2",
                "three": "3",
                "four": "4",
                "five": "5",
                "six": "6",
                "seven": "7",
                "eight": "8",
                "nine": "9"
            }
    # replace the words in the str with corresponding digit
    for i in range(len(lines)):
        # build substrings left-to-right to check if they are special number words
        for j in range(len(lines[i])):
            substr = lines[i][:j+1] # j+1 so we don't start with index 0 -- word[:0]
            # print(substr)
            for word, digit in word2num.items():
                if word in substr:
                    # include the last letter of the word as well
                    new_substr = substr.replace(word, digit + word[-1])
                    lines[i] = lines[i].replace(substr, new_substr)
                    break


    return task_one(lines)

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.rstrip() for line in f.readlines()]
  
    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")