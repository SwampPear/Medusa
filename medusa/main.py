import sys
import os

sys.path[0] = os.getcwd()


from medusa.webdriver.WebDriver import WebDriver


if __name__ == '__main__':
  a = WebDriver()