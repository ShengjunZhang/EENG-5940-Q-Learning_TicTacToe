import numpy as np
import Tkinter as tk
import copy
import pickle
from ttt_game import Game, Player, HumanPlayer, ComputerPlayer, RandomPlayer, THandPlayer, QPlayer
from board import Board


tk.wantobjects = False
root = tk.Tk()
epsilon_set = 0.15
epsilon = 1 - epsilon
bot1 = QPlayer(mark="X",epsilon = epsilon)
bot2 = QPlayer(mark="O",epsilon = epsilon)
game = Game(root, bot1, bot2)

N_episodes = 50000000

for episodes in range(N_episodes):
    game.play()
    game.reset()


print('Training Done!')
Q = game.Q

filename = "Q_table.pickle"
pickle.dump(Q, open(filename, "wb"))
print('Updating Q_Table Done!')
