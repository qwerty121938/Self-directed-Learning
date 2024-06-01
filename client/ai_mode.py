import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from move_logic import Move_logic
from chess_module import Process
from chess_module import debug_print_array
from ai_module import AI
from datatype import Game_type
from image import Open_file
import random
import copy

class AI_mode():
    def __init__(self):
        self.player_color = 0
        
    def array_clear(self, array):
        for i in range(8):
            for j in range(8):
                array[i][j] = ''
                
    def ai_mode_setting(self):
        
        def start(temp):
            if temp == 2:
               temp = random.randint(0, 1) 
               
            self.setting.destroy()
            self.ai_mode_init()
            
            
            if temp == 1:
                self.player_color = 1
                
            elif temp == 0:
                self.player_color = -1
                
            self.ai_move()
            
        
        #把新創的畫布綁定在主畫布
        self.setting = tk.Canvas(self, width=500, height=300, bg="#161823")
        self.canvas.create_window(400, 580, window=self.setting)
        
        #按鈕
        button_w = tk.Button(self, text="white (first)", font=("Arial", 20), bg="#161823", fg="white", command=lambda: start(0),
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="white", bd=0,
                                            cursor="hand2", padx=10, pady=10, state="normal", takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        button_w.bind("<Enter>", lambda event: self.on_enter(button_w, event))
        button_w.bind("<Leave>", lambda event: self.on_leave(button_w, event))
        self.setting.create_window(250, 70, window=button_w)
        
        #按鈕
        button_b = tk.Button(self, text="black (after)", font=("Arial", 20), bg="#161823", fg="white", command=lambda: start(1),
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="white", bd=0,
                                            cursor="hand2", padx=10, pady=10, state="normal", takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        button_b.bind("<Enter>", lambda event: self.on_enter(button_b, event))
        button_b.bind("<Leave>", lambda event: self.on_leave(button_b, event))
        self.setting.create_window(250, 150, window=button_b)            
        
        #按鈕
        button_r = tk.Button(self, text="random", font=("Arial", 20), bg="#161823", fg="white", command=lambda: start(2),
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="white", bd=0,
                                            cursor="hand2", padx=10, pady=10, state="normal", takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        button_r.bind("<Enter>", lambda event: self.on_enter(button_r, event))
        button_r.bind("<Leave>", lambda event: self.on_leave(button_r, event))
        self.setting.create_window(250, 230, window=button_r)  
    
        
    def ai_mode_init(self):
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
        self.reset_button = tk.Button(self, text="reset", font=("Arial", 20), bg="#161823", fg="white", command=lambda: self.reset_screen(),
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="#161823", bd=0,
                                            cursor="hand2", padx=10, pady=10, takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        self.reset_button.bind("<Enter>", lambda event: self.on_enter(self.reset_button, event))
        self.reset_button.bind("<Leave>", lambda event: self.on_leave(self.reset_button, event))
        self.reset_button_id = self.canvas.create_window(990, 400, window=self.reset_button)
        
        self.back_button = tk.Button(self, text="back", font=("Arial", 20), bg="#161823", fg="white", command=lambda: self.back_move(),
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
        self.canvas.bind("<Button-1>", self.click_screen)
        
        self.game.initial()
        
        #返回按鍵初始化
        temp = copy.deepcopy(self.game)
        self.temp_game.append(temp)
        self.temp_game_index = 0
        
        self.refresh_screen()
        
          
    
    def refresh_screen(self):
        def swap(a, b):
            return b, a
        
        def turn_arr(arr1, arr2, arr3):
            for x in range(8):
                for y in range(4):
                    arr1[x][y], arr1[7-x][7-y] = swap(arr1[x][y], arr1[7-x][7-y])
                    arr2[x][y], arr2[7-x][7-y] = swap(arr2[x][y], arr2[7-x][7-y])
                    arr3[x][y], arr3[7-x][7-y] = swap(arr3[x][y], arr3[7-x][7-y])
        #是否合法選擇
        for i in range(8):
            for j in range(8):
                move_selection = self.game.can_move_place[i][j]
                if move_selection == '*':                
                    if  not Process.is_legal_move(self.game, self.select_place, (i,j)):
                        self.game.can_move_place[i][j]=''            
        
        if self.player_color == 1 :
            turn_arr(self.game.board, self.game.can_move_place, self.game.last_move_place)
        
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
                    picture = picture.resize((100, 100))
                    picture = ImageTk.PhotoImage(picture)
                    self.temp_pictures.insert(self.temp_pictures_index, picture)
                    self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                      
                if chess_class != '':
                    
                    if self.game.is_checkmate :
                        if (chess_class == 'k' and self.game.player_turn == -1) or (chess_class == 'K' and self.game.player_turn == 1) :
                            
                            self.temp_pictures_index +=1                            
                            picture = Image.open(self.image_open("checkmate"))
                            picture = picture.resize((100,100))
                            picture = ImageTk.PhotoImage(picture)
                            self.temp_pictures.insert(self.temp_pictures_index, picture)
                            self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                    
                    if chess_class.islower():#白方
                        
                        self.temp_pictures_index +=1
                        picture = Image.open(self.chess_image_open(chess_class, -1))
                        picture = picture.resize((90,90))
                        picture = ImageTk.PhotoImage(picture)
                        self.temp_pictures.insert(self.temp_pictures_index, picture)
                        self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                        
                    elif chess_class.isupper():#黑方
                        
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
                if move_selection == '*':
                    if chess_class.isalpha() :
                        self.temp_pictures_index +=1
                        picture = Image.open(self.image_open("can_move_chess"))
                        picture = picture.resize((100,100))
                        picture = ImageTk.PhotoImage(picture)
                        self.temp_pictures.insert(self.temp_pictures_index, picture)
                        self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                        
                    elif chess_class == '':
                        self.temp_pictures_index +=1
                        picture = Image.open(self.image_open("can_move_place"))
                        picture = picture.resize((100,100))
                        picture = ImageTk.PhotoImage(picture)
                        self.temp_pictures.insert(self.temp_pictures_index, picture)
                        self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                        
                elif move_selection == '!' :
                    self.temp_pictures_index +=1
                    picture = Image.open(self.image_open("select_chess"))
                    picture = picture.resize((100,100))
                    picture = ImageTk.PhotoImage(picture)
                    self.temp_pictures.insert(self.temp_pictures_index, picture)
                    self.canvas.create_image(x, y, image=self.temp_pictures[self.temp_pictures_index])
                    
        if self.player_color == 1 :
            turn_arr(self.game.board, self.game.can_move_place, self.game.last_move_place)
        
        #print(AI.evolution(self.game.board))
        
        
    def reset_screen(self):
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
        self.refresh_screen()
        
    def back_move(self):
        if self.temp_game_index == 0 :
            return
        
        self.select_place = None
        self.temp_game.pop(self.temp_game_index)
        self.temp_game_index -=1
        
        self.game = copy.deepcopy(self.temp_game[self.temp_game_index])
        
        
        self.array_clear(self.game.can_move_place)
        self.refresh_screen()     
        
        if self.game.player_turn != self.player_color :
            self.ai_move()
        
        
    def ai_move(self):
        if self.game.player_turn == self.player_color :
            return
        #ai move
        text = self.canvas.create_text(990, 150, text="AI is thinking", fill="white", font=("Arial", 20))
        
        start_pos, end_pos = AI.random_move(self.game)
        
        self.game = Process.moving(self.game, start_pos, end_pos)
    
        self.array_clear(self.game.can_move_place)
        
        self.canvas.delete(text)
        
        self.refresh_screen()
    
        
    def click_screen(self, event):
        if self.game.player_turn != self.player_color :
            return
        
        
        def clean_board () :
            self.array_clear(self.game.can_move_place)    
            self.refresh_screen()
        
        
            
        x = event.x // 100
        y = event.y // 100
        
        if x<0 or x>7 :
            return
        
        if y<0 or y>7 :
            return 
        
        if self.game.stop_game == 1:
            return
        
        if self.player_color == 1:
            x = 7-x
            y = 7-y
            
            
        
        if self.game.can_move_place[int(x)][int(y)] == '*' :
            
            self.game = Process.moving(self.game, self.select_place, (x, y))
        
            self.array_clear(self.game.can_move_place)
            
            self.temp_game_index +=1
            temp = copy.deepcopy(self.game)
            self.temp_game.append(temp)
            
            self.refresh_screen()
            
            self.ai_move()
            
            
            
        elif self.game.board[x][y].isalpha() :
            
            if Move_logic.white_black_detect(self.game.board[x][y]) == self.game.player_turn:
                self.array_clear(self.game.can_move_place) 
                self.select_place = (x, y)
                Move_logic.chess_choose(self.game, self.select_place)
                
                self.refresh_screen()
            
            else :
                clean_board()
            
        elif self.game.board[x][y] == '':
            clean_board() 