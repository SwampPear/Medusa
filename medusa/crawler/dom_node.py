class DOMNode:
  """
  Represents a DOM object to be used with a DOM Parser object.
  """

  def __init__(self, type, attributes=None, parent=None) -> None:
    """
    Initializes this Parser object.

    Parameters:
    str:type - the type of DOM element this Node represents
    dict:attributes - the attributes represented by this DOM element
    Node:parent - the parent node to this DOM element
    """

    self._type = type
    self._attributes = attributes
    self._parent = parent
    self._children = []

  
  def __str__(self):
    """
    Formats a pretty string to print representing this DOMNode.
    """

    _children = []

    for _child in self._children:
      _children.append(str(_child))

    _output = f'Type: {self._type}; Attributes: {self._attributes}; Children: {_children}'

    return _output

  
  def insert_child(self, child):
    """
    Inserts a child DOMNode into this DOMNode.

    Parameters:
    DOMNode:child - the node to insert
    """
    self._children.append(child)