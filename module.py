import socket
import customtkinter
from customtkinter import *
from PIL import Image
# import threading
# import time




def send_data_to_server(host, port, data_func):
    """
    Continuously sends data obtained from the provided function to the server
    until a keyboard interrupt is received.

    Args:
        host (str): Server hostname or IP address.
        port (int): Server port number.
        data_func (callable): A function that returns the data to be sent.
    """

    while True:
        try:
            # Create a socket and connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            while True:
                # Get data to send from the provided function
                data = data_func()

                # Send data to the server
                client_socket.sendall(data.encode())

                # Receive data from the server (optional, uncomment if needed)
                # received_data = client_socket.recv(1024).decode()
                # print(f"Received from server: {received_data}")

                # Simulate some processing time on the client-side (optional)
                # time.sleep(1)

        except KeyboardInterrupt:
            print("Keyboard interrupt received, stopping client.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the socket connection
            client_socket.close()




def receive_data_from_server(host, port):
    """
    Continuously receives data from the server until a keyboard interrupt is received.

    Args:
        host (str): Server hostname or IP address.
        port (int): Server port number.
    """

    while True:
        try:
            # Create a socket and connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            while True:
                # Receive data from the server (wait indefinitely for new data)
                data = client_socket.recv(1024).decode()
                if not data:
                    print("Server disconnected.")
                    break

                # Process the received data
                print(f"Received from server: {data}")

        except KeyboardInterrupt:
            print("Keyboard interrupt received, stopping client.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the socket connection
            client_socket.close()