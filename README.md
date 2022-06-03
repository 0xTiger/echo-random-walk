# Echo Random Walk

Displays the characters in a file to the terminal along a random walk using python's `curses` module

## Usage
Example:
```
python3 echo-random-walk.py myfile.txt
```
Press q to quit.

All options:
```
usage: echo-random-walk.py [-h] [--log] [--speed SPEED] path

positional arguments:
  path           path of file or directory containing text to display

optional arguments:
  -h, --help     show this help message and exit
  --log          enables logging
  --speed SPEED  set the display speed in characters per second
  ```
