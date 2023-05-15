from typing import Optional
import sys


class Color:
  SUCCESS = '\u001b[32m'
  DANGER = '\u001b[31m'
  WARNING = '\u001b[33m'
  INFO = '\u001b[36m'
  DELIMITER = '\u001b[35m'


class CLI:
  def __init__(self) -> None:
    title = [
        '    __  _____________  __  _______ ___ ',
        '   /  |/  / ____/ __ \/ / / / ___//   |',
        '  / /|_/ / __/ / / / / / / /\__ \/ /| |',
        ' / /  / / /___/ /_/ / /_/ /___/ / ___ |',
        '/_/  /_/_____/_____/\____//____/_/  |_|'
    ]
    info = [
        '@swamppear',
        'v0.0.25'
    ]

    self.write('\n'.join(title), Color.DELIMITER, True, count=False)
    self.write('\n'.join(info), Color.SUCCESS, True, count=False)
    self.write(count=False)

    self.row_count = 0

  
  def write(
    self,
    text: str='',
    color: Optional[str]=None,
    bold: bool=False,
    end: str='\n',
    count: bool=True
) -> None:
    if color:
      text = f'{color}{text}'
    if bold:
      text = f'\033[1m{text}'

    text = f'{text}\033[0m{end}'

    sys.stdout.write(text)
    sys.stdout.flush()

    if count:
      self.row_count += 1


  def read(
    self,
    begin: str='', 
    color: Optional[str]=None, 
    bold: bool=False
  ) -> str:
    text = ''

    self.write(begin, color, bold, end='')

    while True:
      char = ord(sys.stdin.read(1))
      
      if char == 3: 
        return
      elif char in (10, 13): 
        return text
      else: 
        text += chr(char)


  def clear(self) -> None:
    sys.stdout.write(f'\u001b[{self.row_count}F')
    sys.stdout.write('\u001b[0J')
    sys.stdout.flush()

    self.row_count = 0