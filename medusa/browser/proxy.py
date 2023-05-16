import socket
import threading

def handle_client(client_socket):
    # Receive data from the client
    request = client_socket.recv(4096)

    # Log the request
    print('Received request:')
    print(request.decode())

    # Forward the request to the remote server
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect(('www.example.com', 80))
    remote_socket.send(request)

    # Receive data from the remote server
    response = remote_socket.recv(4096)

    # Log the response
    print('Received response:')
    print(response.decode())

    # Send the response back to the client
    client_socket.send(response)

    # Close the sockets
    remote_socket.close()
    client_socket.close()

def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(('127.0.0.1', 8888))

    # Start listening for incoming connections
    server_socket.listen(5)
    print('Proxy server is listening on 127.0.0.1:8080')

    while True:
        # Accept a client connection
        client_socket, addr = server_socket.accept()
        print('Accepted connection from', addr)

        # Start a new thread to handle the client request
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    main()
