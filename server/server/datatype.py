import copy


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
        self.client_socket = ''
        self.client_address = ''
        self.data_list = []
        self.mission_list = []
        self.connect = 'exist'
        self.last_convey_time = 0
        self.room = None
        
class Room():
    def __init__(self, room_id):
        self.room_id = room_id
        self.players = []
        self.game = Game_type()  # 假设 Game_type 是你定义的游戏状态类
        self.room_full = False
        self.mission_list = []

class Message():
    def __init__(self):
        self.message_type = ''
        self.message_content = []