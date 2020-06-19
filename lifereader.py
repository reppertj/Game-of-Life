import re
import board


def reader(filename):
    with open(filename) as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def parse_txt(filename):
    lines = reader(filename)
    return [[1 if character == '1' else 0 for character in line] for line in lines]
# TODO: rn txt parser based on filename

class Readrle:
    def __init__(self, state, born, survive):
        self.state = state
        self.born = born
        self.survive = survive

def parse_rle(filename):
    lines = reader(filename)
    lines = [line for line in lines if line.strip()[0] != '#'] # ignore comments
    header = lines[0]
    lines = lines[1:]
    lines = ''.join(lines).strip('\n')
    header_pattern = re.compile(r'x\s?=\s?(\d+).*?y\s?=\s?(\d+).*?B(\d+).*?S(\d+.)')
    header_matches = header_pattern.search(header)
    try:
        born = header_matches.group(3)
        survive = header_matches.group(4)
    except IndexError:
        print("No or improper rule in file; defaulting to B3/S23.")
        born = "3"
        survive = "23"
    width = int(header_matches.group(1))
    height = int(header_matches.group(2))
    line_pattern = re.compile(r'(\d*)([bo$!])')
    line_data = line_pattern.findall(lines)
    line_data = [(1, match[1]) if match[0] == '' else (int(match[0]), match[1]) for match in line_data]
    return height, width, born, survive, line_data


def pad_last_row(partial_state):
    padding_needed = len(partial_state[0]) - len(partial_state[-1])
    for _ in range(0, padding_needed):
        partial_state[-1].append(0)
    return partial_state


def load_rle(filename, r_padding=20, c_padding=20):
    height, width, born, survive, line_data = parse_rle(filename)
    output = board.dead_board((r_padding, 2 * c_padding + width)).state
    output.append([0 for _ in range(0, c_padding)])
    while len(line_data) > 0:
        sequence = line_data[0]
        for _ in range(0, sequence[0]):
            if sequence[1] == 'b':
                output[-1].append(0)
            elif sequence[1] == 'o':
                output[-1].append(1)
            elif sequence[1] == '$':
                output = pad_last_row(output)
                output.append([0 for _ in range(0, c_padding)])  # start next row
            elif sequence[1] == '!':
                output = pad_last_row(output)
                for _ in range(0, r_padding):
                    output.append([0 for _ in range(0, len(output[0]))])
        line_data = line_data[1:]
    return Readrle(output, born, survive)