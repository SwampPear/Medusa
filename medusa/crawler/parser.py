from typing import Optional, Tuple
import re
from requests import Response
from medusa.crawler.algorithm import Node
from medusa.crawler.constants import SELF_CLOSING_ELEMENTS, NON_DOM_PARENTS


class Parser:
  def __init__(self, response: Response) -> None:
    self.status = response.status_code
    self.headers = response.headers
    self.cookies = response.cookies
    self.raw_text = response.text

    self.tree = Node(type='dom_tree')
    self.elements = {}

    self._parse_DOM(self._sanitize_DOM(response.text))


  def _sanitize_DOM(self, DOM: str) -> str:
    DOM = DOM.replace('\n', '')
    DOM = re.sub('\s+<', '<', DOM)
    DOM = re.sub('>\s+', '>', DOM)

    return DOM


  def _insert_element(self, element: Node) -> None:
    self.elements.setdefault(element.type, []).append(element)


  def _extract_attributes(self, DOM: str) -> dict:
    attrs = {}

    # extract and remove non-empty attributes
    non_empty_attrs = re.findall('[^"\s]*="[^"]*"|[^\'\s]*=\'[^\']*\'', DOM)
    for attr in non_empty_attrs: DOM = DOM.replace(attr, '')

    # extract empty attributes
    empty_attrs = [attr for attr in DOM.split(' ') if attr]

    # format non-empty attributres
    for attr in non_empty_attrs:
      attr_name, attr_value = attr.split('=', 1)
      attrs[attr_name] = attr_value[1:-1]

    # format empty attributes
    for attr in empty_attrs: attrs[attr] = True

    return attrs
  

  def _create_node(
    self, 
    type: str, 
    attributes: dict, 
    parent: Optional[Node]=None
  ) -> Node:
    node = Node(type=type, attributes=attributes)
    self._insert_element(node)

    if parent:
      parent.insert_child(node)
    else:
      self.tree.insert_child(node)

    return node


  def _insert_node(
    self,
    node: Node,
    parent: Optional[Node]=None
  ) -> None:
    self._insert_element(node)

    if parent:
      parent.insert_child(node)
    else:
      self.tree.insert_child(node)
  

  def _parse_open_tag(self, tag: str) -> Tuple[str, dict]:
    tag = tag.strip('<>')
    
    if tag.endswith('/'):
      tag = tag[:-1]
    
    tag = tag.split(maxsplit=1)
    dom_type = tag[0]
    attrs = self._extract_attributes(tag[1]) if len(tag) > 1 else {}
    
    return dom_type, attrs


  def _parse_non_self_closing_tag(
    self,
    DOM: str,
    type: str, 
    attributes: dict, 
    parent: Optional[Node]
  ) -> None:
    """
    Needs to be cleaned up
    """
    if type in NON_DOM_PARENTS:
      if type == '!--':
        _cls_search = re.search(f'-->', DOM)
      else:
        _cls_search = re.search(f'</{type}>', DOM)

      if _cls_search:
        _cls_i, _cls_f = _cls_search.span()

        # create node and parse remainder of document
        _node = self._create_node(
          type=type,
          attributes={
            'content': DOM[:_cls_i]
          },
          parent=parent
        )

        self._parse_DOM(DOM[_cls_f:], parent)
      else:
        # treat everything as script
        _node = self._create_node(
          type=type,
          attributes={
            'content': DOM
          },
          parent=parent
        )
    else:
      _stop = False

      _cls_i, _cls_f, _mid_f = 0, 0, 0
      
      while not _stop:
        _cls_search = re.search(f'</{type}>', DOM[_cls_f:])

        if _cls_search:
          _cls_i = _cls_search.span()[0] + _cls_f
          _cls_f = _cls_search.span()[1] + _cls_f

          _mid_search = re.search(f'<{type}[^<>]*>', DOM[_mid_f:_cls_i])

          if _mid_search:
            _mid_f = _mid_search.span()[1] + _mid_f
          else:
            #DOM[:_cls_i])
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
          _stop = True

          # treat reamainder as child
          _node = self._create_node(
            type,
            attributes,
            parent
          )

          self._parse_DOM(DOM, _node)

  

  def _parse_DOM(self, DOM: str, parent: Optional[Node]=None) -> None:
    """
    Needs to be cleaned up
    """
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

          if _type in SELF_CLOSING_ELEMENTS:  # element is self-closing
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

  
  def get_elements_by_type(self, type: str) -> list[Node]:
    return self.elements.get(type, [])

      
