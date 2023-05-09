from typing import Optional
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
  def write(text: str='\n', color: Optional[str]=None) -> None:
    _out = text

    if color:
      _out = f'{color}{_out}\n'

    sys.stdout.write(_out)
    sys.stdout.flush()