from typing import Optional
import sys

class Color:
  GREEN = '\u001b[32m'




  BLACK = '\u001b[30m'
  RED = '\u001b[31m'

  YELLOW = '\u001b[33m'
  BLUE = '\u001b[34m'
  MAGENTA = '\u001b[35m'
  CYAN = '\u001b[36m'
  WHITE = '\u001b[37m'

class CLI:
  def write(
    text: str='', 
    color: Optional[str]=None, 
    bold: bool=False, 
    end: str='\n'
  ) -> None:
    if color:
      text = f'{color}{text}'

    if bold:
      text = f'\033[1m{text}'

    text = f'{text}\033[0m{end}'


    """
    _out = text

    if color:
      _out = f'{color}{_out}'

    if bold:
      _out = f'\033[1m{_out}'

    if _out != '\n':
      _out = f'{_out}\033[0m{end}'

    """
    sys.stdout.write(text)
    sys.stdout.flush()

  def read(begin: str=''):
    text = ''

    sys.stdout.write(begin)
    sys.stdout.flush()

    while True:
      char = ord(sys.stdin.read(1))
      
      if char == 3: return
      elif char in (10, 13): return text
      else: text += chr(char)