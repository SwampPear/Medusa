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
  'wbr',
  '!DOCTYPE'
]


class Parser:
  def __init__(self, response: Response) -> None:
    """
    Initializes this Parser object.
    """
    self._response = response

    self.headers = self._response.headers

    self.elements = DOMNode(type='dom_tree')

    self._parse_DOM(self._response.text)

    print(self.elements)


  def _sanitize_whitespace(self, DOM):
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

    # sanitize potential closing slash
    if DOM[-1] == '/':
      DOM = DOM[:len(DOM) - 1]

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
      _attribute_name = _valued_attribute.split('=', 1)[0]
      _attribute_value = _valued_attribute.split('=', 1)[1].replace('"', '')

      _attributes.append({
        'name': _attribute_name,
        'value': _attribute_value
      })

    # format non-valued attributes
    for _non_valued_attribute in _non_valued_attributes:
      _attributes.append({
        'name': _non_valued_attribute,
        'value': True
      })

    return _attributes


  def _parse_DOM(self, DOM, parent=None):
    """
    Recursively parses the given DOM into a DOM element tree.

    Parameters:
    str:DOM - the DOM to parse
    DOMNode:parent - the parent to assign a child to
    """

    DOM = self._sanitize_whitespace(DOM)

    # check for text element
    _text_search = re.search('[^<>]+', DOM)

    # if text element found and text elment at beginning of string
    if _text_search and _text_search.span()[0] == 0:
      _text_i, _text_f = _text_search.span()

      # insert text node
      _node = DOMNode(
        'text',
        {
          'name': 'content',
          'value': DOM[_text_i:_text_f]
        }
      )

      if parent:
        parent.insert_child(_node)
      else:
        self.elements.insert_child(_node)

      # parse rest of DOM
      DOM = DOM[_text_f:]
      
      if DOM != '':
        self._parse_DOM(DOM, parent)
    else:
      # extract opening tag
      _open_search = re.search('<[^<>]*>', DOM)

      if _open_search:
        _open_i, _open_f = _open_search.span()
        _open = re.sub('<|>', '', DOM[_open_i:_open_f])

        # extract DOM type from opening tag
        _DOM_type = _open.split(' ', 1)[0]

        if len(_open.split(' ', 1)) < 2:
          _attributes = None
        else:
          _open = _open.split(' ', 1)[1]

          # extract attributes from opening tag
          _attributes = self._extract_attributes(_open)

        # extract opening tag from DOM string
        DOM = DOM[_open_f:]

        # define and insert node
        _node = DOMNode(_DOM_type, attributes=_attributes)

        if parent:
          parent.insert_child(_node)
        else:
          self.elements.insert_child(_node)

        # check if element is self-closing
        if _DOM_type in SELF_CLOSING_ELEMENTS:
          pass
        else:
          _close_search = re.search(f'</{_DOM_type}>', DOM)

          if _close_search:
            _close_i, _close_f = _close_search.span()

            # extract children
            _children = DOM[:_close_i]

            # extract children and closing tag fron DOM
            DOM = DOM[_close_f:]

            # parse DOM on children
            if _children != '':
              self._parse_DOM(_children, _node)

        # parse rest of DOM string
        if DOM != '':
          self._parse_DOM(DOM, parent)







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