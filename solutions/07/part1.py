from collections import Counter
from functools import cmp_to_key

FILE = 'inputs/07/input.txt'

types = {
    'FIVE_OF_KIND': 7,
    'FOUR_OF_KIND': 6,
    'FULL_HOUSE': 5,
    'THREE_OF_KIND': 4,
    'TWO_PAIR': 3,
    'ONE_PAIR': 2,
    'HIGH_CARD': 1
}

worths = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}

class Hand:

    def __init__(self, cards, bet) -> None:
        self.cards = cards
        self.bet = bet

    def get_type(self):
        card_map = Counter(self.cards)
        if len(card_map) == 1:
            hand_type = types['FIVE_OF_KIND']
        elif len(card_map) == 2:
            if sorted(card_map.values()) == [1, 4]:
                hand_type = types['FOUR_OF_KIND']
            elif sorted(card_map.values()) == [2, 3]:
                hand_type = types['FULL_HOUSE']
            else:
                raise ValueError
        elif len(card_map) == 3:
            if sorted(card_map.values()) == [1, 1, 3]:
                hand_type = types['THREE_OF_KIND']
            elif sorted(card_map.values()) == [1, 2, 2]:
                hand_type = types['TWO_PAIR']
            else:
                raise ValueError
        elif len(card_map) == 4:
            hand_type = types['ONE_PAIR']
        elif len(card_map) == 5:
            hand_type = types['HIGH_CARD']
        else:
            raise ValueError
        return hand_type

def compare_hands(hand1: Hand, hand2: Hand):
    h1_type = hand1.get_type()
    h2_type = hand2.get_type()
    if h1_type == h2_type:
        idx = 0
        while worths[hand1.cards[idx]] == worths[hand2.cards[idx]]:
            idx += 1
        if not idx < 5:
            raise ValueError('asserted no hands are equal')
        else:
            return worths[hand1.cards[idx]] - worths[hand2.cards[idx]]
    else:
        return h1_type - h2_type

hands = []
with open(FILE) as infile:
    for line in infile:
        line = line.strip().split()
        hands.append(Hand(line[0], int(line[1])))

hands.sort(key=cmp_to_key(compare_hands))

soln = 0
mul = 1
for hand in hands:
    soln += hand.bet * mul
    mul += 1

print(soln)