import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from chess_module import Process
from chess_module import debug_print_array
from move_logic import Move_logic
from datatype import Game_type
from image import Open_file
import copy

class Two_player_mode():
    def __init__(self):
        pass
        
    def array_clear(self, array):
        for i in range(8):
            for j in range(8):
                array[i][j] = ''
        
    def two_player_chess_init(self):
        #屏幕初始化
        self.width = 1200
        self.heigh = 800
        screen_width = 960 - self.width/2
        screen_heigh = 540 - self.heigh/2
        self.geometry(f"{self.width}x{self.heigh}+{int(screen_width)}+{int(screen_heigh)}")
        
        
        
        #變數
        
        self.temp_game = []
        self.game = Game_type()
        self.game.initial()
        
        self.select_place = None
        
        #畫布創建
        self.canvas.delete("all")
        self.canvas.config(width=self.width, height=self.heigh, bg="#161823")
        self.canvas.config(highlightthickness=0)
        self.canvas.pack()
        
        
        # 建立按鈕，設定點擊時的呼叫函式
        self.reset_button = tk.Button(self, text="reset", font=("Arial", 20), bg="#161823", fg="white", command=self.button_click,
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="#161823", bd=0,
                                            cursor="hand2", padx=10, pady=10, takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        self.reset_button.bind("<Enter>", lambda event: self.on_enter(self.reset_button, event))
        self.reset_button.bind("<Leave>", lambda event: self.on_leave(self.reset_button, event))
        self.reset_button_id = self.canvas.create_window(990, 400, window=self.reset_button)
        
        self.back_button = tk.Button(self, text="back", font=("Arial", 20), bg="#161823", fg="white", command=self.return_game,
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="#161823", bd=0,
                                            cursor="hand2", padx=10, pady=10, takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        self.back_button.bind("<Enter>", lambda event: self.on_enter(self.back_button, event))
        self.back_button.bind("<Leave>", lambda event: self.on_leave(self.back_button, event))
        self.back_button_id = self.canvas.create_window(990, 300, window=self.back_button)
        
        self.leave_t_button = tk.Button(self, text="leave game", font=("Arial", 10), bg="#161823", fg="white", command=lambda: self.leave_game(),
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="#161823", bd=0,
                                            cursor="hand2", padx=10, pady=10, takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        self.leave_t_button.bind("<Enter>", lambda event: self.on_enter(self.leave_t_button, event))
        self.leave_t_button.bind("<Leave>", lambda event: self.on_leave(self.leave_t_button, event))
        self.leave_t_button_id = self.canvas.create_window(1140, 30, window=self.leave_t_button)
        
        
        #螢幕點擊觸發事件
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.game.initial()
        
        #返回按鍵初始化
        temp = copy.deepcopy(self.game)
        self.temp_game.append(temp)
        self.temp_game_index = 0
        
        self.draw_board()
        
          
    
    def draw_board(self):
        #是否合法選擇
        for i in range(8):
            for j in range(8):
                move_selection = self.game.can_move_place[i][j]
                if move_selection == '*':                
                    if  not Process.is_legal_move(self.game, self.select_place, (i,j)):
                        self.game.can_move_place[i][j]=''
        
        #屏幕初始化
        self.canvas.delete("image")
        self.temp_pictures.clear()
        self.temp_pictures_index = -1
        #棋盤
        self.temp_pictures_index +=1
        picture = Image.open(self.image_open("chess_board"))
        picture = picture.resize((800,800))
        picture = ImageTk.PhotoImage(picture)
        self.temp_pictures.insert(self.temp_pictures_index, picture)
        self.canvas.create_image(400, 400, image=self.temp_pictures[self.temp_pictures_index])
        
        
        #顯示贏家
        if self.game.stop_game :
            def confirm():
                self.print_winner.destroy()
                self.button_click()
                self.two_player_chess_init()
            
            print_text = ''
            
            if self.game.is_checkmate == 0:
                print_text = "stalemate"
            elif self.game.player_turn == 1:
                print_text = "white win"
            elif self.game.player_turn == -1:
                print_text = "black win"
                
            #把新創的畫布綁定在主畫布
            self.print_winner = tk.Canvas(self, width=500, height=300, bg="#161823")
            self.canvas.create_window(600, 400, window=self.print_winner)
            self.canvas.delete(self.reset_button_id)
            self.canvas.delete(self.back_button_id)
            self.canvas.delete(self.leave_t_button_id)
            
            #按鈕
            button_c = tk.Button(self, text="confirm", font=("Arial", 20), bg="#161823", fg="white", command=confirm,
                                                highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="white", bd=0,
                                                cursor="hand2", padx=10, pady=10, state="normal", takefocus=True, wraplength=0, justify="center", 
                                                anchor="center", compound="center")
            button_c.bind("<Enter>", lambda event: self.on_enter(button_c, event))
            button_c.bind("<Leave>", lambda event: self.on_leave(button_c, event))
            self.print_winner_id = self.print_winner.create_window(250, 265, window=button_c)
            
            #文字
            self.print_winner.create_text(250, 150, text=f"{print_text}", fill="white", font=("Arial", 20))
            
            self.canvas.create_text(990, 400, text="reset", fill="white", font=("Arial", 20))
            self.canvas.create_text(990, 300, text="back", fill="white", font=("Arial", 20))
            self.canvas.create_text(1140, 30, text="leave game", fill="white", font=("Arial", 10))
            
        else:
            pass

        
        #棋子
        for i in range(8):
            for j in range(8):
                chess_class = self.game.board[i][j]
                last_move_place = self.game.last_move_place[i][j]
                
                x = i*100+50
                y = j*100+50
                
                if last_move_place != '':
                    
                    self.temp_pictures_index +=1
                    picture = Image.open(self.image_open("last_move"))
                    picture = picture.resize((98, 98))
                    picture = ImageTk.PhotoImage(picture)
                    self.temp_pictures.insert(self.temp_pictures_index, picture)
                    self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                      
                if chess_class != '':
                    
                    if self.game.is_checkmate :
                        if (chess_class == 'k' and self.game.player_turn == -1) or (chess_class == 'K' and self.game.player_turn == 1) :
                            # chess_class = self.chess_unicode(chess_class)
                            # self.canvas.create_text(i*100+50, j*100+50, text=chess_class, font=("Arial", 70), fill="red")
                            
                            self.temp_pictures_index +=1                            
                            picture = Image.open(self.image_open("checkmate"))
                            picture = picture.resize((100,100))
                            picture = ImageTk.PhotoImage(picture)
                            self.temp_pictures.insert(self.temp_pictures_index, picture)
                            self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                            
                    
                    if chess_class.islower():#白方
                        #chess_class = self.chess_unicode(chess_class)
                        #self.canvas.create_text(i*100+50, j*100+50, text=chess_class, font=("Arial", 70), fill="#FFEEDD")
                        
                        self.temp_pictures_index +=1
                        picture = Image.open(self.chess_image_open(chess_class, -1))
                        picture = picture.resize((90,90))
                        picture = ImageTk.PhotoImage(picture)
                        self.temp_pictures.insert(self.temp_pictures_index, picture)
                        self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                        
                    elif chess_class.isupper():#黑方
                        #chess_class = self.chess_unicode(chess_class)
                        #self.canvas.create_text(i*100+50, j*100+50, text=chess_class, font=("Arial", 70), fill="black")
                        
                        self.temp_pictures_index +=1
                        picture = Image.open(self.chess_image_open(chess_class, 1))
                        picture = picture.resize((80,80))
                        picture = ImageTk.PhotoImage(picture)
                        self.temp_pictures.insert(self.temp_pictures_index, picture)
                        self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                        
                        
        
                
                
        #棋子選擇
        for i in range(8):
            for j in range(8):
                move_selection = self.game.can_move_place[i][j]
                chess_class = self.game.board[i][j]
                x = i*100+50
                y = j*100+50
                radius = 8
                if move_selection == '*':
                    if chess_class.isalpha() :
                        #self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red")
                        
                        self.temp_pictures_index +=1
                        picture = Image.open(self.image_open("can_move_chess"))
                        picture = picture.resize((90,90))
                        picture = ImageTk.PhotoImage(picture)
                        self.temp_pictures.insert(self.temp_pictures_index, picture)
                        self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                        
                    elif chess_class == '':
                        #self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="yellow", outline="yellow")
                        
                        self.temp_pictures_index +=1
                        picture = Image.open(self.image_open("can_move_place"))
                        picture = picture.resize((100,100))
                        picture = ImageTk.PhotoImage(picture)
                        self.temp_pictures.insert(self.temp_pictures_index, picture)
                        self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                        
                elif move_selection == '!' :
                    
                    #chess_class = self.chess_unicode(chess_class)
                    #self.canvas.create_text(x, y, text=chess_class, font=("Arial", 70), fill="orange")
                    
                    self.temp_pictures_index +=1
                    picture = Image.open(self.image_open("select_chess"))
                    picture = picture.resize((100,100))
                    picture = ImageTk.PhotoImage(picture)
                    self.temp_pictures.insert(self.temp_pictures_index, picture)
                    self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
        
    def button_click(self):
        def initialize_all():
            self.select_place = None
            self.game.player_turn = -1
            self.game.is_checkmate = 0
            self.game.stop_game = 0
            self.game.is_first_move_king = [1,1]
            self.game.is_first_move_castle = [1,1]
            self.array_clear(self.game.can_move_place) 
            self.array_clear(self.game.board)
            self.array_clear(self.game.last_move_place) 
            self.temp_game.clear()
            
            
        initialize_all()
        
        self.game.initial()
        temp = copy.deepcopy(self.game)
        self.temp_game.append(temp)
        self.temp_game_index = 0
        self.draw_board()    
        
    def return_game(self):
        if self.temp_game_index == 0 :
            return
        
        self.select_place = None
        self.temp_game.pop(self.temp_game_index)
        self.temp_game_index -=1
        
        # print(self.temp_game_index)
        # print(id(self.game))
        # print(id(self.temp_game[self.temp_game_index]))
        
        self.game = copy.deepcopy(self.temp_game[self.temp_game_index])
        
        
        self.array_clear(self.game.can_move_place)
        self.draw_board()   
        
    def on_click(self, event):
        def clean_board () :
            self.array_clear(self.game.can_move_place)    
            self.draw_board()
            
        x = event.x // 100
        y = event.y // 100
        
        if x<0 or x>7 :
            return
        if y<0 or y>7 :
            return 
        if self.game.stop_game == 1:
            return
        
        if self.game.can_move_place[int(x)][int(y)] == '*' :
            
            self.game = Process.moving(self.game, self.select_place, (x, y))
            
            self.array_clear(self.game.can_move_place)
            
            self.temp_game_index +=1
            temp = copy.deepcopy(self.game)
            self.temp_game.append(temp)
            
            self.draw_board()
            
            
        elif self.game.board[x][y].isalpha() :
            
            if Move_logic.white_black_detect(self.game.board[x][y]) == self.game.player_turn:
                self.array_clear(self.game.can_move_place) 
                self.select_place = (x, y)
                self.game = Move_logic.chess_choose(self.game, self.select_place)
                
                self.draw_board()
            
            else :
                clean_board()
            
        elif self.game.board[x][y] == '':
            clean_board()
            
    
            
          

      
