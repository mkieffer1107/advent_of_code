'''
Hand Rankings:
    Five of a kind: 
        where all five cards have the same label: AAAAA
    Four of a kind: 
        where four cards have the same label and one card has a different label: AA8AA
    Full house: 
        where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind: 
        where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair: 
        where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair: 
        where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card: 
        where all cards' labels are distinct: 23456
'''

ORDER = {
    **{str(i): i for i in range(2, 10)},
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

ORDER2 = {
    "J": 1,
    **{str(i): i for i in range(2, 10)},
    "T": 10,
    "Q": 12,
    "K": 13,
    "A": 14,
}

RANK = {
    "Five of a kind": 7,   # AAAAA
    "Four of a kind": 6,   # AA8AA
    "Full house": 5,       # 23332
    "Three of a kind": 4,  # TTT98
    "Two pair": 3,         # 23432 
    "One pair": 2,         # A23A4
    "High card": 1         # 23456
}



class Hand:
    def __init__(self, line, special_rules=False):
        hand, bid = line.split()
        self.hand = hand
        self.bid = int(bid)
        self.special_rules = special_rules

        if special_rules: 
            self.cards = [ORDER2[card] for card in hand]
        else: 
            self.cards = [ORDER[card] for card in hand]

    def _rank_hand(self):
        # get the counts of each card
        counts = {}
        for card in self.cards:
            counts[card] = counts.get(card, 0) + 1

        if self.special_rules:
            # Joker cards will convert to the card with the highest count (excluding J, itself)
            
            
            if ORDER2["J"] in counts:
                # remove the joker cards from the count
                # and add them to the most numerous card's count
                J_counts = counts[ORDER2["J"]]
                del counts[ORDER2["J"]]

                # case where hand is JJJJJ
                if len(counts) == 0:
                    counts[ORDER2["J"]] = J_counts
                else:
                    # sort key-value pairs in descending order by value (count number)
                    kvs = list(counts.items())
                    kvs = sorted(kvs, key=lambda x: -x[1])
                    max_card = kvs[0][0]
                    counts[max_card] += J_counts
        
        # get the type of hand
        if len(counts) == 1:
            return RANK["Five of a kind"]
        elif len(counts) == 2:
            if 4 in counts.values():
                return RANK["Four of a kind"]
            return RANK["Full house"] 
        elif len(counts) == 3:
            if 3 in counts.values():
                return RANK["Three of a kind"]
            return RANK["Two pair"]
        elif len(counts) == 4:
            return RANK["One pair"] 
        elif len(counts) == 5:
            return RANK["High card"]      
        
    def __lt__(self, rhs):
        '''Defined so Hands are sortable'''

        # rank hand
        rank1 = self._rank_hand()
        rank2 = rhs._rank_hand()
        if rank1 != rank2:
            return rank1 < rank2

        # if hand rankings are the same, check card rankings
        for c1, c2 in zip(self.cards, rhs.cards):
            # skip cards until unequal
            if c1 != c2: 
                return c1 < c2

    def __str__(self):
        # return self.hand
        return f"Hand: {self.hand}, {self._rank_hand()}"
        

def task_one(input):
    '''
    Camel Cards! Rank each hand in the game. Return the sum of each hand's ranking
    multiplied by its bid number.
    '''
    hands = []
    for line in input:
        hands.append(Hand(line))

    # sort hands in ascending order
    hands.sort()
    
    # (i+1) to skip 0
    return sum((i+1) * hand.bid for i, hand in enumerate(hands))
    

def task_two(input):
    '''
    Now J is the joker card!!! When comparing individual cards, it becomes the weakest card.
    However, when comparing hands, it becomes the card that will yield the highest hand.

        e.g., QJJQ2 is now considered four of a kind: QJJQ2 --> QQQQ2
    '''
    hands = []
    for line in input:
        hands.append(Hand(line, special_rules=True))
    
    # sort hands in ascending order
    hands.sort()

    # (i+1) to skip 0
    return sum((i+1) * hand.bid for i, hand in enumerate(hands))


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [line.rstrip() for line in f.readlines()]

    task1 = task_one(input)
    print(f"task 1: {task1}")

    task2 = task_two(input)
    print(f"task 2: {task2}")
