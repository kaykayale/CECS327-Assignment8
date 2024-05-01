import socket
import ipaddress
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
import random
import sys

maxPacketSize = 1024
defaultPort = 0 #TODO: Set this to your preferred port

def GetFreePort(minPort: int = 1024, maxPort: int = 65535):
    for i in range(minPort, maxPort):
        print("Testing port",i);
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort:
            try:
                potentialPort.bind(('localhost', i));
                potentialPort.close();
                print("Server listening on port",i);
                return i
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    print("Port",i,"already in use. Checking next...");
                else:
                    print("An exotic error occurred:",e);

def GetServerData() -> []:
    import MongoDBConnection as mongo
    return mongo.QueryDatabase();






def ListenOnTCP(tcpSocket, socketAddress):
    print(f"Connected to {socketAddress}")
    try:
        while True:
            data = tcpSocket.recv(maxPacketSize)
            if not data:
                break  # No data, client might have disconnected
            # Assume data is a simple command to fetch best freeway (for simplicity)
            traffic_data = GetServerData()
            current_time = time.time()
            filtered_data = [
                d for d in traffic_data if current_time - d['timestamp'] <= 300  # last 5 minutes
            ]
            freeway_times = {}
            for data in filtered_data:
                freeway = data['freeway_name']
                if freeway in freeway_times:
                    freeway_times[freeway].append(data['travel_time'])
                else:
                    freeway_times[freeway] = [data['travel_time']]
            best_freeway = min(freeway_times, key=lambda k: sum(freeway_times[k]) / len(freeway_times[k]))
            
            response = f"The best freeway to take is {best_freeway}"
            tcpSocket.sendall(response.encode())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        tcpSocket.close()
        print(f"Connection with {socketAddress} closed")







def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    tcpPort = defaultPort
    print("TCP Port:",tcpPort);
    tcpSocket.bind(('localhost', tcpPort));
    return tcpSocket;

def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket();
    tcpSocket.listen(5);
    while True:
        connectionSocket, connectionAddress = tcpSocket.accept();
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress]);
        connectionThread.start();

if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads);
    tcpThread.start();

    while not exitSignal:
        time.sleep(1);
    print("Ending program by exit signal...");
