FILE = 'inputs/15/input.txt'

with open(FILE) as infile:
    string = infile.readline().strip()

score = 0
current = 0
for char in string:
    if char == ',':
        score += current
        current = 0
    else:
        current += ord(char)
        current *= 17
        current = current % 256
score += current

print(score)