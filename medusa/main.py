import sys


sys.path[0] = sys.argv[1]


from medusa.bot import Bot
from medusa.crawler.parser import Parser
from medusa.cli import CLI, FG


if __name__ == '__main__':
  #_bot = Bot()
  CLI.write('test', FG.GREEN)

  #_bot.run()
  #url = 'https://www.google.com'
  #res = requests.get(url)
  #print(res.cookies)
  #parsed = Parser(res)

# access site
# crawl around and scan for vulnerabilities
