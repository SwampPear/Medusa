import sys
from medusa.browser.browser import Browser
from medusa.cli import CLI, Color


class App:
  def __init__(self) -> None:
    self.search_engine = 'https://www.google.com'
    self.browser = None

    self.cli = CLI()
    self.state = ''

  
  def _execute_command(self, input: str) -> None:
    args = input.split(' ')
    cmd = args[0].lower()

    if cmd == 'exit':
      self._exit()
    elif cmd == 'clear':
      self._clear()
    elif cmd == 'browser':
      self._browser()
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


  def _browser(self) -> None:
    self.state = 'browser'
    self.browser = Browser()
    self.browser.go_to_url(self.search_engine)


  def run(self) -> None:
    while True:
      if self.state:
        self.cli.write('[', Color.DELIMITER, True, end='', count=False)
        self.cli.write(f'{self.state}', Color.INFO, True, end='', count=False)
        input = self.cli.read('] ~ ', Color.DELIMITER, True)
      else:
        input = self.cli.read(f'~ ', Color.DELIMITER, True)
        
      self._execute_command(input)