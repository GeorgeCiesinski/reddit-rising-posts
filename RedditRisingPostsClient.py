#!/usr/bin/python3.6
import socket
import sys

HOST = "127.0.0.1"
PORT = 5000


try:
    out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except Exception as e:
    print("Could not create socket {}".format(e))
    sys.exit()
try:
    out_socket.connect((HOST,PORT))
except:
    print("Application not running")
    out_socket.close()
    sys.exit()

args = sys.argv
in_data = " ".join(args[1:])
out_socket.sendall(in_data.encode("utf-8"))
reply = out_socket.recv(1024)
print(reply.decode("utf-8"))
out_socket.close()