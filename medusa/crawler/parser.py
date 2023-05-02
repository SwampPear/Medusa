import requests
from requests import Response
import re


class Parser:
  def __init__(self, response: Response) -> None:
    """
    Initializes this Parser object.
    """
    self._self_closing_html_tags = [
      'area',
      'base',
      'br',
      'col',
      'embed',
      'hr',
      'img',
      'input',
      'link',
      'meta',
      'param',
      'source',
      'track',
      'wbr'
    ]

    self._response = response

    self.headers = self._response.headers
    self._parse_DOM()


  def _parse_DOM(self) -> None:
    """
    Parses DOM in a given response.
    """
    _raw_text = self._response.text

    for i in range(0, 1):
      _prefix_start, _prefix_end = re.search(
        '<[a-zA-Z]*>', self._response.text
      ).span()

      _prefix = re.sub('<|>', '', _raw_text[_prefix_start:_prefix_end])

      _suffix = re.search(
        '</div>', self._response.text
      )

      print(
        _prefix
      )

    

    
url = 'http://127.0.0.1:8000/'
res = requests.get(url)
parsed = Parser(res)
print(parsed._response.headers)