class Node:
  def __init__(self, type: str, attributes: dict={}) -> None:
    self.type = type
    self.attributes = attributes
    self.children = []


  def __str__(self) -> str:
    children = [str(child) for child in self.children]
    output = f'Type: {self.type}; Attributes: {self.attributes}; Children: {children}'
    
    return output


  def insert_child(self, child: 'Node') -> None:
    self.children.append(child)


  def get_attribute(self, attribute: str) -> str:
    return self.attributes.get(attribute, None)