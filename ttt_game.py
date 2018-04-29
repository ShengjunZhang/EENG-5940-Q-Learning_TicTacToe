import numpy as np
import Tkinter as tk
import copy
import pdb
import pickle

from board import Board

class Game:
    def __init__(self, master, bot1, bot2, Q_learn=None, Q={}, alpha=0.3, gamma=0.9):
        frame = tk.Frame()
        frame.grid()
        self.master = master
        master.title("EENG5940 Q_learning_ttt Copyright(C) 2018 Daniel_Zhang")

        self.bot1 = bot1
        self.bot2 = bot2
        self.current_bot = bot1
        self.other_bot = bot2
        self.empty_text = ""
        self.board = Board()

        self.buttons = [[None for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.buttons[i][j] = tk.Button(frame, height=1, width=2,text=self.empty_text,font='Helvetica -150 bold',command=lambda i=i, j=j: self.callback(self.buttons[i][j]))
                self.buttons[i][j].grid(row=i, column=j)

        self.reset_button = tk.Button(text="Try Again", command=self.reset,font='Helvetica -18 bold')
        self.reset_button.grid(row=4)

        self.Q_learn = Q_learn
        self.Q_learn_or_not()
        if self.Q_learn:
            self.Q = Q
            self.alpha = alpha          
            self.gamma = gamma         
            self.share_Q_with_players()

    def Q_learn_or_not(self):       
        if self.Q_learn is None:
            if isinstance(self.bot1, QPlayer) or isinstance(self.bot2, QPlayer):
                self.Q_learn = True

    def share_Q_with_players(self):             
        if isinstance(self.bot1, QPlayer):
            self.bot1.Q = self.Q
        if isinstance(self.bot2, QPlayer):
            self.bot2.Q = self.Q

    def callback(self, button):
        if self.board.over():
            pass               
        else:
            if isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, HumanPlayer):
                if self.empty(button):
                    move = self.get_move(button)
                    self.handle_move(move)
            elif isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, ComputerPlayer):
                computer_player = self.other_player
                if self.empty(button):
                    human_move = self.get_move(button)
                    self.handle_move(human_move)
                    if not self.board.over():              
                        computer_move = computer_player.get_move(self.board)
                        self.handle_move(computer_move)

    def empty(self, button):
        return button["text"] == self.empty_text

    def get_move(self, button):
        info = button.grid_info()
        move = (int(info["row"]), int(info["column"]))               
        return move

    def handle_move(self, move):
       

        if self.Q_learn:
            self.learn_Q(move)
        i, j = move        
        self.buttons[i][j].configure(text=self.current_player.mark)     
        self.board.place_mark(move, self.current_player.mark)          
        if self.board.over():
            self.declare_outcome()
        else:
            self.switch_players()

    def declare_outcome(self):
        if self.board.winner() is None:
            print ("Tie!!!")
        else:
            print ("Game Gver. %s won!") % self.current_player.mark

    def reset(self):
        print ("New Game")
        for i in range(4):
            for j in range(4):
                self.buttons[i][j].configure(text=self.empty_text)
        self.board = Board(grid=np.ones((4,4))*np.nan)
        self.current_player = self.bot1
        self.other_player = self.bot2
       
        self.play()

    def switch_players(self):
        if self.current_player == self.bot1:
            self.current_player = self.bot2
            self.other_player = self.bot1
        else:
            self.current_player = self.bot1
            self.other_player = self.bot2

    def play(self):
        if isinstance(self.bot1, HumanPlayer) and isinstance(self.bot2, HumanPlayer):
            pass       
        elif isinstance(self.bot1, HumanPlayer) and isinstance(self.bot2, ComputerPlayer):
            pass
        elif isinstance(self.bot1, ComputerPlayer) and isinstance(self.bot2, HumanPlayer):
            first_computer_move = bot1.get_move(self.board)      
            self.handle_move(first_computer_move)
        elif isinstance(self.bot1, ComputerPlayer) and isinstance(self.bot2, ComputerPlayer):
            while not self.board.over():       
                self.play_turn()
                
    def play_turn(self):
        move = self.current_player.get_move(self.board)
        self.handle_move(move)

    def gameLearning(self, move):                        
        state_key = QPlayer.updateQvalues(self.board, self.current_player.mark, self.Q)
        next_board = self.board.get_next_board(move, self.current_player.mark)
        reward = next_board.give_reward()
        next_state_key = QPlayer.updateQvalues(next_board, self.other_player.mark, self.Q)
        
        if next_board.over():
            expected = reward
        else:
            next_Qs = self.Q[next_state_key]           
            if self.current_player.mark == "X":
                expected = reward + (self.gamma * min(next_Qs.values()))       
            elif self.current_player.mark == "O":
                expected = reward + (self.gamma * max(next_Qs.values()))      
        change = self.alpha * (expected - self.Q[state_key][move])
        self.Q[state_key][move] += change

class Player(object):
    def __init__(self, mark):
        self.mark = mark
        self.get_opponent_mark()

    def get_opponent_mark(self):
        if self.mark == 'X':
            self.opponent_mark = 'O'
        elif self.mark == 'O':
            self.opponent_mark = 'X'
        else:
            print ("The player's mark must be either 'X' or 'O'.")

class HumanPlayer(Player):
    pass

class ComputerPlayer(Player):
    pass

class RandomPlayer(ComputerPlayer):
    @staticmethod
    def get_move(board):
        moves = board.available_moves()
        if moves:   
            return moves[np.random.choice(len(moves))]   

class THandPlayer(ComputerPlayer):
    def __init__(self, mark):
        super(THandPlayer, self).__init__(mark=mark)

    def get_move(self, board):
        moves = board.available_moves()
        if moves:
            for move in moves:
                if THandPlayer.next_move_winner(board, move, self.mark):
                    return move
                elif THandPlayer.next_move_winner(board, move, self.opponent_mark):
                    return move
            else:
                return RandomPlayer.get_move(board)

    @staticmethod
    def next_move_winner(board, move, mark):
        return board.get_next_board(move, mark).winner() == mark


class QPlayer(ComputerPlayer):
    def __init__(self, mark, Q={}, epsilon=0.2):
        super(QPlayer, self).__init__(mark=mark)
        self.Q = Q
        self.epsilon = epsilon

    def get_move(self, board):
        if np.random.uniform() < self.epsilon:              
            return RandomPlayer.get_move(board)
        else:
            state_key = QPlayer.updateQvalues(board, self.mark, self.Q)
            
            Qs = self.Q[state_key]
            print (Qs)

            if self.mark == "X":
                print (QPlayer.stochastic_argminmax(Qs, max))
                return QPlayer.stochastic_argminmax(Qs, max)
            elif self.mark == "O":
                print (QPlayer.stochastic_argminmax(Qs, min))
                return QPlayer.stochastic_argminmax(Qs, min)

    @staticmethod
    def updateQvalues(board, mark, Q):    
        default_Qvalue = 1.0      
        state_key = board.make_key(mark)
        if Q.get(state_key) is None:
            moves = board.available_moves()
            Q[state_key] = {move: default_Qvalue for move in moves}    
        return state_key

    @staticmethod
    def stochastic_argminmax(Qs, min_or_max):       
        min_or_maxQ = min_or_max(Qs.values())
        if Qs.values().count(min_or_maxQ) > 1:      
            best_options = [move for move in Qs.keys() if Qs[move] == min_or_maxQ]
            move = best_options[np.random.choice(len(best_options))]
        else:
            move = min_or_max(Qs, key=Qs.get)
        return move

