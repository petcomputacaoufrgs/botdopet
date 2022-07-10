from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, CommandNotFound

class Events(commands.Cog):
    """Bot events"""

    def __init__(self, bot):
        self.bot = bot

    # Event: bot is online
    @commands.Cog.listener()
    async def on_ready(self):
        print("Estou pronto!")

    # Event: poorly worded command
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Favor enviar todos os argumentos. Use pet.help para ver quais são os argumentos necessários.")
        if isinstance(error, CommandNotFound):
            await ctx.send("O comando não existe. Use pet.help para ver todos os comandos possíveis.")
        else:
            raise error

def setup(bot):
    bot.add_cog(Events(bot))