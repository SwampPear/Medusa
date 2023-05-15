import sys
from medusa.browser.browser import Browser
from medusa.cli import CLI, Color


class App:
  def __init__(self) -> None:
    self._browser = None
    self._cli = CLI()

  
  def _execute_command(self, input: str) -> None:
    _args = input.split(' ')
    _cmd = _args[0].lower()

    if _cmd == 'exit': self._exit()
    elif _cmd == 'clear': self._clear()
    else: self._invalid(_cmd)


  def _exit(self) -> None:
    if self._browser: self._browser.exit()

    self._cli.write('Medusa terminated.', Color.INFO, True)
    sys.exit(0)

  
  def _clear(self) -> None:
    self._cli.clear()

  
  def _invalid(self, command: str) -> None:
    self._cli.write(f'Invalid command: {command}', Color.DANGER, True)


  def run(self) -> None:
    while True:
      _input = self._cli.read(
        '~ ',
        Color.DELIMITER,
        True
      )
      
      self._execute_command(_input)