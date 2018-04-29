import numpy as np
import Tkinter as tk
import copy
import pdb
import pickle   


class Board:
    def __init__(self, grid=np.ones((4,4))*np.nan):
        self.grid = grid

    def winner(self):
        rows = [self.grid[i,:] for i in range(4)]
        cols = [self.grid[:,j] for j in range(4)]
        diag = [np.array([self.grid[i,i] for i in range(4)])]
        cross_diag = [np.array([self.grid[3-i,i] for i in range(4)])]
        lanes = np.concatenate((rows, cols, diag, cross_diag))      
        any_lane = lambda x: any([np.array_equal(lane, x) for lane in lanes])   
            return "X"
        elif any_lane(np.zeros(4)):
            return "O"

    def over(self):            
        return (not np.any(np.isnan(self.grid))) or (self.winner() is not None)

    def place_mark(self, move, mark):      
        num = Board.mark2num(mark)
        self.grid[tuple(move)] = num

    @staticmethod
    def mark2num(mark):        
        d = {"X": 1, "O": 0}
        return d[mark]

    def available_moves(self):
        return [(i,j) for i in range(4) for j in range(4) if np.isnan(self.grid[i][j])]

    def get_next_board(self, move, mark):
        next_board = copy.deepcopy(self)
        next_board.place_mark(move, mark)
        return next_board

    def make_key(self, mark):          
        fill_value = 16
        filled_grid = copy.deepcopy(self.grid)
        np.place(filled_grid, np.isnan(filled_grid), fill_value)
        return "".join(map(str, (map(int, filled_grid.flatten())))) + mark

    def give_reward(self):                         
        if self.over():
            if self.winner() is not None:
                if self.winner() == "X":
                    return 1.0                      
                elif self.winner() == "O":
                    return -1.0                                            
        else:
            return 0.0                              
