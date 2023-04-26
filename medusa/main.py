import sys
import os
from medusa.webdriver.webdriver import WebDriver


sys.path[0] = os.getcwd()


if __name__ == '__main__':
  a = WebDriver()
  print(a.session_id)
  a.go_to_url('https://www.google.com')
  a.exit()