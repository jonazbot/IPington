#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import urllib.request
from dotenv import dotenv_values
from discord.ext import commands


class IPington(commands.Bot):
    """
    IPington, a Discord bot for automating a self-hosted Minecraft server running on Linux.

    This class is a subclass of :class:`discord.commands.Bot`.

    Attributes
    -----------
    command_prefix
        The command prefix is the string any message intended as a command must start with
        for the bot to execute the following message as a command.
            Example: '!'
    server_version
        The version of the server IPington is managing.
            Example: '1.18.1'
    path_to_server
        The full path to the top-level directory containing the server files.
    path_to_jar
        The relative or full path to the `minecraft_server.jar`.
    server_port
        The port number used to connect to the server.
    """
    def __init__(self,
                 command_prefix: str,
                 server_version: str,
                 path_to_server: str,
                 path_to_jar: str,
                 server_port: str):
        self.prefix = command_prefix
        self.minecraft_version = server_version
        self.server_path = path_to_server
        self.jar_path = path_to_jar
        self.server_port = server_port
        super(IPington, self).__init__(command_prefix=self.prefix)
        self.add_cog(Functions(self))


class Functions(commands.Cog):
    """
    Functions, or commands, for IPington to invoke on messages that contain
    the correct prefix followed by a keyword matching names of methods defined
    in this class.

    This class is a subclass of :class:`discord.commands.Cog`.

    Attributes
    -----------
    bot
        The bot is the :class: `discord.commands.Bot` or any subclass (like IPington)
        which to register this group of commands.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def find_server_ip() -> str:
        """
        Find the current server IP address.
        """
        return urllib.request.urlopen('https://ident.me').read().decode('utf8')

    @staticmethod
    def is_server_running():
        """
        Check if the server is currently running.
        """
        if os.name == 'posix' and len(os.popen('pgrep -f minecraft_server').read().split('\n')[1]) > 0:
            return True
        return False

    @commands.command(name='Info')
    async def info(self, ctx):
        """
        Ask IPington to list the current bot commands.
        """
        cmd = '**Commands**       ***Description*** \n' \
              f'`{bot.prefix}Info`         *Ask IPington to list the bot commands.*\n' \
              f'`{bot.prefix}IP`           *Ask IPington to leak the current Minecraft server IP.*\n' \
              f'`{bot.prefix}Version`      *Ask IPington to leak the current Minecraft server version.*\n' \
              f'`{bot.prefix}Minecraft`    *Ask IPington to start the Minecraft server.*'
        await ctx.send(cmd)

    @commands.command(name='IP')
    async def ip(self, ctx):
        """
        Ask IPington to leak the current Minecraft server IP.
        """
        try:
            await ctx.send(f'Minecraft server address:\n{self.find_server_ip()}:{bot.server_port}')
        except Exception as e:
            await ctx.send('IP service is currently not available.')
            import traceback
            traceback.print_exception(e)

    @commands.command(name='Version')
    async def mc_version(self, ctx):
        """
        Ask IPington to leak the current Minecraft server version.
        """
        await ctx.send(f'Current minecraft server version: {bot.minecraft_version}')

    @commands.command(name='Minecraft')
    async def minecraft(self, ctx):
        """
        Play Minecraft.

        At invocation the bot will check to see if the server is currently running and
        proceed to start the minecraft server.

            .. note:: The bot will only start the server after determining that
            it is not currently running.
        """
        if self.is_server_running():
            await ctx.send('Minecraft server is already running.')
        else:
            await ctx.send('Starting Minecraft server...')
            try:
                # TODO: String building should definitely be cleaned
                subprocess.call(
                    f'cd {bot.server_path}'  # Change into server directory
                    f' && nohup java - Xms2G - Xmx8G - jar {bot.jar_path}'  # Start the server quietly 
                    ' & > / dev / null &',  # Direct garbage collection
                    shell=True)  # This option carries inherent risks due to potential of code injection...
                # ...of which I have currently done NOTHING to prevent.
                # SecurityPatch v0.0.1: Don't let anyone tamper with your .conf file.
                await ctx.send(f'Minecraft server is ready @ {self.find_server_ip()}')
            except Exception as e:
                print(f'Failed to start Minecraft server!\n{e}')
                await ctx.send('Failed to start Minecraft server!')


if __name__ == '__main__':
    # Load .conf file.
    config = dotenv_values('.conf')

    # Setup IPington.
    bot: IPington = IPington(command_prefix=config['PREFIX'],
                             server_version=config['MINECRAFT_VERSION'],
                             path_to_server=config['PATH_TO_SERVER'],
                             path_to_jar=config['PATH_TO_JAR'],
                             server_port=config['SERVER_PORT'])

    # Run IPington
    bot.run(config['TOKEN'])
