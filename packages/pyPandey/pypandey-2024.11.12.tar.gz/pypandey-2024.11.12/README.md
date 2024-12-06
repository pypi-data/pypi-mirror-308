# pyPandey Library

Core library of [The Pragyan](https://github.com/TeamPandey/Pragyan), a python based telegram userbot.

[![CodeFactor](https://www.codefactor.io/repository/github/TeamPandey/pyPandey/badge)](https://www.codefactor.io/repository/github/TeamPandey/pyPandey)
[![PyPI - Version](https://img.shields.io/pypi/v/pyPandey?style=round)](https://pypi.org/project/pyPandey)    
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyPandey?label=DOWNLOADS&style=round)](https://pypi.org/project/pyPandey)    
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/TeamPandey/Pragyan/graphs/commit-activity)
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/TeamPandey/Pragyan)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

# Installation
```bash
pip3 install -U pyPandey
```

# Documentation 
[![Documentation](https://img.shields.io/badge/Documentation-Pragyan-blue)](http://pragyan.tech/)

# Usage
- Create folders named `plugins`, `addons`, `assistant` and `resources`.   
- Add your plugins in the `plugins` folder and others accordingly.   
- Create a `.env` file with following mandatory Environment Variables
   ```
   API_ID
   API_HASH
   SESSION
   REDIS_URI
   REDIS_PASSWORD
   ```
- Check
[`.env.sample`](https://github.com/TeamPandey/Pragyan/blob/main/.env.sample) for more details.   
- Run `python3 -m pyPandey` to start the bot.   

## Creating plugins
 - ### To work everywhere

```python
@Pragyan_cmd(
    pattern="start"
)   
async def _(e):   
    await e.eor("Pragyan Started!")   
```

- ### To work only in groups

```python
@Pragyan_cmd(
    pattern="start",
    groups_only=True,
)   
async def _(e):   
    await eor(e, "Pragyan Started.")   
```

- ### Assistant Plugins 👇

```python
@asst_cmd("start")   
async def _(e):   
    await e.reply("Pragyan Started.")   
```

See more working plugins on [the offical repository](https://github.com/TeamPandey/Pragyan)!

> Made with 💕 by [@TeamPandey](https://t.me/TeamPandey).    


# License
[![License](https://www.gnu.org/graphics/agplv3-155x51.png)](LICENSE)   
Pragyan is licensed under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) v3 or later.

# Credits
* [![TeamPandey-Devs](https://img.shields.io/static/v1?label=TeamPandey&message=devs&color=critical)](https://t.me/PragyanDevs)
* [Lonami](https://github.com/Lonami) for [Telethon](https://github.com/LonamiWebs/Telethon)
