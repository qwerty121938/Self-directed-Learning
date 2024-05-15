import socket
import multiprocessing as mp
import threading as td
import time
import pickle
from datatype import Datatype




def client_message_reception_job(client_list, client):
    while True:
        try:
            
            data = client.client_socket.recv(4096)
            data = pickle.loads(data)
            
            client.data_list.extend(data)
            
            print(f"接收到{client.client_address}的訊息:",client.data_list[len(client.data_list)-1])
            
        except:
            break
        
    client_list.remove(client)
    print(f"連練錯誤與客戶端{client.client_address}中斷連線")
    
    
def client_connect_request_job(server_socket, client_list):
    thread_list = []
    
    while True:
        # 接受客戶端的連線
        client = Datatype()
        
        client.client_socket, client.client_address = server_socket.accept()
        client_list.append(client)
        
        print(f"與客戶端{client.client_address}建立連線")
        
        thread = td.Thread(target=client_message_reception_job, args=(client_list, client, ))
        thread_list.append(thread)
        thread.start()
        



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