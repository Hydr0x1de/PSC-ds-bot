from discord.ext.commands import Bot
from discord import Intents
from typing import *
from os import system
import commands
import toml


intents = Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

bot = Bot(command_prefix='psc!', intents=intents)
bot.remove_command('help')
bot.add_command(commands.common.help)
bot.add_command(commands.common.ping)
bot.add_command(commands.common.serverinfo)
bot.add_command(commands.connections.conn)
bot.add_command(commands.connections.connlst)
bot.add_command(commands.managment.banlist)
bot.add_command(commands.managment.ban)
bot.add_command(commands.managment.unban)
bot.add_command(commands.managment.reboot)

config = toml.load('config.toml')
TOKEN = config['TOKEN']
PORT = config['PORT']

system('touch restart_ctx.json')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    commands.tools.process_restart(bot)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  
    print(f'message from {message.author} : {message.content}')
    await bot.process_commands(message)


#run
if __name__ == '__main__':
    bot.run(TOKEN)