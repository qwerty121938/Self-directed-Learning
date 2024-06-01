import tkinter as tk
from PIL import Image, ImageTk
from move_logic import Move_logic
from chess_module import Process
from chess_module import debug_print_array
from datatype import Game_type
from datatype import Client_type
from datatype import Message
from image import Open_file
import socket
import copy
import multiprocessing as mp
import threading as td
import time
import pickle




def server_message_reception_job(client):
    client.socket.settimeout(5.0)
    while True:
        try:
            message = client.socket.recv(4096)
            client.data_list.append(pickle.loads(message))
            
            #print(f"接收到伺服器的訊息:",client.data_list[-1].message_type)
            
            
        except TimeoutError:
            continue
        
        except:
            break
        
    client.socket.close()
    print(f"連練錯誤與伺服器中斷連線")
    
    mission = Message()
    mission.message_type = "exit"
    client.mission_list.append(mission)
    
    
    
def server_send_message_job(client):
    while True:
        try:
            if len(client.mission_list) > 0:
                message = client.mission_list.pop(0)
                client.socket.sendall(pickle.dumps(message))
                #print(f"傳送訊係給{client.server_ip}:",message.message_type)
            time.sleep(0.2)
        except:
            break
            
    

def main_process(client, root):
    
    while True:
        
        if len(client.data_list) > 0:
            message = client.data_list.pop(0)
            message_type = message.message_type
            
            if message_type == "connection_confirmation":
                message = Message()
                message.message_type = "connection_confirmation"
                client.mission_list.append(message)

            elif message_type == "Wait_for_another_player":
                root.waiting()
            
            elif message_type == "game_start":
                root.game = message.message_content[0]
                root.player_color = message.message_content[1]
                root.online_match_init()
                
            elif message_type == "refresh_screen":
                
                root.game = message.message_content[0]
                root.client_draw_board()
                
            elif message_type == "exit":
                root.wait.destroy()
                root.connect_error()
                                
            else:
                pass
            
        time.sleep(0.1)
                    
                

    
    
class Online_match():
    def __init__(self):
        super().__init__()
        self.player_color = 0
        self.client = Client_type()
        
    def online_match(self):
        
        def get_entry_content(entry):
            self.client.server_ip = entry.get()# 获取输入框的内容
            back()
            self.online_match_setting()
            
        def back():
            self.setting.destroy()   
        
        #把新創的畫布綁定在主畫布
        self.setting = tk.Canvas(self, width=500, height=300, bg="#161823")
        self.canvas.create_window(400, 580, window=self.setting)
        
        #按鈕
        button_b = tk.Button(self, text="<- back", font=("Arial", 20), bg="#161823", fg="white", command=back,
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="white", bd=0,
                                            cursor="hand2", padx=10, pady=10, state="normal", takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        button_b.bind("<Enter>", lambda event: self.on_enter(button_b, event))
        button_b.bind("<Leave>", lambda event: self.on_leave(button_b, event))
        self.setting.create_window(70, 40, window=button_b)
        
        #按鈕
        button_c = tk.Button(self, text="confirm", font=("Arial", 20), bg="#161823", fg="white", command=lambda: get_entry_content(entry),
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="white", bd=0,
                                            cursor="hand2", padx=10, pady=10, state="normal", takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        button_c.bind("<Enter>", lambda event: self.on_enter(button_c, event))
        button_c.bind("<Leave>", lambda event: self.on_leave(button_c, event))
        self.setting.create_window(250, 230, window=button_c)
        
        #文字
        self.setting.create_text(250, 90, text="Please Enter Server IP", fill="white", font=("Arial", 20))
        
        #輸入框
        entry = tk.Entry(self, font=("Arial", 15))
        self.setting.create_window(250, 150, window=entry, width="260", height="30")
        
    def connect_error(self):
        def back():
            self.warn.destroy() 
            
        #把新創的畫布綁定在主畫布
        self.warn = tk.Canvas(self, width=500, height=300, bg="#161823")
        self.canvas.create_window(400, 580, window=self.warn) 
        
        #按鈕
        button_c = tk.Button(self, text="confirm", font=("Arial", 20), bg="#161823", fg="white", command=back,
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="white", bd=0,
                                            cursor="hand2", padx=10, pady=10, state="normal", takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        button_c.bind("<Enter>", lambda event: self.on_enter(button_c, event))
        button_c.bind("<Leave>", lambda event: self.on_leave(button_c, event))
        self.warn.create_window(250, 230, window=button_c)
        
        #文字
        self.warn.create_text(250, 90, text="Connect Error", fill="white", font=("Arial", 20))
        
    
        
    def online_match_setting(self):
        
        # 建立一個 IPv4 TCP Socket
        self.client.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # 嘗試連接到伺服器
        try:
            self.client.socket.connect((self.client.server_ip, self.client.server_port))
            print("成功連接到伺服器")
            
            # 發送資料給伺服器
            message = Message()
            message.message_type = "Hello, Server!"
            self.client.mission_list.append(message)
            
            
            thread = td.Thread(target=server_message_reception_job, args=(self.client, ))
            thread.start()
            
            thread = td.Thread(target=server_send_message_job, args=(self.client, ))
            thread.start()
            
            thread = td.Thread(target=main_process, args=(self.client, self, ))
            thread.start()

        except:
            print("無法連接到伺服器。請確保伺服器正在運行，並檢查 IP 位址和埠號是否正確。")
            self.connect_error()
    
    
    
                    
    def waiting(self):
        #把新創的畫布綁定在主畫布
        self.wait = tk.Canvas(self, width=500, height=300, bg="#161823")
        self.canvas.create_window(400, 580, window=self.wait)
        #文字
        self.wait.create_text(250, 90, text="Wait For Another Player Join", fill="white", font=("Arial", 20))
        
    def array_clear(self, array):
        for i in range(8):
            for j in range(8):
                array[i][j] = ''
        
        
    def online_match_init(self):
        #屏幕初始化
       
        self.width = 1200
        self.heigh = 800
        screen_width = 960 - self.width/2
        screen_heigh = 540 - self.heigh/2
        self.geometry(f"{self.width}x{self.heigh}+{int(screen_width)}+{int(screen_heigh)}")     
             
             
        #畫布創建
        self.canvas.delete("all")
        self.canvas.config(width=self.width, height=self.heigh, bg="#161823")
        self.canvas.config(highlightthickness=0)
        self.canvas.pack()
        
        
        #螢幕點擊觸發事件
        self.canvas.bind("<Button-1>", self.client_on_click)
        
        
        self.client_draw_board()
        
        
    
    def client_draw_board(self):
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
                self.client.socket.close()
                self.online_match_setting()
            
            print_text = ''
            
            if self.game.is_checkmate == 0:
                print_text = "stalemate"
            elif self.game.player_turn != self.player_color:
                print_text = "you win"
            elif self.game.player_turn == self.player_color:
                print_text = "you lose"
                
            #把新創的畫布綁定在主畫布
            self.print_winner = tk.Canvas(self, width=500, height=300, bg="#161823")
            self.canvas.create_window(600, 400, window=self.print_winner)
            
            
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
        
    def client_on_click(self, event):
        
        
        if self.game.player_turn != self.player_color :
            return
        
        def clean_board () :
            self.array_clear(self.game.can_move_place)    
            self.client_draw_board()
            
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
            
            message = Message()
            message.message_type = 'move'
            
            message.message_content.extend([(self.select_place), (x, y)])
            self.client.mission_list.append(message)
            
            self.array_clear(self.game.can_move_place)
            
            
            self.client_draw_board()
            
            
        elif self.game.board[x][y].isalpha() :
            
            if Move_logic.white_black_detect(self.game.board[x][y]) == self.game.player_turn:
                self.array_clear(self.game.can_move_place) 
                self.select_place = (x, y)
                Move_logic.chess_choose(self.game, self.select_place)
                
                self.client_draw_board()
            
            else :
                clean_board()
            
        elif self.game.board[x][y] == '':
            clean_board()        
                
                
        