import socket
import threading
import sys
import json

ip = "127.0.0.1"
port = 5555

name = input('enter your username: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NAME':
                client.send(name.encode('ascii'))
            else:
                print(message)
        except:
            print('an error occured!')
            client.close()
            break
            sys.exit()


def write():
    while True:
        try:
            message = input()
            receivers = input('enter recievers id: ')
            data = {'recievers': recievers,
                    "message": message, "sender_id": name}
            data = json.dumps(data)
            client.send(bytes(data, 'utf-8'))
        except:
            client.close()
            break
            sys.exit()


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
