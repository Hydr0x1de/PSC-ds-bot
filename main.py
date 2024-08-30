from discord.ext import commands
from discord import Intents

from os.path import getsize, exists
from typing import *

import commands as bot_commands

#setup
intents = Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='psc!', intents=intents)
bot.remove_command('help')
bot.add_command(bot_commands.common.help)
bot.add_command(bot_commands.common.ping)
bot.add_command(bot_commands.common.serverinfo)
bot.add_command(bot_commands.connections.conn)
bot.add_command(bot_commands.connections.connlst)
bot.add_command(bot_commands.managment.banlist)
bot.add_command(bot_commands.managment.ban)
bot.add_command(bot_commands.managment.unban)
bot.add_command(bot_commands.managment.reboot)

with open('config.txt', 'r') as f: 
    read = f.readlines()
    read = [line.strip() for line in read]
    TOKEN, PORT, *other = read # *other is just protection
if not exists('restart_ctx.json'):
    with open('restart_ctx.json', 'w') as f:
        f.write('')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    if getsize('restart_ctx.json') != 0:
        # TODO: commands.tools.process_restart(bot)
        pass


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  
    print(f'message from {message.author} : {message.content}')
    await bot.process_commands(message)


#run
if __name__ == '__main__':
    bot.run(TOKEN)