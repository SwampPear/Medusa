import sys
sys.path[0] = sys.argv[1]
import requests


from medusa.app import App


if __name__ == '__main__':
  #_app = App()
  #_app.run()


  proxy = {
    'http': 'http://localhost:8080',
    'https': 'http://localhost:8080',
  }

  a = requests.get('http://localhost:8000', proxies=proxy)
  #a = requests.get('https://www.realpython.com', proxies=proxy)