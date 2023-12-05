FILE = 'inputs/02/input.txt'

def get_contents(filepath):
    with open(filepath, 'r') as infile:
        for line in infile:
            yield line.strip()

def get_sum():
    sum_ids = 0
    for game in get_contents(FILE):
        possible = True
        game = game.split(':')
        id = int(game[0].split()[1])
        rounds = game[1].split(';')
        max_reds = 0
        max_greens = 0
        max_blues = 0
        for round in rounds:
            colors = round.split(',')
            for color_i in colors:
                color_s = color_i.strip().split()
                count = int(color_s[0])
                color = color_s[1]
                if color == 'blue' and count > max_blues:
                    max_blues = count
                if color == 'red' and count > max_reds:
                    max_reds = count
                if color == 'green' and count > max_greens:
                    max_greens = count
        if possible:
            sum_ids += max_blues * max_greens * max_reds
    return sum_ids

print(get_sum())