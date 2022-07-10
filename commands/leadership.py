import os
import pytz
import utils.utils as utils
import datetime
import discord
from discord.ext import commands, tasks


#Constants
PETIANES = os.environ['PETIANES_ID']
LEADERSHIP_CHANNEL = os.environ['WARNINGS_CHANNEL']
leadership = utils.read_file("data/leadership.json")
months_names = {
  "1": "Janeiro",
  "2": "Fevereiro",
  "3": "Março",
  "4": "Abril",
  "5": "Maio",
  "6": "Junho",
  "7": "Julho",
  "8": "Agosto",
  "9": "Setembro",
  "10": "Outubro",
  "11": "Novembro",
  "12": "Dezembro",
}


class Leadership(commands.Cog):
    """PET Computação leadership commands"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.is_first_day_of_month.start()

    @commands.command(name="lideres")
    async def month_leadership(self, ctx):
        global leadership
        current_month = datetime.date.today().month
        current_leadership = leadership[f'{current_month}']
        em = discord.Embed(
            title=f"**Liderança:**",
            description=f"Neste mês de {months_names[f'{current_month}'].lower()}, o líder é **{current_leadership[0]}** e o vice é **{current_leadership[1]}**.\n\nPara os próximos meses:",
            color=0xFDFD96
        )
        i = 1
        while (current_month+i) != 11 and i !=4:
                embed_month = current_month + i
                embed_month = str(embed_month)
                next_leadership = leadership[embed_month]
                em.add_field(
                    name=f"**{months_names[embed_month]}**",
                    value=f"__Líder__: {next_leadership[0]}\n__Vice__: {next_leadership[1]}",
                    inline=False
                )
                i += 1
        await ctx.reply(embed = em)

    @tasks.loop(hours=1)
    async def is_first_day_of_month(self):
        if datetime.date.today().day == 1:
            now = datetime.datetime.now(pytz.timezone('Brazil/East'))
            if now.hour == 13:
                self.disclose_leadership.start()

    @tasks.loop(count=1)
    async def disclose_leadership(self):
        data = utils.read_file("data/leadership.json")
        leadership = data[f'{datetime.date.today().month}']
        channel = self.bot.get_channel(int(LEADERSHIP_CHANNEL))
        await channel.send(f'Atenção, {PETIANES}!\nNesse mês, nosso ditador passa a ser {leadership[0]} e nosso vice, {leadership[1]}.')

def setup(bot):
    bot.add_cog(Leadership(bot))
