#!/usr/bin/env python3
from os import access
import socket, sys
import time
from multiprocessing import Process

#define address & buffer size

HOST = "www.google.com"
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:

        proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        proxy_socket.bind(("", PORT))

        proxy_socket.listen(2)

        while True:
            conn, addr = proxy_socket.accept()
            print("Connected by..", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as google_socket:
                print("Connecting to google...")
                remote_ip = get_remote_ip(HOST)
                port = 80
                google_socket.connect((remote_ip, port))

                p = Process(target=handle_echo, args=(addr, conn, google_socket))
                p.daemon = True
                p.start()

def handle_echo(addr, conn, google_socket):
    print("Connected by...", addr)
    full_data = conn.recv(BUFFER_SIZE)
    google_socket.sendall(full_data)
    google_socket.shutdown(socket.SHUT_WR)
    data = google_socket.recv(BUFFER_SIZE)
    conn.send(data)
    conn.close()

if __name__=="__main__":
    main()
