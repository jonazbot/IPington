# IPington, the Discord bot

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8d56cf56ec1c48868db705f510c5de69)](https://app.codacy.com/gh/jonazbot/IPington?utm_source=github.com&utm_medium=referral&utm_content=jonazbot/IPington&utm_campaign=Badge_Grade_Settings)

IPington is a simple Discord bot for automating remote management of a self-hosted Minecraft server running on Linux. Through a private channel members can send commands to the bot to:
 - Check the Minecraft version currently running on the server
 - Check if the server is currently running
 - Start the server if it is not currently running
 - Leak the current server IP and port number
 - Request a link to the source code repository

## Setup
IPington requires Python 3 to run.

### Install dependencies
```sh
pip install discord.py
```

### Editing the .conf file
```sh
# Server settings
MINECRAFT_VERSION=1.18.1
SERVER_PORT=25565
PATH_TO_SERVER=/path/to/server
SERVER_EXEC=minecraft_server.${MINECRAFT_VERSION}.jar
XMS=2G
XMX=8G

# Bot settings
PREFIX=!
TOKEN=H3R3I$AS@mP1eD1$c0rDT0k3n.1tSh0u1d8eEx4C7Ly59[hAR@CT3r$10N6
```

## Run IPington

The bot can be started from a terminal with the following command:

```sh
./ipington.py
```
or
```sh
python ipington.py
```
or
```sh
python3 ipington.py
```

## Commands

| **Commands** | ***Description***                                       |
|--------------|---------------------------------------------------------|
| `!Info`      | *Post a list available commands.*                       |
| `!IP`        | *Post the current Minecraft server IP and port number.* |
| `!Version`   | *Post the current Minecraft server version.*            |
| `!Minecraft` | *Start the Minecraft server.*                           |
| `!Source`    | *Post a URL to repository for the source code.*         |

