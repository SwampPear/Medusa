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
    self._response = response

    self.headers = self._response.headers

    self.elements = []

    self._parse_DOM(self._response.text)

    for _element in self.elements:
      print(str(_element))



  def _digest_whitespace(self, DOM):
    """
    Removes all white space and newlines in a given DOM string.

    Parameters:
    str:DOM - the DOK string to digest

    Returns:
    str: the digested string
    """
    _output = DOM.replace('\n', '')
    _output = re.sub(re.compile(r'>(\s+)<'), '><', _output)
    _output = re.sub(re.compile(r'>(\s+)'), '>', _output)
    _output = re.sub(re.compile(r'(\s+)<'), '<', _output)

    return _output
  

  def _extract_attributes(self, DOM):
    """
    Extracts attributes froma a given DOM tag.

    Parameters:
    str:DOM - the tag to use

    Returns:
    []: the extracted attributes
    """
    _attributes = []

    # extract valued attributes
    _valued_attributes = re.findall(re.compile(r'[^"\s]*="[^"]*"'), DOM)

    # extract non valued attributes
    _non_valued_attributes = []

    for _valued_attribute in _valued_attributes:
      DOM = re.sub(_valued_attribute, '', DOM)

    for _non_valued_attribute in DOM.split(' '):
      if _non_valued_attribute != '':
        _non_valued_attributes.append(_non_valued_attribute)

    # format valued attributes
    for _valued_attribute in _valued_attributes:
      _attributes.append({
        'name': re.search(re.compile(r'(.*)="[^"]*"'), _valued_attribute).group()
      })

    print(_attributes)


  def _parse_DOM(self, DOM, parent=None):
    """
    Recursively parses the given DOM into a DOM element tree.

    Parameters:
    str:DOM - the DOM to parse
    DOMNode:parent - the parent to assign a child to
    """

    DOM = self._digest_whitespace(DOM)

    # extract opening tag
    _open_search = re.search('<[^<>]*>', DOM)
    _open_i, _open_f = _open_search.span()
    _open = re.sub('<|>', '', DOM[_open_i:_open_f])

    # extract DOM type from opening tag
    _DOM_type = _open.split(' ')[0]

    # extract attributes from opening tag
    _attributes = self._extract_attributes(_open)


    """
    _pfx_search = re.search('<[a-z|A-Z|\s|=|"]*>', DOM)

    if _pfx_search:
      _pfx_start, _pfx_end = _pfx_search.span()

      # extract contents of opening tag
      _prefix = re.sub('<|>', '', DOM[_pfx_start:_pfx_end])

      # DOM type in opening tag
      _DOM_type = _prefix.split(' ')[0]

      # insert attributes
      ######################################################

      # search for suffix
      _sfx_start, _sfx_end = re.search(
        f'</{_DOM_type}>', DOM
      ).span()

      # remove suffix
      if DOM[_sfx_end:] != '':
        self._parse_DOM(DOM[_sfx_end:], parent=parent)

      _node = DOMNode(_DOM_type, attributes=None)

      # insert into tree
      if not parent:
        self.elements.append(_node)
      else:
        parent.insert_child(_node)

      self._parse_DOM(DOM[_pfx_end:_sfx_start], _node)
        
    elif DOM:
      _node = DOMNode('text', attributes=None)
      parent.insert_child(_node)

      DOM = None
    """