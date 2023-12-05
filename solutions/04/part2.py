FILE = 'inputs/04/input.txt'

class CardPile:

    def __init__(self, filename) -> None:
        self.filename = filename
        self.copies = {}

    def add_card(self, card_num):
        self.add_cards(card_num, instances=1)

    def add_cards(self, card_num, instances):
        if card_num not in self.copies:
            self.copies[card_num] = instances
        else:
            self.copies[card_num] += instances

    def solve(self):
        with open(self.filename, 'r') as infile:
            card_num = 1
            for line in infile:
                self.add_card(card_num)
                line = line.strip().split(':')[1]
                components = line.split('|')
                if len(components) != 2:
                    raise ValueError('unexpected input')
                winning = set(int(num) for num in components[0].strip().split())
                mine = set(int(num) for num in components[1].strip().split())
                score = len(winning & mine)
                for card_to_copy in range(card_num + 1, card_num + score + 1):
                    self.add_cards(card_to_copy, self.copies[card_num])
                card_num += 1
        return sum(self.copies.values())

card_pile = CardPile(FILE)
print(card_pile.solve())