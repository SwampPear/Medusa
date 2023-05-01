from medusa.webdriver.webdriver import WebDriver


class Bot:
  """
  Represents an automated process for which all logic will be run through.
  """

  def __init__(self, domains):
    """
    Initializes this Bot object.
    """
    
    self.web_driver = WebDriver()


  def run(self):
    """
    Main loop for this bot.
    """
    pass


domains = [
  'data.mail.yahoo.com',
  'le.yahooapis.com',
  'onepush.query.yahoo.com',
  'proddata.xobni.yahoo.com',
  'apis.mail.yahoo.com',
]