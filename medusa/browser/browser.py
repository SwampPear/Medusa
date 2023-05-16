from typing import Optional
from subprocess import Popen, PIPE
import sys
import requests
from time import sleep
from medusa.exceptions import BrowserInitializationError


class Browser:
  def __init__(self) -> None:
    self.popen = self._init_driver()
    self.session_id = self._get_session_id()
  

  def _fmt_url(self, cmd: str='', session_id: bool=True) -> str:
    url = 'http://localhost:8888/session'

    if session_id:
      url += f'/{self.session_id}'

      if cmd:
        url += f'/{cmd}'

    return url


  def _get_session_id(self) -> str:
    attempts = 0

    while attempts < 5:
      try:
        url = self._fmt_url(session_id=False)
        res = requests.post(
          url, 
          json={
            'desiredCapabilities': {
              'caps': {
                'nativeEvents': False,
                'browserName': 'chrome',
                'version': '',
                'platform': 'ANY'
              }
            }
          }
        ).json()

        return res['sessionId']
      except:
        attempts += 1
        sleep(1)

    self.exit()

    raise BrowserInitializationError('Failed to get session id.')


  def _init_driver(self) -> Popen:
    try:
      return Popen([
        f'{sys.argv[1]}/drivers/chrome/chromedriver',
        '--port=8888'
        #'--headless=new',
        #'start-maximized',
        #'--disable-gpu',
        #'--disable-extensions'
      ],
        stdout=PIPE
      )

    except:

      self.exit()
      raise BrowserInitializationError('Failed to initialize driver.')


  def exit(self) -> None:
    requests.delete(self._fmt_url())    # kill browser window
    self.popen.kill()                   # kill process
    
  
  def _execute_command(
    self, 
    cmd: str, 
    method: str, 
    body: Optional[dict]=None
  ) -> dict:
    url = self._fmt_url(cmd)

    if method == 'GET':
        return requests.get(url).json()
    elif method == 'POST':
      return requests.post(url, json=body).json()


  def get_window_handle(self) -> dict:
    return self._execute_command('window_handle', 'GET')['value']
  

  def get_window_handles(self) -> dict:
    return self._execute_command('window_handles', 'GET')['value']
  

  def get_url(self) -> dict:
    return self._execute_command('url', 'GET')['value']
  

  def url(self, url) -> dict:
    return self._execute_command('url', 'POST', {'url': url})

  
  def forward(self) -> dict:
    return self._execute_command('forward', 'POST')

  
  def back(self) -> dict:
    return self._execute_command('back', 'POST')


  def refresh(self) -> dict:
    return self._execute_command('refresh', 'POST')

  


  """
  def execute(self, script, args=None):
    _body = {
      'script': script
    }

    if args:
      _body['args'] = args

    self._execute_command(
      'execute', 
      method='post', 
      body = _body
    )

  def execute_async(self, script, args=None):
    _body = {
      'script': script
    }

    if args:
      _body['args'] = args

    self._execute_command(
      'execute_async', 
      method='post', 
      body = _body
    )
  """