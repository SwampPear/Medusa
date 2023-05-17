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

    self.port = int(self.port) if self.port else self.default_ports(self.protocol)

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
  

class ProxyResponse:
  def __init__(self, response) -> None:
    self._parse_response(response)


  def _parse_response(self, response) -> None:
    response_lines, self.body = response.decode().split('\r\n\r\n', 1)
    response_lines = response_lines.split('\r\n')

    self.version, self.status = response_lines[0].split(' ', 1)

    raw_headers = [header for header in response_lines[1:] if header]
    self.headers = {header.split(':', 1)[0]: header.split(':', 1)[1].strip() for header in raw_headers}


  @property
  def response(self) -> str:
    response = [' '.join([self.version, self.status])]
    headers = [f'{key}: {self.headers[key]}' for key in self.headers.keys()]

    return '\r\n'.join(response + headers) + '\r\n\r\n' + self.body
  

  @property
  def raw(self) -> bytes:
    return bytes(self.response, 'utf8')



  