import sys
import requests
from time import sleep


sys.path[0] = sys.argv[1]


from medusa.app import App
from medusa.crawler.parser import Parser


if __name__ == '__main__':
  _app = App()
  _app.run()

  a = requests.get('http://127.0.0.1:8000')#'https://www.blackdogcustoms.com')
  b = Parser(a)

  for el in b.typed_elements:
    print(el)