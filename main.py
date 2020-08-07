#importing stuff
import socket
import threading
from encodedecode import encode
from encodedecode import decode 

#defining variables
S_IP = "0.0.0.0"
S_PORT = 25565
HEADERSIZE = 10
IP = input("Enter peer IP: ")
PORT = 25565
socket.setdefaulttimeout(1000000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
USERN = input("Enter display name: ")
KEY = input("Enter obscurity key: ")

#listens and waits for a connection:
def estabsend():
    global clientsocket
    s.bind((S_IP, S_PORT))
    print("Listening for connections...")
    s.listen(5)
    clientsocket, address = s.accept()
    print("connection from {0} has been established!".format(address))
    msg = "Connection established"
    msg = USERN + " says: " + msg
    msg = encode(KEY, msg)
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    clientsocket.send(bytes(msg, "utf-8"))

#once connection established(via estabsend function), sends bytes to whatever address connected:
def send():
    msg = input()
    msg = USERN + " says: " + msg
    msg = encode(KEY, msg)
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    clientsocket.send(bytes(msg, "utf-8"))

#attemt to connect to specified IP and port:
def requestconnection():
    connected = False
    while connected == False:
        try:
            print("Trying to connect...")
            r.connect((IP, PORT))
            connected = True
        except:
            print("No connection found...")
    print("You have successfully connected to {0} on port {1}".format(IP, PORT))

#Waits for a message from a specified address, then decodes the message with given key and prints to console:
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
            decodedmessage = decode(KEY, full_msg[HEADERSIZE:])
            print("\n", decodedmessage)
            new_msg = True
            full_msg = ''

#Defining threads for establishing connections:
est_thread = threading.Thread(target=estabsend)
estrecv_thread = threading.Thread(target=requestconnection)

#Starting threads
est_thread.start()
estrecv_thread.start()

#The join method is used to wait for both send and recieve connections to be ready:
est_thread.join()
estrecv_thread.join()

#Define and start thread for receiving messages:
receive = threading.Thread(target=receive)
receive.start()

#Send function on loop:
while True:
    send()