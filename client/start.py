import tkinter as tk
import os
from tkinter import PhotoImage
from PIL import Image, ImageTk
from two_player_mode import Two_player_mode
from online_match import Online_match
from ai_mode import AI_mode
from image import Open_file

import copy

condition = ["reset"]

class Start_game(Two_player_mode, Online_match, AI_mode, Open_file, tk.Tk):
    def __init__(self, condition):
        tk.Tk.__init__(self)
        self.title("Chess Game")
        self.condition = condition
        self.condition[0] = "close"
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        #儲存螢幕上的圖片
        self.temp_pictures = []
        self.temp_pictures_index = -1
        
        self.initial_interface()
    
    def on_closing(self):
        try:
            self.client.socket.close()
        except:
            pass    
        finally:
            # 在关闭窗口时关闭终端
            os.system("taskkill /f /im cmd.exe")  # Windows系统
            # os.system("kill -9 $$")  # 类Unix系统
            self.destroy()
    
    def on_enter(self, button, event):
        button.config(fg="yellow")

    def on_leave(self, button, event):
        button.config(fg="white")
        
    def leave_game(self):
        self.condition[0] = "reset"
        self.destroy()
        
    def initial_interface(self):
        def two_player_chess():
            Two_player_mode.__init__(self)
            self.two_player_chess_init()
            
        def online_match():
            Online_match.__init__(self)
            self.online_match()
            
        def ai_mode():
            AI_mode.__init__(self)
            self.ai_mode_setting()
        
        
        #屏幕初始化
        self.width = 800
        self.heigh = 800
        screen_width = 960 - self.width/2
        screen_heigh = 540 - self.heigh/2
        self.geometry(f"{self.width}x{self.heigh}+{int(screen_width)}+{int(screen_heigh)}")
        self.resizable(False, False)
        self.configure(bg='#161823')
        
        #畫布創建
        self.canvas = tk.Canvas(self, width=self.width, height=self.heigh, bg="#161823")
        self.canvas.config(highlightthickness=0)
        self.canvas.pack()
        
        
        #選擇遊戲的按鈕
        button_t = tk.Button(self, text="Two Player Mode", font=("Arial", 20), bg="#161823", fg="white", command=two_player_chess,
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="white", bd=0,
                                            cursor="hand2", padx=10, pady=10, state="normal", takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        button_t.bind("<Enter>", lambda event: self.on_enter(button_t, event))
        button_t.bind("<Leave>", lambda event: self.on_leave(button_t, event))
        self.canvas.create_window(400, 480, window=button_t)
        
        
        #選擇遊戲的按鈕
        button_o = tk.Button(self, text="Online Match", font=("Arial", 20), bg="#161823", fg="white", command=online_match,
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="white", bd=0,
                                            cursor="hand2", padx=10, pady=10, state="normal", takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        button_o.bind("<Enter>", lambda event: self.on_enter(button_o, event))
        button_o.bind("<Leave>", lambda event: self.on_leave(button_o, event))
        self.canvas.create_window(400, 580, window=button_o)
        
        
        #選擇遊戲的按鈕
        button_a = tk.Button(self, text="AI Mode", font=("Arial", 20), bg="#161823", fg="white", command=ai_mode,
                                            highlightthickness=0, relief="flat", activebackground="#161823", activeforeground="white", bd=0,
                                            cursor="hand2", padx=10, pady=10, state="normal", takefocus=True, wraplength=0, justify="center", 
                                            anchor="center", compound="center")
        button_a.bind("<Enter>", lambda event: self.on_enter(button_a, event))
        button_a.bind("<Leave>", lambda event: self.on_leave(button_a, event))
        self.canvas.create_window(400, 680, window=button_a)
        
        
        #選擇遊戲的按鈕
        self.temp_pictures_index +=1
        picture = Image.open(self.image_open("start_game"))
        picture = picture.resize((300, 300))
        picture = ImageTk.PhotoImage(picture)
        self.temp_pictures.insert(self.temp_pictures_index, picture)
        self.canvas.create_image(400, 180, image=self.temp_pictures[self.temp_pictures_index])
        
        
        
        
        
        
if __name__ == "__main__":
    while True:
        if condition[0] == "reset":
            game = Start_game(condition)
            game.mainloop()
        elif condition[0] == "close":
            break