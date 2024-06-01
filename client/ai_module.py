import numpy
import random
import copy
import multiprocessing as mp
import threading as td
from move_logic import Move_logic
from chess_module import Process
from datatype import Game_type
from datatype import advantage_position


class AI():
    @staticmethod
    def array_clear(array):
        for i in range(8):
            for j in range(8):
                array[i][j] = ''
                
                
    @staticmethod
    def min(game, depth, alpha, beta):            
        if game.stop_game == 1:
            return -1000000
        elif depth == 0:
            return AI.evaluation(game.board)
                    
        board = game.board
        depth -= 1
        score = 1000000
        
        for x in range(8):
            for y in range(8):
                if Move_logic.white_black_detect(board[x][y]) == game.player_turn:
                    Move_logic.chess_choose(game, (x, y))
                    for det_x in range(8):
                        for det_y in range(8):
                            if game.can_move_place[det_x][det_y] == '*':
                                if Process.is_legal_move(game, (x, y), (det_x, det_y)):
                                    original_game = copy.copy(game)
                                    Process.moving(game, (x, y), (det_x, det_y))
                                    
                                    score = min(score, AI.max(game, depth, alpha, beta))
                                    game = original_game
                                    
                                    if score <= alpha:
                                        return score
                                    beta = min(beta, score)
                    AI.array_clear(game.can_move_place)
                    
        return score            

    @staticmethod
    def max(game, depth, alpha, beta):            
        if game.stop_game == 1:
            return 1000000
        elif depth == 0:
            return AI.evaluation(game.board)
                    
        board = game.board
        depth -= 1
        score = -1000000
        
        for x in range(8):
            for y in range(8):
                if Move_logic.white_black_detect(board[x][y]) == game.player_turn:
                    Move_logic.chess_choose(game, (x, y))
                    for det_x in range(8):
                        for det_y in range(8):
                            if game.can_move_place[det_x][det_y] == '*':
                                if Process.is_legal_move(game, (x, y), (det_x, det_y)):
                                    original_game = copy.copy(game)
                                    Process.moving(game, (x, y), (det_x, det_y))
                                    
                                    score = max(score, AI.min(game, depth, alpha, beta))
                                    game = original_game
                                    
                                    if score >= beta:
                                        return score
                                    alpha = max(alpha, score)
                    AI.array_clear(game.can_move_place)
                    
        return score         

    @staticmethod
    def threading_job(queue, game, depth):
        score = AI.max(game, depth, -1000000, 1000000)
        queue.put(score)
        
    @staticmethod
    def multiprocessing_job(queue, game, depth, start_pos, end_pos):
        original_game = copy.copy(game)
        Process.moving(game, start_pos, end_pos)
                                    
        board = game.board
        depth -= 1
        threads = []
        thread_queue = mp.Queue()

        for x in range(8):
            for y in range(8):
                if Move_logic.white_black_detect(board[x][y]) == game.player_turn:
                    Move_logic.chess_choose(game, (x, y))
                    for det_x in range(8):
                        for det_y in range(8):
                            if game.can_move_place[det_x][det_y] == '*':
                                if Process.is_legal_move(game, (x, y), (det_x, det_y)):
                                    temp = copy.copy(game)
                                    Process.moving(temp, (x, y), (det_x, det_y))
                                    
                                    thread = td.Thread(target=AI.threading_job, args=(thread_queue, temp, depth,))
                                    thread.start()
                                    threads.append(thread)
                    AI.array_clear(game.can_move_place)
                    
        for thread in threads:
            thread.join()             

        scores = []
        while not thread_queue.empty():
            scores.append(thread_queue.get())
        
        arr = [start_pos, end_pos, min(scores)]
        queue.put(arr)
        
    @staticmethod
    def ai_move(game):
        mps = []
        game = copy.copy(game)
        board = game.board
        
        queue = mp.Queue()
        
        for x in range(8):
            for y in range(8):
                if Move_logic.white_black_detect(board[x][y]) == game.player_turn:
                    Move_logic.chess_choose(game, (x, y))
                    for det_x in range(8):
                        for det_y in range(8):
                            if game.can_move_place[det_x][det_y] == '*':
                                if Process.is_legal_move(game, (x, y), (det_x, det_y)):
                                    p = mp.Process(target=AI.multiprocessing_job, args=(queue, game, 3, (x, y), (det_x, det_y),))
                                    p.start()
                                    mps.append(p)
                    AI.array_clear(game.can_move_place)
        
        for p in mps:
            p.join()
        
        best_move = None
        best_score = -1000000
        
        while not queue.empty():
            move = queue.get()
            if move[2] > best_score:
                best_score = move[2]
                best_move = (move[0], move[1])
        
        return best_move

            
            
        
    
    def evaluation(board):
        total_score = 0
            
        for x in range(8):
            for y in range(8):
                chess_class = board[x][y]
                if chess_class == "":
                    continue
                elif Move_logic.white_black_detect(chess_class) == 1:#黑棋
                    
                    total_score += advantage_position.chess_values[chess_class]
                    
                    if chess_class == 'P':
                        total_score -= advantage_position.PAWN_TABLE[7-y][7-x]
                    elif chess_class == 'N':
                        total_score -= advantage_position.KNIGHT_TABLE[7-y][7-x]
                    elif chess_class == 'B':
                        total_score -= advantage_position.BISHOP_TABLE[7-y][7-x]
                    elif chess_class == 'R':
                        total_score -= advantage_position.ROOK_TABLE[7-y][7-x]
                    elif chess_class == 'Q':
                        total_score -= advantage_position.QUEEN_TABLE[7-y][7-x]
                
                elif Move_logic.white_black_detect(chess_class) == -1:#白棋
                    
                    total_score += advantage_position.chess_values[chess_class]
                    
                    if chess_class == 'p':
                        total_score += advantage_position.PAWN_TABLE[y][x]
                    elif chess_class == 'n':
                        total_score += advantage_position.KNIGHT_TABLE[y][x]
                    elif chess_class == 'b':
                        total_score += advantage_position.BISHOP_TABLE[y][x]
                    elif chess_class == 'r':
                        total_score += advantage_position.ROOK_TABLE[y][x]
                    elif chess_class == 'q':
                        total_score += advantage_position.QUEEN_TABLE[y][x]   
        
        return total_score 
                    
                    
    
    def random_move(game):
        
        
        game = copy.deepcopy(game)
        board = game.board
        
        start_pos = None
        end_pos = None
        
        
        total = 0
        
        for x in range(8):
            for y in range(8):
                if Move_logic.white_black_detect(board[x][y]) == game.player_turn:
                    Move_logic.chess_choose(game, (x, y))
                    for det_x in range(8):
                        for det_y in range(8):
                            if game.can_move_place[det_x][det_y] == '*':
                                if Process.is_legal_move(game, (x, y), (det_x, det_y)):
                                    total += 1
                    AI.array_clear(game.can_move_place)          
                    
                    
        if total == 0:
            return
        #print(total)
        rand = random.randint(100, 1000)    
        rand = rand % total
        
        for x in range(8):
            for y in range(8):
                if Move_logic.white_black_detect(board[x][y]) == game.player_turn:
                    Move_logic.chess_choose(game, (x, y))
                    for det_x in range(8):
                        for det_y in range(8):
                            if game.can_move_place[det_x][det_y] == '*':
                                if Process.is_legal_move(game, (x, y), (det_x, det_y)):
                                    rand -= 1
                                    #print(-1) 
                                    if rand < 0 and start_pos is None:
                                        start_pos = (x, y)
                                        end_pos = (det_x, det_y)
                                        #print("get_move")
                                        
                    AI.array_clear(game.can_move_place)               
        
        
        return start_pos, end_pos