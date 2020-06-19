import random
import time
import blessed

from ant import Ant
import lifereader
from board import Board, random_board, dead_board
from arg_parser import init_argparse

ANT_DESCRIPTION = "Dead Initial State, Random Initial Direction | Langton's Ant"
RANDOM_DESCRIPTION = "Random Initial State"
QUIT_MESSAGE = "press 'q' to quit"


def pretty(state, ant=None):
    chars = [['#' if cell == 1 else ' ' for cell in row] for row in state]
    if ant is not None:
        ant_char_dict = {0: '^', 1: '>', 2: 'v', 3: '<'}
        try:
            chars[ant.r][ant.c] = ant_char_dict[ant.d]
        except IndexError:
            pass  
    string = ('|' + '-' * len(chars[0]) + '|\n')
    for row in chars:
        string += ('|' + ''.join(row) + '|\n')
    string += ('|' + '-' * len(chars[0]) + '|')
    return string


def status_string(filename, step, born, survive, height, width):
    return f" {filename} | {width}x{height} | Survival Rule: {survive} | Birth Rule: {born} | Step: {step}"


def get_file_extension(filename):
    filename = filename.split('/')[-1].split('\\')[-1]
    if len(filename.split('.')) > 1:
        return filename.split('.')[-1].lower()
    else:
        return None


def initialize(args):
    born = "3"
    survive = "23"
    if args.file is not None:
        args.file.close()
        filename = args.file.name
        description = filename
        extension = get_file_extension(filename)
        if extension == 'txt':
            state = lifereader.parse_txt(filename)
            board = Board(state)
        elif extension == 'rle':
            rle_object = lifereader.load_rle(filename, args.addrows, args.addcolumns)
            board = Board(rle_object.state)
            born = rle_object.born
            survive = rle_object.survive
    elif not args.ant:
        description = RANDOM_DESCRIPTION
        board = random_board((args.height, args.width))
    if args.ant:
        description = ANT_DESCRIPTION
        board = dead_board((args.height, args.width))
        survive = "N/A"
        born = "N/A"
        ant = Ant(round(args.height / 2), round(args.width / 2),
                  random.randrange(0, 4)) 
    else: 
        ant = None
    if args.birth is not None:
        born = args.birth
    if args.survival is not None:
        survive = args.survival
    return board, ant, born, survive, description
  
def main():
    parser = init_argparse()
    args = parser.parse_args()
    board, ant, born, survive, description = initialize(args)
    step = 0
    term = blessed.Terminal()
    with term.hidden_cursor():
        with term.fullscreen():    
            with term.cbreak():
                while True:
                    with term.location(0,0):
                        print(term.white + pretty(board.state, ant))
                        status = status_string(description, step, born, survive, board.shape[0], board.shape[1])
                        print(status + ' ' * (board.shape[1] - len(status) - len(QUIT_MESSAGE)) + QUIT_MESSAGE)
                    if args.ant:
                        ant, board.state = ant.next_state(board.state, args.wrap)
                    else:
                        board.next_board_state(born, survive, args.neumann, args.wrap)
                    step += 1
                    if term.inkey(0) == 'q':
                        break
                    else:
                        time.sleep(args.delay)


if __name__ == "__main__":
    main()