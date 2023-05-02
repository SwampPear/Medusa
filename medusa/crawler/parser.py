import requests
from requests import Response
import re
from medusa.crawler.dom_node import DOMNode


SELF_CLOSING_ELEMENTS = [
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


class Parser:
  def __init__(self, response: Response) -> None:
    """
    Initializes this Parser object.
    """
    self.elements = []

    self._response = response

    self.headers = self._response.headers
    self._parse_DOM(self._response.text)

    print(str(self.elements[0]))


  def _parse_DOM(self, DOM, parent=None):
    """
    Recursively parses the given DOM into a DOM element tree.

    Parameters:
    str:DOM - the DOM to parse
    DOMNode:parent - the parent to assign a child to
    """
    DOM = DOM.replace('\n', '')

    _pfx_search = re.search('<[a-z|A-Z|\s|=|"]*>', DOM)

    if _pfx_search:
      _pfx_start, _pfx_end = _pfx_search.span()

      # extract contents of opening tag
      _prefix = re.sub('<|>', '', DOM[_pfx_start:_pfx_end])

      # DOM type in opening tag
      _DOM_type = _prefix.split(' ')[0]

      # search for suffix
      _sfx_start, _sfx_end = re.search(
        f'</{_DOM_type}>', DOM
      ).span()

      # remove suffix
      #DOM = DOM[_pfx_end:_sfx_start]
      print(DOM)
      if DOM[_sfx_end:] != '':
        print('kas')
        print(DOM[_sfx_end:])
        self._parse_DOM(DOM[_sfx_end:], parent=parent)
        pass

      # insert into tree
      if not parent:
        _node = DOMNode(_DOM_type, attributes=None)
        self.elements.append(_node)

        self._parse_DOM(DOM[_pfx_end:_sfx_start], _node)
      else:
        _node = DOMNode(_DOM_type, attributes=None)
        parent.insert_child(_node)

        self._parse_DOM(DOM[_pfx_end:_sfx_start], _node)
        
   
    elif DOM:
      _node = DOMNode('text', attributes=None)
      parent.insert_child(_node)

      DOM = None


  def _parse__DOM(self) -> None:
    """
    Parses DOM in a given response.
    """
    _raw_text = self._response.text

    while _raw_text:
      # search for any occurence of opening tag and get start and end positions
      _pfx_search = re.search('<[a-z|A-Z|\s|=|"]*>', _raw_text)

      if _pfx_search:
        _pfx_start, _pfx_end = _pfx_search.span()

        # extract contents of starting tag
        _prefix = re.sub('<|>', '', _raw_text[_pfx_start:_pfx_end])

        # get first string in starting tag, should be type
        _DOM_type = _prefix.split(' ')[0]

        # remove prefix from raw text
        _raw_text = _raw_text[_pfx_end:]

        # check if element is self-closing
        if _DOM_type in SELF_CLOSING_ELEMENTS:
          # insert into tree
          ############# inserting
          pass
        else:
          # search for suffix
          _sfx_start, _sfx_end = re.search(
            f'</{_DOM_type}>', _raw_text
          ).span()

          # remove suffix
          _raw_text = _raw_text[:_sfx_start]

          # insert into tree
          ############# inserting

        print(
          _raw_text
        )
      elif _raw_text:
        # insert text element into tree
        _raw_text = None