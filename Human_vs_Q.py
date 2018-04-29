# import packages
import numpy as np
import Tkinter as tk
import copy
import pickle
import timeit
import gc
from datetime import datetime

from ttt_game import Game, Player, HumanPlayer, ComputerPlayer, RandomPlayer, THandPlayer, QPlayer
from board import Board

tk.wantobjects = False

print('Starting loading Q_table, just be patient please...')

print(str(datetime.now()))
output = open('Q_table.pickle','rb')

print('opening file...')
gc.disable()
print('disable gc...')
Q = pickle.load(output)
print(str(datetime.now()))
gc.enable()
print('enable gc...')
output.close()
print('closing output...')

print('Load Q table Done!')
print('Loading Game...')
print(str(datetime.now()))
root = tk.Tk()

bot1 = HumanPlayer(mark="X")
bot2 = QPlayer(mark="O", epsilon=0)

game = Game(root, bot1, bot2, Q=Q)
print(str(datetime.now()))
print('Enjoy Game with Q-agent, if you can beat it, please let me know!')
game.play()
print('game.play')
print(str(datetime.now()))
root.mainloop()

