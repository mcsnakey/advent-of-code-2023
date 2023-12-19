FILE = 'inputs/15/input.txt'

def get_hash(value):
    current = 0
    for char in value:
        current += ord(char)
        current *= 17
        current = current % 256
    return current

def parse_cmd(command):
    box = ''
    opt = None
    idx = 0
    while cmd[idx].isalpha():
        box += cmd[idx]
        idx += 1
    opt = cmd[idx]
    focal_length = cmd[idx+1:]
    if focal_length:
        focal_length = int(focal_length)
    else:
        focal_length = None
    return box, opt, focal_length

with open(FILE) as infile:
    cmds = infile.readline().strip().split(',')

boxes = {}
for i in range(256):
    boxes[i] = []

for cmd in cmds:
    label, opt, focal_length = parse_cmd(cmd)
    box = boxes[get_hash(label)]
    if opt == '-':
        idx = 0
        while idx < len(box):
            if box[idx][0] == label:
                box.pop(idx)
                break
            idx += 1
    elif opt == '=':
        idx = 0
        while idx < len(box):
            if box[idx][0] == label:
                box[idx] = (label, focal_length)
                break
            idx += 1
        else:
            box.append((label, focal_length))
    else:
        raise ValueError('you messed up')

score = 0
for box_key in boxes:
    idx = 0
    box = boxes[box_key]
    while idx < len(box):
        score += (box_key + 1) * (idx + 1) * box[idx][1]
        idx += 1

print(score)
