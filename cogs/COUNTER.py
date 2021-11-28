from os import name
import discord
from discord.ext import commands
from time import ctime, process_time
from datetime import datetime
import time
import datetime
import random
import json
import asyncio
import os
import sqlite3
import traceback
import logging

from discord.ext.commands.core import check, has_permissions
from dotenv import load_dotenv
from dotenv.main import resolve_variables
load_dotenv()

def is_it_me(ctx):
    return ctx.author.id == 430937026045673474

current_local = time.localtime()
currDate = datetime.date.today()
countingConnection = sqlite3.connect("scores.db")
countingCursor = countingConnection.cursor()

settingsConnection = sqlite3.connect("settings.db")
settingsCursor = settingsConnection.cursor()


def isItCountingChannel(ctx):
    return ctx.channel.id == getCountingChannel(ctx.guild.id)

def checkIfExists(workingID):
    tempAllIDsEnrolled = []
    countingCursor.execute(f'''
        SELECT memberID
        FROM countingScoreboard
        WHERE EXISTS (SELECT memberID FROM countingScoreboard)''')
    fetchResult = countingCursor.fetchall()
    if fetchResult == []:
        #print("Alright, the list was empty and now imma create a new record")
        countingCursor.execute(f'''INSERT INTO countingScoreboard VALUES ({workingID}, 0, 0)''')
        return
    else:
        pass

    for eachQuery in fetchResult:
        tempAllIDsEnrolled.append(eachQuery[0])

    for individualID in tempAllIDsEnrolled:
        if workingID in tempAllIDsEnrolled:
            #print("Great! This user was already in the database")
            return
        else:
            #print("Oh no! This user was not in the database. They will be added right now.")
            countingCursor.execute(f'''INSERT INTO countingScoreboard VALUES ({workingID}, 0, 0)''')
            countingConnection.commit()
            return

def checkforNegativePoints(suspectID, typaLoss, authorativeGuild):
    if typaLoss == None:
        raise Exception("You must provide what type of loss.")
    if authorativeGuild == None:
        raise Exception("You must provide the server ID or else this dont work!")
    if typaLoss == "wn": #wn is wrong number
        settingsCursor.execute(f'''
        SELECT numberLoss FROM serverSettings
        WHERE serverID = {authorativeGuild}
        ''')
        temp = settingsCursor.fetchone()
        takeaway = temp[0]
    if typaLoss == "wp": #wp is wrong person
        settingsCursor.execute(f'''
        SELECT authorLoss FROM serverSettings
        WHERE serverID = {authorativeGuild}
        ''')
        temp = settingsCursor.fetchone()
        takeaway = temp[0]
    countingCursor.execute(f'''
    SELECT memberID, points
    FROM countingScoreboard
    WHERE EXISTS (SELECT memberID, points FROM countingScoreboard)''')
    ID_AND_Score = countingCursor.fetchall()
    idList = []
    scoreList = []
    #print(ID_AND_Score)
    ## The next 4 lines just make 2 lists that are used to split apart the users and their scores, they keep the same index tho so thats how i can use a "union" to find out which score belongs to who
    for eachQuery in ID_AND_Score:
        idList.append(eachQuery[0])
    for eachQuery in ID_AND_Score:
        scoreList.append(eachQuery[1])
    ##

    whosAccount = idList.index(suspectID)
    if scoreList[whosAccount] - takeaway < 0:
        countingCursor.execute(f'''
        UPDATE countingScoreboard 
        SET points = points +{takeaway}
        WHERE memberID = {suspectID}''')
    else:
        return
def getProfit(authorativeGuild):
    settingsCursor.execute(f'''
    SELECT profitAmount FROM serverSettings
    WHERE serverID = {authorativeGuild}
    ''')
    tempVarLol = settingsCursor.fetchone()
    return tempVarLol[0]

def getAuthorLoss(authorativeGuild):
    settingsCursor.execute(f'''
    SELECT authorLoss FROM serverSettings
    WHERE serverID = {authorativeGuild}
    ''')
    temp = settingsCursor.fetchone()
    return temp[0]

def getNumberLoss(authorativeGuild):
    settingsCursor.execute(f'''
    SELECT numberLoss FROM serverSettings
    WHERE serverID = {authorativeGuild}
    ''')
    temp = settingsCursor.fetchone()
    return temp[0]

def getFailBoolean(authorativeGuild):
    settingsCursor.execute(f'''
    SELECT resetOnFail FROM serverSettings
    WHERE serverID = {authorativeGuild}
    ''')
    temp = settingsCursor.fetchone()
    return temp[0]

def getTimesCounted(member_id):
    countingCursor.execute(f'''
    SELECT timesCounted FROM countingScoreboard
    WHERE memberID={member_id}
    ''')
    temp = countingCursor.fetchone()
    return temp[0]

def getCountingChannel(authorativeGuild):
    settingsCursor.execute(f'''
    SELECT countingChannel FROM serverSettings
    WHERE serverID = {authorativeGuild}
    ''')
    temp = settingsCursor.fetchone()
    return temp[0]

def youLoosePointsHA(coolparam):
    with open("PreviousAuthor.txt", "w") as temp:
        temp.write(str(coolparam))


class counter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def enableGame(self, ctx):
        await ctx.message.delete()
        try:
            settingsCursor.execute('''CREATE TABLE serverSettings (
                            serverID BIGINT, countingChannel BIGINT, resetOnFail BOOLEAN, authorLoss INT, numberLoss INT, profitAmount INT)''')
            countingCursor.execute('''CREATE TABLE countingScoreboard (
                            memberID BIGINT, points INT, timesCounted INT)''')
        except sqlite3.Error as e:
            await ctx.send(e)
        settingsConnection.commit()
        countingConnection.commit()




        await ctx.send("Counting game enabled! Use ``c!updatesettings`` to customize the settings.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def updateCountingChannel(self, ctx, channelID=None):
        if channelID==None:
            return await ctx.send("You need to specify a channel.")

        #in case they tag the channel this will remove the stuff on the outside so i can work with it in the sql thing below

        channelID = channelID.replace(">","")
        channelID = channelID.replace("<","")
        channelID = channelID.replace("#","")

        settingsCursor.execute(f'''
        UPDATE serverSettings
        SET countingChannel={channelID}
        WHERE serverID={ctx.guild.id}''')
        settingsConnection.commit()
        await ctx.send(f"New counting channel: <#{channelID}> ({channelID})")



    # @commands.command()
    # #@commands.has_permissions(administrator=True)
    # async def makeTable(self, ctx):
    #     """Creates the database tables for the counting game."""
    #     try:
    #         settingsCursor.execute('''CREATE TABLE serverSettings (
    #                         serverID BIGINT, countingChannel BIGINT, resetOnFail BOOLEAN, authorLoss INT, numberLoss INT, profitAmount INT)''')
    #         await ctx.send("**Settings table created.**")
    #         countingCursor.execute('''CREATE TABLE countingScoreboard (
    #                         memberID BIGINT, points INT, timesCounted INT)''')
    #         await ctx.send("**Counting table created.**")
    #     except sqlite3.Error as e:
    #         await ctx.send(e)

    @commands.command()
    #@commands.has_permissions(administrator=True)
    async def initializeGame(self, ctx, countingChannel=None):
        """Initalizes the counting game."""
        if countingChannel == None:
            return await ctx.send("You have to specify the channel ID for the counting channel.")
        countingChannel = countingChannel.replace(">","")
        countingChannel = countingChannel.replace("<","")
        countingChannel = countingChannel.replace("#","")
        settingsCursor.execute(f'''
        INSERT INTO serverSettings
        VALUES ({ctx.guild.id}, {countingChannel}, false, 2, 4, 3)''')
        settingsConnection.commit()
        await ctx.send("Counting game initialized. Default values have been set in the settings and can be changed with ``c!updateSettings``. To view default values, try ``c!showSettings``")

    @commands.command()
    #@commands.has_permissions(administrator=True)
    async def updateSettings(self, ctx, newID=None, failBool = None ,newAuthorLoss=None, newNumberLost=None, newProfit=None):

        if isItCountingChannel(ctx):
            pass
        else:
            return
        """Updates the settings of the counting game."""
        # first check if they are empty bcuz its gonna break if its empty
        if newID == None:
            return await ctx.send("you didnt say an id")
        if newAuthorLoss == None:
            return await ctx.send("you didnt say author loss amount")
        if newNumberLost == None:
            return await ctx.send("you didnt say number loss amount")
        if newProfit == None:
            return await ctx.send("you didnt say profit amount")
        # next check to make sure the newAuthor and newNumber are positive cuz its gonna break if its not
        if int(newAuthorLoss) <= 0:
            return await ctx.send("newauthorloss can't be negative or 0")
        if int(newNumberLost) <= 0:
            return await ctx.send("newnumberloss can't be negative or 0")
        if failBool == None:
            return await ctx.send("failbool not specified")
        if int(newProfit) <=0:
            return await ctx.send("newprofit can't be negative or 0")

        usableBoolean = failBool.capitalize()
        if usableBoolean == "True" or "False":
            pass
        else:
            return await ctx.send("failbool needs to be a boolean")

        newID = newID.replace(">","")
        newID = newID.replace("<","")
        newID = newID.replace("#","")

        settingsCursor.execute(f'''
        UPDATE serverSettings
        SET countingChannel={newID}
        , resetOnFail={failBool}
        , authorLoss={newAuthorLoss}
        , numberLoss={newNumberLost}
        , profitAmount={newProfit}
        WHERE serverID={ctx.guild.id}''')
        settingsConnection.commit()
        await ctx.send("settings.db updated with the following information:")
        await ctx.send(f"```({newID}, {failBool}, {newAuthorLoss}, {newNumberLost}, {newProfit})```")

    @commands.command()
    async def showSettings(self, ctx):
        """This command shows the current counting game settings."""
        # if isItCountingChannel(ctx):
        #     pass
        # else:
        #     return
        settingsCursor.execute("SELECT * FROM serverSettings")
        rows = settingsCursor.fetchall()
        for row in rows:
            serverID_value = row[0]
            countingChannel_value = row[1]
            resetOnFail_value = row[2]
            authorLoss_value = row[3]
            numberLoss_value = row[4]
            profit_value = row[5]
        resetOnFail_value_2 = bool(resetOnFail_value)
        await ctx.send(f'''
**Server ID:** {serverID_value}
**Counting Channel:** <#{countingChannel_value}> ({countingChannel_value})
**Reset count on fail:** {resetOnFail_value_2}
**Loss for double counting:** {authorLoss_value}
**Loss for incorrect number:** {numberLoss_value}
**Profit for correct number:** {profit_value}
        ''')

    @commands.command()
    #@commands.has_permissions(administrator=True)
    async def manuallyAddMember(self, ctx, userID=None):
        """Manually add a member to the counting game."""
        # if isItCountingChannel(ctx):
        #     pass
        # else:
        #     return
        if userID == None:
            return await ctx.send("need to say id")
        try:
            countingCursor.execute(f'''
            INSERT INTO countingScoreboard VALUES ({userID}, {random.randint(1,100)}, {random.randint(1,300)})
            ''')
            countingConnection.commit()
            await ctx.send(f"ok i did it")
        except:
            await ctx.send('broken')
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def editPoints(self, ctx, userID=None, amt=None):
        """Edits the points of a users account."""
        # if isItCountingChannel(ctx):
        #     pass
        # else:
        #     return
        if userID == None:
            return await ctx.send('userid missing')
        if amt == None:
            return await ctx.send('amt missing')
        else:
            countingCursor.execute(f'''
                UPDATE countingScoreboard 
                SET points = points+{amt}, timesCounted = timesCounted+{random.randint(1,100)}
                WHERE memberID = {userID}''')
            countingConnection.commit()
            return await ctx.send(f"{userID} was given {amt} points")

    @commands.command()
    async def showtable(self, ctx):
        """Shows the database for the counting game."""
        # if isItCountingChannel(ctx):
        #     pass
        # else:
        #     return
        countingCursor.execute("SELECT * FROM countingScoreboard")
        rows = countingCursor.fetchall()
        for row in rows:
            await ctx.send(row)

    # @commands.command()
    # async def seePoints(self, ctx):
    #     """See the amount of points you have in the counting game."""
    #     countingCursor.execute(f"SELECT * FROM countingScoreboard")
    #     urmom = countingCursor.fetchone()[1]
    #     await ctx.send(urmom)

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        """See the leaderboard for the counting game."""
        leaderboardEmbed = discord.Embed(title="Chaotic Destiny Hosting | Top 10 Leaderboard:", color=discord.Color.dark_purple())
        # if isItCountingChannel(ctx):
        #     pass
        # else:
        #     return
        countingCursor.execute(f'''
        SELECT *
        FROM countingScoreboard ORDER BY timesCounted DESC LIMIT 10''')
        entiretuple = countingCursor.fetchall()
        santasBag = entiretuple
        await ctx.send(santasBag)
        leadNum = 1
        for i, dontmind in enumerate(santasBag):
            theUser = await self.client.fetch_user([x[0] for x in santasBag][i])
            leaderboardEmbed.add_field(name=f"{leadNum}. {theUser}:", value=f"Times Counted: {getTimesCounted(theUser.id)}", inline=False)
            #Score: {[x[1] for x in santasBag][i]}\n
            #add this later ig if we want it
            leadNum+=1

        leaderboardEmbed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        leaderboardEmbed.timestamp = datetime.datetime.now()
        leaderboardEmbed.set_footer(icon_url=ctx.author.avatar_url)
        await ctx.send(embed=leaderboardEmbed)


    @commands.command()
    async def rank(self, ctx, search:discord.Member=None):
        """See how many times you or someone else have counted."""
        if search==None:
            search = ctx.author

        countingCursor.execute(f'''
        SELECT *
        FROM countingScoreboard ORDER BY timesCounted DESC''')

        everything = countingCursor.fetchall()
        who = await self.client.fetch_user(search.id)
        
        timesCounted = getTimesCounted(search.id)

        countingCursor.execute(f'''
        SELECT * 
        FROM countingScoreboard
        WHERE memberID={search.id}
        ''')
        yk = countingCursor.fetchone()
        rankNUM=int(everything.index(yk))+1
        yourRanking="Oops, I could not find your rank."
        if rankNUM == 1:
            yourRanking = str(rankNUM)+"st"
        if rankNUM == 2:
            yourRanking = str(rankNUM)+"nd"
        if rankNUM ==3:
            yourRanking= str(rankNUM)+"rd"
        if rankNUM >=4:
            yourRanking = str(rankNUM)+"th"

        scoreembed = discord.Embed(title="Score", color=discord.Color.blue())
        scoreembed.add_field(name=f"{who}", value=f"Times Counted: {timesCounted}")
        scoreembed.add_field(name=f"Your rank:", value=f"{yourRanking}", inline=False)
        await ctx.send(embed=scoreembed)


    @commands.Cog.listener()
    async def on_message(self, msg):
        try:
            settingsCursor.execute(f'''
            SELECT countingChannel FROM serverSettings
            WHERE serverID={msg.guild.id}
            ''')
            CountingChannel = settingsCursor.fetchone()
            if msg.channel.id != CountingChannel[0]:
                return
            if msg.author.bot:
                return
        except:
            return 



        with open("PreviousAuthor.txt", "r") as confirmAuthor:
            authorContent = confirmAuthor.read()
            if int(authorContent) == msg.author.id:
                await msg.add_reaction("❌")
                noice = await msg.channel.send(f"{msg.author.mention} you can not count twice in a row...")
                checkIfExists(msg.author.id)
                checkforNegativePoints(msg.author.id, "wp", msg.guild.id)
                lossAmt = getAuthorLoss(msg.guild.id)
                countingCursor.execute(f'''
                UPDATE countingScoreboard 
                SET points = points-{lossAmt}
                WHERE memberID = {msg.author.id}''')
                countingConnection.commit()
                await asyncio.sleep(6)
                await noice.delete()
                await msg.delete()
                return
            else:
                pass
                # this is just to continue to check if the number is right
        
        
        with open("PreviousNumber.txt", "r") as confirmNumber:
            try:
                checkingThisNumber = confirmNumber.read() #file value ONLY GETS UPDATED AT THE END OF THIS FUNCTION
                checkby = int(checkingThisNumber) +1 # FILE VALUE PLUS 1
                if int(checkby) == int(msg.content):
                    pass
                else:
                    youLoosePointsHA(msg.author.id)

                    await msg.add_reaction("❌")
                    verycool = await msg.channel.send(f"{msg.author.mention} wrong number!")
                    checkIfExists(msg.author.id)
                    checkforNegativePoints(msg.author.id, "wn", msg.guild.id)
                    lossAmt = getNumberLoss(msg.guild.id)
                    resetGame = getFailBoolean(msg.guild.id)
                    if bool(resetGame):
                        with open("PreviousNumber.txt", "w") as temp2:
                            temp2.truncate(0)
                            temp2.writelines("0")
                        shutshut = await msg.channel.send(f"{msg.author.mention} that's the wrong number! Counting reset to 0")
                        await asyncio.sleep(7)
                        await shutshut.delete()
                    else:
                        pass
                    countingCursor.execute(f'''
                    UPDATE countingScoreboard 
                    SET points = points-{lossAmt} 
                    WHERE memberID = {msg.author.id}''')
                    countingConnection.commit()
                    await asyncio.sleep(5)
                    await verycool.delete()
                    await msg.delete()

                    return
                tempAllIDsEnrolled = []
                if int(checkingThisNumber) == int(checkby)-1:
                    await msg.add_reaction("✅")
                    checkIfExists(msg.author.id)
                    usersProfit = getProfit(msg.guild.id)
                    countingCursor.execute(f'''
                    UPDATE countingScoreboard 
                    SET points = points+{usersProfit}, timesCounted = timesCounted+1
                    WHERE memberID = {msg.author.id}''')
                    countingConnection.commit()
            except ValueError as ve:
                return await msg.delete()
                

        # Here the bot will log the user's ID and the 'number' they sent to the channel
        with open("PreviousNumber.txt", "w") as logNumber:
            logNumber.write(str(msg.content))
        with open("PreviousAuthor.txt", "w") as logAuthor:
            logAuthor.write(str(msg.author.id))

    @commands.Cog.listener()
    async def on_message_delete(self, deleted_message):
        countingChannelYay = getCountingChannel(deleted_message.guild.id)
        if deleted_message.channel.id != countingChannelYay:
            return
        if deleted_message.author.bot:
            return
        
        
        deletedMessageID = deleted_message.id
        deletedMessageContent = deleted_message.content

        with open("PreviousNumber.txt", "r") as idk:
            PrevNum = idk.read()

        try:
            checkby = int(PrevNum) +1 # FILE VALUE PLUS 1
            if int(checkby) == int(deleted_message.content):
                pass
        except Exception as ve2:
            return await deleted_message.delete()
        if PrevNum == deletedMessageContent:
            await deleted_message.channel.send(f"**{deleted_message.content}**, {deleted_message.author.mention}")
		



def setup(client):
    client.add_cog(counter(client))