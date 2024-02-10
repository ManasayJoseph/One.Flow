import socket
import pyperclip
import threading

# Host and port configuration
HOST = '192.168.1.4'  # Localhost
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# List to keep track of client connections
client_connections = []

def get_clipboard_content():
    """Retrieve the content of the clipboard."""
    return pyperclip.paste()

def set_clipboard_content(content):
    """Set the content of the clipboard."""
    pyperclip.copy(content)

def handle_client_connection(conn, addr):
    """Handle a client connection."""
    print("Connected by", addr)
    with conn:
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print("Received from {}: {}".format(addr, data))
                # set_clipboard_content(data)
                # Send received data to all connected clients
                for client_conn in client_connections[:]:
                    if client_conn != conn:
                        try:
                            client_conn.sendall(data.encode())
                        except Exception as e:
                            print("Error sending data to client:", e)
                            # Remove invalid socket from the list
                            client_connections.remove(client_conn)
        except Exception as e:
            print("Error with client connection:", e)
            # Remove invalid socket from the list
            client_connections.remove(conn)

def server():
    """Clipboard sync server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server listening on {}:{}".format(HOST, PORT))
        while True:
            conn, addr = s.accept()
            # Add client connection to the list
            client_connections.append(conn)
            client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    server()
