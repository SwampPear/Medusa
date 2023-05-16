"""
raw_request = client_socket.recv(4096)
    request = raw_request.decode()


def _parse_request(self, request) -> list[str]:
    parsed_request = request.split('\r\n')

    method, path, version = parsed_request[0].split(' ')
    protocol, address, port = re.search('([^:/]+)://([^:/]+)(?::([0-9]+))?', path).groups()

    port = port if port else self.default_ports(protocol)

    raw_headers = [header for header in parsed_request[1:] if header]
    headers = {header.split(':', 1)[0]: header.split(':', 1)[1].strip() for header in raw_headers}

    print(protocol)
    print(address)
    print(port)
    print(headers)
"""
import re


class ProxyRequest:
  def __init__(self, request) -> None:
    self.default_ports = {
      'http': 80,
      'https': 493
    }

    self._parse_request(request)


  def _parse_request(self, request) -> None:
    request_lines, self.body = request.decode().split('\r\n\r\n', 1)
    request_lines = request_lines.split('\r\n')

    self.method, self.path, self.version = request_lines[0].split(' ')
    self.protocol, self.address, self.port = re.search(
        r'([^:/]+)://([^:/]+)(?::([0-9]+))?', self.path
    ).groups()

    self.port = self.port if self.port else self.default_ports(self.protocol)

    raw_headers = [header for header in request_lines[1:] if header]
    self.headers = {header.split(':', 1)[0]: header.split(':', 1)[1].strip() for header in raw_headers}


  def append_header(self, key: str, value: str) -> None:
    self.headers[key] = value


  def remove_header(self, key: str) -> str:
    return self.headers.pop(key, None)


  @property
  def request(self) -> str:
    request = [' '.join([self.method, self.path, self.version])]
    headers = [f'{key}: {self.headers[key]}' for key in self.headers.keys()]

    return '\r\n'.join(request + headers) + '\r\n\r\n' + self.body
  

  @property
  def raw(self) -> bytes:
    return bytes(self.request, 'utf8')


  