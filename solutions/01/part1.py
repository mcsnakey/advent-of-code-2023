FILE = 'inputs/01/input.txt'

def get_contents(filepath):
    with open(filepath, 'r') as infile:
        for line in infile:
            yield line.strip()

def get_magicnum(code):
    s_p = 0
    e_p = len(code) - 1
    go = True
    while go:
        go = False
        if not code[s_p].isdigit():
            s_p += 1
            go = True
        if not code[e_p].isdigit():
            e_p -= 1
            go = True
    return 10 * int(code[s_p]) + int(code[e_p])

print(sum(get_magicnum(x) for x in get_contents(FILE)))