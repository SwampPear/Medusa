from typing import Union, Optional
from subprocess import Popen, PIPE
import sys
import requests
from time import sleep
from medusa.exceptions import BrowserInitializationError


DRIVER_PATH = f'{sys.argv[1]}/drivers/chrome/chromedriver'
ADDRESS = 'http://localhost:9515'
SESSION_ID_REQUEST_BODY = {
  'desiredCapabilities': {
    'caps': {
        'nativeEvents': False,
        'browserName': 'chrome',
        'version': '',
        'platform': 'ANY'
    }
  }
}


class Browser:
  def __init__(self) -> None:
    self.popen = self._init_driver()
    self.session_id = self._get_session_id()


  def _fmt_url(self, session_id: bool=False, command: str='/') -> str:
    _url = f'{ADDRESS}/session'

    if session_id:
      _url += f'/{self.session_id}'

      _url += command

    return _url


  def _get_session_id(self) -> str:
    _attempts = 0

    while _attempts < 5:
      try:
        # get session id
        _url = self._fmt_url()
        _res = requests.post(
          _url, 
          json=SESSION_ID_REQUEST_BODY
        ).json()

        return _res['sessionId']
      except:
        _attempts += 1
        sleep(1)

      if _attempts >= 5:
        self.exit()
        raise BrowserInitializationError('Failed to get session id.')


  def _init_driver(self) -> Popen:
    try:
      return Popen([
        DRIVER_PATH,
        '--headless=new',
        'start-maximized',
        '--disable-gpu',
        '--disable-extensions'
      ],
        stdout=PIPE
      )

    except:
      self.exit()
      raise BrowserInitializationError('Failed to initialize chrome driver.')
    

  def _kill(self) -> None:
    self.popen.kill()


  def _quit_browser(self) -> None:
    requests.delete(self._fmt_url(session_id=True))


  def exit(self) -> None:
    self._quit_browser()
    self._kill()

  
  def _execute_command(
    self, 
    command: str, 
    type: str, 
    body: Optional[dict]=None
  ) -> dict:
    if type == 'GET':
      return requests.get(
        self._fmt_url(session_id=True, command=command)
      ).json()
    elif type == 'POST':
      return requests.post(
        self._fmt_url(session_id=True, command=command),
        json=body
      ).json()


  def get_current_window_handle(self) -> dict:
    return self._execute_command('window_handle', type='GET')['value']
  

  def get_available_window_handles(self) -> dict:
    return self._execute_command('window_handles', type='GET')['value']
  

  def get_current_url(self) -> dict:
    return self._execute_command('url', type='GET')['value']
  

  def go_to_url(self, url) -> dict:
    return self._execute_command(
      'url', 
      type='POST', 
      body = {
        'url': url
      }
    )

  
  def forward(self) -> dict:
    return self._execute_command('forward', type='POST')

  
  def back(self) -> dict:
    return self._execute_command('back', type='POST')


  def refresh(self) -> dict:
    return self._execute_command('refresh', type='POST')

  



  def execute(self, script, args=None):
    _body = {
      'script': script
    }

    if args:
      _body['args'] = args

    self._execute_command(
      'execute', 
      type='post', 
      body = _body
    )

  def execute_async(self, script, args=None):
    """
    Executes a script in the currently selected frame.

    Parameters:
    str:script - the script to execute
    []:args - the script arguments

    Returns:
    *: value returned from the script
    """

    _body = {
      'script': script
    }

    if args:
      _body['args'] = args

    self._execute_command(
      'execute_async', 
      type='post', 
      body = _body
    )