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

  
  def insert_attribute(self, key: str, value):
    #self._attributes[key] = value
    print(key)
    print(value)