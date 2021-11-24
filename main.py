import asyncio
import discord
from discord.ext import commands
#from discord.ext import tasks
import random
import math
import json
from io import BytesIO
from time import ctime
import datetime
from datetime import datetime
import time
from http import client as http_client
import os
import secrets
from datetime import timezone
import sqlite3
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.messages = True

current_local = time.localtime()
CURRENT_UTC_TIME = str(datetime.now().time().strftime('%I:%M %p') + " " +current_local.tm_zone)
DISCORD_BOT_TOKEN = os.environ.get("BOT_TOKEN")

client = commands.Bot(command_prefix="c!", case_insensitive=True, intents=intents)


def is_it_me(ctx):
    return ctx.author.id == 430937026045673474
directory = 'cogs'
@client.event
async def on_ready():
    cogList = []
    for filename in os.scandir(directory):
        if filename.is_file:
            working = filename.name[:-3]
            cogList.append(working)
    
    for i in cogList:
        try:    
            client.load_extension(f"cogs.{i}")
            print(f"Cog Loaded: {i}")
        except:
            pass
    #client.unload_extension("cogs.PTEROCONTROL")
    #client.load_extension('cogs.COUNTER')
    print(f"Currently in {len(client.guilds)} server(s)")
    print(f"{len(client.users)} users detected")
    print("Chaotic Destiny Counting is online.")

@client.command()
@commands.check(is_it_me)
async def reload(ctx, extension):
    """This command reloads a specified cog."""
    try:
        workingCog = extension.upper()
        client.unload_extension(f"cogs.{workingCog}")
        client.load_extension(f"cogs.{workingCog}")
        conf_Message = await ctx.send(f"The cog **{workingCog}** has been unloaded and reloaded.")
        print(f"Unloaded and Loaded {workingCog}")
    except Exception as e:
        await ctx.send(e)
    
@client.command()
@commands.check(is_it_me)
async def turnoff(ctx, extension):
    """This command unloads a specified cog."""
    try:
        workingCog = extension.upper()
        client.unload_extension(f"cogs.{workingCog}")
        conf_Message = await ctx.send(f"The cog **{workingCog}** has been disabled.")
    except Exception as e:
        await ctx.send(e)

@client.command()
@commands.check(is_it_me)
async def turnon(ctx, extension):
    """This command loads a specified cog."""
    try:
        workingCog = extension.upper()
        client.load_extension(f"cogs.{workingCog}")
        conf_Message = await ctx.send(f"The cog **{workingCog}** has been enabled.")
        await asyncio.sleep(3)
    except Exception as e:
        await ctx.send(e)


client.run(DISCORD_BOT_TOKEN)
