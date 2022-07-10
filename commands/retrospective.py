import os
import discord
import datetime
import pytz 
import utils.utils as utils
from discord.ext import commands, tasks


# Constants
PETIANES = os.environ['PETIANES_ID']
RETRO_CHANNEL = os.environ['WARNINGS_CHANNEL']


flag = 1
retro_day = utils.initialize_date(datetime.date(2022, 1, 28), 14)


class Retrospective(commands.Cog):
    """Commands about the biweekly retrospective on discord"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.is_retrospective_eve.start()

    # Command: Retrospectiva
    @commands.command(name="retro")
    async def retrospective(self, ctx):
        embed = discord.Embed(color=0xF0E68C)
        days_to_retro = retro_day - datetime.date.today()
        if days_to_retro.days < 2:
            if days_to_retro.days == 1:
                embed.add_field(
                        name="**Retrospectiva**",
                        value=f'Falta {days_to_retro.days} dia até a próxima retrospectiva, que será no dia {retro_day.day:02d}/{retro_day.month:02d}.'
                )
            elif days_to_retro.days == 0:
                embed.add_field(
                    name="**Retrospectiva**",
                    value='Hoje é o dia da retrospectiva! Corre que ainda da tempo de escrever.'
                )
            else:
                embed.add_field(
                    name="**Retrospectiva**",
                    value="Erro na data da retrospectiva"
                )
        else:
            embed.add_field(
                name="**Retrospectiva**",
                value=f'Faltam {days_to_retro.days} dias até a próxima retrospectiva, que será no dia {retro_day.day:02d}/{retro_day.month:02d}.'
            )
        await ctx.reply(embed = embed) 

    # Command: Retrospectiva Manual
    @commands.command(name="retro_manual")
    async def set_retrospective(self, ctx, arg):
        day, month = arg.split('/')
        embed = discord.Embed(color=0xF0E68C)
        if int(day) < 1 or int(day) > 31 or int(month) < 1 or int(month) > 12:
            embed.add_field(
                name="**Retrospectiva**",
                value="Informe uma data válida."
            )
        elif (datetime.date(int(datetime.date.today().year), int(month), int(day)) - datetime.date.today()).days < 0:
            embed.add_field(
                name="**Retrospectiva**",
                value="Informe uma data válida."
            )
        else:
            global flag
            if flag == 1:
                flag = 0
                await self.turn_off_retrospective.start()
                await self.set_retrospective(ctx, arg)
            else:    
                global retro_day
                retro_day = datetime.date(int(datetime.date.today().year), int(month), int(day))
                self.is_retrospective_eve.start()
                flag = 1
                embed.add_field(
	                name="**Retrospectiva**",
	                value=f'Retrospectiva manualmente ajustada para a data {retro_day.day:02d}/{retro_day.month:02d}.'
            	)
        await ctx.reply(embed = embed)

    # Command: Retrospectiva Ferias
    @commands.command(name="retro_ferias")
    async def set_retrospective_vacation(self, ctx):
        embed = discord.Embed(color=0xF0E68C)
        self.turn_off_retrospective.start()
        embed.add_field(
	        name="**Retrospectiva**",
	        value="Bot entrando de férias das retrospectivas! Sem mais avisos ou afins."
        )
        await ctx.send(embed = embed)

    # Internal Task: Desliga retro
    @tasks.loop(count=1)
    async def turn_off_retrospective(self):
        self.is_retrospective_eve.cancel()

    # Task: check if today is retrospective eve
    @tasks.loop(hours=1)
    async def is_retrospective_eve(self):
        global retro_day
        now = datetime.datetime.now(pytz.timezone('Brazil/East'))
        if retro_day == datetime.date.today() + datetime.timedelta(days=1):
            if now.hour == 15:
                self.remember_retrospective.start()
        if retro_day == datetime.date.today():
            if now.hour == 23:
                self.update_retro_day.start()

    # Task: send the warning to every petiane
    @tasks.loop(count=1)
    async def remember_retrospective(self):
        global RETRO_CHANNEL
        channel = self.bot.get_channel(int(RETRO_CHANNEL))
        await channel.send(f'Atenção, {PETIANES}!\nLembrando que amanhã é dia de retrospectiva, já aproveitem pra escrever o textos de vocês.')

    # Task: set the retrospective day to 2 weeks later
    @tasks.loop(count=1)
    async def update_retro_day(self):
        global retro_day
        retro_day += datetime.timedelta(days=14)


def setup(bot):
    bot.add_cog(Retrospective(bot))
