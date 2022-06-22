#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IPington, a Discord bot for automating a self-hosted Minecraft server running on Linux.
"""

import os
import subprocess
import urllib.request
from dotenv import dotenv_values
from discord.ext import commands


class IPington(commands.Bot):
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
        self.add_cog(Cmd(self))


class Cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_server_ip() -> str:
        return urllib.request.urlopen('https://ident.me').read().decode('utf8')

    @staticmethod
    def is_server_running():
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
        """ Ask IPington to leak the current Minecraft server IP. """
        try:
            await ctx.send(f'Minecraft server address:\n{self.get_server_ip()}:{bot.server_port}')
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
        """ Check if the Minecraft server is running and start it if it is not. """
        if self.is_server_running():
            await ctx.send('Minecraft server is already running.')
        else:
            await ctx.send('Starting Minecraft server...')
            try:
                subprocess.call(
                    f'cd {bot.server_path}'
                    f' && nohup java - Xms2G - Xmx8G - jar {bot.jar_path}'
                    ' & > / dev / null &',
                    shell=True)
                await ctx.send(f'Minecraft server is ready @ {self.get_server_ip()}')
            except Exception as e:
                print(f'Failed to start Minecraft server!\n{e}')
                await ctx.send('Failed to start Minecraft server!')


if __name__ == '__main__':
    # Load .conf as `dict`.
    config = dotenv_values('.env.conf')  # TODO: Replace `.env.conf` with `.conf`

    # Setup IPington.
    bot: IPington = IPington(command_prefix=config['PREFIX'],
                             server_version=config['MINECRAFT_VERSION'],
                             path_to_server=config['PATH_TO_SERVER'],
                             path_to_jar=config['PATH_TO_JAR'],
                             server_port=config['SERVER_PORT'])

    # Run IPington
    bot.run(config['TOKEN'])
