import random
from typing import List, Tuple


class Board:
    def __init__(self, initial_state: List[str]):
        self.state = initial_state
        self._resize()
    
                
    def _resize(self):
        self.shape = (len(self.state), len(self.state[0]))


    def neumann_neighbors(self, r, c, wrap):
        yaxis, xaxis = self.shape
        n_live = (-1) * self.state[r][c]  # Don't count the spot you're checking!
        if wrap:
            xs = [(c - 2) % xaxis, (c - 1) % xaxis, c, (c + 1) % xaxis, (c + 2) % xaxis]
            ys = [(r - 2) % yaxis, (r - 1) % yaxis, r, (r + 1) % yaxis, (r + 2) % xaxis]
        else:
            xs = [x for x in range(c - 2, c + 3) if (0 <= x < xaxis)]
            ys = [y for y in range(r - 2, r + 3) if (0 <= y < yaxis)]
        for x in xs:
            for y in ys:
                if (x == c or y == r) and self.state[y][x]:
                    n_live += 1
        return n_live

    
    def moore_neighbors(self, y, x, wrap):
        yaxis, xaxis = self.shape
        n_live = (-1) * self.state[y][x]  # Don't count the spot you're checking!
        if wrap:
            xs = [(x - 1) % xaxis, x, (x + 1) % xaxis]
            ys = [(y - 1) % yaxis, y, (y + 1) % yaxis]
        else:
            xs = [x for x in [(x - 1), x, (x + 1)] if (0 <= x < xaxis)]
            ys = [y for y in [(y - 1), y, (y + 1)] if (0 <= y < yaxis)]
        for x in xs:
            for y in ys:
                if self.state[y][x]:
                    n_live += 1
        return n_live
    
    
    def next_board_state(self, born, survive, neumann, wrap):
        new_state = dead_board(self.shape).state
        for n_row, row in enumerate(self.state):
            for n_col, cell in enumerate(row):
                if neumann:
                    n_live = self.neumann_neighbors(n_row, n_col, wrap)
                else:
                    n_live = self.moore_neighbors(n_row, n_col, wrap)
                if (not cell) and str(n_live) in born:
                    new_state[n_row][n_col] = 1
                elif cell and str(n_live) in survive:
                    new_state[n_row][n_col] = 1
                else:
                    new_state[n_row][n_col] = 0
        self.state = new_state

        
def dead_board(shape: Tuple[int]):
    state = [[0 for cell in range(shape[1])] for row in range(shape[0])]
    return Board(state)


def random_board(shape: Tuple[int], threshhold=0.5):
    dead = dead_board(shape)
    state = [[1 if random.random() >= threshhold else 0
              for element in row] for row in dead.state]
    return Board(state)
