import socket
import sys


def start_tcp_client(ip, port):
    # server port and ip
    server_ip = ip
    server_port = port
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_client.connect((server_ip, server_port))
    except socket.error:
        print('fail to setup socket connection')
    tcp_client.close()


start_tcp_client('192.168.10.27', 30012)
