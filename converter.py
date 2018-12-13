from enum import Enum
import sys
from functools import reduce


class Inst(Enum):
    INCP = 1
    DECP = 2
    INCV = 3
    DECV = 4
    OUTV = 5
    INPV = 6
    JMPIFZ = 7
    RETIFNZ = 8


dictionary = {
    '>': Inst.INCP,
    '<': Inst.DECP,
    '+': Inst.INCV,
    '-': Inst.DECV,
    '.': Inst.OUTV,
    ',': Inst.INPV,
    '[': Inst.JMPIFZ,
    ']': Inst.RETIFNZ
}

luna_dictionary = {
    'こんちわぁぁ': Inst.INCP,
    'こんばんはぁ': Inst.DECP,
    'おはよぉぉぉ': Inst.INCV,
    'ヘケッ☆': Inst.DECV,
    'みてみてこれエビ！': Inst.OUTV,
    'それは竹www': Inst.INPV,
    'おきてぇぇぇ': Inst.JMPIFZ,
    'おやすみぃぃぃ': Inst.RETIFNZ
}


def convert_bf_to_instruction(string):
    def convert(c):
        try:
            return dictionary[c]
        except:
            return

    out = reduce(lambda arr, c: arr + [convert(c)]
                 if convert(c) else arr, string, [])
    return out


def convert_luna_to_brainfxck(string):
    p = 0
    keys = luna_dictionary.keys()
    key_lengths = list(set([len(key) for key in keys]))
    instructions = []

    while p < len(string):
        try:
            new_instruction = reduce(
                lambda arr, length: arr + [string[p: p+length]] if string[p: p+length] in keys else arr, key_lengths, [])[0]
        except:
            p += 1
            continue
        instructions.append(luna_dictionary[new_instruction])
        p += len(new_instruction)

    return instructions


def convert_bf_to_luna(string):
    def convert(c):
        try:
            return dictionary[c]
        except:
            return

    inverted_luna_dict = {v: k for k, v in luna_dictionary.items()}
    insts = reduce(lambda arr, c: arr +
                   [convert(c)] if convert(c) else arr, string, [])
    luna = [inverted_luna_dict[i] for i in insts]
    return ''.join(luna)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Filename is not found.')
        exit()
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    with open(input_filename) as f:
        bf = f.read()

    luna = convert_bf_to_luna(bf)
    with open(output_filename, 'w') as f:
        f.write(luna)
