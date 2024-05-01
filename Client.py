import socket
import ipaddress
import threading
import time
import contextlib
import errno

maxPacketSize = 1024
defaultPort = 6543 # TODO: Change this to your expected port
serverIP = '35.202.88.245' #TODO: Change this to your instance IP

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
try:
    tcpPort = int(input("Please enter the TCP port of the host..."));
except:
    tcpPort = 0;
if tcpPort == 0:
    tcpPort = defaultPort;
tcpSocket.connect((serverIP, tcpPort));

clientMessage = "";
while clientMessage != "exit":
    clientMessage = input("Please type the message that you'd like to send (Or type \"exit\" to exit):\n>");

    #TODO: Send the message to your server
    #TODO: Receive a reply from the server for the best highway to take
    #TODO: Print the best highway to take
    tcpSocket.sendall(clientMessage.encode())

    # Receive a reply from the server for the best highway to take
    serverResponse = tcpSocket.recv(maxPacketSize).decode()

    # Print the best highway to take
    print(f"Recommended freeway: {serverResponse}")
tcpSocket.close();

