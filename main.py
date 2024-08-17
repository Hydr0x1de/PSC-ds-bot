from discord.ext import commands
from discord import Intents

from subprocess import Popen, PIPE
from os.path import getsize, exists
from typing import *
from shutil import disk_usage
from psutil import virtual_memory, cpu_freq, cpu_percent  # type: ignore
from re import search
from time import sleep

import json


#setup
intents = Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='psc!', intents=intents)
bot.remove_command('help')

with open('config.txt', 'r') as f: 
    read = f.readlines()
    read = [line.strip() for line in read]
    TOKEN, PORT, *other = read # *other is just protection
if not exists('restart_ctx.json'):
    with open('restart_ctx.json', 'w') as f:
        f.write('')

#tools
def serialize_ctx(ctx: commands.context.Context) -> None:
    data = {
        'channel_id': ctx.channel.id,
        'guild_id': ctx.guild.id
    }
    with open('restart_ctx.json', 'w') as f:
        f.write(json.dumps(data))


def deserialize_ctx() -> dict:
    with open('restart_ctx.json', 'r') as f:
        return json.load(f)
    

def fetch_ctx(bot, data: dict):
    guild = bot.get_guild(data['guild_id']) if data['guild_id'] else None
    channel = guild.get_channel(data['channel_id']) if guild else bot.get_channel(data['channel_id'])
    return channel


def execute(cmd: str) -> Any:
    """executes command in terminal and returns output"""
    temp = Popen(cmd, stdout=PIPE, shell=True)
    return temp.communicate()[0].decode()


def get_size(bytes: int) -> str:
    """Returns size of bytes in a nice format"""
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

#bot logic
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    if getsize('restart_ctx.json') != 0:
        data = deserialize_ctx()
        channel = fetch_ctx(bot, data)
        await channel.send('Restarted successfully')
        with open('restart_ctx.json', 'w') as f:
            f.write('')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  
    print(f'message from {message.author} : {message.content}')
    await bot.process_commands(message)

# @bot.event
# async def on_command(ctx):
#     if ctx.message.author == bot.user:
#         return
#     if not ctx.author.guild_permissions.administrator:
#         await ctx.send('You do not have admin perms to use commands')
#         return 
#     await bot.process_commands(ctx.message)


@bot.command()
@commands.has_permissions(administrator=True)
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


@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    """Pong!"""
    await ctx.send('Pong!')


@bot.command()
@commands.has_permissions(administrator=True)
async def conn(ctx):
    """send amount of connected devices"""
    result = execute(
        "netstat -anp | grep :" + PORT + " | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq | wc -l").strip()
    await ctx.send(f'{result} devices connected')


@bot.command()
@commands.has_permissions(administrator=True)
async def connlst(ctx):
    """send list of IPs of connected devices"""
    #get and write to file list of estabilished connections (their IP's actually)
    result = execute(
        "netstat -anp | grep :" + PORT + " | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq")
    if result:
        await ctx.send(f'List of all connected devices:\n{result}')
    else:
        await ctx.send('No devices connected yet')


@bot.command()
@commands.has_permissions(administrator=True)
async def banlist(ctx):
    """send list of banned IPs"""
    tmp = execute('firewall-cmd --zone=public --list-rich-rules').strip()
    if not tmp:
        await ctx.send('Banlist is blank!')
    else:
        pattern = r'source address="(\d+\.\d+\.\d+\.\d+)"'
        result = ''
        for line in tmp.split('\n'):
            match = search(pattern, line)
            print(match)
            result += match.group(1) + '\n'
        await ctx.send('Banlist:\n' + result)


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, ip: str):
    """ban IP connection; provide correct IP to ban"""
    addStatus = execute(f'firewall-cmd --zone=public --add-rich-rule=\'rule family="ipv4" source address="{ip}" drop\' --permanent')
    addStatus = 'ERR' if not addStatus else addStatus.upper()
    reloadStatus = execute('firewall-cmd --reload')
    reloadStatus = 'ERR' if not reloadStatus else reloadStatus.upper()
    execute(f'ss -K dst {ip}')
    await ctx.send(f'add firewall rule: {addStatus}\nreload firewall: {reloadStatus}\ndevice kicked out: SUCCESS')


@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, ip: str):
    """unban IP connection; provide correct IP to unban"""
    removeStatus = execute(f'firewall-cmd --zone=public --remove-rich-rule=\'rule family="ipv4" source address="{ip}" drop\' --permanent')
    removeStatus =  'ERR' if not removeStatus else removeStatus.upper()
    reloadStatus = execute('firewall-cmd --reload')
    reloadStatus = 'ERR' if not reloadStatus else reloadStatus.upper()
    await ctx.send(f'remove firewall rule: {removeStatus}\nreload firewall: {reloadStatus}')


@bot.command()
@commands.has_permissions(administrator=True)
async def serverinfo(ctx):
    """send info about server"""
    disk = disk_usage('/')
    disk.total, disk.used, disk.free
    memory = virtual_memory()
    memory.total, memory.used
    result =  f'**Disk**    {get_size(disk.used)} / {get_size(disk.total)} \n' \
            + f'**RAM**     {get_size(memory.used)} / {get_size(memory.total)}\n' \
            + f'**CPU**     {cpu_freq().current}MHz / {cpu_freq().max}MHz  perc:{cpu_percent()}%'
    await ctx.send(result)

 
@bot.command()
@commands.has_permissions(administrator=True)
async def restart(ctx):
    """reboot server"""
    await ctx.send('Going to reboot the server')
    serialize_ctx(ctx)
    execute('reboot')


@bot.command()
@commands.has_permissions(administrator=True)
async def reboot(ctx):
    """alias of restart"""
    await ctx.send('Going to reboot the server')
    serialize_ctx(ctx)
    execute('reboot')


#run
if __name__ == '__main__':
    bot.run(TOKEN)