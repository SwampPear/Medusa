from typing import Optional, Tuple
import re
from requests import Response
from medusa.crawler.data import DOMNode
from xml.dom.minidom import parseString
from time import sleep


class Parser:
  def __init__(self, response: Response, text) -> None:
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

    self._parse_DOM(self._sanitize_DOM(text))

  
  def _sanitize_DOM(self, DOM) -> None:
    _out = DOM.replace('\n', '')

    return _out
  

  def _insert_typed_element(self, element: DOMNode) -> None:
    if element.type not in self.typed_elements.keys():
      self.typed_elements[element.type] = []

    self.typed_elements[element.type].append(element)


  def _extract_attributes(self, DOM: str) -> dict:
    _attributes = {}

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

      _attributes[_attribute_name] = _attribute_value

    # format non-valued attributes
    for _non_valued_attribute in _non_valued_attributes:
      _attributes[_non_valued_attribute] = True

    return _attributes
  

  def _create_node(
    self,
    type: str, 
    attributes: dict, 
    parent: Optional[DOMNode]=None
  ) -> None:
    _node = DOMNode(
      type=type,
      attributes=attributes
    )

    if parent:
      parent.insert_child(_node)
    else:
      self.elements.insert_child(_node)

    return _node

  
  def _insert_node(
    self,
    node: DOMNode,
    parent: Optional[DOMNode]=None
  ) -> None:
    if parent:
      parent.insert_child(node)
    else:
      self.elements.insert_child(node)


  def _parse_open_tag(self, open: str) -> Tuple[str, dict]:
    # remove carat delimeters
    open = open[1:-1]

    # sanitize potential closing delimeter for self-closing tags
    if open[-1] == '/':
      open = open[:-1]

    # extract type and attributes
    _type = open.split(' ', 1)[0]
    _attributes = {}

    if len(open.split(' ', 1)) > 1:
      _attributes = self._extract_attributes(open.split(' ', 1)[1])

    return (_type, _attributes)
  
  """
  def _parse_non_self_closing_tag(
    self,
    DOM: str,
    type: str, 
    attributes: dict, 
    parent: Optional[DOMNode]
  ) -> None:
    # <div><div></div><div></div></div>
    _should_stop = False

    _close_search_i = 0
    _mid_search_i = 0

    while not _should_stop:
      sleep(2)
      _close_search = re.search(f'</{type}>', DOM[_close_search_i:])

      if _close_search:                           # close tag found
        _close_i, _close_f = _close_search.span()

        _mid_search = re.search(f'<{type}[^<>]*>', DOM[_mid_search_i:])

        print('Close found')
        print(type)
        print(attributes)
        print(_close_i, _close_f)
        

        if _mid_search:
          _close_search_i = _close_search_i + _close_f
          _mid_search_i = _mid_search_i + _mid_search.span()[1]
          print('Mid found')
          print(_mid_search_i)
          print(_mid_search.group())
          print(_close_search_i)
          print(_close_search.group())
          print(f'Mid: {DOM[_mid_search_i:]}')
          print(f'Close: {DOM[_close_search_i:]}')
          print()
        else:                                     # end loop
          print('No Mid Found')
          print(f'Children: {DOM[:_close_search_i]}')
          print(f'Remainder: {DOM[_close_search_i + _close_f:]}')
          print()
          _should_stop = True
          
          # create node and parse children
          _node = self._create_node(
            type=type,
            attributes=attributes,
            parent=parent
          )

          # parse children
          self._parse_DOM(DOM[:_close_search_i], _node)

          # parse rest of dOM
          self._parse_DOM(DOM[_close_search_i + _close_f:], parent)

      else:                                       # close tag not found
        _should_stop = True

        # parse rest as child
        
        print('Close not found')
        print(DOM)
        print(type)
        print(attributes)
        print()
        
        _node = self._create_node(
          type=type,
          attributes=attributes,
          parent=parent
        )

        self._parse_DOM(DOM, _node)
  """

  def _parse_non_self_closing_tag(
    self,
    DOM: str,
    type: str, 
    attributes: dict, 
    parent: Optional[DOMNode]
  ) -> None:
    Z  = '<div class="container"><div class="one"></div><div class="two"></div></div>'
    ZR = '<div class="one"></div><div class="two"></div></div>'
    A  = '<div class="one"><div class="inner"></div></div><div class="two"></div>'
    AR = '</div><div class="two"></div>'
    B  = '<div class="two"></div>'
    BR = '</div>'
    C  = ''

    _stop = False

    _cls_i, _cls_f = 0, 0
    _mid_i, _mid_f = 0, 0

    # look for close, update close search i
    # if close, look for mid between mid i and close i
    # if mid, update mid_search and close_search
    
    while not _stop:
      _cls_search = re.search(f'</{type}>', DOM[_cls_f:])

      if _cls_search:
        _cls_i = _cls_search.span()[0] + _cls_f
        _cls_f = _cls_search.span()[1] + _cls_f

        _mid_search = re.search(f'<{type}[^<>]*>', DOM[_mid_f:_cls_i])

        if _mid_search:
          print('sadf')
          _mid_i = _mid_search.span()[0] + _mid_f
          _mid_f = _mid_search.span()[1] + _mid_f
        else:
          print(DOM[_cls_i:])
          _stop = True

          # parse children
          _node = self._create_node(
            type,
            attributes,
            parent
          )

          self._parse_DOM(DOM[:_cls_i], _node)

          # parse remainder
          self._parse_DOM(DOM[_cls_f:], parent)
      else:
        print('ds')
        _stop = True
      
    """
    while not _should_stop:
      sleep(2)
      _close_search = re.search(f'</{type}>', DOM[_close_search_i:])

      if _close_search:                           # close tag found
        _close_i, _close_f = _close_search.span()

        _mid_search = re.search(f'<{type}[^<>]*>', DOM[_mid_search_i:])

        if _mid_search:
          _close_search_i = _close_search_i + _close_f
          _mid_search_i = _mid_search_i + _mid_search.span()[1]
          print('Mid found')
          print(_mid_search_i)
          print(_mid_search.group())
          print(_close_search_i)
          print(_close_search.group())
          print(f'Mid: {DOM[_mid_search_i:]}')
          print(f'Close: {DOM[_close_search_i:]}')
          print()
        else:                                     # end loop
          print('No Mid Found')
          print(f'Children: {DOM[:_close_search_i]}')
          print(f'Remainder: {DOM[_close_search_i + _close_f:]}')
          print()
          _should_stop = True
          
          # create node and parse children
          _node = self._create_node(
            type=type,
            attributes=attributes,
            parent=parent
          )

          # parse children
          self._parse_DOM(DOM[:_close_search_i], _node)

          # parse rest of dOM
          self._parse_DOM(DOM[_close_search_i + _close_f:], parent)

      else:                                       # close tag not found
        _should_stop = True

        # parse rest as child
        _node = self._create_node(
          type=type,
          attributes=attributes,
          parent=parent
        )

        self._parse_DOM(DOM, _node)
  """
  

  def _parse_DOM(self, DOM: str, parent: Optional[DOMNode]=None) -> None:
    if DOM:                                       # if string is not empty
      # search for open tag
      _open_search = re.search('<[^<>]+>', DOM)

      if _open_search:                            # open tag found
        _open_i, _open_f = _open_search.span()
        
        if _open_i != 0:                          # text at start of string
          self._create_node(
            type='text',
            attributes={
              'content': DOM[:_open_i]
            },
            parent=parent
          )

          # parse with remainder of DOM after text
          self._parse_DOM(DOM[_open_i:], parent)
        else:                                     # element at start of string
          _type, _attributes = self._parse_open_tag(DOM[_open_i:_open_f])

          if _type in self.self_closing_elements:  # element is self-closing
            self._create_node(_type, _attributes, parent)

            # parse with remainder of DOM after self-closing tag
            self._parse_DOM(DOM[_open_f:], parent)
          else:                                   # element is not self-closing
            self._parse_non_self_closing_tag(
              DOM[_open_f:],
              _type,
              _attributes,
              parent
            )

      else:                                       # open tag not found
        # everything treated as text
        self._create_node(
          type='text',
          attributes={
            'content': DOM
          },
          parent=parent
        )
      

  """
  def _parse_DOM(self, DOM: str, parent: Optional[DOMNode]=None) -> None:
    _node = None

    if DOM:
      # search for open tag
      _open_search = re.search('<[^<>]+>', DOM)

      if _open_search:                    # if tag found, continue
        _open_i, _open_f = _open_search.span()

        if _open_i == 0:                  # if tag is at beginning, continue
          # extract open tag and remove from DOM
          _open = DOM[_open_i + 1:_open_f - 1]
          DOM = DOM[_open_f:]

          # extract type
          _type = _open.split(' ', 1)[0]

          # sanitize potential closing tag for self closing elements
          if _open[-1] == '/':
            _open = _open[:-1]

          # extract attributes
          _attributes = {}

          if len(_open.split(' ')) > 1: # if tag has attributes
            _attributes = self._extract_attributes(_open.split(' ', 1)[1])
          
          _node = DOMNode(
            type=_type,
            attributes=_attributes
          )

          if _type not in self.self_closing_elements: # not self-closing, continue





            # search for close tag
            # must have matched tags of same type within bounds of closing tag

            # find first closing tag
            _close_search_start = 0
            _should_stop = False

            while not _should_stop:
              print(_close_search_start)
              _close_search = re.search(f'</{_type}>', DOM[_close_search_start:])

              if _close_search:
                _close_i, _close_f = _close_search.span()

                _mid_open_search = re.search(f'<{_type} [^<>]*>', DOM[_close_search_start:])

                if _mid_open_search:
                  _close_search_start = _close_f
                  # continue loop
                else:
                  _should_stop = True

                  self._parse_DOM(DOM[:_close_i], _node)    # parse children
                  self._parse_DOM(DOM[_close_f:], parent)    # parse remainder
              
              else:
                _should_stop = True

                self._parse_DOM(DOM, _node)                 # parse children






          else:                           # self-closing
            # continue with rest of DOM
            self._parse_DOM(DOM, parent)
            
        else:                             # else remove treat beginning as text
          _node = DOMNode(
            type='text',
            attributes={
              'content': DOM[:_open_i]
            }
          )

          # continue with rest of DOM
          self._parse_DOM(DOM[_open_f:], parent)
      else:                               # else treat all DOM as text
        _node = DOMNode(
          type='text',
          attributes={
            'content': DOM
          }
        )

      if _node:
        self._insert_typed_element(_node)

        if parent:
          parent.insert_child(_node)
        else:
          self.elements.insert_child(_node)

  """
  """

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
            if _DOM_type == 'script':
              _node.insert_attribute('script', _children)
            else:
              if _children != '':
                self._parse_DOM(_children, _node)

        # parse rest of DOM string
        if DOM != '':
          self._parse_DOM(DOM, parent)
  """