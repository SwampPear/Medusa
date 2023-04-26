DRIVER_PATH = 'drivers/chrome/chromedriver'
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