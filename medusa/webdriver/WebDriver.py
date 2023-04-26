import subprocess
import requests
from medusa.common.constants import DRIVER_PATH, ADDRESS, SESSION_ID_REQUEST_BODY
from medusa.common.exceptions import DriverInitializationError
from time import sleep


class WebDriver:
  def __init__(self):
    self.popen = self._init_driver()
    self.session_id = self._get_session_id()

  def _get_session_id(self):
    """
    Gets a valid session id for this webdriver session.
    """
    """
    Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

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
    try:
      return subprocess.Popen([
        DRIVER_PATH, 
        '--headless'
      ])

    except:
      raise DriverInitializationError('Failed to initialize chrome driver.')