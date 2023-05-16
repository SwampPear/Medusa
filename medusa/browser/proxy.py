import socket
import threading

def handle_client(client_socket):
    request = client_socket.recv(4096)
    print(f"Received request:\n{request.decode()}")
    
    # Forward the request to the destination server
    # Modify the following lines to redirect requests to your desired server
    
    server_host = 'https://www.geeksforgeeks.org'  # Destination server hostname
    server_port = 443             # Destination server port
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_host, server_port))
    server_socket.send(request)
    
    # Receive the response from the server
    response = server_socket.recv(4096)
    print(f"Received response:\n{response.decode()}")
    
    # Forward the response back to the client
    client_socket.send(response)
    
    # Close the sockets
    client_socket.close()
    server_socket.close()

def start_proxy():
    proxy_host = 'localhost'  # Proxy hostname
    proxy_port = 8080         # Proxy port
    
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind((proxy_host, proxy_port))
    proxy_socket.listen(5)
    print(f"Proxy server listening on {proxy_host}:{proxy_port}")
    
    while True:
        client_socket, client_address = proxy_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

start_proxy()
