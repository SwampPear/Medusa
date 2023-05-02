from medusa.browser.browser import Browser


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

    self.browser.go_to_url('https://www.google.com')
    self.browser.exit()