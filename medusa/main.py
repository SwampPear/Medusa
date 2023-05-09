import sys
import os
import requests


sys.path[0] = sys.argv[1]


from medusa.bot import Bot
from medusa.crawler.parser import Parser


if __name__ == '__main__':
  #_bot = Bot()
  sys.stdout.write('\u001b[36mtest\n')
  sys.stdout.flush()

  #_bot.run()
  #url = 'https://www.google.com'
  #res = requests.get(url)
  #print(res.cookies)
  #parsed = Parser(res)

# access site
# crawl around and scan for vulnerabilities
