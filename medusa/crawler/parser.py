from typing import Optional
import re
from requests import Response
from medusa.crawler.dom_node import DOMNode


class Parser:
  def __init__(self, response: Response) -> None:
    self.self_closing_elements = [
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

    self.status = response.status_code
    self.headers = response.headers
    self.cookies = response.cookies
    self.raw_text = response.text

    self.elements = DOMNode(type='dom_tree')
    self.typed_elements = {}

    self._parse_DOM(response.text)


  def _insert_typed_element(self, element: DOMNode) -> None:
    if element.type not in self.typed_elements.keys():
      self.typed_elements[element.type] = []

    self.typed_elements[element.type].append(element)


  def _sanitize_whitespace(self, DOM: str) -> None:
    _output = DOM.replace('\n', '')
    _output = re.sub(re.compile(r'>(\s+)<'), '><', _output)
    _output = re.sub(re.compile(r'>(\s+)'), '>', _output)
    _output = re.sub(re.compile(r'(\s+)<'), '<', _output)

    return _output
  

  def _extract_attributes(self, DOM: str) -> dict:
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


  def _parse_DOM(self, DOM: str, parent: Optional[DOMNode]=None):
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

      self._insert_typed_element(_node)

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

        self._insert_typed_element(_node)

        # check if element is self-closing
        if _DOM_type not in self.self_closing_elements:
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