FILE = 'inputs/01/input.txt'

int_as_str = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

def get_contents(filepath):
    with open(filepath, 'r') as infile:
        for line in infile:
            yield line.strip()

def get_magicnum(code):
    start_num = None
    end_num = None
    ch_idx = 0
    while ch_idx < len(code):
        num = 0
        adv = 1
        if code[ch_idx].isdigit():
            num = int(code[ch_idx])
        else:
            for numstr in int_as_str:
                if code[ch_idx:ch_idx + len(numstr)] == numstr:
                    num = int_as_str[numstr]
                    adv = 1
                    break
        if num:
            if not start_num:
                start_num = num
            end_num = num
        ch_idx += adv
    return 10 * start_num + end_num

print(sum(get_magicnum(x) for x in get_contents(FILE)))        