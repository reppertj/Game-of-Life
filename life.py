import random
import numpy as np
import time
import re
import blessed
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python life.py",
        usage="%(prog)s 'life.rle' -c -m 'lightness' -u -width 80 -scale 2",
        description="Run Conway's Game of Life in a bounded grid."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        '-file', type=argparse.FileType('r'), 
        help="path to RLE-formatted text file, random board if omitted unless in -ant mode"                
    )
    parser.add_argument(
        '-ant', action='store_true',
        help="implementation of Langton's ant starting with a dead board, wrapping on itself"
    )
    parser.add_argument(
        '-rows', type=int, action='store', default=30,
        help='number of rows to add on top and bottom of RLE data (default: 30)'
    )
    parser.add_argument(
        '-columns', type=int, action='store', default=40,
        help='number of columns to add to left and right of RLE data (default: 40)'
    )
    parser.add_argument(
        '-wrap', action='store_true', 
        help='wrap around edges of grid instead of cutting off edges'
    )
    parser.add_argument(
        '-delay', type=float, action='store', default=.02,
        help='approximate delay in seconds between steps (default=.02)'
    )
    return parser

def read_txt(filename):
    with open(filename) as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return [[1 if character == '1' else 0 for character in line] for line in lines]

def read_rle(filename):
    with open(filename) as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line[0] != '#']
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
    line_data = [(1, match[1]) if match[0] == '' else (int(match[0]), match[1]) for match in line_data ]
    return height, width, born, survive, line_data

def pad_last_row(partial_state):
    padding_needed = len(partial_state[0]) - len(partial_state[-1])
    for _ in range(0, padding_needed):
        partial_state[-1].append(0)
    return partial_state

def load_rle(filename, r_padding=20, c_padding=20):
    height, width, born, survive, line_data = read_rle(filename)
    output = dead_state(r_padding, 2 * c_padding + width)
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
                output.append([0 for _ in range(0, c_padding)]) # start next row
            elif sequence[1] == '!':
                output = pad_last_row(output)
                for _ in range(0, r_padding):
                    output.append([0 for _ in range(0, len(output[0]))])
        line_data = line_data[1:]
    return output, born, survive     

def dead_state(height, width):
    return [[0 for cell in range(width)] for row in range(height)]

def random_state(height, width, threshhold=0.5):
    state = dead_state(width, height)
    return [[1 if random.random() >= threshhold else 0 for element in row] for row in state]

def render(state, ant=None):
    chars = [['#' if cell == 1 else ' ' for cell in row] for row in state]
    if ant != None:
        ant_char_dict = {0: '^', 1: '>', 2: 'v', 3: '<'}
        chars[ant.r][ant.c] = ant_char_dict[ant.d]
    string = ('|' + '-' * len(chars[0]) + '|\n')
    for row in chars:
        string += ('|'+ ''.join(row) + '|\n')
    string += ('|' + '-' * len(chars[0]) + '|')
    return string

def dimensions(state):
    x = len(state[0])
    y = len(state)
    return y, x

# Number of live Moore neighbors
def moore_neighbors(y, x, state, wrap):
    yaxis, xaxis = dimensions(state)
    n_live = (-1) * state[y][x] # Don't count the square you're checking!
    if wrap:
        xs = [(x - 1) % xaxis, x, (x + 1) % xaxis]
        ys = [(y - 1) % yaxis, y, (y + 1) % yaxis]
    else:
        xs = [x for x in [(x - 1), x, (x + 1)]  if (0 <= x < xaxis)]
        ys = [y for y in [(y - 1), y, (y + 1)] if (0 <= y < yaxis)]
    for x in xs:
        for y in ys:
            if state[y][x]:
                n_live += 1
    return n_live

# Number of live Von Neumann neighbors
def neumann_neighbors(r, c, state, wrap):
    yaxis, xaxis = dimensions(state)
    n_live = (-1) * state[r][c] # Don't count the square you're checking!
    if wrap:
        xs = [(c - 2) % xaxis, (c - 1) % xaxis, c, (c + 1) % xaxis, (c + 2) % xaxis]
        ys = [(r - 2) % yaxis, (r - 1) % yaxis, r, (r + 1) % yaxis, (r + 2) % xaxis]
    else:
        xs = [x for x in range(c - 2, c + 3)  if (0 <= x < xaxis)]
        ys = [y for y in range(r - 2, r + 3) if (0 <= y < yaxis)]
    for x in xs:
        for y in ys:
            if (x == c or y == r) and state[y][x]:
                n_live += 1
    return n_live
    
def next_board_state(state, born, survive, n_live_function=moore_neighbors, wrap=False):
    new_state = dead_state(*dimensions(state))
    for n_row, row in enumerate(state):
        for n_col, cell in enumerate(row):
            n_live = n_live_function(n_row, n_col, state, wrap)
            if (not cell) and  str(n_live) in born:
                new_state[n_row][n_col] = True
            elif cell and str(n_live) in survive:
                new_state[n_row][n_col] = True
            else:
                new_state[n_row][n_col] = False
    return new_state

class Ant:
    def __init__(self, r, c, d):
        self.r = r
        self.c = c
        self.d = d
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
        
    def __str__(self):
        return str((self.r, self.c, self.d))
        
    def move_forward(self, yaxis, xaxis):
        if self.d == 0:
            self.r =  (self.r - 1) % yaxis
        elif self.d == 1:
            self.c = (self.c + 1) % xaxis
        elif self.d == 2:
            self.r = (self.r + 1) % yaxis
        elif self.d == 3:
            self.c = (self.c - 1) % xaxis
        return self
        
    def next_state(self, board):
        yaxis, xaxis = dimensions(board)
        if board[self.r][self.c]:
            self.d = (self.d + 1) % 4
            board[self.r][self.c] = False
        else:
            self.d = (self.d - 1) % 4
            board[self.r][self.c] = True
        self = self.move_forward(yaxis, xaxis)
        return self, board

def step_ant(board, ant):
    while True:
        # input("Press enter to continue...")
        print(render(board, ant))
        ant, board = ant.next_state(board)
        time.sleep(.02)    

def status_string(filename, step, born, survive, height, width):
    return f" {filename} | {width}x{height} | Survival Rule: {survive} | Birth Rule: {born} | Step: {step}"
        
def main():
    parser = init_argparse()
    args = parser.parse_args()
    if args.file == None:
        if not args.ant:
            state = random_state(200, 100, .05)
            filename = 'Random Initial State'
            born = '2'
            survive = '23'
    else:
        args.file.close()
        filename = args.file.name
        state, born, survive = load_rle(filename, r_padding=args.rows, c_padding=args.columns)    
    if args.ant:
        state = dead_state(100, 200)
        height, width = dimensions(state)
        filename = "Dead Initial State, Random Initial Direction | Langton's Ant"
        survive = "N/A"
        born = "N/A"
        ant = Ant(round(height / 2), round(width / 2), random.randrange(0,4)) 
    else:
        ant = None
        height, width = dimensions(state)
    quit_message = "press 'q' to quit"
    step = 0

    term = blessed.Terminal()
    with term.hidden_cursor():
        with term.fullscreen():    
            with term.cbreak():
                while True:
                    with term.location(0,0):
                        print(term.white + render(state, ant))
                        status = status_string(filename, step, born, survive, height, width)
                        print(status + ' ' * (len(state[0]) - len(status) - len(quit_message)) + quit_message)
                    if args.ant:
                        ant, state = ant.next_state(state)
                    else:
                        state = next_board_state(state, born, survive, wrap=args.wrap)
                    step += 1
                    if term.inkey(0) == 'q':
                        break
                    else:
                        time.sleep(args.delay)

if __name__ == "__main__":
    main()