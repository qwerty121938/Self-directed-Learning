import copy
import numpy as np

class Game_type():
    def __init__(self):
        #主要會用到的變數
        self.last_move_place = [['' for _ in range(8)] for _ in range(8)]
        self.can_move_place = [['' for _ in range(8)] for _ in range(8)]
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.player_turn = -1
        self.is_checkmate = 0
        self.stop_game = 0
        self.is_first_move_king = [1,1]
        self.is_first_move_castle = [1,1]
    
    def initial(self):
        # 在这里定义你想要的行为
        self.player_turn = -1
        self.is_checkmate = 0
        self.stop_game = 0
        self.is_first_move_king = [1,1]
        self.is_first_move_castle = [1,1]
        
        #初始化棋子
        self.board[0][0] = 'R'
        self.board[1][0] = 'N'
        self.board[2][0] = 'B'
        self.board[3][0] = 'Q'
        self.board[4][0] = 'K'
        self.board[5][0] = 'B'
        self.board[6][0] = 'N'
        self.board[7][0] = 'R'
        for i in range(8):
            self.board[i][1] = 'P'

        self.board[0][7] = 'r'
        self.board[1][7] = 'n'
        self.board[2][7] = 'b'
        self.board[3][7] = 'q'
        self.board[4][7] = 'k'
        self.board[5][7] = 'b'
        self.board[6][7] = 'n'
        self.board[7][7] = 'r'
        for i in range(8):
            self.board[i][6] = 'p'
    
    def __copy__(self):
        # 建立一個新實例，並複製屬性
        new_instance = copy.deepcopy(self)
        return new_instance
    
class Client_type():
    def __init__(self):
        self.server_ip = ''
        self.server_port = 1080
        self.socket = ''
        self.mission_list = []
        self.data_list = []
        
class Message():
    def __init__(self):
        self.message_type = ''
        self.message_content = []
        
        
class advantage_position():
    
    chess_values = {
            'K': -1200, 'Q': -550, 'R': -230, 'B': -145, 'N': -130, 'P': -50,
            'k':  1200, 'q':  550, 'r':  230, 'b':  145, 'n':  130, 'p':  50
        }
    
    
    PAWN_TABLE = np.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,  5,  5, 10, 10,  5],
        [ 5,  5,  5,  5,  5,  5,  5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 30, 30, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [10, 50, 50, 10, 10, 50, 50, 10],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = np.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  25,  25,  15,   0, -30],
        [-30,   5,  15,  25,  25,  15,   5, -30],
        [-30,   5,  15,  20,  20,  15,   5, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = np.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   5,   5,   5,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = np.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  5,  5,  5,  5,  0,  0]
    ])

    QUEEN_TABLE = np.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5, 10,  5,   5,   0, -10],
        [  0,   5,  10, 10, 10,   5,   5,  -5],
        [ -5,   0,   5, 10,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])