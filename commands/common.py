from discord.ext import commands
from shutil import disk_usage
from psutil import virtual_memory, cpu_freq, cpu_percent
from .tools import hr_size


@commands.command()
async def help(ctx):
    """send help message"""
    msg = """commands list:\n```
    - help       - this message
    - ping       - ping the bot
    - conn       - get amount of connected devices
    - connlst    - get list of connected devices (their IPs)
    - banlist    - get the ban list
    - ban <IP>   - ban
    - unban <IP> - unban
    - serverinfo - get basic information about host server
    - restart    - restart (reboot) entire server
    - reboot     - alias of restart```
    """
    await ctx.send(msg)


@commands.command()
async def ping(ctx):
    """Pong!"""
    await ctx.send('Pong!')


@commands.command()
async def serverinfo(ctx):
    """send info about server"""
    disk = disk_usage('/')
    disk.total, disk.used, disk.free
    memory = virtual_memory()
    memory.total, memory.used
    result =  f'**Disk**    {hr_size(disk.used)} / {hr_size(disk.total)} \n' \
            + f'**RAM**     {hr_size(memory.used)} / {hr_size(memory.total)}\n' \
            + f'**CPU**     {cpu_freq().current}MHz / {cpu_freq().max}MHz  perc:{cpu_percent()}%'
    await ctx.send(result)