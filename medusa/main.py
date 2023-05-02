import sys
import os
import requests


sys.path[0] = sys.argv[1]


from medusa.bot.bot import Bot
from medusa.crawler.parser import Parser


if __name__ == '__main__':
  #_bot = Bot()
  #_bot.run()
  url = 'http://127.0.0.1:8000/'
  res = requests.get(url)
  parsed = Parser(res)

# access site
# crawl around and scan for vulnerabilities
