import datetime
import unidecode
import discord
from discord.ext import commands, tasks
from dateutil.relativedelta import relativedelta

class Custom_commands(commands.Cog):
    """Customizable commands for the BOT"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.restart_parameters.start()

    @commands.command(name="aviso")
    async def notice(self, ctx, *args):
        global step
        global notice_name
        global notice_number
        global notice_string
        global ping_list 
        global notice_channel
        global notice_date
        global is_date_form

        step += 1

        # Aborting its creation 
        if step > 1 and args[0] == "cancelar":
            self.restart_parameters.start()
            if step == 6:
                self.is_notice_time.cancel()
            em = discord.Embed(
                title=f"**__Evento cancelado__**",
                description="Evento cancelado com sucesso. Outro já pode ser criado em seu lugar.",
                color=0xBDECB6
            )
            await ctx.send(embed = em)

        else:

            # Step 1: choosing the notice's name
            if step == 1:
                await ctx.channel.purge(limit=1)
                em = discord.Embed(
                    title=f"**__Criando um aviso:__ etapa {step}/4**",
                    description="Primeiramente, escolha um nome para o aviso.",
                    color=0xBDECB6
                )
                em.add_field(
                    name="Como a função deve ser rechamada:",
                    value="```pet.aviso <nome do aviso>```",
                    inline=False
                )
                em.set_footer(text="Deseja cancelar a criação deste aviso? Digite pet.aviso cancelar")
                await ctx.send(embed = em)

            # Step 2: defining when the notice will happen
            elif step == 2:
                await ctx.channel.purge(limit=2)
                notice_name = ' '.join(args)
                if notice_name == "":
                    step -= 1
                    await ctx.reply("O nome do aviso não pode ser vazio! Rechame a função, mas agora não se esqueça de colocar um nome.")
                else:
                    em = discord.Embed(
                        title=f"**__Criando um aviso:__ etapa {step}/4**",
                        description=f'Perfeito! A criação do aviso "{notice_name}" foi iniciada.\n\nAgora, defina daqui a quanto tempo o aviso deve acontecer.',
                        color=0xBDECB6
                    )
                    em.add_field(
                        name="**Como a função deve ser rechamada:**",
                        value="```pet.aviso <tempo até o aviso acontecer> ou <dd/mm/aaaa>```",
                        inline=False
                    )
                    em.set_footer(text="Deseja cancelar a criação deste aviso? Digite pet.aviso cancelar")
                    await ctx.send(embed = em)

            # Step 3: deciding who to ping    
            elif step == 3:
                await ctx.channel.purge(limit=2)
                if len(args) == 2:    
                    notice_number = int(args[0])
                    notice_string = args[1]
                    is_date_form = False
                    em = discord.Embed(
                        title=f"**__Criando um aviso:__ etapa {step}/4**",
                        description=f'Quase acabando! Evento programado para daqui {args[0]} {args[1]}.\n\nChegou a hora de escolher quem será pingado no aviso.',
                        color=0xBDECB6
                    )
                elif len(args) == 1:
                    day, month, year = args[0].split('/')
                    day = int(day)
                    month = int(month)
                    year = int(year)
                    is_date_form = True
                    notice_date = datetime.datetime(year, month, day, 9)
                    em = discord.Embed(
                        title=f"**__Criando um aviso:__ etapa {step}/4**",
                        description=f'Quase acabando! Evento programado para a data {day:02d}/{month:02d}/{year:04d}.\n\nChegou a hora de escolher quem será pingado no aviso.',
                        color=0xBDECB6
                    )
                else:
                    step -= 1
                    await ctx.send("Verifique as entradas para o comando.")

                em.add_field(
                    name="**Como a função deve ser rechamada:**",
                    value="```pet.aviso <@pessoa 1> <@pessoa 2> ... <@pessoa n>```*Lembrando que tanto cargos quanto pessoas podem ser pingadas.*",
                    inline=False
                )
                em.set_footer(text="Deseja cancelar a criação deste aviso? Digite pet.aviso cancelar")
                await ctx.send(embed = em)
            
            # Step 4: channel to send the message
            elif step == 4:
                await ctx.channel.purge(limit=2)
                for i in range(len(args)):
                    ping_list.append(args[i])
                printable_ping_list = ', '.join(ping_list)
                em = discord.Embed(
                    title=f"**__Criando um aviso:__ etapa {step}/4**",
                    description=f'Tudo anotado! Será/serão pingade(s): {printable_ping_list}.\n\nPor fim, escreva o canal no qual o aviso deverá ser enviado.',
                    color=0xBDECB6
                )
                em.add_field(
                    name="**Como a função deve ser rechamada:**",
                    value="```pet.aviso <#nome do canal>```*Não esqueça de checar se o bot tem acesso ao canal desejado!.*",
                    inline=False
                )
                em.set_footer(text="Deseja cancelar a criação deste aviso? Digite pet.aviso cancelar")
                await ctx.send(embed = em)

            # Step 5: review
            elif step == 5:
                await ctx.channel.purge(limit=2)
                notice_channel = args[0]
                printable_ping_list = ', '.join(ping_list)
                em = discord.Embed(
                    title=f"**__Evento criado com sucesso!__**",
                    description=f'Confira as informações sobre ele abaixo:',
                    color=0xBDECB6
                )
                em.add_field(
                    name="**Nome:**",
                    value=f'*{notice_name}*',
                    inline=False
                )
                if is_date_form == False:
                    em.add_field(
                        name="**Quando:**",
                        value=f'Daqui *{notice_number} {notice_string}*',
                        inline=False
                    )
                else:
                    em.add_field(
                        name="**Quando:**",
                        value=f'No dia *{notice_date.day:02d}/{notice_date.month:02d}/{notice_date.year:04d}*',
                        inline=False
                    )
                em.add_field(
                    name="**Quem será pingado:**",
                    value=f'*{printable_ping_list}*',
                    inline=False
                )
                em.add_field(
                    name="**Onde:**",
                    value=f'*{notice_channel}*',
                    inline=False
                )
                em.set_footer(text="Deseja cancelar esse aviso? Digite pet.aviso cancelar")
                await ctx.send(embed = em)

                # The creation itself
                if is_date_form == False:
                    notice_string = unidecode.unidecode(notice_string)
                    if notice_string == "minuto" or notice_string == "minutos":
                        notice_date = datetime.datetime.today() + datetime.timedelta(minutes=notice_number)
                    if notice_string == "hora" or notice_string == "horas":
                        notice_date = datetime.datetime.today() + datetime.timedelta(hours=notice_number)
                    if notice_string == "dia" or notice_string == "dias":
                        notice_date = datetime.datetime.today() + datetime.timedelta(days=notice_number)
                    if notice_string == "mes" or notice_string == "meses":
                        notice_date = datetime.datetime.today() + relativedelta(months=notice_number)
                self.is_notice_time.start()

            else:
                self.current_notice(ctx)

    @commands.command(name="aviso_atual")
    async def current_notice(self, ctx):
        if(self.is_notice_time.is_running() == True):
            printable_ping_list = ', '.join(ping_list)
            em = discord.Embed(
                title=f"**Já há um aviso programado.**",
                description=f'Confira as informações sobre ele abaixo:',
                color=0xBDECB6
            )
            em.add_field(
                name="**Nome:**",
                value=f'*{notice_name}*',
                inline=False
            )
            if is_date_form == False:
                em.add_field(
                    name="**Quando:**",
                    value=f'Daqui *{notice_number} {notice_string}*',
                    inline=False
                )
            else:
                em.add_field(
                    name="**Quando:**",
                    value=f'No dia *{notice_date.day:02d}/{notice_date.month:02d}/{notice_date.year:04d}*',
                    inline=False
                )
            em.add_field(
                name="**Quem será pingado:**",
                value=f'*{printable_ping_list}*',
                inline=False
            )
            em.add_field(
                name="**Onde:**",
                value=f'*{notice_channel}*',
                inline=False
            )
            em.set_footer(text="Deseja cancelar esse aviso? Digite pet.aviso cancelar")
            await ctx.send(embed = em)
        else:
            em = discord.Embed(
                title=f"**Ainda não há um aviso programado.**",
                description=f'Use `pet.aviso` para criar um novo!',
                color=0xBDECB6
            )
            await ctx.send(embed = em)


    @tasks.loop(count=1)
    async def restart_parameters(self):
        global step
        global notice_name
        global notice_number
        global notice_string
        global ping_list
        global notice_channel
        global notice_date
        global is_date_form

        step = 0
        notice_name = ""
        notice_number = 0
        notice_string = ""
        ping_list = []
        notice_channel = ""
        notice_date = datetime.datetime.today()
        is_date_form = False

    @tasks.loop(seconds=30)
    async def is_notice_time(self):
        global notice_date
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%y as %H:%M")
        if type(notice_date) == datetime.datetime:
            notice_date = notice_date.strftime("%d/%m/%y as %H:%M")
        if notice_date == now:
            self.send_notice.start()
    
    @tasks.loop(count=1)
    async def send_notice(self):
        global notice_channel
        global notice_name
        characters_to_remove = "<#>"
        for character in characters_to_remove:
            notice_channel = notice_channel.replace(character, "")
        channel = self.bot.get_channel(int(notice_channel))

        em = discord.Embed(
            title=f"**{notice_name}**",
            description=f'A hora do aviso chegou!',
            color=0xBDECB6
        )
        await channel.send(embed = em)

        printable_ping_list = ', '.join(ping_list)
        await channel.send(f"{printable_ping_list}")
        self.restart_parameters.start()
        self.is_notice_time.cancel()


def setup(bot):
    bot.add_cog(Custom_commands(bot))
