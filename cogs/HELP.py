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
from dotenv import load_dotenv
load_dotenv()

def is_it_me(ctx):
    return ctx.author.id == 430937026045673474


class helpEmbed:
    def __init__(self, client):
        self.client = client

    def makeEmbed(self, embed_color, cmd_name, cmd_desc, REQargs=None, OPTargs = None, aliases=None):
        GOTCHA=True
        temp = discord.Embed(title=f"{cmd_name} Command", description=f"{cmd_desc}", color=embed_color)
        if REQargs != None:
            argumentsList = []
            for x in REQargs:
                argumentsList.append(x)
            if len(argumentsList)==1:
                temp.add_field(name="Syntax:", value=f"```c!{cmd_name} <{argumentsList[0]}>```", inline=False)
            if len(argumentsList)==2:
                temp.add_field(name="Syntax:", value=f"```c!{cmd_name} <{argumentsList[0]}> <{argumentsList[1]}>```", inline=False)
            if len(argumentsList)==3:
                temp.add_field(name="Syntax:", value=f"```c!{cmd_name} <{argumentsList[0]}> <{argumentsList[1]}> <{argumentsList[2]}>```", inline=False)
            if len(argumentsList)==4:
                temp.add_field(name="Syntax:", value=f"```c!{cmd_name} <{argumentsList[0]}> <{argumentsList[1]}> <{argumentsList[2]}> <{argumentsList[3]}>```", inline=False)
            if len(argumentsList)==5:
                temp.add_field(name="Syntax:", value=f"```c!{cmd_name} <{argumentsList[0]}> <{argumentsList[1]}> <{argumentsList[2]}> <{argumentsList[3]}> <{argumentsList[4]}>```", inline=False)
            GOTCHA=False
        if OPTargs != None:
            otherArgumentsList=[]
            for i in OPTargs:
                otherArgumentsList.append(i)
            if len(otherArgumentsList)==1:
                temp.add_field(name="Syntax:", value=f"```c!{cmd_name} <{otherArgumentsList[0]}>```", inline=False)
            if len(otherArgumentsList)==2:
                temp.add_field(name="Syntax:", value=f"```c!{cmd_name} <{otherArgumentsList[0]}> <{otherArgumentsList[1]}>```", inline=False)
            if len(otherArgumentsList)==3:
                temp.add_field(name="Syntax:", value=f"```c!{cmd_name} <{otherArgumentsList[0]}> <{otherArgumentsList[1]}> <{otherArgumentsList[2]}>```", inline=False)
            if len(otherArgumentsList)==4:
                temp.add_field(name="Syntax:", value=f"```c!{cmd_name} <{otherArgumentsList[0]}> <{otherArgumentsList[1]}> <{otherArgumentsList[2]}> <{otherArgumentsList[3]}>```", inline=False)
            if len(otherArgumentsList)==5:
                temp.add_field(name="Syntax:", value=f"```c!{cmd_name} <{otherArgumentsList[0]}> <{otherArgumentsList[1]}> <{otherArgumentsList[2]}> <{otherArgumentsList[3]}> <{otherArgumentsList[4]}>```", inline=False)      
            GOTCHA=False
        if REQargs==None and GOTCHA:
            temp.add_field(name="Syntax:", value=f"```c!{cmd_name}```", inline=False)
        elif OPTargs == None and GOTCHA:
            temp.add_field(name="Syntax:", value=f"```c!{cmd_name}```", inline=False)
        
        if aliases==None:
            aliases == str("None")
        temp.add_field(name="Aliases:", value=f"{aliases}", inline=False)

        return temp


class helpcommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def help(self, ctx):
        em = discord.Embed(title="Help", description="Use ``c!help <command>`` for extended help on that command. **NOTE:** arguments surrounded in <> are required, [] are optional.", color=ctx.author.color)
        em.add_field(name="Counting Game:",value="> enableGame\n> leaderboard\n > rank\n> updateSettings\n> updateCountingChannel\n> editPoints\n> seeSettings")
        em.add_field(name="General Purpose", value="> errors\n> ping\n> serverinfo")
        await ctx.send(embed=em)

#failBool = None ,newAuthorLoss=None, newNumberLost=None, newProfit=None
    @help.command()
    async def enableGame(self, ctx):
        p1 = helpEmbed(self.client)
        lmfao = p1.makeEmbed(ctx.author.color,"EnableGame", "This command shows the top 10 counters in your server.", ["counting_channel"],None, None)
        await ctx.send(embed=lmfao)

    @help.command()
    async def leaderboard(self, ctx):
        p1 = helpEmbed(self.client)
        lmfao = p1.makeEmbed(ctx.author.color,"Leaderboard", "This command shows the top 10 counters in your server.",None, None, "lb")
        await ctx.send(embed=lmfao)


    @help.command()
    async def rank(self, ctx):
        p1 = helpEmbed(self.client)
        lmfao = p1.makeEmbed(ctx.author.color,"Rank", "This command shows how many times you have counted and your rank in your server.",None, ["@user/user_id"],None)
        await ctx.send(embed=lmfao)

    @help.command()
    async def updatesettings(self, ctx):
        #color, cmdname, desc, reqARGS, OPTargs, aliases
        p1 = helpEmbed(self.client)
        lmfao = p1.makeEmbed(ctx.author.color,"UpdateSettings", "This command updates the counting game settings in your server.",["failbool", "newauthorloss", 'newnumberloss', 'newprofit'], None, None)
        await ctx.send(embed=lmfao)

    @help.command()
    async def updatecountingchannel(self, ctx):
        p1 = helpEmbed(self.client)
        lmfao = p1.makeEmbed(ctx.author.color,"UpdateCountingChannel", "This command updates which channel is used for the counting game.",["#channel/channel_id"], None, None)
        await ctx.send(embed=lmfao)

    @help.command()
    async def editpoints(self, ctx):
        p1 = helpEmbed(self.client)
        lmfao = p1.makeEmbed(ctx.author.color,"EditPoints", "This command updates the amount of points a user has in the counting game (Use negative value to remove points).",["@user/user_id", "amount"],None,None)
        await ctx.send(embed=lmfao)

    @help.command()
    async def seesettings(self, ctx):
        p1 = helpEmbed(self.client)
        lmfao = p1.makeEmbed(ctx.author.color,"SeeSettings", "This command shows you your server settings for the counting game.", None, None, None)
        await ctx.send(embed=lmfao)

    @help.command()
    async def errors(self, ctx):
        p1 = helpEmbed(self.client)
        lmfao = p1.makeEmbed(ctx.author.color,"Errors", "This command shows the possible errors the bot could return. And how to fix them.", None, None, None)
        await ctx.send(embed=lmfao)

    @help.command()
    async def ping(self, ctx):
        p1 = helpEmbed(self.client)
        lmfao = p1.makeEmbed(ctx.author.color,"Ping", "This command shows the bot's latency", None, None)
        await ctx.send(embed=lmfao)

    @help.command()
    async def serverinfo(self, ctx):
        p1 = helpEmbed(self.client)
        lmfao = p1.makeEmbed(ctx.author.color,"ServerInfo", "This command shows the basic server information for your server.", None,None, "si")
        await ctx.send(embed=lmfao)





def setup(client):
    client.add_cog(helpcommands(client))
