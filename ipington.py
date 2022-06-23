#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import subprocess
import urllib.request
from dotenv import dotenv_values
from discord.ext import commands


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
                 server_version: str,
                 server_path: str,
                 server_exec: str,
                 server_port: str,
                 xms: str,
                 xmx: str):
        super(IPington, self).__init__(command_prefix=command_prefix)
        self.minecraft_version = server_version
        self.server_path = server_path
        self.jar_path = server_exec
        self.server_port = server_port
        self.xms = xms
        self.xmx = xmx
        self.add_cog(Functions(self))
        self.server_process = None
        logging.basicConfig(
            filename='ipington.log',
            level=logging.WARNING,
            format='%(asctime)s %(message)s')


class Functions(commands.Cog):
    """
    Functions, or commands, for IPington to invoke on messages that contain
    the correct prefix followed by a keyword matching names of methods defined
    in this class.

    This class is a subclass of :class:`discord.commands.Cog`.

    Attributes
    -----------
    bot
        The bot is the :class: `discord.commands.Bot.IPington`.
        which to register this group of commands.
    """

    def __init__(self, bot: IPington):
        self.bot = bot

    @staticmethod
    def _find_server_ip() -> str:
        """
        Find the current server IP address.
        """
        return urllib.request.urlopen('https://ident.me').read().decode('utf8')

    @staticmethod
    def _is_process_running(process_name: str) -> bool:
        """
        Check if a process is running by name.
        """
        import psutil
        for proc in psutil.process_iter():
            try:
                if process_name.lower() in proc.name().lower():
                    return True
            except psutil.ZombieProcess:
                logging.warning('Process is a zombie!')
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                logging.warning('Access Denied!')
        return False

    @commands.command(name='Source')
    async def source(self, ctx):
        """
        Ask IPington to share a link to the source code.
        """
        await ctx.send('https://github.com/jonazbot/IPington')

    @commands.command(name='Info')
    async def info(self, ctx):
        """
        Ask IPington to list the current bot commands.
        """
        cmd = '**Commands**       ***Description*** \n' \
              f'`{self.bot.command_prefix}Info`         *Ask IPington to list the bot commands.*\n' \
              f'`{self.bot.command_prefix}IP`           *Ask IPington to leak the current Minecraft server IP.*\n' \
              f'`{self.bot.command_prefix}Version`      *Ask IPington for the current Minecraft server version.*\n' \
              f'`{self.bot.command_prefix}Minecraft`    *Ask IPington to start the Minecraft server.*\n' \
              f'`{self.bot.command_prefix}Source`       *Ask IPington for a link to the source code.*'
        await ctx.send(cmd)

    @commands.command(name='IP')
    async def ip(self, ctx):
        """
        Ask IPington to leak the current Minecraft server IP.
        """
        try:
            await ctx.send(f'Minecraft server address: ***{self._find_server_ip()}:{self.bot.server_port}***')
        except Exception:
            await ctx.send('IP service is currently not available.')
            logging.warning('IP address leak failed')

    @commands.command(name='Version')
    async def mc_version(self, ctx):
        """
        Ask IPington to leak the current Minecraft server version.
        """
        await ctx.send(f'The minecraft server is currently running version: ***{self.bot.minecraft_version}***')

    @commands.command(name='Minecraft')
    async def minecraft(self, ctx):
        """
        Play Minecraft.

        At invocation the bot will check to see if the server is currently running and
        proceed to start the minecraft server.

            .. note:: The bot will only start the server after determining that
            it is not currently running.
        """
        if self._is_process_running('minecraft_server'):
            await ctx.send('Minecraft server is already running.')
        else:
            try:
                if os.path.exists(self.bot.server_path):
                    if os.name == 'posix' or os.name == 'nt':
                        subprocess.Popen(
                            ['java', f'-Xms{self.bot.xms}', f'-Xmx{self.bot.xms}', '-jar', f'{self.bot.jar_path}'],
                            cwd=self.bot.server_path,
                            shell=False)
                        await ctx.send(f'Minecraft server is starting and can be accessed at:\n'
                                       f'***{self._find_server_ip()}:{self.bot.server_port}***')
                    else:
                        logging.warning(f'Unable to recognize OS: {os.name}')
                        raise OSError
                else:
                    logging.warning(f'The server directory {self.bot.server_path} was not found!')
                    raise NotADirectoryError
            except Exception:
                msg = 'Failed to start Minecraft server!'
                logging.exception(msg)
                await ctx.send(msg)


if __name__ == '__main__':
    # Load .conf file.
    config = dotenv_values('.conf')

    # Setup IPington.
    ipington: IPington = IPington(command_prefix=config['PREFIX'],
                                  server_version=config['MINECRAFT_VERSION'],
                                  server_path=config['PATH_TO_SERVER'],
                                  server_exec=config['SERVER_EXEC'],
                                  server_port=config['SERVER_PORT'],
                                  xms=config['XMS'],
                                  xmx=config['XMX'])

    # Run IPington
    ipington.run(config['TOKEN'])
