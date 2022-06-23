# IPington, the Discord bot

IPington is a simple Discord-bot for automating remote management of a self-hosted Minecraft server.


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


#### Linux/Mac

```sh
./ipington.py
```


#### Linux

```sh
python3 ipington.py
```


#### Windows, Linux, and Mac

```sh
python ipington.py
```


## Discord message commands

| **Commands** | ***Description***                                       |
|--------------|---------------------------------------------------------|
| `!Info`      | *Post a list available commands.*                       |
| `!IP`        | *Post the current Minecraft server IP and port number.* |
| `!Version`   | *Post the current Minecraft server version.*            |
| `!Minecraft` | *Start the Minecraft server.*                           |
| `!Source`    | *Post a URL to repository for the source code.*         |
