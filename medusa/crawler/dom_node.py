from typing import Optional


class DOMNode:
  def __init__(
    self, 
    type: str, 
    attributes: Optional[dict]=None, 
    parent: Optional['DOMNode']=None
  ) -> None:
    self.type = type
    self._attributes = attributes
    self._parent = parent
    self._children = []

  
  def __str__(self) -> str:
    _children = []

    for _child in self._children:
      _children.append(str(_child))

    _output = f'Type: {self.type}; Attributes: {self._attributes}; Children: {_children}'

    return _output

  
  def insert_child(self, child) -> None:
    self._children.append(child)