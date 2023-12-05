FILE = 'inputs/02/input.txt'

def get_contents(filepath):
    with open(filepath, 'r') as infile:
        for line in infile:
            yield line.strip()

def get_sum(reds, greens, blues):
    sum_ids = 0
    for game in get_contents(FILE):
        possible = True
        game = game.split(':')
        id = int(game[0].split()[1])
        rounds = game[1].split(';')
        for round in rounds:
            if not possible:
                break
            colors = round.split(',')
            for color_i in colors:
                color_s = color_i.strip().split()
                count = int(color_s[0])
                color = color_s[1]
                if color == 'blue' and count > blues:
                    possible = False
                    break
                if color == 'red' and count > reds:
                    possible = False
                    break
                if color == 'green' and count > greens:
                    possible = False
                    break
        if possible:
            sum_ids += id
    return sum_ids

print(get_sum(12, 13, 14))