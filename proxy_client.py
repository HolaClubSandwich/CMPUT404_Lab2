#!/usr/bin/env python3
import socket, sys


def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    try:
        #define address info, payload, and buffer size
        port = 80
        payload = f'GET / HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n'
        buffer_size = 4096

        #make the socket, get the ip, and connect
        s = create_tcp_socket()

        s.connect(("127.0.0.1" , 8001))
        print (f'Socket Connected to localhost on ip 127.0.0.1')
        
        #send the data and shutdown
        send_data(s, payload)
        s.shutdown(socket.SHUT_WR)

        #continue accepting data until no more left
        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                 break
            full_data += data
        print(full_data)
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        s.close()
if __name__ == "__main__":
    main()