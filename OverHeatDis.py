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
    avg = checktemp()
    print(avg)
    embed = discord.Embed(description=f"**Average temp for CPU : {avg}° Celsius")
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator= True)
async def addvip(ctx, id):
    with open("id.txt", "a") as t:
        t.write(str(id)+ "\n")
    UL()
    print(vip)


async def Presence():
    heat = checktemp()
    if heat >= critTemp:
        for number in vip:
            vipUser = await client.fetch_user(number)
            await vipUser.send(f"CPU Temperature is critical : {str(heat)}°")

    await client.change_presence(activity=discord.Game(f"CPU Temp. : {heat}°"))
    

@client.event
async def on_disconnect():
    for number in vip:
        vipUser = await client.fetch_user(number)
        await vipUser.send(f"Cannot connecting to Discord Server")

logo= f'''
                ████              
            ████░░░░██                    OverHeat
          ██░░░░░░██                  Version : 1.0.D
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
    client.run("")