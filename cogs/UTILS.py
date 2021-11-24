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

class util(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """Shows the basic server information of the server."""
        embed = discord.Embed(title=f"<:DiscordLogoEmote:855572468039286804> Server information for {ctx.guild.name}", color=ctx.author.color)
        embed.add_field(name=f"<:DiscordNameEmote:855575294629642310> Server Name:", value=f"{ctx.guild.name} ({ctx.guild.id})", inline=False)
        embed.add_field(name=f"<:DiscordDescriptionEmote:855575622649905202> Server Description:", value=f"{ctx.guild.description}", inline=False)
        embed.add_field(name=f"<:DiscordVoiceChannelEmote:855572491756765214> Server Voice Channels: ", value=f"{len(ctx.guild.voice_channels)}", inline=False)
        embed.add_field(name=f"<:DiscordTextChannelEmote:855572482614755328> Server Text Channels: ", value=f"{len(ctx.guild.text_channels)}", inline=False)
        embed.add_field(name=f"<:DiscordLockEmote:855573514782113823> Server Verficiation Level: ", value=f"{ctx.guild.verification_level}", inline=False)
        embed.add_field(name=f"<:DiscordBoostEmote:855572453165891596> Server Boost Level:", value=f"{ctx.guild.premium_tier}", inline=False)
        embed.add_field(name=f"Server Owner: ", value=f"{ctx.guild.owner.mention} ({ctx.guild.owner_id})", inline=False)
        embed.add_field(name=f"Server Created: ", value=f"{ctx.guild.created_at}", inline=False)
        embed.add_field(name=f"<:MultiplePeopleEmote:855572507464826921> Server Member Count: ", value=f"{ctx.guild.member_count}", inline=False)
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by: {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """This command shows the bot's latency."""
        latency=round(self.client.latency * 1000)
        await ctx.reply("Pong! "+"``"+str(latency) + "ms``", mention_author=False)


def setup(client):
    client.add_cog(util(client))
