class DriverInitializationError(Exception):
  """
  Error with driver initializing.
  """

  def __init__(self, message):
    """
    Initializes this error object.
    """
    self.message = message
    super().__init__(self.message)