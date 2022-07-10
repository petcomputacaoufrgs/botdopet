import os
import discord
import pytz
import utils.utils as utils
import datetime
from discord.ext import commands, tasks


#Constants
PETIANES = os.environ['PETIANES_ID']
ANNIVERSARY_CHANNEL = os.environ['WARNINGS_CHANNEL']
data = utils.read_file("data/anniversaries.json")


class Anniversaries(commands.Cog):
    """Routines to congratulate the petianes"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.test_aniversary.start()      

    @commands.command(name="aniversario")
    async def anniversary(self, ctx):
        loop = True
        today = datetime.date.today()
        today += datetime.timedelta(days=1)
        while loop:     
            today_formated = today.strftime("%d/%m")
            try:
                birthday_person = data[f'{today_formated}']
                loop = False
            except:
                today += datetime.timedelta(days=1)
        em = discord.Embed(color=0xFF8AD2)
        em.add_field(
            name=f"**Aniversário**",
            value=f"O próximo aniversariante é {birthday_person}, no dia {today_formated}.",
            inline=False
        )
        await ctx.send(embed = em)
    
    @tasks.loop(hours=1)
    async def test_aniversary(self):
        today = datetime.date.today().strftime("%d/%m")
        now = datetime.datetime.now(pytz.timezone('Brazil/East'))
        try:
            if now.hour == 8:
                birthday_person = data[f'{today}']
                self.congratulate.start(birthday_person)
        except:
            pass

    @tasks.loop(count=1)
    async def congratulate(self, birthday_person):
        channel = self.bot.get_channel(int(ANNIVERSARY_CHANNEL))
        await channel.send(f'Atenção, {PETIANES}, pois é dia de festa!\nO aniversariante de hoje é {birthday_person}, não se esqueçam de desejar tudo de bom e mais um pouco.')


def setup(bot):
    bot.add_cog(Anniversaries(bot))
