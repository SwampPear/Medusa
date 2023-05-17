import socket
import ssl
import threading

from data import ProxyRequest, ProxyResponse


class Proxy:
  def __init__(self, port: int) -> None:
    self.port = port


  def _handle_request(self, client_socket) -> None:
    request = ProxyRequest(client_socket.recv(4096))
    print(request.raw)
    print(request.port)
    
    # Forward the request to the destination server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((request.host, int(request.port)))

    ######################################################################
    
    # Load necessary SSL/TLS certificates and keys
    print('1')
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    print('1')
    #ontext.check_hostname = False
    #context.verify_mode = ssl.CERT_NONE
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile='medusa/browser/proxy/ca_certificate.pem')
    print('1')

    # Wrap the destination socket with SSL/TLS
    ssl_server_socket = context.wrap_socket(server_socket, server_hostname=request.host)
    print('1')
    ssl_server_socket.do_handshake()
    
    ######################################################################
    server_socket.sendall(request.raw)                     # http
    #ssl_server_socket.sendall(request.raw)                  # https

    response = ProxyResponse(server_socket.recv(4096))     # http
    #response = ProxyResponse(ssl_server_socket.recv(4096))  # https
 
    # Forward the response to the client
    client_socket.sendall(response.raw)
    print(response.raw)
    
    # Close the sockets
    server_socket.close()                                  # http
    #ssl_server_socket.close()                               # https
    client_socket.close()

  
  def run(self):
    
    # Create a listening socket for the proxy server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(('localhost', self.port))
    proxy_socket.listen(1)
    
    #print(f"Proxy server listening on {self.host}:{self.port}")
    
    while True:
        # Accept client connections
        client_socket, addr = proxy_socket.accept()
        
        # Handle the client request
        self._handle_request(client_socket)


if __name__ == '__main__':
  p = Proxy(8080)
  p.run()



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