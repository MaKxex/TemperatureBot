import sys, os

try:
    import discord
    from discord.ext import commands
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except Exception as e:
    print(e)
    os.system('pip install discord & pip install wmi')
    sys.exit("Restart the Prototype.")

from CheckTemp import checktemp, checkusage
import config

client = commands.Bot(command_prefix=".")
sched = AsyncIOScheduler()

vip = []
critTemp = int(input("Critical Heat level : "))


def UL():
    vip.clear()
    with open("id.txt", "r") as t:
        numbers = t.readlines()
        for i in numbers:
            vip.append(i)


@client.event
async def on_ready():
    print("Ready")
    UL()
    print(vip)


@client.command()
async def temp(ctx):
    author = ctx.author

    cpuTemp, gpuTemp  = checktemp()

    embed=discord.Embed(color=0xcb0b0b)
    embed.set_author(name=author)
    embed.add_field(name="CPU Temp:", value= f"{cpuTemp}°", inline=True)
    embed.add_field(name="GPU Temp:", value= f"{gpuTemp}°", inline=True)
    embed.set_footer(text="Temperature in celsius")

    await ctx.send(embed=embed)


@client.command()
async def info(ctx):
    author = ctx.author
    cpuTemp, gpuTemp = checktemp()
    cpu, ram, gpu= checkusage()

    embed=discord.Embed(color=0xcb0b0b)
    embed.set_author(name=author)
    embed.add_field(name="CPU Usage:", value= f"{str(cpu).partition('.')[0]}% \n Temperature : {cpuTemp}°", inline=True)
    embed.add_field(name="GPU Usage:", value= f"{str(gpu).partition('.')[0]}% \n Temperature : {gpuTemp}°", inline=True)
    embed.add_field(name="Memory:", value= f"{str(ram).partition('.')[0]}%", inline=False)
    embed.set_footer(text="Temperature in celsius")
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator= True)
async def addvip(ctx, id):
    with open("id.txt", "a") as t:
        t.write(str(id)+ "\n")
    UL()
    print(vip)


@client.command()
@commands.has_permissions(administrator= True)
async def clear(ctx, number):
    await ctx.channel.purge(limit=int(number) + 1)

async def Presence():
    cpuTemp, gpuTemp = checktemp()
    if cpuTemp >= critTemp:
        for number in vip:
            vipUser = await client.fetch_user(number)
            await vipUser.send(f"CPU Temperature is critical : {str(cpuTemp)}°")
    await client.change_presence(activity=discord.Game(f"CPU Temp. : {cpuTemp}°"))

@client.event
async def on_disconnect():
    for number in vip:
        vipUser = await client.fetch_user(number)
        await vipUser.send(f"Cannot connect to the Discord Server")

logo= f'''
                    ████              
                ████░░░░██                    OverHeat
              ██░░░░░░██                  Version : 1.1.D
            ██░░░░░░██                     Author : MaKxex
          ██░░░░░░░░██                 Crit. heat : {critTemp}
          ██░░░░░░██  ██                  
        ██░░░░░░░░████░░██                
        ██░░░░░░░░██░░░░░░██              
        ██░░░░░░░░░░░░░░░░░░██        
      ████░░░░░░░░░░░░░░░░░░░░████    
    ██░░██░░░░░░░░░░░░░░░░░░░░░░░░██  
    ██░░░░██░░░░░░░░░░░░░░░░░░░░░░░░██
    ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
    ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
    ██░░░░░░░░░░░░░░░░░░░░  ██░░░░░░██
    ██░░░░░░  ██░░░░░░░░░░████░░░░░░██
    ██░░░░░░▓▓██░░░░░░██░░░░░░░░░░░░██
      ██░░░░░░░░░░████░░░░░░░░░░░░░░██
      ██░░░░░░░░░░░░░░░░░░░░░░░░░░██  
        ██░░░░░░░░░░░░░░░░░░░░░░██    
          ██░░░░░░░░░░░░░░░░░░██      
            ████░░░░░░░░░░░░██        
                ████████████          
'''

sched.add_job(Presence, 'interval', seconds=10)
sched.start()

print(logo)

if __name__ == "__main__":
    client.run(config.settings.get("token"))
