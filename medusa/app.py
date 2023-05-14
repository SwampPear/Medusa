from medusa.browser.browser import Browser
from medusa.cli import CLI, Color
from time import sleep


class App:
  def __init__(self) -> None:
    self.browser = Browser()

  
  def _print_welcome(self) -> None:
    CLI.write(
      '\n'.join([
        '    __  _____________  __  _______ ___ ',
        '   /  |/  / ____/ __ \/ / / / ___//   |',
        '  / /|_/ / __/ / / / / / / /\__ \/ /| |',
        ' / /  / / /___/ /_/ / /_/ /___/ / ___ |',
        '/_/  /_/_____/_____/\____//____/_/  |_|',
        '@swamppear',
        'v0.0.1'
      ]), 
      color=Color.GREEN, 
      bold=True
    )
    CLI.write()
    CLI.write(
      '\n'.join([
        'Usage:',
        ' --- <command> --help',
        ' --- crawl <url> (IN PROGRESS)',
        ' --- fuzz <url> <flags> (NOT IMPLEMENTED)'
      ]), 
      color=Color.GREEN
    )


  def run(self) -> None:
    self._print_welcome()

    self.browser.go_to_url('https://www.google.com')
    sleep(100)
    self.browser.exit()