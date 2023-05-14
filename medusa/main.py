import sys
sys.path[0] = sys.argv[1]


from medusa.app import App


if __name__ == '__main__':
  _app = App()
  _app.run()