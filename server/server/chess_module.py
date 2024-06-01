import copy
from datatype import Game_type
from move_logic import Move_logic

def debug_print_array (array) :
    for i in range(8):
        print(array[i])
        
        
class Process():
    
    def __init__(self):
        pass
    
    def array_clear(array):
        for i in range(8):
            for j in range(8):
                array[i][j] = ''
                
            
    def moving (game, start_pos, end_pos):
        game.player_turn *= -1
        
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        chess_class = game.board[start_x][start_y]
        
        if chess_class == 'k' :
            if end_pos == (6, 7) and game.board[7][7] == 'r' and game.is_first_move_castle[0] and game.is_first_move_king[0]:
                print(1)
                game.board[5][7] = 'r'
                game.board[7][7] = '' 
                game.is_first_move_castle[0] = 0
            
            game.is_first_move_king[0] = 0
            
        elif chess_class == 'K' :
            if end_pos == (6, 0) and game.board[7][0] == 'R' and game.is_first_move_castle[1] and game.is_first_move_king[1]:
                print(2)
                game.board[5][0] = 'R'
                game.board[7][0] = '' 
                game.is_first_move_castle[1] = 0
                   
            game.is_first_move_king[1] = 0
            
        elif chess_class == 'r':
            game.is_first_move_castle[0] = 0
        elif chess_class == 'R':
            game.is_first_move_castle[1] = 0
                
        game.board[start_x][start_y] = ''
        game.board[end_x][end_y] = chess_class

        if chess_class == "p" and end_y == 0 :
            game.board[end_x][end_y] = 'q'
        
        if chess_class == "P" and end_y == 7 :
            game.board[end_x][end_y] = 'Q'
            
       
        game.is_checkmate = Process.checkmate_detect(game)
        game.stop_game = Process.is_win_game_detect(game)
        Process.array_clear(game.last_move_place)
        game.last_move_place[start_x][start_y] = '!'
        game.last_move_place[end_x][end_y] = '!' 
        
        return game
        
        
        
    def is_legal_move(game, select_place, want_move_place): #判端如果我方移動這個位置後 我方是否被將軍
        
        def moving (start_pos, end_pos): #移動
            
            start_x, start_y = start_pos
            end_x, end_y = end_pos
            chess_class = temp_game.board[start_x][start_y]
            
            if chess_class == 'k' :
                if end_pos == (6, 7) and temp_game.board[7][7] == 'r' and temp_game.is_first_move_castle[0] and temp_game.is_first_move_king[0]:
                    temp_game.board[5][7] = 'r'
                    temp_game.board[7][7] = '' 
                
                temp_game.is_first_move_king[0] = 0
            elif chess_class == 'K' :
                if end_pos == (6, 0) and temp_game.board[7][0] == 'R' and temp_game.is_first_move_castle[1] and temp_game.is_first_move_king[1]:
                    temp_game.board[5][0] = 'R'
                    temp_game.board[7][0] = '' 
                    
                temp_game.is_first_move_king[1] = 0
            elif chess_class == 'r':
                temp_game.is_first_move_castle[0] = 0
            elif chess_class == 'R':
                temp_game.is_first_move_castle[1] = 0
                    
            temp_game.board[start_x][start_y] = ''
            temp_game.board[end_x][end_y] = chess_class

            if chess_class == "p" and end_y == 0 :
                temp_game.board[end_x][end_y] = 'q'
            
            if chess_class == "P" and end_y == 7 :
                temp_game.board[end_x][end_y] = 'Q'
        
        #複製原本的棋盤
        temp_game = game.__copy__()
        #移動後        
        moving (select_place , want_move_place)
        
        
        #偵測是不是被將軍
        if Process.checkmate_detect(temp_game) :
            return 0

        return 1
    
    
    
    def is_win_game_detect (game) :
        
        #print(1)
        def check_all_place_can_move(select):
            for i in range(8):
                for j in range(8):
                    move_selection = temp_game.can_move_place[i][j]
                    
                    #這個位置規則上是可以走得 而且不會被將軍        
                    if move_selection == '*' and Process.is_legal_move(temp_game, select, (i, j)) == 1 : 
                        return 0
                    
            return 1
        
                        
        temp_game = game.__copy__()
        Process.array_clear(temp_game.can_move_place)
        
        for i in range(8):
            for j in range(8):
                if Move_logic.white_black_detect(temp_game.board[i][j]) == temp_game.player_turn : #我方棋子
                    
                    Process.array_clear(temp_game.can_move_place)
                    
                    #尋找這個棋子可以走的路徑
                    Move_logic.chess_choose(temp_game, (i, j))
                    
                    #尋找這個棋子真正可以走的路徑  
                    if check_all_place_can_move((i, j)) == 0 :
                        # print("目前的偵測棋子:")
                        # print((i, j))
                        return 0
                    
        return 1                
        
    
    
    #判定目前回合的玩家是否被將軍    
    def checkmate_detect(game):
        def is_move_place_have_king():
            for i in range(8):
                for j in range(8):
                    if temp_game.can_move_place[i][j] == '*' and (i,j) == king_place : # *字是可以走的位置如果是我方國王的位置 => 將軍   
                        return 1
                    
        #預設沒有將軍
        temp_game = game.__copy__()
        Process.array_clear(temp_game.can_move_place)
        king_place = (-1,-1)
        
        #先找到目前回合的玩家將軍位置
        for i in range(8):
            for j in range(8):
                chess_class = temp_game.board[i][j]
                if temp_game.player_turn == -1 and chess_class == 'k':
                    king_place = (i,j)
                elif temp_game.player_turn == 1 and chess_class == 'K' :
                    king_place = (i,j)
                    
        #尋找所有敵方棋子 如果敵方其中一個棋子的路徑包含我方國王 => 被將軍                
        for i in range(8):
            for j in range(8):
                chess_class = temp_game.board[i][j]
                if Move_logic.white_black_detect(chess_class) == -temp_game.player_turn: #敵方棋子
                    Process.array_clear(temp_game.can_move_place)
                    move_selection = (i,j)
                    Move_logic.chess_choose(temp_game, move_selection) #找出現在搜尋的敵方棋子可以走的所有路徑
                    
                    if is_move_place_have_king() :  #搜尋可以走的路徑是不是包含我方將軍
                        return 1
        return 0
    
