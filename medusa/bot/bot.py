from medusa.webdriver.webdriver import WebDriver


class Bot:
  """
  Represents an automated process for which all logic will be run through.
  """

  def __init__(self):
    """
    Initializes this Bot object.
    """
    
    self.web_driver = WebDriver()


  def run(self):
    """
    Main loop for this bot.
    """
    print(self.web_driver.session_id)
    self.web_driver.go_to_url('https://www.google.com')
    self.web_driver.exit()