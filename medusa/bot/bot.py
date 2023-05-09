from medusa.browser.browser import Browser
from time import sleep


class Bot:
  def __init__(self) -> None:
    """
    Initializes this Bot object.
    """
    
    self._print_welcome()
    #self.browser = Browser()

  
  def _print_welcome(self):
    """
    Prints the welcome screen for the CLI.
    """

    _message = [
      '    __  _____________  __  _______ ___ ',
      '   /  |/  / ____/ __ \/ / / / ___//   |',
      '  / /|_/ / __/ / / / / / / /\__ \/ /| |',
      ' / /  / / /___/ /_/ / /_/ /___/ / ___ |',
      '/_/  /_/_____/_____/\____//____/_/  |_|',
      '@swamppear',
      'v0.0.1',
    ]
    _message = '\n'.join(_message)
    

    print(f"\033[92m{_message}\033[0m")
                                       

  def run(self):
    """
    Main loop for this bot.
    """

    self.browser.go_to_url('https://www.google.com')
    sleep(100)
    self.browser.exit()