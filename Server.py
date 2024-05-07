import socket
import ipaddress
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
from collections import defaultdict
import random
import sys

maxPacketSize = 1024
defaultPort = 6543 

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
    return mongo.QueryDatabase()


def SortSensors(sensors):
    saved_sensors = defaultdict(list)
    for sensor in sensors:
        saved_sensors[sensor["sensor_name"]].append(sensor["sensor_value"])
    return dict(saved_sensors)

def BestHighway(highways):
     return min(highways, key=lambda h: sum(highways[h]) / len(highways[h]), default=None)



def ListenOnTCP(tcpSocket: socket.socket, socketAddress):
    serverResponse = GetServerData()
    print("Received Data!")
    sortedSensors = SortSensors(serverResponse)
    print(sortedSensors)
    best_highway = BestHighway(sortedSensors)
    tcpSocket.send(best_highway.encode())
    tcpSocket.close()
    pass


def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpPort = defaultPort
    print("TCP Port:",tcpPort)
    tcpSocket.bind(('localhost', tcpPort))
    return tcpSocket

def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket();
    tcpSocket.listen(5)
    while True:
        connectionSocket, connectionAddress = tcpSocket.accept();
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress]);
        connectionThread.start()

if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads);
    tcpThread.start();

    # try:
    #     while not exitSignal:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     exitSignal = True  # Set exitSignal to True to stop the loop

    # print("Ending program by exit signal...")
