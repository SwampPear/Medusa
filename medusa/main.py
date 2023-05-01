import sys
import os


sys.path[0] = sys.argv[1]


from medusa.bot.bot import Bot


if __name__ == '__main__':
  print(sys.argv[1])
  _bot = Bot()
  #_bot.run()