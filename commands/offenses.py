import utils.utils as utils
import os
import discord
import random
from discord.ext import commands


# Constants
MATHEUS = os.environ['MATHEUS_ID']


# Get swearings from file
data = utils.read_file('data/data.json')
offense_list = data['offenses']
praise_list = data['praises']


class Offenses(commands.Cog):
    """Offense commands against Matheus"""

    def __init__(self, bot):
        self.bot = bot

    # Command: Xingar Matheus
    @commands.command(name="xingar_matheus", help="não é necessário gastar sua saliva xingando o Matheus, o bot faz isso por você")
    async def offend_matheus(self, ctx):
        num = random.randint(0, len(offense_list))
        await ctx.send(f'{offense_list[num].capitalize()}, {MATHEUS}')   


    # Command: Adicionar xingamento
    @commands.command(name="add_xingamento", help="adicione uma nova forma de ofender o Matheus!")
    async def add_offense(self, ctx, *args):
        message = ' '.join(args).lower()
        embed = discord.Embed(color=0xFF6347)
        if message == '':
            embed.add_field(
                name="**Adicionar xingamento**",
                value="Não se esqueça de escrever o xingamento a ser adicionado!"
            )
        else:
            if message in offense_list:
                embed.add_field(
                    name="**Adicionar xingamento**",
                    value="Esse xingamento já está na lista."
                )  
            else:
                offense_list.append(message)
                utils.add_new_item_to_dict(offense_list, praise_list)
                embed.add_field(
                    name="**Adicionar xingamento**",
                    value=f'"{message}" foi adicionado à lista!'
                )
        await ctx.reply(embed = embed)


    # Command: Remover xingamento
    @commands.command(name="rem_xingamento", help="não gostou de algum xingamento? ele nunca mais será usado")
    async def remove_offense(self, ctx, *args):
        swear_to_be_removed = ' '.join(args).lower()
        embed = discord.Embed(color=0xFF6347)
        if swear_to_be_removed in offense_list:
            offense_list.remove(swear_to_be_removed)
            utils.add_new_item_to_dict(offense_list, praise_list)
            embed.add_field(
                name="**Remover xingamento**",
                value=f'"{swear_to_be_removed}" foi removido da lista!'
            )
        else:
            embed.add_field(
                name="**Remover xingamento**",
                value='Esse xingamento não existe.'
            )
        await ctx.reply(embed = embed)


    # Command: Mostrar xingamentos
    @commands.command(name="xingamentos")
    async def show_offenses(self, ctx):
        printable_offense_list = ', '.join(offense_list).capitalize()
        embed = discord.Embed(color=0xFF6347)
        embed.add_field(
            name="**Lista de xingamentos**",
            value=f'{printable_offense_list}.'
        )
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Offenses(bot))
