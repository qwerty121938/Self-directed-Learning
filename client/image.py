class Open_file():
    def __init__(self):
        pass
    def image_open (self, file_name) :
            return f"./picture/{file_name}.png"
            
    def chess_image_open (self, file_name, chess_class) :
        if chess_class == 1:
            return f"./picture/{file_name}_b.png"
        elif chess_class == -1:
            return f"./picture/{file_name}.png"
        
    def chess_unicode (self, chess_class):
        if chess_class == 'k' :
            return "♔"
        elif chess_class == 'q' :
            return "♕"
        elif chess_class == 'r' :
            return "♖"
        elif chess_class == 'n' :
            return "♘"
        elif chess_class == 'b' :
            return "♗"
        elif chess_class == 'p' :
            return "♙"
        
        
        elif chess_class == 'K' :
            return "♚"
        elif chess_class == 'Q' :
            return "♛"
        elif chess_class == 'R' :
            return "♜"
        elif chess_class == 'N' :
            return "♞"
        elif chess_class == 'B' :
            return "♝"
        elif chess_class == 'P' :
            return "♟"