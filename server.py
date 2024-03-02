import socket
import threading
import pyperclip

# Global variables
clients = set()
server_address = ('localhost', 5050)  # Change as needed


def handle_client(client_socket):
    global clients
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                clients.remove(client_socket)
                client_socket.close()
                break
            print("Received clipboard data from client:", data)
            for client in clients:
                if client != client_socket:
                    client.send(data.encode('utf-8'))
            pyperclip.copy(data)
        except ConnectionResetError:
            clients.remove(client_socket)
            client_socket.close()
            break


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(server_address)
    server.listen(5)
    print("Server listening on", server_address)

    while True:
        client_socket, _ = server.accept()
        clients.add(client_socket)
        print("Client connected:", client_socket)

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()

