import os
import datetime
import pytz
import utils.utils as utils
import discord
import json
from discord.ext import commands, tasks


# Constants
PETIANES = os.environ['PETIANES_ID']
INTERPET_CHANNEL = os.environ['WARNINGS_CHANNEL']

flag = 1
interpet_day = utils.format_date().date()


class Interpet(commands.Cog):
    """Commands about the monthly interpet meeting"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.is_interpet_eve.start()

    # Command: Interpet
    @commands.command(name="interpet")
    async def interpet(self, ctx):
        embed = discord.Embed(color=0x9370DB)
        days_to_interpet = interpet_day - datetime.date.today()   
        if days_to_interpet.days < 2:
            if days_to_interpet.days == 1:
                embed.add_field(
                    name="**Interpet**",
                    value=f'Falta {days_to_interpet.days} dia até o próximo interpet, que será no dia {interpet_day.day:02d}/{interpet_day.month:02d}.'
                )
            elif days_to_interpet.days == 0:
                embed.add_field(
                    name="**Interpet**",
                    value="Hoje é o dia do interpet! Corre pra não perder a reunião."
                )
            else:
                embed.add_field(
                    name="**Interpet**",
                    value="Erro na data do interpet"
                )
        else:
            embed.add_field(
                name="**Interpet**",
                value=f'Faltam {days_to_interpet.days} dias até o próximo interpet, que será no dia {interpet_day.day:02d}/{interpet_day.month:02d}.'
            )
        await ctx.reply(embed = embed)  
        
    # Command: Interpet Ferias
    @commands.command(name="interpet_ferias")
    async def set_interpet_vacation(self, ctx):
        embed = discord.Embed(color=0x9370DB)
        self.turn_off_interpet.start()
        embed.add_field(
	        name="**Interpet**",
	        value="Bot entrando de férias das retrospectivas! Sem mais avisos ou afins."
        )
        await ctx.send(embed = embed) 

    # Command: Adionar data de interpet
    @commands.command(name="add_interpet")
    async def add_interpet(self, ctx, arg):
        data = utils.read_file('data/interpet_dates.json')
        date_list = data['dates']
        embed = discord.Embed(color=0x9370DB)
        try:
            day, month, year = arg.split('/')
            new_date = datetime.datetime(int(year), int(month), int(day)).date()
            today_date = datetime.date.today()
            if (new_date - today_date).days > 0:
                if arg == '':
                    embed.add_field(
                        name="**Adicionar data de interpet**",
                        value="Não se esqueça de escrever a data a ser adicionada!"
                    )
                else:
                    if arg in date_list:
                        embed.add_field(
                            name="**Adicionar data de interpet**",
                            value="Essa data já está na lista."
                        ) 
                    else:
                        date_list.append(arg)
                        dict = {'dates': date_list}
                        with open('data/interpet_dates.json', 'w+', encoding='utf-8') as outfile:
                            json.dump(dict, outfile)
                        embed.add_field(
                            name="**Adicionar data de interpet**",
                            value=f'A data {arg} foi adicionada com sucesso!'
                        )
            else:
                raise
        except:
            embed.add_field(
                        name="**Adicionar data de interpet**",
                        value=f'Lembre-se de usar o formato `<dd/mm/aaaa>` e com datas válidas!'
                    )              
        await ctx.send(embed = embed)

    # Command: Remover data de interpet
    @commands.command(name="rem_interpet")
    async def remove_offense(self, ctx, arg):
        data = utils.read_file('data/interpet_dates.json')
        date_list = data['dates']
        embed = discord.Embed(color=0x9370DB)
        if arg in date_list:
            date_list.remove(arg)
            dict = {'dates': date_list}
            with open('data/interpet_dates.json', 'w+', encoding='utf-8') as outfile:
                json.dump(dict, outfile)
            embed.add_field(
                name="**Remover data de interpet**",
                value=f'A data foi removida da lista!'
            )
        else:
            embed.add_field(
                name="**Remover data de interpet**",
                value='Essa data não está na lista.'
            )
        await ctx.send(embed = embed)

    # Command: Mostrar datas de interpet
    @commands.command(name="interpet_datas")
    async def show_dates(self, ctx):
        data = utils.read_file('data/interpet_dates.json')
        date_list = data['dates']
        for date in date_list:
            day, month, year = date.split('/')
            difference = datetime.datetime(int(year), int(month), int(day)).date() - datetime.date.today()
            if (difference).days < 0:
                date_list.remove(date)
            else:
                date =f"{date} - daqui a {(difference).days}"
        printable_date_list = '\n'.join(date_list)
        embed = discord.Embed(color=0x9370DB)
        embed.add_field(
            name="**Datas dos próximos interpets:**",
            value=f'{printable_date_list}'
        )
        await ctx.send(embed = embed)
        
    # Internal Task: Desliga interpet
    @tasks.loop(count=1)
    async def turn_off_interpet(self):
        self.is_interpet_eve.cancel()
    
    # Task: check if today is interpet eve
    @tasks.loop(hours=1)
    async def is_interpet_eve(self):
        global interpet_day
        now = datetime.datetime.now(pytz.timezone('Brazil/East'))
        if interpet_day == datetime.date.today() + datetime.timedelta(days=1):
            if now.hour == 20:
                self.remember_interpet.start()
        if interpet_day == datetime.date.today():
            if now.hour == 8:
                self.awake_interpet.start()
        if interpet_day == datetime.date.today() - datetime.timedelta(days=1):
            if now.hour == 1:
                self.update_interpet_day.start()

    # Task: send the warning to every petiane
    @tasks.loop(count=1)
    async def remember_interpet(self):
        global interpet_day
        channel = self.bot.get_channel(int(INTERPET_CHANNEL))
        await channel.send(f'Atenção, {PETIANES}!\nLembrando que amanhã é dia de interpet, estejam acordados às 9h.')         

    @tasks.loop(count=1)
    async def awake_interpet(self):
        global interpet_day
        channel = self.bot.get_channel(int(INTERPET_CHANNEL))
        await channel.send(f'Atenção, {PETIANES}!\nMenos de uma hora para começar o interpet, espero que todos já estejam acordados.')  
      
    # Task: set the interpet day to the next date in the list
    @tasks.loop(count=1)
    async def update_interpet_day(self):
        global interpet_day
        interpet_day = utils.format_date().date()


def setup(bot):
    bot.add_cog(Interpet(bot))
