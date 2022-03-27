from logging import exception
import discord
import os
import random
from discord.ext import commands
from datetime import datetime, time, timedelta
import asyncio

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

trigger = time(23, 00, 2)
async def background_task():
    now = datetime.utcnow()
    if now.time() > trigger:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), trigger)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await polnoc()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)



client.loop.create_task(background_task())
client.run(DISCORD_TOKEN)