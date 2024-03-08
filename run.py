import module  # Assuming this file is saved as module.py

def get_data_to_send():
    # Implement your logic to get data from the UI, e.g., from an entry field
    # This function should return the data to be sent to the server
    user_input = input("blah blah blah")
    return user_input

HOST = 'localhost'  # Replace with the server's IP address if needed
PORT = 5000

module.send_data_to_server(HOST, PORT, get_data_to_send)




# import module  # Assuming this file is saved as client_helper.py

# HOST = 'localhost'  # Replace with the server's IP address if needed
# PORT = 5000

# module.receive_data_from_server(HOST, PORT)   