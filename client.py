"""
*-----------------------------------
* @file client.py
* CP372 - Socket Assignment
* Aurthor Sunvir Bains, Donil Patel
* Version 2024-10-21
*-----------------------------------
"""
import socket
import os

# CONSTANTS
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "exit"
SERVER =socket.gethostbyname(socket.gethostname()) # "127.0.0.1 #Global in home wifi "192.168.4.32"  
ADDR = (SERVER, PORT)
FILE_DIRECTORY = os.getcwd() 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(ADDR)
except ConnectionRefusedError:
    print("Connection failed. The server may not be running or is full.")
    exit()

def send(msg): ##Handles sending a message from the server##
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive_message():
    #Handles receiving a message from the server##
    msg_length = client.recv(HEADER).decode(FORMAT)
    
    if msg_length:  # If there's a message length
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        return msg
    return None

# Step 1: Receive initial server message
initial_message = client.recv(HEADER).decode(FORMAT)
if initial_message.startswith("Client"):
    print(f"Connected as {initial_message}")
else:
    print(initial_message)  # This is "Server is full" if the server is full
    client.close()
    exit()

# Client interaction loop
connected = True
while connected:
    msg = input("Message to server: ")
    
    if msg.strip() == "":
        continue  # Skip sending empty messages

    send(msg)
    
    if msg.lower() == DISCONNECT_MSG:
        print("[DISCONNECTED]")
        connected = False
    elif msg.lower() == "list":
        # Expecting a list of files in response
        server_response = receive_message()
        print("Files in repository:\n" + server_response)
    elif msg.lower().startswith("get "):
        # Requesting a file from the server
        server_response = receive_message()
        print(f"Server response: {server_response}")

        if server_response.startswith('FILESIZE '):
            # Handle file transfer initiation
            try:
                # Extract file size by removing 'FILESIZE' and "Filename" and converting the rest to an integer
                parts = server_response.split()
                file_size = int(parts[1])
                orignalfilename=(parts[2])
                client.send("READY".encode(FORMAT)) 

                save_as_filename= f"retrived_{orignalfilename}"
                # Open a file to write the received data
                with open(save_as_filename, 'wb') as file:
                    total_received = 0
                    while total_received < file_size:
                        bytes_received = client.recv(1024)
                        if not bytes_received:
                            break
                        file.write(bytes_received)
                        total_received += len(bytes_received)

                print(f"File '{save_as_filename}' received successfully.")
            except ValueError:
                print("Invalid file size received from the server.")


        elif server_response.startswith("ERROR"):
            print(f"Server response:\n{server_response}")
        else:
            print(f"Unexpected response: {server_response}")
    else:
        # General server response for other commands
        server_response = receive_message()
        print(f"Server: {server_response}")

# Close the client socket after exiting the loop
client.close()
