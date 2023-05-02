import requests
from requests import Response


class Parser:
  def __init__(self, response: Response) -> None:
    """
    Initializes this Parser object.
    """
    self._response = response


  def _parse_DOM(self) -> None:
    """
    Parses DOM in a given response.
    """

    pass

    
url = 'https://github.com/SwampPear/Medusa'
res = requests.get(url)
print(res.text)