import subprocess
from medusa.common import CHROME_DRIVER_PATH


class WebDriver:
  def __init__(self, port, address):
    self.port = port
    self.address = address


class ChromeDriver(WebDriver):
  def __init__(self):
    super().__init__(
      port=9515,
      address='113.0.5672.24'
    )

  subprocess.Popen(CHROME_DRIVER_PATH)

def WebDriverr():
  subprocess.Popen(CHROME_DRIVER_PATH)