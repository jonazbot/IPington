#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import logging
from dotenv import dotenv_values
from discord.ext import commands

import functions


class IPington(commands.Bot):
    """
    A Discord bot for automating a self-hosted Minecraft server.

    This class is a subclass of :class:`discord.commands.Bot`.

    Attributes
    -----------
    command_prefix
        The command prefix is the string any message intended as a command must start with
        for the bot to execute the following message as a command.
            Example: '!'
    server_name
        The name of the server IPington is managing.
    server_version
        The version of the server IPington is managing.
            Example: '1.18.1'
    server_path
        The full path to the top-level directory containing the server files.
    server_exec
        The relative or full path to the `minecraft_server.jar`.
    server_port
        The port number used to connect to the server.
    xms
        The amount of memory to give the server at start
    xmx
        The maximum amount of memory the server is allowed
    """

    def __init__(self,
                 command_prefix: str,
                 server_name: str,
                 server_version: str,
                 server_path: str,
                 server_exec: str,
                 server_port: str,
                 xms: str,
                 xmx: str):
        super(IPington, self).__init__(command_prefix=command_prefix,
                                       intents=discord.Intents(messages=True, message_content=True))

        self.server_name = server_name
        self.minecraft_version = server_version
        self.server_path = server_path
        self.jar_path = server_exec
        self.server_port = server_port
        self.xms = xms
        self.xmx = xmx
        # self.wait_for(self.add_cog(functions.Functions(self)))
        self.server_process = None

        logging.basicConfig(
            filename='ipington.log',
            level=logging.WARNING,
            format='%(asctime)s %(message)s')


async def cogs(ipington):
    await ipington.add_cog(functions.Functions(ipington))


if __name__ == '__main__':
    import asyncio
    # Load .conf file.
    config = dotenv_values('.conf')

    # Setup IPington.
    ipington: IPington = IPington(server_name=config['NAME'],
                                  command_prefix=config['PREFIX'],
                                  server_version=config['MINECRAFT_VERSION'],
                                  server_path=config['PATH_TO_SERVER'],
                                  server_exec=config['SERVER_EXEC'],
                                  server_port=config['SERVER_PORT'],
                                  xms=config['XMS'],
                                  xmx=config['XMX'])
    asyncio.run(cogs(ipington))

    # Run IPington
    ipington.run(config['TOKEN'])

