from discord.ext import commands

import subprocess
import urllib.request
import psutil
import os
import logging


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

    def __init__(self, bot):
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
              f'`{self.bot.command_prefix}IP`           *Ask IPington to leak the current server IP.*\n' \
              f'`{self.bot.command_prefix}Version`      *Ask IPington for the current Minecraft server version.*\n' \
              f'`{self.bot.command_prefix}Minecraft`    *Ask IPington to start {self.bot.server_name}.*\n' \
              f"`{self.bot.command_prefix}Source`       *Ask IPington for a link to it's source code."
        await ctx.send(cmd)

    @commands.command(name='IP')
    async def ip(self, ctx):
        """
        Ask IPington to leak the current Minecraft server IP.
        """
        try:
            await ctx.send(
                f'{self.bot.server_name} server address: ***{self._find_server_ip()}:{self.bot.server_port}***')
        except Exception:
            await ctx.send('IP service is currently not available.')
            logging.warning('IP address leak failed')

    @commands.command(name='Version')
    async def mc_version(self, ctx):
        """
        Ask IPington to leak the current Minecraft server version.
        """
        await ctx.send(f'{self.bot.server_name} is currently running version: ***{self.bot.minecraft_version}***')

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
            await ctx.send(f'{self.bot.server_name} is currently running.')
            await self.ip(ctx)
        else:
            try:
                if os.path.exists(self.bot.server_path):
                    if os.name == 'posix' or os.name == 'nt':
                        subprocess.Popen(
                            ['java', f'-Xms{self.bot.xms}', f'-Xmx{self.bot.xms}', '-jar', f'{self.bot.jar_path}'],
                            cwd=self.bot.server_path,
                            shell=False)
                        await ctx.send(f'{self.bot.server_name} is starting and can be accessed at:\n'
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
