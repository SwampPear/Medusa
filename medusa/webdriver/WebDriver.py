import subprocess
import requests
from medusa.common.constants import DRIVER_PATH, ADDRESS, SESSION_ID_REQUEST_BODY
from medusa.common.exceptions import DriverInitializationError
from time import sleep


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
        _res = requests.post(
          f'{ADDRESS}/session', 
          json=SESSION_ID_REQUEST_BODY
        ).json()

        return _res['sessionId']
      except:
        _attempts += 1
        sleep(1)

      if _attempts >= 5:
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
    _url = f'{ADDRESS}/session/{self.session_id}'
    _res = requests.delete(_url)

  def exit(self):
    """
    Exits the program and deallocates all running processes.
    """
    self._quit_browser()
    self._kill()

