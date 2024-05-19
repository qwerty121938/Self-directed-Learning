from datatype import Game_type


class Move_logic() :
    def __init__(self) :
        pass
    
    def white_black_detect (chess_class) :
        if chess_class.islower() :
            return -1
        elif chess_class.isupper() :
            return 1
        else :
            return 0
        
    def chess_choose(game, select_place) :
        
        def is_position_meaningful(x, y) :
            if x<0 or x>7 :
                return 0
            if y<0 or y>7:
                return 0
            return 1
        
        x, y = select_place
        chess_class = game.board[x][y]
        game.can_move_place[x][y] = '!'
        
        base = 0
        
        if Move_logic.white_black_detect(chess_class) == -1 :
            base = -1
            
            if chess_class == 'p' :
                if is_position_meaningful(x, y+base) and game.board[x][y+base] == '' :
                    game.can_move_place[x][y+base] = '*'
                    if y == 6 :
                        if is_position_meaningful(x, y+base*2) and game.board[x][y+base*2] == '' :
                            game.can_move_place[x][y+base*2]= '*'
                if is_position_meaningful(x-base, y+base) and Move_logic.white_black_detect(game.board[x-base][y+base]) == -base:
                    game.can_move_place[x-base][y+base] = '*'
                if is_position_meaningful(x+base, y+base) and Move_logic.white_black_detect(game.board[x+base][y+base]) == -base:
                    game.can_move_place[x+base][y+base] = '*'
                
                    
            if chess_class == 'r' :
                
                for direction in range(4) :
                    x_change = 0
                    y_change = 0
                    
                    if direction == 0 :
                        x_change = 0
                        y_change = -1
                    if direction == 1 :
                        x_change = 1
                        y_change = 0
                    if direction == 2 :
                        x_change = 0
                        y_change = 1
                    if direction == 3 :
                        x_change = -1
                        y_change = 0
                    distance = 1
                    while is_position_meaningful(x+x_change*distance, y+y_change*distance) :
                        x_det = x+x_change*distance
                        y_det = y+y_change*distance
                        if game.board[x_det][y_det] == '' or Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                            game.can_move_place[x_det][y_det] = '*'
                            if Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                                break
                        elif Move_logic.white_black_detect(game.board[x_det][y_det]) == base :
                            break
                        distance += 1
                        
            if chess_class == 'n' :
                for direction in range(8) :
                    x_change = 0
                    y_change = 0
                    
                    if direction == 0 :
                        x_change = 1
                        y_change = -2
                    if direction == 1 :
                        x_change = 2
                        y_change = -1
                    if direction == 2 :
                        x_change = 2
                        y_change = 1
                    if direction == 3 :
                        x_change = 1
                        y_change = 2
                    if direction == 4 :
                        x_change = -1
                        y_change = 2
                    if direction == 5 :
                        x_change = -2
                        y_change = 1
                    if direction == 6 :
                        x_change = -2
                        y_change = -1
                    if direction == 7 :
                        x_change = -1
                        y_change = -2
                    
                    if is_position_meaningful(x+x_change, y+y_change) :
                        if game.board[x+x_change][y+y_change] == '' or Move_logic.white_black_detect(game.board[x+x_change][y+y_change]) == -base :
                            game.can_move_place[x+x_change][y+y_change] = '*'
                            
            if chess_class == 'b' :
                
                for direction in range(4) :
                    x_change = 0
                    y_change = 0
                    
                    if direction == 0 :
                        x_change = 1
                        y_change = 1
                    if direction == 1 :
                        x_change = 1
                        y_change = -1
                    if direction == 2 :
                        x_change = -1
                        y_change = 1
                    if direction == 3 :
                        x_change = -1
                        y_change = -1
                    distance = 1
                    while is_position_meaningful(x+x_change*distance, y+y_change*distance) :
                        x_det = x+x_change*distance
                        y_det = y+y_change*distance
                        if game.board[x_det][y_det] == '' or Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                            game.can_move_place[x_det][y_det] = '*'
                            if Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                                break
                        elif Move_logic.white_black_detect(game.board[x_det][y_det]) == base :
                            break
                        distance += 1
                        
            if  chess_class == 'q' :
                for direction in range(8) :
                    x_change = 0
                    y_change = 0
                    
                    if direction == 0 :
                        x_change = 1
                        y_change = 1
                    if direction == 1 :
                        x_change = 1
                        y_change = -1
                    if direction == 2 :
                        x_change = -1
                        y_change = 1
                    if direction == 3 :
                        x_change = -1
                        y_change = -1
                    if direction == 4 :
                        x_change = 0
                        y_change = -1
                    if direction == 5 :
                        x_change = 1
                        y_change = 0
                    if direction == 6 :
                        x_change = 0
                        y_change = 1
                    if direction == 7 :
                        x_change = -1
                        y_change = 0    
                    
                    distance = 1
                    while is_position_meaningful(x+x_change*distance, y+y_change*distance) :
                        x_det = x+x_change*distance
                        y_det = y+y_change*distance
                        if game.board[x_det][y_det] == '' or Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                            game.can_move_place[x_det][y_det] = '*'
                            if Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                                break
                        elif Move_logic.white_black_detect(game.board[x_det][y_det]) == base :
                            break
                        distance += 1     
            if  chess_class == 'k' :
                if game.is_first_move_castle[0] and game.is_first_move_king[0] :
                    if game.board[5][7] == '' and game.board[6][7] == '' :
                        game.can_move_place[6][7] = '*'
                
                for direction in range(8) :
                    x_change = 0
                    y_change = 0
                    
                    if direction == 0 :
                        x_change = 1
                        y_change = 1
                    if direction == 1 :
                        x_change = 1
                        y_change = -1
                    if direction == 2 :
                        x_change = -1
                        y_change = 1
                    if direction == 3 :
                        x_change = -1
                        y_change = -1
                    if direction == 4 :
                        x_change = 0
                        y_change = -1
                    if direction == 5 :
                        x_change = 1
                        y_change = 0
                    if direction == 6 :
                        x_change = 0
                        y_change = 1
                    if direction == 7 :
                        x_change = -1
                        y_change = 0    
                    
                    
                    if is_position_meaningful(x+x_change, y+y_change) :
                        x_det = x+x_change
                        y_det = y+y_change
                        if game.board[x_det][y_det] == '' or Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                            game.can_move_place[x_det][y_det] = '*'
                            
                    
        if Move_logic.white_black_detect(chess_class) == 1 :
            base = 1
            
            if chess_class == 'P' :
                if is_position_meaningful(x, y+base) and game.board[x][y+base] == '' :
                    game.can_move_place[x][y+base] = '*'
                    if y == 1 :
                        if is_position_meaningful(x, y+base*2) and game.board[x][y+base*2] == '' :
                            game.can_move_place[x][y+base*2]= '*'
                if is_position_meaningful(x-base, y+base) and Move_logic.white_black_detect(game.board[x-base][y+base]) == -base:
                    game.can_move_place[x-base][y+base] = '*'
                if is_position_meaningful(x+base, y+base) and Move_logic.white_black_detect(game.board[x+base][y+base]) == -base:
                    game.can_move_place[x+base][y+base] = '*'
            if chess_class == 'R' :
                
                for direction in range(4) :
                    x_change = 0
                    y_change = 0
                    
                    if direction == 0 :
                        x_change = 0
                        y_change = -1
                    if direction == 1 :
                        x_change = 1
                        y_change = 0
                    if direction == 2 :
                        x_change = 0
                        y_change = 1
                    if direction == 3 :
                        x_change = -1
                        y_change = 0
                    distance = 1
                    while is_position_meaningful(x+x_change*distance, y+y_change*distance) :
                        x_det = x+x_change*distance
                        y_det = y+y_change*distance
                        if game.board[x_det][y_det] == '' or Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                            game.can_move_place[x_det][y_det] = '*'
                            if Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                                break
                        elif Move_logic.white_black_detect(game.board[x_det][y_det]) == base :
                            break
                        distance += 1
            if chess_class == 'N' :
                for direction in range(8) :
                    x_change = 0
                    y_change = 0
                    
                    if direction == 0 :
                        x_change = 1
                        y_change = -2
                    if direction == 1 :
                        x_change = 2
                        y_change = -1
                    if direction == 2 :
                        x_change = 2
                        y_change = 1
                    if direction == 3 :
                        x_change = 1
                        y_change = 2
                    if direction == 4 :
                        x_change = -1
                        y_change = 2
                    if direction == 5 :
                        x_change = -2
                        y_change = 1
                    if direction == 6 :
                        x_change = -2
                        y_change = -1
                    if direction == 7 :
                        x_change = -1
                        y_change = -2
                    
                    if is_position_meaningful(x+x_change, y+y_change) :
                        if game.board[x+x_change][y+y_change] == '' or Move_logic.white_black_detect(game.board[x+x_change][y+y_change]) == -base :
                            game.can_move_place[x+x_change][y+y_change] = '*'
            if chess_class == 'B' :
                
                for direction in range(4) :
                    x_change = 0
                    y_change = 0
                    
                    if direction == 0 :
                        x_change = 1
                        y_change = 1
                    if direction == 1 :
                        x_change = 1
                        y_change = -1
                    if direction == 2 :
                        x_change = -1
                        y_change = 1
                    if direction == 3 :
                        x_change = -1
                        y_change = -1
                    distance = 1
                    while is_position_meaningful(x+x_change*distance, y+y_change*distance) :
                        x_det = x+x_change*distance
                        y_det = y+y_change*distance
                        if game.board[x_det][y_det] == '' or Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                            game.can_move_place[x_det][y_det] = '*'
                            if Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                                break
                        elif Move_logic.white_black_detect(game.board[x_det][y_det]) == base :
                            break
                        distance += 1
                        
            if  chess_class == 'Q' :
                for direction in range(8) :
                    x_change = 0
                    y_change = 0
                    
                    if direction == 0 :
                        x_change = 1
                        y_change = 1
                    if direction == 1 :
                        x_change = 1
                        y_change = -1
                    if direction == 2 :
                        x_change = -1
                        y_change = 1
                    if direction == 3 :
                        x_change = -1
                        y_change = -1
                    if direction == 4 :
                        x_change = 0
                        y_change = -1
                    if direction == 5 :
                        x_change = 1
                        y_change = 0
                    if direction == 6 :
                        x_change = 0
                        y_change = 1
                    if direction == 7 :
                        x_change = -1
                        y_change = 0    
                    
                    distance = 1
                    while is_position_meaningful(x+x_change*distance, y+y_change*distance) :
                        x_det = x+x_change*distance
                        y_det = y+y_change*distance
                        if game.board[x_det][y_det] == '' or Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                            game.can_move_place[x_det][y_det] = '*'
                            if Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                                break
                        elif Move_logic.white_black_detect(game.board[x_det][y_det]) == base :
                            break
                        distance += 1
            if  chess_class == 'K' :
                if game.is_first_move_castle[1] and game.is_first_move_king[1] :
                    if game.board[5][0] == '' and game.board[6][0] == ''  :
                        game.can_move_place[6][0] = '*'
                
                for direction in range(8) :
                    x_change = 0
                    y_change = 0
                    
                    if direction == 0 :
                        x_change = 1
                        y_change = 1
                    if direction == 1 :
                        x_change = 1
                        y_change = -1
                    if direction == 2 :
                        x_change = -1
                        y_change = 1
                    if direction == 3 :
                        x_change = -1
                        y_change = -1
                    if direction == 4 :
                        x_change = 0
                        y_change = -1
                    if direction == 5 :
                        x_change = 1
                        y_change = 0
                    if direction == 6 :
                        x_change = 0
                        y_change = 1
                    if direction == 7 :
                        x_change = -1
                        y_change = 0    
                    
                    
                    if is_position_meaningful(x+x_change, y+y_change) :
                        x_det = x+x_change
                        y_det = y+y_change
                        if game.board[x_det][y_det] == '' or Move_logic.white_black_detect(game.board[x_det][y_det]) == -base :
                            game.can_move_place[x_det][y_det] = '*'
                            
        return game