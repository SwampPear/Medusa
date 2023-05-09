import sys

class FG:
  BLACK = '\u001b[30m'
  RED = '\u001b[31m'
  GREEN = '\u001b[32m'
  YELLOW = '\u001b[33m'
  BLUE = '\u001b[34m'
  MAGENTA = '\u001b[35m'
  CYAN = '\u001b[36m'
  WHITE = '\u001b[37m'

class CLI:
  def __init__(self) -> None:
    self.END = '\033[0m'

  def write(text: str='\n') -> None:
    sys.stdout.write(text)
    sys.stdout.flush()