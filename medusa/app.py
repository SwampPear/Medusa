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
    elif cmd == 'browser' and self.state != 'browser':
      self.state = 'browser'
    elif self.state == 'browser':
      self._browser(cmd, args)
    else:
      self._invalid(cmd)

  
  def _log(self, msg: str, color: str) -> None:
    if self.state:
      self.cli.write('[', Color.DELIMITER, True, end='', count=False)
      self.cli.write(f'{self.state}', Color.INFO, True, end='', count=False)
      self.cli.write('] ', Color.DELIMITER, True, end='', count=False)
    
    self.cli.write(msg, color)


  def _exit(self) -> None:
    if self.state:
      self.state = ''
    else:
      if self.browser:
        self.browser.exit()

      self._log('Medusa terminated.', Color.INFO)
      sys.exit(0)

  
  def _clear(self) -> None:
    self.cli.clear()

  
  def _invalid(self, command: str) -> None:
    self.cli.write(f'Invalid command: {command}', Color.DANGER)


  def _browser(self, cmd: str, args: list[str]) -> None:
    if cmd == 'activate':
      self._browser_activate()
    elif cmd == 'deactivate':
      self._browser_deactivate()
    else:
      self._invalid(cmd)

  
  def _browser_activate(self) -> None:
    if not self.browser:
      try:
        self._log('Browser activating...', Color.INFO)
        self.browser = Browser()
        self._log('Browser activated.', Color.SUCCESS)
        self.browser.url(self.search_engine)
      except:
        self._log('Browser failed to activate.', Color.DANGER)


  def _browser_deactivate(self) -> None:
    if self.browser:
      try:
        self._log('Browser deactivating...', Color.INFO)
        self.browser.exit()
        self.browser = None
        self._log('Browser deactivated.', Color.SUCCESS)
      except:
        self._log('Browser failed to deactivate.', Color.DANGER)


  def run(self) -> None:
    while True:
      if self.state:
        self.cli.write('[', Color.DELIMITER, True, end='', count=False)
        self.cli.write(f'{self.state}', Color.INFO, True, end='', count=False)
        input = self.cli.read('] ~ ', Color.DELIMITER, True)
      else:
        input = self.cli.read(f'~ ', Color.DELIMITER, True)

      self._execute_command(input)