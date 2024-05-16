import socket
import multiprocessing as mp
import threading as td
import time
import pickle
from client_datatype import Client_type
from game_datatype import Game_type


def client_send_message_job(client_list, client):
    while True:
        if client.connect == 'disappear':
            break
        try:
            if len(client.mission_list) > 0:
                massage = client.mission_list.pop(0)
                client.client_socket.sendall(pickle.dumps(massage))
                print(f"傳送訊係給{client.client_address}:",massage)
        except:
            pass


def is_client_still_connect_detect(thread_list, client_list, client):
    
    while True:
        if client.connect == 'disappear':
            break
        now_time = time.time()
        if now_time - client.last_time_convey > 5:
            client.mission_list.append("connection_confirmation")
            
        time.sleep(1.5)
        


def client_message_reception_job(client_list, client):
    while True:
        try:
            
            data = client.client_socket.recv(4096)
            data = pickle.loads(data)
            client.last_time_convey = time.time()
            
            client.data_list.append(data)
            
            print(f"接收到{client.client_address}的訊息:",client.data_list[len(client.data_list)-1])
            
        except:
            client.connect = 'disappear'
            break
        
        time.sleep(0.2)
        
    client_list.remove(client)
    print(f"連練錯誤與客戶端{client.client_address}中斷連線")
    
    
def client_connect_request_job(server_socket, client_list):
    thread_list = []
    
    while True:
        # 接受客戶端的連線
        client = Client_type()
        
        client.client_socket, client.client_address = server_socket.accept()
        client_list.append(client)
        
        print(f"與客戶端{client.client_address}建立連線")
        
        client.last_time_convey = time.time()
        
        #偵測客戶端的傳訊
        thread_1 = [td.Thread(target=client_message_reception_job, args=(client_list, client, ))]
        thread_list.extend(thread_1)
        thread_1[0].start()
        
        
        #傳訊息
        thread_2 = [td.Thread(target=client_send_message_job, args=(client_list, client,))]
        thread_list.extend(thread_2)
        thread_2[0].start()
        
        #偵測客戶端的練線
        thread_3 = [td.Thread(target=is_client_still_connect_detect, args=(thread_list, client_list, client,))]
        thread_list.extend(thread_3)
        thread_3[0].start()


def main():
    # 建立一個 IPv4 TCP Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取主机名
    hostname = socket.gethostname()

    # 根据主机名获取IP地址
    ip_address = socket.gethostbyname(hostname)

    # 綁定伺服器的 IP 位址和埠號
    server_ip = ip_address  # 你可以修改為你的 IP 位址
    server_port = 878  # 你可以使用未被佔用的埠號
    server_socket.bind((server_ip, server_port))

    # 讓伺服器開始監聽連線
    server_socket.listen(10)  # 允許最多 10 個連線


    print(f"伺服器正在監聽 {server_ip}:{server_port}")
    
    client_list = []
    
    
    thread = td.Thread(target=client_connect_request_job, args=(server_socket, client_list))
    thread.start()
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()