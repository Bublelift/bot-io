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
    print("Bot ready!")

@client.command(aliases = ["ping"], brief = "Oznacza obecnego chada")
async def kto(ctx):
    chad_role = discord.utils.find(lambda x: x.name == "Chad", ctx.guild.roles)
    current_chad = discord.utils.find(lambda x: chad_role in x.roles, ctx.guild.members)
    await ctx.send(f"Chadem jest {current_chad.mention}")

@client.command(brief = "Wyznacza losowo innego Chada. Tylko Chad może użyć tej komendy.")
async def roll(ctx):#, user : discord.Member, *, role : discord.Role):
    chad_role = discord.utils.find(lambda x: x.name == "Chad", ctx.guild.roles)
    admin = discord.utils.find(lambda x: x.id == 693164199261503569, ctx.guild.roles)
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
        await announce(wybraniec)
    else:
        return await ctx.send("Nie możesz tego zrobić.")

@client.command(aliases = ["przekaz", "oddaj", "daj"], brief = "Oddaje rolę Chada oznaczonej osobie. Tylko Chad może użyć tej komendy.")
async def przekaż(ctx, user : discord.Member):
    chad_role = discord.utils.find(lambda x: x.name == "Chad", ctx.guild.roles)
    admin = discord.utils.find(lambda x: x.id == 693164199261503569, ctx.guild.roles)
    if chad_role in ctx.message.author.roles or admin in ctx.message.author.roles:
        aktywista = discord.utils.find(lambda x: x.name == "Aktywista", ctx.guild.roles)
        if aktywista not in user.roles:
            return await ctx.send("To nie jest kandydat do roli Chada.")
        current_chad = discord.utils.find(lambda x: chad_role in x.roles, ctx.guild.members)
        await current_chad.remove_roles(chad_role)
        await user.add_roles(chad_role)
        await ctx.send("Ok :smiling_face_with_tear:")
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
        if chad_role in member.roles:
            await member.remove_roles(chad_role)
        elif aktywista in member.roles:
            kandydaci.append(member)
    wybraniec = random.choice(kandydaci)
    await wybraniec.add_roles(chad_role)
    await announce(wybraniec)

async def announce(wybraniec):
    piaskownica = client.get_guild(473907456007995403)
    kanal = discord.utils.find(lambda x: x.name == "ja-robot", piaskownica.channels)
    content = random.choice(
        [f"Nowym Chadem jest {wybraniec.mention}.", 
        f"Od teraz dzierżysz władzę {wybraniec.mention}!",
        f"{wybraniec.mention} osiąga ponad 9000 poziom :open_mouth:",
        f"{wybraniec.mention} ma teraz prawo do rozstawiania wszystkich po kątach",
        f"To ptak? To samolot? Nie, to {wybraniec.mention} spuszcza na nas bombę!",
        f"{wybraniec.mention} wygrywa totalnie demokratyczne wybory",
        f"Uważajcie na {wybraniec.mention}, może zrobić krzywdę!",
        f"{wybraniec.mention} na mocy prawa niespodzianki zostaje dzisiaj Chadem.",
        f"Jakie uniwersum wymyśli nam dzisiaj {wybraniec.mention}?",
        f"Chadowy outfit {wybraniec.mention} :wink:",
        f"Dzisiaj {wybraniec.mention} będzie wyjaśniać frajerów :sunglasses:",
        f"Habemus Chadam! {wybraniec.mention} I!",
        f"{wybraniec.mention} wychodował bujną brodę.",
        f"Dzisiaj {wybraniec.mention} ma zawsze rację :shrug:",
        f"{wybraniec.mention} włącza godmode na 24h.",
        f"Główną nagrodę Lotto zgarnia dzisiaj {wybraniec.mention}! Wielkie brawa!",
        f"Chodząca doskonałość? Tak, to {wybraniec.mention} :heart:",
        f"Jeszcze gdy chodziłem do podstawówki, to był tam taki {wybraniec.mention} i ja jechałem na rowerze, i go spotkałem, i potem jeszcze pojechałem do biedronki na lody, i po drodze do domu wtedy jeszcze, już do domu pojechałem.",
        f"{wybraniec.mention} przejmuje wszystkie akcje Tesli",
        f"Oddajcie pokłon {wybraniec.mention}",
        f"Mamo nie sprzątaj. {wybraniec.mention} pozamiatał XDDDDDD",
        f"Hej {wybraniec.mention}, zrób coś fajnego :grinning:",
        f"{wybraniec.mention} ma w posiadaniu kamień nieskończoności",
        f"Lepiej zapnijcie pasy, {wybraniec.mention} zaczyna swoją kadencję",
        f"chciałem powiedzieć tu coś kreatywnego, ale nie \n||Chadem jest {wybraniec.mention}||",
        f"Masz tę moc {wybraniec.mention}!",
        f"**TOP 10 najfajniejszych ludzi na świecie.** \n1: {wybraniec.mention}",
        f"Wyobrażacie sobie świat bez {wybraniec.mention}? Ja też nie.",
        f"Dzwoni papuga, mówi że chce autograf od {wybraniec.mention}",
        f"Przychodzi {wybraniec.mention} do lekarza, a lekarz aż się schował.",
        f"{wybraniec.mention} nauczył się strzelać laserem z tyłu!",
        f"Tajny agent {wybraniec.mention} rozpoczyna obalanie komuny",
        f"{wybraniec.mention} nie mógł się doczekać awansu",
        f"Prezydent uhonorował {wybraniec.mention} odznaką Virtutti Chadari :crown:",
        f"Nowy bestseller J.K.Rowling: 'Ludzie sukcesu. Być jak {wybraniec.mention}'"
        ])
    await kanal.send(content)

trigger = time(23, 00, 2) #22 dla czasu letniego
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


# client.loop.create_task(background_task())
# client.run(DISCORD_TOKEN)

async def run():
    async with client:
        client.loop.create_task(background_task())
        await client.start(DISCORD_TOKEN)

asyncio.run(run())