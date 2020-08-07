import socket
import threading
from encodedecode import encode
from encodedecode import decode 

#define things:
S_IP = "0.0.0.0"
S_PORT = 25565
HEADERSIZE = 10
IP = input("Enter peer IP")
PORT = 25565
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
USERN = input("Enter display name")
KEY = input("Enter obscurity key")
#send setup:
def estabsend():
    global clientsocket
    s.bind((S_IP, S_PORT))
    print("Listening for connections...")
    s.listen(5)
    clientsocket, address = s.accept()
    print("sending connection from {0} has been established!".format(address))
    msg = "Connection established"
    msg = USERN + " says: " + msg
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    clientsocket.send(bytes(msg, "utf-8"))
def send():
    msg = input()
    msg = USERN + " says: " + msg
    
    msg = encode(KEY, msg)
    
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    clientsocket.send(bytes(msg, "utf-8"))
#receive setup:
def requestconnection():
    print("Trying to connect...")
    r.connect((IP, PORT))
    print("Connection successful")
def receive():
    HEADERSIZE = 10
    full_msg = ''
    new_msg = True
    msglen = 0
    while True:
        msg = r.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False        
        full_msg += msg.decode("utf-8")
        if len(full_msg)-HEADERSIZE == msglen:
            decode(KEY, full_msg)
            print("\n", full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''
#run:
est_thread = threading.Thread(target=estabsend)
estrecv_thread = threading.Thread(target=requestconnection)
est_thread.start()
estrecv_thread.start()
est_thread.join()
estrecv_thread.join()
receive = threading.Thread(target=receive)
receive.start()
while True:
    send()