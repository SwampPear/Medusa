from medusa.browser.browser import Browser
from time import sleep


class Bot:
  """
  Represents an automated process for which all logic will be run through.
  """

  def __init__(self):
    """
    Initializes this Bot object.
    """
    
    self.browser = Browser()


  def run(self):
    """
    Main loop for this bot.
    """

    self.browser.go_to_url('http://127.0.0.1:8000/')
    sleep(10)
    self.browser.exit()