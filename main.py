import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

# SETUP
bot = commands.Bot(command_prefix='pet.', activity = discord.Activity(type=discord.ActivityType.watching, name="Use pet.help"))
bot.remove_command("help")
os.system("pip3 install py-cord")

# Loading the bot commands
def load_cogs(bot):
    # COMMANDS
    for file in os.listdir("commands"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f'commands.{cog}')

    # EVENTS
    for file in os.listdir("events"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f'events.{cog}')

    # HELP
    for file in os.listdir("help"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f'help.{cog}')


load_cogs(bot)

keep_alive()
TOKEN = os.environ['OFFICIAL_TOKEN']

try:
    bot.run(TOKEN)
except:
    os.system("kill 1")
    bot.run(TOKEN)
