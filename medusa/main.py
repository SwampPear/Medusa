import sys
import requests
from time import sleep


sys.path[0] = sys.argv[1]


from medusa.app import App
from medusa.crawler.parser import Parser


if __name__ == '__main__':
  _app = App()
  _app.run()

  sleep(3)

  a = requests.get('https://www.blackdogcustoms.com')
  #b = Parser(a)
  print(a.text)

  #for element in b.typed_elements['a']:
  #  print(element._attributes['href'])