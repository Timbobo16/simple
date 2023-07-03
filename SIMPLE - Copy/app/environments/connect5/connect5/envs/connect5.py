
import gym
import numpy as np

import config

from stable_baselines import logger

import chess


class Player():
    def __init__(self, id, token):
        self.id = id
        self.token = token
        

class Token():
    def __init__(self, symbol, number):
        self.number = number
        self.symbol = symbol
        
        
class Connect5Env(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(Connect5Env, self).__init__()
        self.name = 'connect5'
        self.manual = manual

        self.rows = 8
        self.cols = 8
        self.n_players = 2
        self.grid_shape = (self.rows, self.cols)
        self.num_squares = self.rows * self.cols
        self.action_space = gym.spaces.Discrete((self.num_squares*self.num_squares) + 64)
        self.observation_space = gym.spaces.Box(-1, 1, self.grid_shape + (13, ))
        self.verbose = verbose
        self.board = chess.Board()
        

    @property
    def observation(self):
        # logger.debug(f'\n\n-2:--- {self.board.fen()} ----')
        # board_file = open(r"board.txt","r")
        # read = board_file.read()
        # logger.debug(f'\n\n--READ2:-- {read} ----')
        # board_file.close()

        board_file = open(r"board.txt","r")
        self.board = chess.Board(board_file.read())
        # logger.debug(f'\n\n--3:-- {self.board.fen()} ----')
        board_file.close()

        # board_file = open(r"board.txt","r")
        # read = board_file.read()
        # logger.debug(f'\n\n--READ3:-- {read} ----')
        # board_file.close()

        # logger.debug(f'\n\n--4:-- {self.board.fen()} ----')
        flatboard = np.array(self.board_fen_to_array(self.board.board_fen())).reshape(self.num_squares)
        if self.current_player == 1:
            position_1 = np.array([1 if x == 'P' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_2 = np.array([1 if x == 'N' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_3 = np.array([1 if x == 'B' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_4 = np.array([1 if x == 'R' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_5 = np.array([1 if x == 'Q' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_6 = np.array([1 if x == 'K' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_7 = np.array([1 if x == 'p' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_8 = np.array([1 if x == 'n' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_9 = np.array([1 if x == 'b' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_10 = np.array([1 if x == 'r' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_11 = np.array([1 if x == 'q' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_12 = np.array([1 if x == 'k' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_13 = np.array([1 if x == '.' else 0  for x in flatboard]).reshape(self.grid_shape)
        else:
            position_1 = np.array([1 if x == 'p' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_2 = np.array([1 if x == 'n' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_3 = np.array([1 if x == 'b' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_4 = np.array([1 if x == 'r' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_5 = np.array([1 if x == 'q' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_6 = np.array([1 if x == 'k' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_7 = np.array([1 if x == 'P' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_8 = np.array([1 if x == 'N' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_9 = np.array([1 if x == 'B' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_10 = np.array([1 if x == 'R' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_11 = np.array([1 if x == 'Q' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_12 = np.array([1 if x == 'K' else 0  for x in flatboard]).reshape(self.grid_shape)
            position_13 = np.array([1 if x == '.' else 0  for x in flatboard]).reshape(self.grid_shape)

        out = np.stack([position_1, position_2, position_3, position_4, position_5, position_6, position_7, position_8, position_9, position_10, position_11, position_12, position_13], axis = -1) 
        return out

    @property
    def legal_actions(self):
        #return [self.uci_to_int(m.uci()) for m in self.board.legal_moves]
        # legal_actions = []
        # for action_num in range(self.action_space.n):
        #     legal = self.is_legal(action_num)
        #     legal_actions.append(legal)
        legal_actions = np.zeros(self.action_space.n)    
        for action_num in [self.uci_to_int(m.uci()) for m in self.board.legal_moves]:
            legal_actions[action_num] = 1
        return legal_actions

    def board_fen_to_array(self, fenboard):
        result = []
        rows = fenboard.split('/')
        for row in rows:
            newrow = [x for x in row]
            for c in row:
                if c.isnumeric():
                    idx = row.index(c)
                    newrow.pop(idx)
                    for i in range(0, int(c)):
                        newrow.insert(idx, '.')
            result.append(newrow)
        return result
    
    def int_to_square(self, i):
        if i%8 == 0:
            first = "a"
        elif i%8 == 1:
            first = "b"
        elif i%8 == 2:
            first = "c"
        elif i%8 == 3:
            first = "d"
        elif i%8 == 4:
            first = "e"
        elif i%8 == 5:
            first = "f"
        elif i%8 == 6:
            first = "g"
        elif i%8 == 7:
            first = "h"
        second = str((i//8)+1)
        return first + second
    
    def int_to_uci(self, i):
        if i >= 4096:
            if i%4 == 0:
                last = "n"
            elif i%4 == 1:
                last = "b"
            elif i%4 == 2:
                last = "r"
            elif i%4 == 3:
                last = "q"
            if i < 4100:
                first = "a7a8"
            elif i < 4104:
                first = "b7b8"
            elif i < 4108:
                first = "c7c8"
            elif i < 4112:
                first = "d7d8"
            elif i < 4116:
                first = "e7e8"
            elif i < 4120:
                first = "f7f8"
            elif i < 4124:
                first = "g7g8"
            elif i < 4128:
                first = "h7h8"
            elif i < 4132:
                first = "a2a1"
            elif i < 4136:
                first = "b2b1"
            elif i < 4140:
                first = "c2c1"
            elif i < 4144:
                first = "d2d1"
            elif i < 4148:
                first = "e2e1"
            elif i < 4152:
                first = "f2f1"
            elif i < 4156:
                first = "g2g1"
            elif i < 4160:
                first = "h2h1"
            return first + last
        first = self.int_to_square(i//64)
        second = self.int_to_square(i%64)
        return first + second

    def uci_to_int(self, uci):
        if len(uci) == 5:
            if uci[:2] == "a7":
                result = 4096
            elif uci[:2] == "b7":
                result = 4100
            elif uci[:2] == "c7":
                result = 4104
            elif uci[:2] == "d7":
                result = 4108
            elif uci[:2] == "e7":
                result = 4112
            elif uci[:2] == "f7":
                result = 4116
            elif uci[:2] == "g7":
                result = 4120
            elif uci[:2] == "h7":
                result = 4124
            elif uci[:2] == "a2":
                result = 4128
            elif uci[:2] == "b2":
                result = 4132
            elif uci[:2] == "c2":
                result = 4136
            elif uci[:2] == "d2":
                result = 4140
            elif uci[:2] == "e2":
                result = 4144
            elif uci[:2] == "f2":
                result = 4148
            elif uci[:2] == "g2":
                result = 4152
            elif uci[:2] == "h2":
                result = 4156
            if uci[4] == "n":
                result += 0
            elif uci[4] == "b":
                result += 1
            elif uci[4] == "r":
                result += 2
            elif uci[4] == "q":
                result += 3
            return result
        result = 0
        if uci[0] == "a":
            result += 0
        elif uci[0] == "b":
            result += 64
        elif uci[0] == "c":
            result += 128
        elif uci[0] == "d":
            result += 192
        elif uci[0] == "e":
            result += 256
        elif uci[0] == "f":
            result += 320
        elif uci[0] == "g":
            result += 384
        elif uci[0] == "h":
            result += 448
        if uci[1] == "1":
            result += 0
        elif uci[1] == "2":
            result += 512
        elif uci[1] == "3":
            result += 1024
        elif uci[1] == "4":
            result += 1536
        elif uci[1] == "5":
            result += 2048
        elif uci[1] == "6":
            result += 2560
        elif uci[1] == "7":
            result += 3072
        elif uci[1] == "8":
            result += 3584
        if uci[2] == "a":
            result += 0
        elif uci[2] == "b":
            result += 1
        elif uci[2] == "c":
            result += 2
        elif uci[2] == "d":
            result += 3
        elif uci[2] == "e":
            result += 4
        elif uci[2] == "f":
            result += 5
        elif uci[2] == "g":
            result += 6
        elif uci[2] == "h":
            result += 7
        if uci[3] == "1":
            result += 0
        elif uci[3] == "2":
            result += 8
        elif uci[3] == "3":
            result += 16
        elif uci[3] == "4":
            result += 24
        elif uci[3] == "5":
            result += 32
        elif uci[3] == "6":
            result += 40
        elif uci[3] == "7":
            result += 48
        elif uci[3] == "8":
            result += 56
        return result

                

    def is_legal(self, action_num):
        if self.int_to_uci(action_num) in [m.uci() for m in self.board.legal_moves]:
            return True
        else:
            return False

    def can_be_placed(self, square_num):
        
        if self.board[square_num].number==0:
            for height in range(square_num + self.cols, self.num_squares , self.cols):
                if self.board[height].number==0:
                    return 0
        else:
            return 0

        return 1



    def square_is_player(self, board, square, player):
        return board[square].number == self.players[player].token.number

    def check_game_over(self, board = None , player = None):

        if board is None:
            board = self.board

        if player is None:
            player = self.current_player_num

        if self.board.is_game_over():
            #outcome = self.board.outcome()
            result = self.board.result()
            if result != "*":
                if result[2] == 2:
                    return 0.5, True
                elif result[2] == player:
                    return 0, True
                else:
                    return 1, True

        return 0, False #-0.01 here to encourage choosing the win?

    def get_square(self, board, action):
        for height in range(1, self.rows + 1):
            square = self.num_squares - (height * self.cols) + action
            if board[square].number == 0:
                return square

    @property
    def current_player(self):
        return self.players[self.current_player_num]

    def step(self, action):
        
        reward = [0,0]
        
        # check move legality
        board = self.board
        if action == 0000:
            done = False
            board_file = open(r"board.txt","r")
            read = board_file.read()
            #logger.debug(f'\n\n---- {read} ----')
            self.board = chess.Board(read)
            #logger.debug(f'\n\n---- {self.board.fen()} ----')
            board_file.close()
            # self.board.push_uci("0000")
            # board_file = open(r"board.txt","w")
            # board_file.write(self.board.fen())
            # board_file.close()

            # board_file = open(r"board.txt","r")
            # read = board_file.read()
            # logger.debug(f'\n\n--READC:-- {read} ----')
            # board_file.close()
            #logger.debug(f'\n\n---- {self.board.fen()} ----')
        elif not self.is_legal(action): 
            done = True
            reward = [1,1]
            reward[self.current_player_num] = -1
            # board_file = open(r"board.txt","r")
            # read = board_file.read()
            # logger.debug(f'\n\n--READD:-- {read} ----')
            # board_file.close()
        else:
            # board_file = open(r"board.txt","r")
            # read = board_file.read()
            # logger.debug(f'\n\n--READE:-- {read} ----')
            # board_file.close()

            self.board.push_uci(self.int_to_uci(action))
            board_file = open(r"board.txt","w")
            board_file.write(self.board.fen())
            board_file.close()

            # board_file = open(r"board.txt","r")
            # read = board_file.read()
            # logger.debug(f'\n\n--READF:-- {read} ----')
            # board_file.close()

            #self.turns_taken += 1
            r, done = self.check_game_over()
            reward = [-r,-r]
            reward[self.current_player_num] = r

            # board_file = open(r"board.txt","r")
            # read = board_file.read()
            # logger.debug(f'\n\n--READG:-- {read} ----')
            # board_file.close()
        self.done = done

        # board_file = open(r"board.txt","r")
        # read = board_file.read()
        # logger.debug(f'\n\n--READH:-- {read} ----')
        # board_file.close()

        if not done:
            self.current_player_num = (self.current_player_num + 1) % 2
            #self.current_player_num = board.turn
        # logger.debug(f'\n\n--1:-- {self.board.fen()} ----')
        # board_file = open(r"board.txt","r")
        # read = board_file.read()
        # logger.debug(f'\n\n--READ1:-- {read} ----')
        # board_file.close()
        return self.observation, reward, done, {}

    def reset(self):
        self.board.reset()
        board_file = open(r"board.txt","w")
        board_file.write(self.board.fen())
        board_file.close()
        self.players = [Player('1', Token('X', 1)), Player('2', Token('O', -1))]
        self.current_player_num = chess.WHITE
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation


    def render(self, mode='human', close=False):
        #logger.debug('')
        if close:
            return
        if self.done:
            logger.debug(f'GAME OVER')
        else:
            logger.debug(f"It is Player {self.current_player.id}'s turn to move")
            # logger.debug(f'\n\n--6:-- {self.board.fen()} ----')
        logger.debug(self.board)
        #for i in range(0,self.num_squares,self.cols):
            #logger.debug(' '.join([x.symbol for x in self.board[i:(i+self.cols)]]))

        if self.verbose:
            logger.debug(f'\nObservation: \n{self.observation}')
        
        if not self.done:
            logger.debug(f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}')



    def rules_move(self):
        WRONG_MOVE_PROB = 0.01
        player = self.current_player_num

        for action in range(self.action_space.n):
            if self.is_legal(action):
                new_board = self.board.copy()
                square = self.get_square(new_board, action)
                new_board[square] = self.players[player].token
                _, done = self.check_game_over(new_board, player)
                if done:
                    action_probs = [WRONG_MOVE_PROB] * self.action_space.n
                    action_probs[action] = 1 - WRONG_MOVE_PROB * (self.action_space.n - 1)
                    return action_probs

        player = (self.current_player_num + 1) % 2

        for action in range(self.action_space.n):
            if self.is_legal(action):
                new_board = self.board.copy()
                square = self.get_square(new_board, action)
                new_board[square] = self.players[player].token
                _, done = self.check_game_over(new_board, player)
                if done:
                    action_probs = [0] * self.action_space.n
                    action_probs[action] = 1 - WRONG_MOVE_PROB * (self.action_space.n - 1)
                    return action_probs

        
        action, masked_action_probs = self.sample_masked_action([1] * self.action_space.n)
        return masked_action_probs




