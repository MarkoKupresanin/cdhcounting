from os import name
import discord
from discord.ext import commands
from time import ctime
from datetime import datetime
import time
import datetime
import random
import json
import asyncio
import os
from pydactyl import PterodactylClient
from dotenv import load_dotenv
load_dotenv()
pteroAPIKey = os.environ.get("PTERODACTYL_API_KEY")


def is_it_me(ctx):
    return ctx.author.id == 430937026045673474

pteroAccessPoint = PterodactylClient('https://panel.chaoticdestiny.host/', pteroAPIKey)


class pterocontrol(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role(895220614011420712)
    async def stopserver(self, ctx, srvIndex=None):
        dontknow = int(srvIndex)
        try:
            my_servers = pteroAccessPoint.client.list_servers()
            srv_id = my_servers[dontknow]['identifier']
            await ctx.send("Ok, stopping "+srv_id+" "+my_servers[dontknow]["name"])
            pteroAccessPoint.client.send_power_action(srv_id, 'stop')
        except:
            return await ctx.send("an error occured")

    @commands.command()
    @commands.has_role(895220614011420712)
    async def restartServer(self, ctx, passedIndex):
        dontknow = int(passedIndex)
        try:
            my_servers = pteroAccessPoint.client.list_servers()
            srv_id = my_servers[dontknow]['identifier']
            await ctx.send("Ok, restarting "+srv_id+" "+my_servers[dontknow]["name"])
            pteroAccessPoint.client.send_power_action(srv_id, 'restart')
        except:
            return await ctx.send("an error occured")

    @commands.command()
    @commands.has_role(895220614011420712)
    async def listServer(self, ctx):
        my_servers = pteroAccessPoint.client.list_servers()
        for index, i in enumerate(my_servers):
            await ctx.send("> "+"Index: "+str(index) + "```"+str(i["name"])+"``` "+"Server ID: "+"``"+str(i["identifier"])+"``")


def setup(client):
    client.add_cog(pterocontrol(client))