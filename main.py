import subprocess
import requests
from medusa.bot import DRIVER_PATH
from time import sleep


class WebDriver:
  def __init__(self):
    self.address = 'http://localhost:9515'

    self._init_chrome_driver()

  def _init_chrome_driver(self):
    try:
      # create chromedriver process
      self.popen = subprocess.Popen(['drivers/chrome/chromedriver', '--headless'])

      _attempts = 0
      _valid_driver = False

      while _attempts < 5 and not _valid_driver:
        try:
          # get session id
          _res = requests.post(
            f'{self.address}/session', 
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
          )

          self.session_id = _res.json()['sessionId']
          _valid_driver = True
        except:
          # sleep for one second between tries
          _attempts += 1
          sleep(1)

        if _attempts >= 5:
          raise Exception('Failed to get session id.')

      self.popen.kill()
    except:
      raise Exception('Failed to initialize chrome driver.')
    
q = WebDriver()