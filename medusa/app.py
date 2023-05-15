import sys
from medusa.browser.browser import Browser
from medusa.cli import CLI, Color


class App:
  def __init__(self) -> None:
    #self.browser = Browser()
    self._browser = None
    self._cli = CLI()

  
  def _execute_command(self, input: str) -> None:
    _args = input.split(' ')
    _command = _args[0].lower()

    if _command == 'exit': self._exit()
    elif _command == 'clear': self._cli.clear()


  def _exit(self) -> None:
    if self._browser: self._browser.exit()

    self._cli.write('Medusa terminated.', Color.INFO, True)
    sys.exit(0)


  def run(self) -> None:
    while True:
      _input = self._cli.read(
        '~ ',
        Color.DELIMITER,
        True
      )
      
      self._execute_command(_input)