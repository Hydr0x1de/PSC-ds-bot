from discord.ext import commands
from discord import Intents
from os import system


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
    #get and write to file amount of estabilished connections
    system("netstat -anp | grep :" + PORT + " | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq | wc -l > conn-amount.dat")
    #send result
    with open('conn-amount.dat', 'r') as f:
        result = f.read().strip()
    await ctx.send(f'{result} devices connected')


@bot.command()
async def connlst(ctx):
    """send list of IPs of connected devices"""
    #get and write to file list of estabilished connections (their IP's actually)
    system("netstat -anp | grep :" + PORT + " | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq > conn-lst.dat")
    #send result
    with open('conn-lst.dat', 'r') as f:
        result = f.read().strip()
    await ctx.send(f'List of all connected devices:\n{result}')


#run
if __name__ == '__main__':
    bot.run(TOKEN)