![jeju_logo](assets/images/jeju_logo_flat.png "jeju logo")

![](https://badgen.net/github/checks/SyedAhkam/jeju-bot)
![](https://badgen.net/github/stars/SyedAhkam/jeju-bot)
![](https://badgen.net/github/commits/SyedAhkam/jeju-bot)
![](https://badgen.net/github/last-commit/SyedAhkam/jeju-bot)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/SyedAhkam/jeju-bot/?ref=repository-badge)

A Multi-Purpose discord bot made using [discord.py](https://github.com/Rapptz/discord.py) library focused on simplicity.

# Invite

Please use [this](https://discord.com/oauth2/authorize?client_id=699595477934538782&permissions=2080763126&scope=bot) link to invite the instance hosted by me.

## Features

1. Easy to use.

2. Fast and good uptime.

3. Custom Prefixes for every guild.

4. Enable bot features using only one command:

   - `+enable logging`

5. Auto join roles which will be added on member join.

6. Logging system which can use single or multiple channels.

7. Join and leave messages. (Coming soon)

8. Some fun commands to use when you're bored.

9. Detailed help messages.

10. Moderation commands.

11. Blacklisting system.

12. Support server coming soon!

13. Web dashboard coming soon!

## Self Hosting

1. Clone the repo:
   ```sh
       $ git clone https://github.com/SyedAhkam/jeju-bot.git
   ```
2. Change directory:
   ```sh
       $ cd jeju-bot
   ```
3. Create `.env` file and set these env variables:
   - `DISCORD_TOKEN`
   - `MONGODB_URI`
4. Initialize pipenv and Install dependencies:
   ```sh
       $ pipenv install
   ```
   - These are the optional dependencies:
     - [uvloop](https://github.com/MagicStack/uvloop) - This is not supported on windows.
5. Run bot:
   ```sh
       $ cd src
       $ python3 jeju.py
   ```

## Development

Similar to [self-hosting](#Self-Hosting) but fork the repo first. Then clone, Make changes and create a pull request.
You can also set `DISCORD_TOKEN_BETA` environment variable and run the bot in DEV mode:

```sh
    $ DEV=True python3 jeju.py
```

## Contact me

My discord tag: `SyedAhkam#6584`
