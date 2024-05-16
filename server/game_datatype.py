import copy

class Game_type ():
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
    
    def __copy__(self):
        # 建立一個新實例，並複製屬性
        new_instance = copy.deepcopy(self)
        return new_instance