#from asyncio.windows_events import NULL
from logging import exception
from sqlite3 import Time
import discord
import os
import random
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta

DISCORD_TOKEN = os.environ["discord_token"]

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents, command_prefix="!")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Losowanie Chada"))
    print("Ready!")

@client.command(brief = "Wyznacza losowo innego Chada. Tylko Chad może użyć tej komendy.")
async def roll(ctx):#, user : discord.Member, *, role : discord.Role):
    chad_role = discord.utils.find(lambda x: x.name == "Chad", ctx.guild.roles)
    admin = discord.utils.find(lambda x: x.name == "Bąbel", ctx.guild.roles)
    if chad_role in ctx.message.author.roles or admin in ctx.message.author.roles:
        aktywista = discord.utils.find(lambda x: x.name == "Aktywista", ctx.guild.roles)
        kandydaci = []
        for member in ctx.guild.members:
            if aktywista in member.roles:
                kandydaci.append(member)
            if chad_role in member.roles:
                await member.remove_roles(chad_role)
        wybraniec = random.choice(kandydaci)
        await wybraniec.add_roles(chad_role)
        await ctx.send(f"Nowym chadem jest {wybraniec.display_name}")
    else:
        return await ctx.send("Nie możesz tego zrobić.")

@client.command(aliases = ["przekaz", "oddaj", "daj"], brief = "Oddaje rolę Chada oznaczonej osobie. Tylko Chad może użyć tej komendy.")
async def przekaż(ctx, user : discord.Member):
    chad_role = discord.utils.find(lambda x: x.name == "Chad", ctx.guild.roles)
    admin = discord.utils.find(lambda x: x.name == "Bąbel", ctx.guild.roles)
    if chad_role in ctx.message.author.roles or admin in ctx.message.author.roles:
        aktywista = discord.utils.find(lambda x: x.name == "Aktywista", ctx.guild.roles)
        if aktywista not in user.roles:
            return await ctx.send("To nie jest kandydat do roli Chada.")
        for member in ctx.guild.members:
            if chad_role in member.roles:
                await member.remove_roles(chad_role)
        await user.add_roles(chad_role)
        await ctx.send("Ok :)")
    else:
        return await ctx.send("Nie możesz tego zrobić.")

@przekaż.error
async def przekaż_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        tag = discord.utils.find(lambda x: x.name == "oznaczyć", ctx.guild.roles)
        await ctx.send(f"Musisz {tag.mention} osobę, która ma być Chadem. Alternatywnie możesz użyć **!roll**, żeby przekazać losowo.")


@client.event
async def on_message(message):
    if(message.channel.name not in ("muzyka", "ja-robot", "developer", "tajny")):
        #if(message.content.startswith(("-p ", "!p ", "qquiz"))):
        badwords = ("-p ", "!p ", "qquiz")
        if(any(map(message.content.startswith, badwords))):
            return await message.delete()
    await client.process_commands(message)

async def polnoc():
    await client.wait_until_ready()
    piaskownica = client.get_guild(473907456007995403)
    chad_role = discord.utils.find(lambda x: x.name == "Chad", piaskownica.roles)
    aktywista = discord.utils.find(lambda x: x.name == "Aktywista", piaskownica.roles)
    kandydaci = []
    for member in piaskownica.members:
        if aktywista in member.roles:
            kandydaci.append(member)
        if chad_role in member.roles:
            await member.remove_roles(chad_role)
    
    wybraniec = random.choice(kandydaci)
    await wybraniec.add_roles(chad_role)


@tasks.loop(seconds=1)
async def bg_task():
    now = datetime.utcnow()
    nower = now.strftime("%H:%M:%S")
    if(nower == '23:00:01'):
        await polnoc()

bg_task.start()
client.run(DISCORD_TOKEN)