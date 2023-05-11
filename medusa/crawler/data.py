class DOMNode:
  def __init__(
    self, 
    type: str, 
    attributes: dict={}
  ) -> None:
    self.type = type
    self._attributes = attributes
    self._children = []

  
  def __str__(self) -> str:
    _children = []

    for _child in self._children:
      _children.append(str(_child))

    _output = f'Type: {self.type}; Attributes: {self._attributes}; Children: {_children}'

    return _output
  

  def insert_child(self, child: 'DOMNode') -> None:
    self._children.append(child)


  def get_attribute(self, attribute: str) -> str:
    try:
      return self._attributes[attribute]
    except:
      return None