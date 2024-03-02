import socket
import pyperclip
import time

# Host and port configuration
HOST = '192.168.1.4'  # Server's IP address
PORT = 65432        # Port the server is listening on

def get_clipboard_content():
    """Retrieve the content of the clipboard."""
    return pyperclip.paste()

def set_clipboard_content(content):
    """Set the content of the clipboard."""
    pyperclip.copy(content)

def client():
    """Clipboard sync client."""
    previous_content = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server")
        while True:
            content = s.recv(1024).decode()
            print("Recived:content on client side " , content)
            c_content = get_clipboard_content()
            
            s.sendall(content.encode())
            print("Sent:" , c_content)
            previous_content = c_content
        
            time.sleep(1)

            if not content:
                break
            print("Received:", content)
            set_clipboard_content(content)



if __name__ == "__main__":
    client()
                    