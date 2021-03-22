import sys, os

try:
    import discord
    from discord.ext import commands
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except Exception as e:
    print(e)
    os.system('pip install discord & pip install wmi')
    sys.exit("Restart the Prototype.")

from CheckTemp import checktemp

client = commands.Bot(command_prefix=".")
sched = AsyncIOScheduler()

@client.event
async def on_ready():
    print("Ready")

@client.command()
async def temp(ctx):
    avg = checktemp()
    print(avg)
    embed = discord.Embed(description=f"**Average temp for CPU : {avg}** Celsius")
    await ctx.send(embed=embed)

async def Presence():
    presence = checktemp()
    await client.change_presence(activity=discord.Game(f"CPU Temp. : {presence}°"))

sched.add_job(Presence, 'interval', seconds=10)
sched.start()

client.run("TOKEN")
