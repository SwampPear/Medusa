from medusa.browser.browser import Browser
from medusa.cli import CLI, Color
from time import sleep


class App:
  def __init__(self) -> None:
    #self.browser = Browser()
    self.browser = None

  
  def _print_welcome(self) -> None:
    CLI.write(
      '\n'.join([
        '    __  _____________  __  _______ ___ ',
        '   /  |/  / ____/ __ \/ / / / ___//   |',
        '  / /|_/ / __/ / / / / / / /\__ \/ /| |',
        ' / /  / / /___/ /_/ / /_/ /___/ / ___ |',
        '/_/  /_/_____/_____/\____//____/_/  |_|',
        '@swamppear',
        'v0.0.2'
      ]), 
      color=Color.GREEN, 
      bold=True
    )


  def run(self) -> None:
    self._print_welcome()

    #self.browser.go_to_url('https://www.google.com')
    #sleep(10)
    #self.browser.exit()