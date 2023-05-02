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
      # search for any occurence of opening tag and get start and end positions
      _pfx_start, _pfx_end = re.search('<[a-z|A-Z|\s|=|"]*>', _raw_text).span()

      # extract contents of starting tag
      _prefix = re.sub('<|>', '', _raw_text[_pfx_start:_pfx_end])

      # get first string in starting tag, should be type
      _DOM_type = _prefix.split(' ')[0]

      # remove prefix from raw text
      _raw_text = _raw_text[_pfx_end:]

      # check if element is self-closing
      if _DOM_type in self._self_closing_html_tags:
        # insert into tree
        ############# inserting
        pass
      else:
        # search for suffix
        _sfx_start, _sfx_end = re.search(
          f'</{_DOM_type}>', _raw_text
        ).span()

        _suffix = re.sub('<|>', '', _raw_text[_sfx_start:_sfx_end])

        # remove suffix
        _raw_text = _raw_text[:_sfx_start]

        # insert into tree
        ############# inserting

      print(
        _raw_text
      )

    

    
url = 'http://127.0.0.1:8000/'
res = requests.get(url)
parsed = Parser(res)
print(parsed._response.headers)