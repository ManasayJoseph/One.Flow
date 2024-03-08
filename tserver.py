import socket
import threading

HOST = 'localhost'  # Replace with your server's IP address if needed
PORT = 5000

clients = []
lock = threading.Lock()


def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            print(f"[{client_socket} sent]  {data}")
            if not data:
                break

            # Broadcast message to all connected clients
            with lock:
                for client in clients:
                    if client != client_socket:
                        try:
                            client.sendall(data)
                        except:
                            # Handle potential client disconnection errors
                            clients.remove(client)

        except:
            break

    # Client disconnected, remove from list
    with lock:
        clients.remove(client_socket)
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Client connected from {address}")

        with lock:
            clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    main()