import argparse


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python life.py",
        usage="%(prog)s '-f life.rle -r 30 -c 40 -d .02'",
        description="Run Conway's Game of Life in a bounded grid."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        '-file', type=argparse.FileType('r'), 
        help="path to RLE-formatted text file, random board if omitted unless in -ant mode"                
    )
    parser.add_argument(
        '-ant', action='store_true',
        help="implementation of Langton's ant"
    )
    parser.add_argument(
        '-neumann', action='store_true',
        help="use Von Neumann instead of Moore neighborhoods"
    )
    parser.add_argument(
        '-birth', type=str, action='store', default=None,
        help="Birth rule as a sequence of numbers between 0 and 8 (e.g., 2 if cell is born with 2 live neighbors); overrides rle file"
    )
    parser.add_argument(
        '-survival', type=str, action='store', default=None,
        help="Survival rule as a sequence of numbers between 0 and 8 (e.g., 23 if cell survives with 2 or 3 live neighbors); overrides rle file"
    )
    parser.add_argument(
        '-width', type=int, action='store', default=200,
        help='width of board if no file specified (default: 200)'
    )
    parser.add_argument(
        '-height', type=int, action='store', default=100,
        help='height of board if no file specified (default: 100)'
    )
    parser.add_argument(
        '-addrows', type=int, action='store', default=30,
        help='number of rows to add on top and bottom of RLE data (default: 30)'
    )
    parser.add_argument(
        '-addcolumns', type=int, action='store', default=40,
        help='number of columns to add to left and right of RLE data (default: 40)'
    )
    parser.add_argument(
        '-wrap', action='store_true', 
        help='wrap around edges of grid instead of cutting off edges'
    )
    parser.add_argument(
        '-delay', type=float, action='store', default=.01,
        help='approximate delay in seconds between steps (default=.01)'
    )
    return parser