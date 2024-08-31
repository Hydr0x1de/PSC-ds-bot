from discord.ext import commands

from .tools import execute


@commands.command()
async def conn(ctx):
    """send amount of connected devices"""
    global PORT
    result = execute(
        "netstat -anp | grep :" + PORT + " | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq | wc -l").strip()
    await ctx.send(f'{result} devices connected')


@commands.command()
async def connlst(ctx):
    """send list of IPs of connected devices"""
    global PORT
    #get and write to file list of estabilished connections (their IP's actually)
    result = execute(
        "netstat -anp | grep :" + PORT + " | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq")
    if result:
        await ctx.send(f'List of all connected devices:\n{result}')
    else:
        await ctx.send('No devices connected yet')