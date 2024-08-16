from discord.ext import commands
from discord import Intents
from subprocess import Popen, PIPE
from typing import *


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
    temp = Popen(cmd, stdout=PIPE)
    return temp.communicate()[0].decode()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author.bot:
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
        "netstat -anp | grep :" + PORT + " | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq | wc -l")
    await ctx.send(f'{result} devices connected')


@bot.command()
async def connlst(ctx):
    """send list of IPs of connected devices"""
    #get and write to file list of estabilished connections (their IP's actually)
    result = execute(
        "netstat -anp | grep :" + PORT + " | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq")
    await ctx.send(f'List of all connected devices:\n{result}')


@bot.commnad()
async def banlist(ctx):
    """send list of banned IPs"""
    result = execute('firewall-cmd --zone-=public --list-rich-rules')
    await ctx.send(result)

@bot.commnad()
async def ban(ctx, ip: str):
    """ban IP connection; provide correct IP to ban"""
    addStatus = execute(f'firewall-cmd --zone=public --add-rich-rule=\'rule family="ipv4" source address="{ip}" drop\' --permanent')
    reloadStatus = execute('firewall-cmd --reload')
    execute(f'ss -K dst {ip}')
    await ctx.send(f'add firewall rule: {addStatus}\nreload firewall: {reloadStatus}\ndevice kicked out: success')


@bot.commnad()
async def unban(ctx, ip: str):
    """unban IP connection; provide correct IP to unban"""
    removeStatus = execute(f'firewall-cmd --zone=public --remove-rich-rule=\'rule family="ipv4" source address="{ip} drop\' --permanent')
    reloadStatus = execute('firewall-cmd --reload')
    await ctx.send(f'remove firewall rule: {removeStatus}\nreload firewall: {reloadStatus}')


#run
if __name__ == '__main__':
    bot.run(TOKEN)