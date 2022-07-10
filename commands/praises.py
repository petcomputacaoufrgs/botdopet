import utils.utils as utils
import discord
import random
from discord.ext import commands


# Get swearings from file
data = utils.read_file('data/data.json')
offense_list = data['offenses']
praise_list = data['praises']


class Praises(commands.Cog):
    """Commands to praise someone for their positive contribution"""
    
    def __init__(self, bot):
        self.bot = bot

    # Command: Elogiar
    @commands.command(name="elogiar", help="elogie alguém que fez um bom trabalho recentemente!")
    async def praise(self, ctx, arg):
        num = random.randint(0, len(praise_list))
        await ctx.send(f'{praise_list[num].capitalize()}, {arg}!')   


    # Command: Adionar elogio
    @commands.command(name="add_elogio", help="adicione mais uma forma de falarmos bem dos nossos coleguinhas")
    async def add_praise(self, ctx, *args):
        message = ' '.join(args).lower()
        embed = discord.Embed(color=0x98FB98)
        if message == '':
            embed.add_field(
                name="**Adicionar elogio**",
                value="Não se esqueça de escrever o elogio a ser adicionado!"
            )
        else:
            if message in praise_list:
                embed.add_field(
                    name="**Adicionar elogio**",
                    value="Esse elogio já está na lista."
                ) 
            else:
                praise_list.append(message)
                utils.add_new_item_to_dict(offense_list, praise_list)
                embed.add_field(
                    name="**Adicionar elogio**",
                    value=f'"{message}" foi adicionado à lista!'
                ) 
        await ctx.reply(embed = embed) 



    # Command: Remover elogio
    @commands.command(name="rem_elogio", help="não gostou de algum elogio? só mandar o elogio a ser removido")
    async def remove_praise(self, ctx, *args):
        praise_to_be_removed = ' '.join(args).lower()
        embed = discord.Embed(color=0x98FB98)
        if praise_to_be_removed in praise_list:
            praise_list.remove(praise_to_be_removed)
            utils.add_new_item_to_dict(offense_list, praise_list)
            embed.add_field(
                name="**Adicionar elogio**",
                value=f'"{praise_to_be_removed}" foi removido da lista!'
            )
        else:
            embed.add_field(
                name="**Adicionar elogio**",
                value='Esse elogio não existe'
            )
        await ctx.reply(embed = embed)


    # Command: Mostrar elogios
    @commands.command(name="elogios")
    async def show_offenses(self, ctx):
        printable_praise_list = ', '.join(praise_list).capitalize()
        embed = discord.Embed(color=0x98FB98)
        embed.add_field(
            name="**Lista de elogios**",
            value=f'{printable_praise_list}.'
        )
        await ctx.send(embed = embed)


    # Command: Hug    
    @commands.command(name="hug", help="demonstre seu carinho por alguém")
    async def hug(self, ctx, arg):
        await ctx.send(f'<@{ctx.author.id}> abraçou beeeeem forte {arg} <3')


def setup(bot):
    bot.add_cog(Praises(bot))
