# IPington, the Discord bot

IPington is a simple Discord bot for automating remote management of a self-hosted Minecraft server running on Linux.

Through a private channel members can send commands to the bot to:
 - Check the Minecraft version currently running on the server
 - Check if the server is currently running
 - Start the server if it is not currently running
 - Leak the current server IP and port number

## Setup
IPington requires Python 3 to run.

### Install dependencies
```sh
pip install -r discord.py
```

### Editing the .conf file
```sh
# Server settings
MINECRAFT_VERSION=1.18.1
SERVER_PORT=25565
PATH_TO_SERVER=/path/to/server
PATH_TO_JAR=minecraft_server.${MINECRAFT_VERSION}.jar

# Bot settings
PREFIX=!
TOKEN=T1$is@SaMPleD1$C0RDTok3n.1tSh0ulDbeEx4ctLy59[hAr@ct3rS.LoN6
```

## Run IPington
The bot can be started from a terminal with the following command:
```sh
python ipington.py
```
or
```sh
python3 ipington.py
```
