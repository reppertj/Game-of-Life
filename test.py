import unittest

from board import Board


class BoardTest(unittest.TestCase):
        
    def test_empty_board_stays_emtpy(self):
        init_state1 = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]
        born = "3"
        survive = "23"
        expected_next_state1 = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]        
        board = Board(init_state1)
        board.next_board_state(born, survive, False, False)
        self.assertEqual(board.state, expected_next_state1)
        
    def test_dead_cells_with_3_neighbors_come_alive(self):
        init_state2 = [
            [0,0,1],
            [0,1,1],
            [0,0,0]
        ]
        born = "3"
        survive = "23"
        expected_next_state2 = [
            [0,1,1],
            [0,1,1],
            [0,0,0]
        ]
        board = Board(init_state2)
        board.next_board_state(born, survive, False, False)
        self.assertEqual(board.state, expected_next_state2)
        
if __name__ == "__main__":
    unittest.main()
    