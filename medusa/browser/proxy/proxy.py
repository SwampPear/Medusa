import socket
import ssl
import threading

from data import ProxyRequest, ProxyResponse


class Proxy:
  def __init__(self, port: int) -> None:
    self.port = port


  def _handle_http_request(self, client_socket, request) -> None:
    print(request.raw)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((request.host, int(request.port)))

    server_socket.sendall(request.raw)

    response = ProxyResponse(server_socket.recv(4096))
 
    client_socket.sendall(response.raw)
    
    server_socket.close()
    client_socket.close()


  def _handle_https_request(self, client_socket, request) -> None:
    request.set_header('Host', f'{request.host}:{request.port}')
    request.set_header('Proxy-Connection', 'Keep-Alive')
    print(request.headers)

    # proxy/destination handshake
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.connect((request.host, int(request.port)))

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile='medusa/browser/proxy/ca_certificate.pem', keyfile='medusa/browser/proxy/private_key.pem')
    client_socket = context.wrap_socket(client_socket, server_hostname=request.host)

    # request sent and response received
    #server_socket.sendall(request.raw)
    #response = ProxyResponse(server_socket.recv(4096))
    #client_socket.sendall(response.raw)
    server_socket.close()
    client_socket.close()

    print(request.raw)
    #print(response.raw)

  
  def run(self):
    # Create a listening socket for the proxy server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(('localhost', self.port))
    proxy_socket.listen(1)


    
    
    while True:
      client_socket, addr = proxy_socket.accept()

      request = ProxyRequest(client_socket.recv(4096))

      if request.protocol == 'https':
        self._handle_https_request(client_socket, request)
      else:
        self._handle_http_request(client_socket, request)

        


if __name__ == '__main__':
  p = Proxy(8080)
  p.run()