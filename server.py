"""
*-----------------------------------
* @file Server.py
* CP372 - Socket Assignment
* Aurthor Sunvir Bains, Donil Patel
* Version 2024-10-21
*-----------------------------------
"""

import socket
import threading
import datetime
import os

# CONSTANTS
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  #"192.168.4.32"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'exit'
MAX_CLIENTS = 3

active_clients = 0
client_cache = {}
client_id = 1
REPOSITORY_PATH = os.path.dirname(os.path.abspath(__file__))

# SETUP SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    global active_clients, client_id
    client_name = f"Client{client_id:02}"
    client_id += 1
    start_time = datetime.datetime.now()
    
    ip_address = addr[0]
    client_cache[client_name] = {
        "Start Time": start_time.strftime("%Y-%m-%d %H:%M:%S"), 
        "End Time": None,
        "Address": addr
    }
    active_clients += 1
    print(f"[NEW CONNECTION] {client_name} connected from {ip_address}")

    # Send the client its assigned name
    conn.send(client_name.encode(FORMAT))

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg.lower() == DISCONNECT_MSG:
                connected = False
                end_time = datetime.datetime.now()
                client_cache[client_name]["End Time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
                active_clients -= 1
                print(f"[DISCONNECTED] {client_name} disconnected from {ip_address}.")

            elif msg.lower() == "status":
                response = str(client_cache)
                send_message(conn, response)

            elif msg.lower() == "list":
                files = os.listdir(REPOSITORY_PATH)
                send_message(conn, "\n ".join(files))

            elif msg.lower().startswith ("get "):
                filename= msg[4:].strip()
                filepath=os.path.join(REPOSITORY_PATH,filename)
                if os.path.isfile(filepath):
                    try:
                        file_size=os.path.getsize(filepath)
                        send_message(conn,f"FILESIZE {file_size} {filename}")
                        ack=conn.recv(HEADER).decode(FORMAT)
                        if ack== 'READY':
                            with open(filepath,'rb') as file:
                                while True:
                                    bytesread= file.read(1024)
                                    if not bytesread:
                                        break
                                    conn.sendall(bytesread)
                            print(f"File '{filename}' sent to {client_name}")
                        else:
                            print(f"{client_name} did not acknowledge file transfer.")
                    except Exception as e:
                        send_message(conn, f"Error sending file: {str(e)}")
                else:
                    send_message(conn, f"ERROR: File '{filename}' not found.")

            else:
                print(f"[{client_name}] {msg}")
                send_message(conn, f"{msg} ACK")

    conn.close()
#this so their isnt any lost data
def send_message(conn, message):
    """Send a message to the client with a header for its length."""
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

# Start the program
def start():
    global active_clients
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        if active_clients >= MAX_CLIENTS:
            conn.send("Server is full. Please try again later.".encode(FORMAT))
            conn.close()
            print(f"[FULL CAPACITY] {addr[0]} tried to connect but the server is full.")
        else:
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] SERVER is starting...")
start()
