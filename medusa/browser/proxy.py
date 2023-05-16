"""
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request('GET')

    def do_POST(self):
        self.proxy_request('POST')

    def do_PUT(self):
        self.proxy_request('PUT')

    def do_DELETE(self):
        self.proxy_request('DELETE')

    def proxy_request(self, method):
        url = self.path
        headers = self.headers
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))

        # Forward the request to the destination server
        response = requests.request(method, url, headers=headers, data=body)

        # Print the intercepted request and response details
        print(f"Request:\n{method} {url}")
        print(f"Headers:\n{headers}")
        print(f"Body:\n{body.decode()}")
        print(f"Response:\n{response.status_code} {response.reason}")
        print(f"Response Headers:\n{response.headers}")
        print(f"Response Body:\n{response.text}")

        self.send_response(response.status_code)
        for header, value in response.headers.items():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(response.content)

def run_proxy_server():
    host = 'localhost'
    port = 8080

    server = HTTPServer((host, port), ProxyHandler)
    print(f"Proxy server listening on {host}:{port}")
    server.serve_forever()

if __name__ == '__main__':
    run_proxy_server()

"""
import socket

def handle_request(client_socket):
    # Receive the request from the client
    request_data = client_socket.recv(4096)
    
    # Print the intercepted request
    print("Request:\n" + request_data.decode())
    
    # Forward the request to the destination server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('localhost', 8000))  # Replace with the actual destination server
    
    server_socket.sendall(request_data)
    
    # Receive the response from the destination server
    response_data = server_socket.recv(4096)
    
    # Print the intercepted response
    print("Response:\n" + response_data.decode())
    
    # Forward the response to the client
    client_socket.sendall(response_data)
    
    # Close the sockets
    server_socket.close()
    client_socket.close()

def run_proxy_server():
    proxy_host = 'localhost'
    proxy_port = 8080
    
    # Create a listening socket for the proxy server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxy_host, proxy_port))
    proxy_socket.listen(1)
    
    print(f"Proxy server listening on {proxy_host}:{proxy_port}")
    
    while True:
        # Accept client connections
        client_socket, addr = proxy_socket.accept()
        
        # Handle the client request
        handle_request(client_socket)

if __name__ == '__main__':
    run_proxy_server()



# The client sends an HTTPS request to the proxy server. The request is typically addressed to the destination server using the HTTPS scheme (e.g., https://www.example.com/path).

# The transparent proxy intercepts the client's request. It receives the encrypted data sent by the client.

# The transparent proxy acts as a man-in-the-middle (MITM) between the client and the destination server. It initiates a new SSL/TLS connection with the client, acting as the server, and presents a dynamically generated SSL/TLS certificate to the client. This certificate is signed by a certificate authority (CA) that the client recognizes.

# The client receives the SSL/TLS certificate from the proxy and verifies its authenticity. Since the proxy-generated certificate is signed by a trusted CA, the client accepts it as valid.

# The client establishes the SSL/TLS connection with the proxy, encrypting the subsequent communication between them.

# The client sends the encrypted HTTPS request to the proxy through the established SSL/TLS connection. The proxy decrypts the encrypted data received from the client.

# The proxy examines the decrypted request, including the request method, URL, headers, and body, to gather information or perform any required modifications.

# The proxy forms a new encrypted HTTPS request to the destination server, using a separate SSL/TLS connection.

# The proxy forwards the encrypted request to the destination server, acting as the client in this connection.

# The destination server receives the HTTPS request from the proxy and processes it.

# The destination server generates an HTTPS response containing the requested data.

# The destination server encrypts the response using SSL/TLS and sends it back to the proxy over the SSL/TLS connection.

# The proxy receives the encrypted response from the destination server.

# The proxy decrypts the response to examine its content, including the response status, headers, and body.

# The proxy encrypts the response again using a separate SSL/TLS connection to the client.

# The proxy forwards the encrypted response to the client.

# The client receives the encrypted response from the proxy and decrypts it using the established SSL/TLS connection.

# The client processes the decrypted response, including the response status, headers, and body, and performs any necessary actions based on the received data.

# By acting as a mediator, the transparent proxy can intercept, examine, and modify the encrypted HTTPS traffic between the client and the destination server without the client being aware of it.