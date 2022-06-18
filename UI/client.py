import socket
import threading
import sys
import json
from utils import json_constructor


class Client():
    def __init__(self, ip):
        self.ip = ip
        self.port = 5555

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip, self.port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NAME':
                    self.client.send(name.encode('utf-8'))
                else:
                    if message:

                        json_data = json.loads(message)
                        print(json_data)
                        if json_data['type'] == 'message':
                            print(
                                f"{json_data['sender']}: {json_data['message']}")
                        elif json_data['type'] == 'alert':
                            print(json_data['message'])
                    else:
                        break
            except Exception as e:
                raise e
                print('an error occured!')
                message = json.dumps({'type': 'leave'})
                self.client.send(bytes(message, encoding='utf-8'))
                self.client.close()
                # sys.exit()
                break

    def receive_a(self):
        try:
            msg = self.client.recv(1024).decode('utf-8')
            if msg:
                return self.message
        except:
            self.client.close()
            return False

    def write(self, name, msg=None):
        if not msg:
            while True:
                try:
                    message = json_constructor(
                        'message', input(), sender=name.capitalize())
                    # message_a = {'name':'abdul', 'msg':'ismo'}
                    self.client.send(message.encode('utf-8'))
                except:
                    message = json.dumps({'type': 'leave'})
                    self.client.send(bytes(message, encoding='utf-8'))
                    self.client.close()
                    break
        else:
            msg = f'{name.capitalize()}::43$*(){msg}'
            self.client.send(msg.encode('utf-8'))


if __name__ == '__main__':

    name = input('Enter username')
    client = Client("127.0.0.1")

    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()

    write_thread = threading.Thread(target=client.write, args=(name,))
    write_thread.start()
