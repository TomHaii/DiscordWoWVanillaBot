# Discord WoW Vanilla Bot
[![PyPI](https://img.shields.io/pypi/v/discord.py.svg)](https://pypi.python.org/pypi/discord.py/)
[![PyPI](https://img.shields.io/pypi/pyversions/discord.py.svg)](https://pypi.python.org/pypi/discord.py/)

Discord bot for getting item information using selenium, discord python api and Vanillagaming website.
using command `!help` in order to learn about the bot features.

[test bot](https://discordapp.com/oauth2/authorize?client_id=373173447603257364&scope=bot)

## Installation

  Make sure you have installed Python 3.4.2+ and that it is in your PATH

  Make sure to have [Mozilla Firefox binaries](https://www.mozilla.org/) installed and to download [Geckodriver](https://github.com/mozilla/geckodriver/releases)

  ```
  > cd path/to/bot/dir

  > python -m pip install -r requirements.txt
  ```

  Open bot.py and replace:
   - on line 6 and 7 the variables `FIREFOX_PATH` and `GECKODRIVER_PATH` by your own paths to the executables files
   - on the last line token in `client.run('token')` by your own Discord App token

  Run it !

  ```
  > python bot.py
  ```

### Arguments

  - `> python bot.py -c` in order to active cache.


## Requirements

- Python 3.4.2+
- [discord.py](https://github.com/Rapptz/discord.py)
- `Selenium for 3.3+` library with Geckodriver and Firefox Binary
- `logging` library
- `fuzzywuzzy` and `python-Levenshtein` libraries
