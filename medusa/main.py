import sys
import os


sys.path[0] = os.getcwd()


from medusa.webdriver.webdriver import WebDriver


if __name__ == '__main__':
  a = WebDriver()
  print(a.session_id)
  a.go_to_url('https://www.google.com')
  a.exit()