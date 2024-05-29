import copy
import socket
import threading as td
import multiprocessing as mp
import time
import pickle
from datatype import Client_type
from datatype import Game_type
from datatype import Room
from datatype import Message
from chess_module import Process
import random

def client_mission_process_job(client):
    while True:
        if client.connect == 'disappear':
            break
        if len(client.data_list) > 0:
            message = client.data_list.pop(0)
            message_type = message.message_type
            if message_type == "connection_confirmation":
                pass
            elif message_type == "move":
                client.room.mission_list.append(message)
            else:
                pass
        
        

def client_send_message_job(client):
    while True:
        if client.connect == 'disappear':
            break
        try:
            if len(client.mission_list) > 0:
                message = client.mission_list.pop(0)
                client.client_socket.sendall(pickle.dumps(message))
                #print(f"傳送訊係給{client.client_address}:",message.message_type)
        except:
            pass
        
        time.sleep(0.1)

def is_client_still_connect_detect(client):
    
    while True:
        if client.connect == 'disappear':
            break
        now_time = time.time()
        if now_time - client.last_time_convey > 10:
            if now_time - client.last_time_convey > 30:
                client.connect = 'disappear'
                break
            
            message = Message()
            message.message_type = "connection_confirmation"
            client.mission_list.append(message)
            
        time.sleep(2)
        


def client_message_reception_job(clients, client):
    
    client.client_socket.settimeout(5.0)
    
    while True:
        if client.connect == 'disappear':
            break
        try:
            data = client.client_socket.recv(4096)
            client.last_time_convey = time.time()
            
            client.data_list.append(pickle.loads(data))
        
            ##print(f"接收到{client.client_address}的訊息:",client.data_list[-1].message_type)
        except TimeoutError:
            continue
        
        except:
            break
        
        time.sleep(0.2)
        
    client.room.players.remove(client)
    clients.remove(client)
    client.client_socket.close()    
    
    print(f"連練錯誤與客戶端{client.client_address}中斷連線")
    
    

def game_start_job(rooms, room):
    rand = random.randint(0, 1)
    if rand == 1:
        temp = room.players[0]
        room.players[0] = room.players[1]
        room.players[1] = temp

    white_player = room.players[0]
    black_player = room.players[1]    
    
    game = Game_type()
    game.initial()
    
    message = Message()
    message.message_type = "game_start"
    message.message_content.append(game)
    
    message_w = copy.deepcopy(message)
    message_b = copy.deepcopy(message)
    
    message_w.message_content.append(-1)
    message_b.message_content.append(1)
    
    white_player.mission_list.append(message_w)
    black_player.mission_list.append(message_b)
    
    
    
    while True:
        if len(room.players) == 2:
            
            if len(room.mission_list) > 0:
                
                mission = room.mission_list.pop(0)
                mission_type = mission.message_type
                
                if mission_type == "move":
                    temp_message = Message()
                    temp_message.message_type = "refresh_screen"
                    
                    
                    game = Process.moving(game, mission.message_content[0], mission.message_content[1])
                    temp_message.message_content.append(game)
                    
                    white_player.mission_list.append(temp_message)
                    black_player.mission_list.append(temp_message)
                else:
                    pass
            
            
            
        elif len(room.players) == 1:
            break
        else:
            break
    
        time.sleep(0.1)
    


def main():
    # 建立一個 IPv4 TCP Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取主机名
    hostname = socket.gethostname()

    # 根据主机名获取IP地址
    ip_address = socket.gethostbyname(hostname)

    # 綁定伺服器的 IP 位址和埠號
    server_ip = ip_address  # 你可以修改為你的 IP 位址
    server_port = 1080  # 你可以使用未被佔用的埠號
    server_socket.bind((server_ip, server_port))

    # 讓伺服器開始監聽連線
    server_socket.listen(10)  # 允許最多 10 個連線


    print(f"伺服器正在監聽 {server_ip}:{server_port}")
    
    clients = []
    threads = []
    rooms = []
    
    
    while True:
        # 接受客戶端的連線
        client = Client_type()
        
        client.client_socket, client.client_address = server_socket.accept()
        clients.append(client)
        
        print(f"與客戶端{client.client_address}建立連線")
        
        client.last_time_convey = time.time()
        
        
        # 分配房間
        temp_room = None
        for room in rooms:
            if not room.room_full:  # 查找未满的房间
                room.players.append(client)
                temp_room = room
                
                
        if not temp_room:# 如果没有找到未满的房间，创建新房间
            temp_room_id = random.randint(1, 1000)
            temp_room = Room(temp_room_id)
            temp_room.players.append(client)
            rooms.append(temp_room)
            
        client.room = temp_room  # 将房间分配给客户端
        
        if len(client.room.players) == 2:
            room.room_full = True# 房间满员
            thread = td.Thread(target=game_start_job, args=(rooms, temp_room, ))#開始遊戲
            threads.append(thread)
            thread.start()
        else:
            message = Message()
            message.message_type = "Wait_for_another_player"
            client.mission_list.append(message)    
        
        #偵測客戶端的傳訊
        thread= td.Thread(target=client_message_reception_job, args=(clients, client, ))
        threads.append(thread)
        thread.start()
        
        #傳訊息
        thread = td.Thread(target=client_send_message_job, args=(client, ))
        threads.append(thread)
        thread.start()
        
        #偵測客戶端的練線
        thread = td.Thread(target=is_client_still_connect_detect, args=(client, ))
        threads.append(thread)
        thread.start()
        
        #開始處理客戶端的數據
        thread = td.Thread(target=client_mission_process_job, args=(client, ))
        threads.append(thread)
        thread.start()
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()