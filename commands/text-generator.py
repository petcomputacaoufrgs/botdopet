from discord.ext import commands
import discord
import utils.shakespeare as shks

class TextGenerator(commands.Cog):
    """Create random texts based on the chosen artist"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nome")
    async def shakespeare_name(self, ctx, arg):
        loop = True
        pedro = ""
        try:
            while loop:
                pedro = shks.generate_until_dot_temperature_pedro(f'{arg.upper()}')
                if pedro != "":
                    loop = False
            em = discord.Embed(color=0x80CEE1)
            em.add_field(
                name=f"**Nome shakespeariano gerado pela rede:**",
                value=f'{pedro[:-1]}',
                inline=False
            )
            await ctx.send(embed = em)
        except:
            await ctx.send('Lembre-se de não usar caractéres ausentes nos textos originais de Shakespeare, tais quais acentos e "ç".')

    @commands.command(name="frase")
    async def shakespeare_phrase(self, ctx, *args):
        message = ' '.join(args)       
        try:
            phrase = shks.generate_until_dot_temperature(message)
            em = discord.Embed(color=0x80CEE1)
            em.add_field(
                name=f"**Frase shakespeariana gerada pela rede:**",
                value=f'{phrase}',
                inline=False
            )
            await ctx.send(embed = em)
        except:
            await ctx.send('Lembre-se de não usar caractéres ausentes nos textos originais de Shakespeare, tais quais acentos e "ç".') 

def setup(bot):
    bot.add_cog(TextGenerator(bot))
