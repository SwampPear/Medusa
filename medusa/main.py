import sys
import requests
from time import sleep


sys.path[0] = sys.argv[1]


from medusa.app import App
from medusa.crawler.parser import Parser
import re


if __name__ == '__main__':
  _app = App()
  _app.run()
  #<td\s*.*>\s*.*<\/td>
  text = '<div><div class="one">Testing one</div><div class="two">Testing two</div></div>'

  a = requests.get('http://127.0.0.1:8000')#'https://www.blackdogcustoms.com')
  b = Parser(a)
  print(b.elements)

  #for el in b.typed_elements:
  #  print(el)