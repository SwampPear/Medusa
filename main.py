import subprocess
import os
import requests
from medusa.common import CHROME_DRIVER_PATH
from time import sleep


class WebDriver:
  def __init__(self):
    self.address = 'http://localhost:9515'

    self.init_chrome_driver()

  def init_chrome_driver(self):
    try:
      # create chromedriver process
      self.popen = subprocess.Popen(['drivers/chrome/chromedriver', '--headless'])

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

      self.session_id = _res['sessionId']

      self.popen.kill()
    except:
      raise Exception('Failed to initialize chrome driver.')
    
q = WebDriver()