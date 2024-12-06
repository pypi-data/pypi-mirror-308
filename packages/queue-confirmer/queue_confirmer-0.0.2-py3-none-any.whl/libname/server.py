import socket
import threading



def main_server():
    HOST = "127.0.0.1"  # localhost
    PORT = 13200         # port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    # Waits for a client to connect
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = client_handle, args = (conn, addr))
        thread.start()
def client_handle(conn, addr):

    # Runs the communication loop
    while True:
        data = conn.recv(1024)

        if not data:  # If no data is received, break the loop
            print('End of queue!')

        # Print the received data
        show = data.decode('utf8')
        print('Data:', show)

        # Send a confirmation to the client
        conn.send(str(1).encode('utf8'))

        # Identifies end of trip
        if show == "endtrip":
            break



    # Handles clean closing of the client
    print("closed")
    conn.close()

if __name__ == "__main__":
    main_server()