import sys
import requests


sys.path[0] = sys.argv[1]


from medusa.app import App
from medusa.crawler.parser import Parser


if __name__ == '__main__':
  #_app = App()
  #_app.run()

  a = requests.get('https://www.waspbarcode.com')
  b = Parser(a)

  for element in b.typed_elements['a']:
    print(element)