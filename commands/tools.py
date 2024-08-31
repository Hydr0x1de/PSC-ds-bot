from subprocess import Popen, PIPE
from os.path import getsize
from functools import wraps
import json 
import re

from discord.ext import commands
from discord.abc import GuildChannel


def serialize_ctx(ctx: commands.context.Context) -> None:
    """serialize ctx and write to file (to save it through system reboot)"""
    data = {
        'channel_id': ctx.channel.id,
        'guild_id': ctx.guild.id,
        'author_mention': ctx.author.mention
    }
    with open('restart_ctx.json', 'w') as f:
        f.write(json.dumps(data))


def deserialize_ctx() -> dict:
    with open('restart_ctx.json', 'r') as f:
        return json.load(f)
    

def fetch_ctx(bot: commands.Bot, data: dict) -> GuildChannel:
    guild = bot.get_guild(data['guild_id']) if data['guild_id'] else None
    channel = guild.get_channel(data['channel_id']) if guild else bot.get_channel(data['channel_id'])
    return channel


def process_restart(bot: commands.Bot) -> None:
    if getsize('restart_ctx.json') == 0:
        return
    #if file is not blank:
    data = deserialize_ctx()
    channel = fetch_ctx(bot, data)
    user_mention = data['author_mention']
    channel.send(f'{user_mention} Restarted successfully') 
    with open('restart_ctx.json', 'w') as f:
        f.write('')


def execute(cmd: str) -> str:
    """executes command in terminal and returns output"""
    temp = Popen(cmd, stdout=PIPE, shell=True)
    return temp.communicate()[0].decode()


def hr_size(bytes: int) -> str:
    """Returns size of bytes in a human readable format"""
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024


def is_valid_ipv4(ip):
    ipv4_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$')
    return bool(ipv4_pattern.match(ip))


def validate_ip(func):
    @wraps(func)
    async def wrapper(ctx, ip):
        if not is_valid_ipv4(ip):
            print('provided ip is invalid')
            await ctx.send("Invalid IP!")
            return
        return await func(ctx, ip)
    
    return wrapper
