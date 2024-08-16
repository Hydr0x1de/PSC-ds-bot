from discord.ext import commands
from discord import Intents

from subprocess import Popen, PIPE
from typing import *
from shutil import disk_usage
from psutil import virtual_memory, cpu_freq, cpu_percent  # type: ignore


#setup
intents = Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='psc!', intents=intents)
with open('config.txt', 'r') as f: 
    read = f.readlines()
    read = [line.strip() for line in read]
    TOKEN, PORT, *other = read # *other is just protection


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


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  
    print(f'message from {message.author} : {message.content}')
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    """Pong!"""
    await ctx.send('Pong!')


@bot.command()
async def conn(ctx):
    """send amount of connected devices"""
    result = execute(
        "netstat -anp | grep :" + PORT + " | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq | wc -l").strip()
    await ctx.send(f'{result} devices connected')


@bot.command()
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
async def banlist(ctx):
    """send list of banned IPs"""
    result = execute('firewall-cmd --zone=public --list-rich-rules')
    if result:
        await ctx.send(result)
    else:
        await ctx.send('Banlist is blank!')


@bot.command()
async def ban(ctx, ip: str):
    """ban IP connection; provide correct IP to ban"""
    addStatus = execute(f'firewall-cmd --zone=public --add-rich-rule=\'rule family="ipv4" source address="{ip}" drop\' --permanent')
    reloadStatus = execute('firewall-cmd --reload')
    execute(f'ss -K dst {ip}')
    await ctx.send(f'add firewall rule: {addStatus}\nreload firewall: {reloadStatus}\ndevice kicked out: success')


@bot.command()
async def unban(ctx, ip: str):
    """unban IP connection; provide correct IP to unban"""
    removeStatus = execute(f'firewall-cmd --zone=public --remove-rich-rule=\'rule family="ipv4" source address="{ip} drop\' --permanent')
    reloadStatus = execute('firewall-cmd --reload')
    await ctx.send(f'remove firewall rule: {removeStatus}\nreload firewall: {reloadStatus}')


@bot.command()
async def serverinfo(ctx):
    """send info about server"""
    disk = disk_usage('/')
    disk.total, disk.used, disk.free
    memory = virtual_memory()
    memory.total, memory.used
    result =  f'**Disk**    total:{get_size(disk.total)}   used:{get_size(disk.used)}   free:{get_size(disk.free)}\n' \
            + f'**RAM**     {get_size(memory.used)} / {get_size(memory.total)}\n' \
            + f'**CPU**     {cpu_freq().current}MHz / {cpu_freq().max}MHz  perc:{cpu_percent()}%'
    await ctx.send(result)


#run
if __name__ == '__main__':
    bot.run(TOKEN)