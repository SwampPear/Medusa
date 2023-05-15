import sys
from medusa.browser.browser import Browser
from medusa.cli import CLI, Color


class App:
  def __init__(self) -> None:
    self.browser = None
    self.cli = CLI()

  
  def _execute_command(self, input: str) -> None:
    args = input.split(' ')
    cmd = args[0].lower()

    if cmd == 'exit':
      self._exit()
    elif cmd == 'clear':
      self._clear()
    else:
      self._invalid(cmd)


  def _exit(self) -> None:
    if self.browser:
      self.browser.exit()

    self.cli.write('Medusa terminated.', Color.INFO, True)
    sys.exit(0)

  
  def _clear(self) -> None:
    self.cli.clear()

  
  def _invalid(self, command: str) -> None:
    self.cli.write(f'Invalid command: {command}', Color.DANGER, True)


  def run(self) -> None:
    while True:
      input = self.cli.read('~ ', Color.DELIMITER, True)
      self._execute_command(input)