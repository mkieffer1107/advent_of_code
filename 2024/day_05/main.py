def get_mid_val(arr):
    if len(arr) % 2 == 0:
        print("ahhhhhh") # should always be odd
    else:
        # should always be int since len(arr) is odd
        # but need to explicitly convert type
        idx = (len(arr)-1) // 2
        return arr[idx]


def is_valid_seq(page_seq, page_rules):
    # for every number, check that all the numbers that come after
    # it in the sequence are valid. in other words, make sure future
    # numbers are not required to come before the current number.
    for i in range(len(page_seq)):
        curr_page = page_seq[i]
        next_pages = page_seq[i:]
        
        if curr_page in page_rules:
            pages_that_come_b4 = page_rules[curr_page]
        else:
            # no pages required to come before curr_page
            continue
        
        # make sure no future page is required to come before
        # the current page
        for next_page in next_pages:
            if next_page in pages_that_come_b4:
                return False, (curr_page, next_page)
    return True, -1


def task_one(input):
    """
    Given some page orderings X|Y, meaning if both X and Y are present,
    that X must come some point before Y, determine if the sequences
    of pages are correct. For all correct sequences, identify the middle
    number (by index, not value), and return their sum.
    """
    page_rules = {} # map from num -> [nums that must come before]
    page_seqs = []
    for line in input:
        if "|" in line:
            # page rules: "X|Y"
            X, Y = map(int, line.split("|"))
            # build out dictionary
            if Y in page_rules:
                page_rules[Y].append(X)
            else:
                page_rules[Y] = [X]
        elif "," in line:
            # page number sequences: "a, b, c, d, ..."
            page_seqs.append(list(map(int, line.split(","))))
    
    total = 0 
    for page_seq in page_seqs:
        is_valid, _ = is_valid_seq(page_seq, page_rules)
        if is_valid: 
            total += get_mid_val(page_seq)

    return total


def task_two(input):
    """
    Put all the invalid sequences in the correct order. Then
    return the sum of all middle values in the sequences of each.
    """
    page_rules = {} # map from num -> [nums that must come before]
    page_seqs = []
    for line in input:
        if "|" in line:
            # page rules: "X|Y"
            X, Y = map(int, line.split("|"))
            # build out dictionary
            if Y in page_rules:
                page_rules[Y].append(X)
            else:
                page_rules[Y] = [X]
        elif "," in line:
            # page number sequences: "a, b, c, d, ..."
            page_seqs.append(list(map(int, line.split(","))))

    total = 0 
    for i in range(len(page_seqs)):
        # check if sequence is invalid in the first place
        page_seq = page_seqs[i]
        is_valid, invalid_pages = is_valid_seq(page_seq, page_rules)
        if not is_valid:
            # then continue until sequence is valid... yucky, i know 🤮
            while not is_valid:
                # get the indexes of the page and the invalid page after it
                curr_page, invalid_page = invalid_pages
                page_idx = page_seq.index(curr_page)
                invalid_idx = page_seq.index(invalid_page)

                # put the invalid page one before the current page
                page_seq.pop(invalid_idx)
                page_seq.insert(page_idx, invalid_page)
                is_valid, invalid_pages = is_valid_seq(page_seq, page_rules)
            # only add the mid value of an invalid sequence that has been fixed
            total += get_mid_val(page_seq)
    return total

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.strip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")