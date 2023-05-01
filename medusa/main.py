import sys
import os


sys.path[0] = os.getcwd()


from medusa.bot.bot import Bot


if __name__ == '__main__':
  _bot = Bot()
  _bot.run()