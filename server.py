import socket
import threading
import json

ip = "127.0.0.1"
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()

session = {}
client_name = {}


def broadcast(message, dont=None):
    for users in session:
        if users == dont:
            continue
        client = session[users]
        client.send(bytes(message, encoding='utf-8'))


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if json.loads(message)['type'] == 'leave':
                remove_client(client)
                break
            broadcast(message)
        except:
            remove_client(client)
            break


def remove_client(client):
    name = client_name[client]
    del client_name[client]
    del session[name]

    message = json_constructor('alert', f'{name} left the chat!')
    broadcast(message)
    client.close()
    print(session)


def json_constructor(type_, message, sender=None):
    data = {'type': type_, 'message': message}
    if sender:
        data['sender'] = sender
    json_data = json.dumps(data)
    return json_data


def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')
        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('utf-8')

        session[name] = client
        client_name[client] = name

        client.send(
            bytes(json.dumps({'type': 'alert', 'message': 'welcome to the chat!'}), encoding='utf-8'))
        message = json_constructor('alert', f'{name} join the chat!')

        broadcast(message, name)
        print(session)
        # client.send('Connected with server, you can now start to chat!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('Server is listening.................')
receive()
