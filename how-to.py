# import client_helper  # Assuming this file is saved as client_helper.py

# def get_data_to_send():
#     # Implement your logic to get data from the UI, e.g., from an entry field
#     # This function should return the data to be sent to the server
#     user_input = input("blah blah blah")
#     return user_input

# HOST = 'localhost'  # Replace with the server's IP address if needed
# PORT = 5000

# client_helper.send_data_to_server(HOST, PORT, get_data_to_send)




import client_helper  # Assuming this file is saved as client_helper.py

HOST = 'localhost'  # Replace with the server's IP address if needed
PORT = 5000

client_helper.receive_data_from_server(HOST, PORT)
