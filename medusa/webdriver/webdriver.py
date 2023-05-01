import subprocess
import sys
import requests
from time import sleep
from medusa.webdriver.exceptions import DriverInitializationError


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


class WebDriver:
  """
  Interface to interact with chrome using the chromium webdriver.
  """
  def __init__(self):
    """
    Initializes this WebDriver object.
    """
    self.popen = self._init_driver()
    self.session_id = self._get_session_id()


  def _fmt_url(self, session_id=False, command=None):
    """
    Formats a url for usage with the JSON wire protocol.

    Parameters:
    bool:session_id - session id used or not
    str:command - command to be used

    Returns:
    str:the formatted url
    """
    _url = f'{ADDRESS}/session'

    if session_id:
      _url += f'/{self.session_id}'

      if command:
        _url += f'/{command}'

    return _url


  def _get_session_id(self):
    """
    Gets a valid session id for this webdriver session.

    Returns:
    str:session id

    Throws:
    DriverInitializationError:error on request failing
    """
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
        raise DriverInitializationError('Failed to get session id.')


  def _init_driver(self):
    """
    Initializes the driver process for this webdriver.

    Returns:
    subprocess.Popen:driver process

    Throws:
    DriverInitializationError:error on driver creation failing
    """
    try:
      return subprocess.Popen([
        DRIVER_PATH,
        '--headless'
      ])

    except:
      self.exit()
      raise DriverInitializationError('Failed to initialize chrome driver.')
    

  def _kill(self):
    """
    Kills the webdriver process.
    """
    self.popen.kill()


  def _quit_browser(self):
    """
    Quits the browser.
    """
    _url = self._fmt_url(session_id=True)
    requests.delete(_url)


  def exit(self):
    """
    Exits the program and deallocates all running processes.
    """
    self._quit_browser()
    self._kill()

  
  def _execute_command(self, command, type, body=None):
    """
    Executes a given command.

    Parameters:
    str:command - the command to execute

    Returns:
    json:response
    """

    if type == 'get':
      return requests.get(
        self._fmt_url(session_id=True, command=command)
      ).json()
    elif type == 'post':
      return requests.post(
        self._fmt_url(session_id=True, command=command),
        json=body
      ).json()


  def get_current_window_handle(self):
    """
    Gets the current window handle.

    Returns:
    str:current window handle
    """
    return self._execute_command('window_handle', type='get')['value']
  

  def get_available_window_handles(self):
    """
    Gets all available window handles.

    Returns:
    str[]:list of available window handles
    """
    return self._execute_command('window_handles', type='get')['value']
  

  def get_current_url(self):
    """
    Gets the current url.

    Returns:
    str:current url
    """
    return self._execute_command('url', type='get')['value']
  

  def go_to_url(self, url):
    """
    Goes to a url.

    Parameters:
    str:url - the url to navigate to
    """
    self._execute_command(
      'url', 
      type='post', 
      body = {
        'url': url
      }
    )

  
  def forward(self):
    """
    Goes forward in browser history if possible.
    """
    self._execute_command('forward', type='post')

  
  def back(self):
    """
    Goes forward in browser history if possible.
    """
    self._execute_command('back', type='post')


  def refresh(self):
    """
    Goes forward in browser history if possible.
    """
    self._execute_command('refresh', type='post')

  
  def execute(self, script, args=None):
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