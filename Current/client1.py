import socket
import threading
import pyperclip

# Global variables
server_address = ('localhost', 5050)  # Change as needed


def receive_clipboard():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_address)

    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break
            print("Received clipboard data from server:", data)
            pyperclip.copy(data)
        except ConnectionResetError:
            break

    client.close()


def main():
    while True:
        current_clipboard = pyperclip.paste()
        user_input = input("Type 'sync' to sync clipboard, or 'exit' to exit: ")

        if user_input.lower() == 'sync':
            if pyperclip.paste() != current_clipboard:
                current_clipboard = pyperclip.paste()
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(server_address)
                client.send(current_clipboard.encode('utf-8'))
                client.close()
                print("Clipboard synced successfully!")
            else:
                print("Clipboard already synced.")
        elif user_input.lower() == 'exit':
            break
        else:
            print("Invalid command. Please type 'sync' or 'exit'.")


if __name__ == "__main__":
    receive_clipboard_thread = threading.Thread(target=receive_clipboard)
    receive_clipboard_thread.start()
    main()

