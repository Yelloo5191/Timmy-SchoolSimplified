import datetime
from datetime import datetime, timedelta

import discord
import pytz
from core import database
from core.checks import is_botAdmin
from core.common import Emoji
from discord.ext import commands

#from main import vc

#Variables
'''
channel_id = 843637802293788692
categoryID = 776988961087422515

staticChannels = [784556875487248394, 784556893799448626]
presetChannels = [843637802293788692, 784556875487248394, 784556893799448626]
'''
time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
EST = pytz.timezone('US/Eastern')


def convert_time_to_seconds(time):
    try:
        value = int(time[:-1]) * time_convert[time[-1]]
    except:
        value = time
    finally:
        if value < 60:
            return None
        else:
            return value
    

def showFutureTime(time):
    now = datetime.now(EST)
    output = convert_time_to_seconds(time)
    if output == None:
        return None

    add = timedelta(seconds = int(output))
    now_plus_10 = now + add
    print(now_plus_10)

    return now_plus_10.strftime(r"%I:%M %p")

def showTotalMinutes(dateObj: datetime):
    now = datetime.now(EST)

    deltaTime = now - dateObj

    minutes = str(deltaTime.total_seconds() // 60)

    return minutes, now
    

class TutorVCCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 843637802293788692
        self.categoryID = [776988961087422515, 895041016057446411]
        self.staticChannels = [784556875487248394, 784556893799448626]
        self.presetChannels = [843637802293788692, 784556875487248394, 784556893799448626]

        self.ownerID = 409152798609899530
        self.botID = 852251896130699325
        #852251896130699325

        self.AT = "Academics Team"
        self.SB = "Simplified Booster"
        self.Legend = "Legend"
        
        self.TMOD = "Mod Trainee"
        self.MOD = "Moderator"
        self.SMOD = "Senior Mod"
        self.CO = "Corporate Officer"
        self.VP = "Vice President"

        self.MAT = "Marketing Team"
        self.TT = "Technical Team"

        self.ST = "Lead Tutor"

        #Level Roles

        self.leveledRoles = ["〚Level 120〛Grandmaster","〚Level 110〛Master","〚Level 100〛Prodigy","〚Level 90〛 Legend","〚Level 80〛Connoisseur","〚Level 70 〛Professor","〚Level 60〛Mentor","〚Level 50〛Scholar","〚Level 40〛Expert","〚Level 35〛Experienced","〚Level 30〛Apprentice","〚Level 25〛Amateur","〚Level 20〛Student","〚Level 15〛Learner","〚Level 10〛Beginner","〚Level 5〛Novice","〚Level 1〛New"]
        self.renameRoles = ["〚Level 120〛Grandmaster","〚Level 110〛Master","〚Level 100〛Prodigy","〚Level 90〛 Legend","〚Level 80〛Connoisseur","〚Level 70 〛Professor","〚Level 60〛Mentor","〚Level 50〛Scholar","〚Level 40〛Expert", "Simplified Booster", "Legend", "Moderator", "Marketing Team", "Technical Team"]

        self.L120 = "〚Level 120〛Grandmaster"
        self.L110 = "〚Level 110〛Master"
        self.L100 = "〚Level 100〛Prodigy"
        self.L90 = "〚Level 90〛 Legend"
        self.L80 = "〚Level 80〛Connoisseur"
        self.L70 = "〚Level 70 〛Professor"
        self.L60 = "〚Level 60〛Mentor"
        self.L50 = "〚Level 50〛Scholar"
        self.L40 = "〚Level 40〛Expert"

        self.TutorRole = "Tutor"
        self.TutorLogID = 873326994220265482

        

        
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def rename(self, ctx, *, name = None):
        database.db.connect(reuse_if_open=True)
        SB = discord.utils.get(ctx.guild.roles, name = self.SB)
        legend = discord.utils.get(ctx.guild.roles, name = self.Legend)

        MT = discord.utils.get(ctx.guild.roles, name= self.MOD)
        MAT = discord.utils.get(ctx.guild.roles, name= self.MAT)
        TT = discord.utils.get(ctx.guild.roles, name=self.TT)
        AT = discord.utils.get(ctx.guild.roles, name=self.AT)
        VP = discord.utils.get(ctx.guild.roles, name=self.VP)
        CO = discord.utils.get(ctx.guild.roles, name=self.CO)

        L120 = discord.utils.get(ctx.guild.roles, name=self.L120)
        L110 = discord.utils.get(ctx.guild.roles, name=self.L110)
        L100 = discord.utils.get(ctx.guild.roles, name=self.L100)
        L90 = discord.utils.get(ctx.guild.roles, name=self.L90)
        L80 = discord.utils.get(ctx.guild.roles, name=self.L80)
        L70 = discord.utils.get(ctx.guild.roles, name=self.L70)
        L60 = discord.utils.get(ctx.guild.roles, name=self.L60)
        L50 = discord.utils.get(ctx.guild.roles, name=self.L50)
        L40 = discord.utils.get(ctx.guild.roles, name=self.L40)

        member = ctx.guild.get_member(ctx.author.id)
            
        if ctx.author.id != 415629932798935040:
            if SB not in ctx.author.roles and AT not in ctx.author.roles and legend not in ctx.author.roles and MT not in ctx.author.roles and MAT not in ctx.author.roles and TT not in ctx.author.roles and VP not in ctx.author.roles and CO not in ctx.author.roles and L120 not in ctx.author.roles and L110 not in ctx.author.roles and L100 not in ctx.author.roles and L90 not in ctx.author.roles and L80 not in ctx.author.roles and L70 not in ctx.author.roles and L60 not in ctx.author.roles and L50 not in ctx.author.roles and L40 not in ctx.author.roles and ctx.guild.id == 763119924385939498:
                embed = discord.Embed(title = f"{Emoji.deny} Insufficient Rank", description = "Sorry! But only the following people who have these roles can rename their channel!\n\n- **Moderators**\n- **Marketing Team**\n- **Technical Team**\n- **Academics Team**\n- **VP**\n- **CO**\n- **Legends**\n- **Simplified Boosters**\n- **Level 40+**", color = discord.Colour.blurple())
                return await ctx.send(embed = embed)

        voice_state = member.voice

        if voice_state == None:
            await ctx.send(f"{Emoji.deny} You need to be in a voice channel you own to use this!")

        else:
            if member.voice.channel.category_id in self.categoryID:
                query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))

                if query.exists():
                    q: database.VCChannelInfo = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                    
                    print(member.voice.channel.id)
                    print(q.ChannelID)
                    if member.voice.channel.id == int(q.ChannelID):
                        if name != None:
                            embed = discord.Embed(title = f"{Emoji.cycle} ReNamed Channel", description = f"I have changed the channel's name to:\n**{name}**", color = discord.Colour.green())
                            
                            print(name)
                            await member.voice.channel.edit(name = name)
                            await ctx.send(embed = embed)

                            q.name = name
                            q.save()
                        else:
                            embed = discord.Embed(title = f"{Emoji.cycle} ReNamed Channel", description = f"I have changed the channel's name to:\n**{name}**", color = discord.Colour.green())
                            
                            await member.voice.channel.edit(name = f"{member.display_name}'s Channel")
                            await ctx.send(embed = embed)
                            q.name = f"{member.display_name}'s Channel"
                            q.save()

                    else:
                        embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = f"You are not the owner of this voice channel, please ask the original owner <@{q.authorID}>, to rename it!", color = discord.Colour.red())
                        
                        await ctx.send(embed = embed)

                else:
                    q = database.VCChannelInfo.select().where((database.VCChannelInfo.ChannelID == member.voice.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))
                    embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = f"You are not the owner of this voice channel, please ask the original owner <@{q.authorID}>, to rename it!", color = discord.Colour.dark_red())
                        
                    await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title = f"{Emoji.invalidchannel} Unknown Channel", description = "You are not the owner of this voice channel nor is this a valid channel. Please execute the command under a channel you own!", color = discord.Colour.red())
                        
                await ctx.send(embed = embed)
        database.db.close()

    @commands.command()
    async def end(self, ctx):
        database.db.connect(reuse_if_open=True)
        team = discord.utils.get(ctx.guild.roles, name= self.AT)
        member = ctx.guild.get_member(ctx.author.id)
        timestamp2 = datetime.now(EST)

        voice_state = member.voice
        if voice_state == None:

            query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))
            if query.exists():
                query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                print(f"T: {query.TutorBotSessionID}")
                VCDatetime = pytz.timezone("America/New_York").localize(query.datetimeObj)

                day, now = showTotalMinutes(VCDatetime)
                #daySTR = VCDatetime.strftime("%-I:%-M %p EST")
                #nowSTR = now.strftime("%-I:%-M %p EST")

                daySTR = int(VCDatetime.timestamp())
                nowSTR = int(now.timestamp())

                day = str(day)

                channel = await self.bot.fetch_channel(int(query.ChannelID))

                embed = discord.Embed(title = f"{Emoji.archive} Ended Session", description = "I have successfully ended the session!", color = discord.Colour.blue())
                embed.add_field(name = "Time Spent", value = f"{member.mention} you have spent a total of {Emoji.calender} `{day} minutes` in voice channel, **{query.name}**.")
                embed.set_footer(text = "WARNING: Time displayed may not be accurate.")
                await ctx.send(embed = embed)

                print(query.TutorBotSessionID)
                tutorSession = database.TutorBot_Sessions.select().where(database.TutorBot_Sessions.SessionID == query.TutorBotSessionID)
                
                query.delete_instance()

                if tutorSession.exists():
                    tutorSession = tutorSession.get()

                    student = await self.bot.fetch_user(tutorSession.StudentID)
                    tutor = await self.bot.fetch_user(tutorSession.TutorID)

                    HOURCH = await self.bot.fetch_channel(self.TutorLogID)

                    hourlog = discord.Embed(title = "Hour Log", description = f"{tutor.mention}'s Tutor Log", color = discord.Colour.blue())
                    hourlog.add_field(name = "Information", value = f"**Tutor:** {tutor.mention}\n**Student:** {student.mention}\n**Time Started:** <t:{daySTR}:t>\n**Time Ended:** <t:{nowSTR}:t>\n\n**Total Time:** {day}")
                    hourlog.set_footer(text = f"Session ID: {tutorSession.SessionID}")
                    await HOURCH.send(embed = hourlog)

                    embed = discord.Embed(title = "Feedback!", description = "Hey it looks like you're tutor session just ended, if you'd like to let us know how we did please fill out the form below!\n\nhttps://forms.gle/Y1oobNFEBf7vpfMM8", color = discord.Colour.green())
                    await student.send(embed = embed)

                #ignorethis = database.IgnoreThis.create(ChannelID = channel.id, authorID = ctx.author.id)
                await channel.delete()
                return

            else:
                return print("Ignore VC Leave")


        if voice_state.channel.id in self.presetChannels:
            embed = discord.Embed(title = f"{Emoji.invalidchannel} UnAuthorized Channel Deletion", description = "You are not allowed to delete these channels!\n\n**Error Detection:**\n**1)** Detected Static Channels", color = discord.Colour.dark_red())
            return await ctx.send(embed = embed)

        if member.voice.channel.category_id in self.categoryID:
            query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))

            if query.exists():
                q: database.VCChannelInfo = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                
                tag: database.IgnoreThis = database.IgnoreThis.create(channelID = voice_state.channel.id, authorID = member.id, GuildID = ctx.guild.id)
                tag.save()
                VCDatetime = pytz.timezone("America/New_York").localize(q.datetimeObj)

                day, now = showTotalMinutes(VCDatetime)
                #daySTR = VCDatetime.strftime("%-I:%-M %p EST")
                #nowSTR = now.strftime("%-I:%-M %p EST")

                daySTR = int(VCDatetime.timestamp())
                nowSTR = int(now.timestamp())

                day = str(day)

                print("In VC")

                embed = discord.Embed(title = f"{Emoji.archive} Ended Session", description = "I have successfully ended the session!", color = discord.Colour.blue())
                embed.add_field(name = "Time Spent", value = f"{member.mention} you have spent a total of {Emoji.calender} `{day} minutes` in voice channel, **{q.name}**.")
                embed.set_footer(text = "WARNING: Time displayed may not be accurate.")
                await ctx.send(embed = embed)

                print(q.TutorBotSessionID)
                tutorSession = database.TutorBot_Sessions.select().where(database.TutorBot_Sessions.SessionID == q.TutorBotSessionID)
                if tutorSession.exists():
                    tutorSession = tutorSession.get()

                    student = await self.bot.fetch_user(tutorSession.StudentID)
                    tutor = await self.bot.fetch_user(tutorSession.TutorID)

                    HOURCH = await self.bot.fetch_channel(self.TutorLogID)

                    hourlog = discord.Embed(title = "Hour Log", description = f"{tutor.mention}'s Tutor Log", color = discord.Colour.blue())
                    hourlog.add_field(name = "Information", value = f"**Tutor:** {tutor.mention}\n**Student:** {student.mention}\n**Time Started:** <t:{daySTR}:t>\n**Time Ended:** <t:{nowSTR}:t>\n\n**Total Time:** {day} minutes")
                    hourlog.set_footer(text = f"Session ID: {tutorSession.SessionID}")
                    await HOURCH.send(embed = hourlog)

                    embed = discord.Embed(title = "Feedback!", description = "Hey it looks like you're tutor session just ended, if you'd like to let us know how we did please fill out the form below!\n\nhttps://forms.gle/Y1oobNFEBf7vpfMM8", color = discord.Colour.green())
                    try:
                        await student.send(embed = embed)
                    except discord.HTTPException: 
                        pass
                    
                    embed = discord.Embed(title = "Logged Hours", description = "Hey! It looks like you've finished your tutor session, I've already went ahead and sent your session legnth in <#873326994220265482>.\n**NOTE:** You'll still need to fill in your hours on the hour log spreadsheet.", color = discord.Color.green())
                    try:
                        await tutor.send(embed = embed)
                    except discord.HTTPException: 
                        pass

                q.delete_instance()
                await voice_state.channel.delete()


            else:
                try:
                    q = database.VCChannelInfo.select().where((database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                except:
                    embed = discord.Embed(title = f"{Emoji.invalidchannel} Ownership Check Failed", description = "This isn't a valid channel! Please use the command on an actual voice channel thats inside the correct category!", color = discord.Colour.red())
                else:
                    embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = f"You are not the owner of this voice channel, please ask the original owner <@{q.authorID}>, to end it!", color = discord.Colour.red())
                finally:
                    await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = f"{Emoji.invalidchannel} Unknown Channel", description = "You are not the owner of this voice channel nor is this a valid channel. Please execute the command under a channel you own!", color = discord.Colour.red())
                    
            await ctx.send(embed = embed)
        database.db.close()

    @commands.command()
    @is_botAdmin
    async def forceend(self, ctx, channel):
        database.db.connect(reuse_if_open=True)
        channel = await self.bot.fetch_channel(channel)
        print(channel)
        team = discord.utils.get(ctx.guild.roles, name= self.AT)
        member = ctx.guild.get_member(ctx.author.id)

        if channel.id in self.presetChannels:
            embed = discord.Embed(title = f"{Emoji.invalidchannel} UnAuthorized Channel Deletion", description = "You are not allowed to delete these channels!\n\n**Error Detection:**\n**1)** Detected Static Channels", color = discord.Colour.dark_red())
            return await ctx.send(embed = embed)

        if channel.category_id in self.categoryID:
            query = database.VCChannelInfo.select().where((database.VCChannelInfo.ChannelID == channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))

            if query.exists():
                q: database.VCChannelInfo = database.VCChannelInfo.select().where((database.VCChannelInfo.ChannelID == channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                VCDatetime = pytz.timezone("America/New_York").localize(q.datetimeObj)

                day, now = showTotalMinutes(VCDatetime)


                for VCMember in channel.members:
                    if VCMember.id == q.authorID:
                        tag: database.IgnoreThis = database.IgnoreThis.create(channelID = channel.id, authorID = VCMember.id, GuildID = ctx.guild.id)
                        tag.save()
                        print(f"Added: {VCMember.id}")
                    
                
                await channel.delete()
                q.delete_instance()
                embed = discord.Embed(title = f"{Emoji.archive} Force Ended Session", description = "Session has been forcefully removed.", color = discord.Colour.blue())
                embed.add_field(name = "Time Spent", value = f"<@{q.authorID}> you have spent a total of {Emoji.calender} `{day} minutes` in voice channel, **{q.name}**.")
                embed.set_footer(text = "WARNING: Time displayed may not be accurate.")
                await ctx.send(embed = embed)

                

            else:
                await channel.delete()
                embed = discord.Embed(title = f"{Emoji.warn} Partial Completion", description = "The database indicates there is no owner or data related to this voice channel but I have still deleted the channel!", color = discord.Colour.gold())
                    
                await ctx.send(embed = embed)
                print(query.authorID)
                
        else:
            embed = discord.Embed(title = f"{Emoji.warn} Unknown Channel", description = "You are not the owner of this voice channel nor is this a valid channel. Please execute the command under a valid voice channel!", color = discord.Colour.red())
                    
            await ctx.send(embed = embed)

        database.db.close()


    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def lock(self, ctx):
        database.db.connect(reuse_if_open=True)
        member = ctx.guild.get_member(ctx.author.id)

        BOT = ctx.guild.get_member(self.botID)
        OWNER = ctx.guild.get_member(self.ownerID)
        TMOD = discord.utils.get(ctx.guild.roles, name= self.TMOD)
        MOD = discord.utils.get(ctx.guild.roles, name= self.MOD)
        SMOD = discord.utils.get(ctx.guild.roles, name= self.SMOD)
        CO = discord.utils.get(ctx.guild.roles, name= self.CO)
        VP = discord.utils.get(ctx.guild.roles, name= self.VP)
        ST = discord.utils.get(ctx.guild.roles, name=self.ST)

        SE = discord.utils.get(ctx.guild.roles, name="Senior Executive")
        BM = discord.utils.get(ctx.guild.roles, name="Board Member")
        E = discord.utils.get(ctx.guild.roles, name="Executive")

        voice_state = member.voice

        if voice_state == None:
            embed = discord.Embed(title = f"{Emoji.warn} Unknown Voice Channel", description = "You have to be in a voice channel you own in order to use this!", color = discord.Colour.dark_red())
            return await ctx.send(embed = embed)
        
        else:
            if voice_state.channel.id in self.presetChannels:
                embed = discord.Embed(title = f"{Emoji.deny} UnAuthorized Channel Modification", description = "You are not allowed to modify these channels!\n\n**Error Detection:**\n**1)** Detected Static Channels", color = discord.Colour.dark_red())
                return await ctx.send(embed = embed)

            if member.voice.channel.category_id in self.categoryID:
                query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))

                if query.exists():
                    LOCK : database.VCChannelInfo = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                    LOCK.lockStatus = "1"
                    LOCK.save()

                    if ctx.channel.id == 763119924385939498:
                        await member.voice.channel.set_permissions(BOT, connect = True, manage_channels = True, manage_permissions = True)
                        await member.voice.channel.set_permissions(OWNER, connect = True, manage_channels = True, manage_permissions = True)
                        await member.voice.channel.set_permissions(member, connect = True, stream = True)

                        await member.voice.channel.set_permissions(ctx.guild.default_role, connect = False)
                        await member.voice.channel.set_permissions(TMOD, connect = True)
                        await member.voice.channel.set_permissions(MOD, connect = True)
                        await member.voice.channel.set_permissions(SMOD, connect = True)
                        await member.voice.channel.set_permissions(ST, connect = True)
                        await member.voice.channel.set_permissions(VP, connect = True, manage_channels = True, manage_permissions = True)
                        await member.voice.channel.set_permissions(CO, connect = True, manage_channels = True, manage_permissions = True)
                    else:
                        await member.voice.channel.set_permissions(ctx.guild.default_role, connect = False, view_channel = False)
                        await member.voice.channel.set_permissions(BM, connect = True, manage_channels = True, manage_permissions = True, view_channel = True)
                        await member.voice.channel.set_permissions(SE, connect = True, manage_channels = True, manage_permissions = True, view_channel = True)
                        await member.voice.channel.set_permissions(E, connect = True, manage_channels = True, manage_permissions = True, view_channel = True)
                        await member.voice.channel.set_permissions(OWNER, connect = True, manage_channels = True, manage_permissions = True, view_channel = True)
                        
                    embed = discord.Embed(title = f"{Emoji.lock} Locked Voice Channel", description = "Your voice channel has been locked and now only authorized users can join it!\n\n**NOTE:** Moderators and other Administrators will always be allowed into your voice channels!", color = discord.Colour.green())
                    await ctx.send(embed = embed)

                else:
                    try:
                        q = database.VCChannelInfo.select().where((database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                    except:
                        embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = "This isn't a valid voice channel! Please use the command on an actual voice channel thats under the correct category!", color = discord.Colour.red())
                    else:
                        embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = f"You are not the owner of this voice channel, please ask the original owner <@{q.authorID}>, to end it!", color = discord.Colour.red())
                    finally:
                        await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title = f"{Emoji.warn} Unknown Channel", description = "You are not the owner of this voice channel nor is this a valid channel. Please execute the command under a channel you own!", color = discord.Colour.red())
                        
                await ctx.send(embed = embed)
        
        database.db.close()

    @commands.command()
    async def settutor(self, ctx, tutorcode):
        TR = discord.utils.get(ctx.guild.roles, name=self.TutorRole)
        if TR not in ctx.author.roles or ctx.guild.id == 891521033700540457:
            return await ctx.message.add_reaction("❌")
        else:
            member = ctx.guild.get_member(ctx.author.id)
            voice_state = member.voice

            if voice_state == None:
                embed = discord.Embed(title = f"{Emoji.warn} Unknown Voice Channel", description = "You have to be in a voice channel you own in order to use this!", color = discord.Colour.dark_red())
                return await ctx.send(embed = embed)

            tutorSession = database.TutorBot_Sessions.select().where(database.TutorBot_Sessions.SessionID == tutorcode)
            if tutorSession.exists():
                tutorSession = tutorSession.get()
                if member.voice.channel.category_id in self.categoryID:

                    query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))
                    if query.exists():
                        query = query.get()
                        student = await self.bot.fetch_user(tutorSession.StudentID)
                        tutor = await self.bot.fetch_user(tutorSession.TutorID)
                        #date = tutorSession.Date.strftime("%m/%d/%Y")
                        ts = int(tutorSession.Date.timestamp())

                        query.TutorBotSessionID = tutorcode
                        query.save()
                        
                        hourlog = discord.Embed(title = "Tutor Session Convert Complete", description = f"I have successfully converted this voice session into a tutor session, when you end this session I will log this session for you.", color = discord.Colour.blue())
                        hourlog.add_field(name = "Information", value = f"**Tutor:** {tutor.mention}\n**Student:** {student.mention}\n**Date:** <t:{ts}:R>")
                        await ctx.send(embed = hourlog)


                    else:
                        embed = discord.Embed(title = f"{Emoji.warn} Unknown Voice Channel", description = "You have to be in a voice channel you own in order to use this!", color = discord.Colour.dark_red())
                        return await ctx.send(embed = embed)
                else:
                    embed = discord.Embed(title = f"{Emoji.warn} Unknown Voice Channel", description = "You have to be in a voice channel you own in order to use this!", color = discord.Colour.dark_red())
                    return await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title = "Invalid Session", description = "This session does not exist, please check the ID you've provided!", color = discord.Color.red())
                await ctx.send(embed = embed)





    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def unlock(self, ctx):
        database.db.connect(reuse_if_open=True)
        member = ctx.guild.get_member(ctx.author.id)
        timestamp2 = datetime.now(EST)

        voice_state = member.voice

        if voice_state == None:
            embed = discord.Embed(title = f"{Emoji.warn} Unknown Voice Channel", description = "You have to be in a voice channel you own in order to use this!", color = discord.Colour.dark_red())
            return await ctx.send(embed = embed)

        else:
            if voice_state.channel.id in self.presetChannels:
                embed = discord.Embed(title = f"{Emoji.deny} UnAuthorized Channel Modification", description = "You are not allowed to modify these channels!\n\n**Error Detection:**\n**1)** Detected Static Channels", color = discord.Colour.dark_red())
                return await ctx.send(embed = embed)

            if member.voice.channel.category_id in self.categoryID:
                query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))

                if query.exists():
                    LOCK : database.VCChannelInfo = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                    LOCK.lockStatus = "0"
                    LOCK.save()

                    query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                    print(query.lockStatus)

                    await member.voice.channel.edit(sync_permissions=True)

                    embed = discord.Embed(title = f"{Emoji.unlock} Unlocked Voice Channel", description = "Your voice channel has been unlocked and now anyone can join it!", color = discord.Colour.green())
                    await ctx.send(embed = embed)

                else:
                    try:
                        q = database.VCChannelInfo.select().where((database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                    except:
                        embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = "This isn't a valid voice channel! Please use the command on an actual voice channel thats under the correct category!", color = discord.Colour.red())
                    else:
                        embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = f"You are not the owner of this voice channel, please ask the original owner <@{q.authorID}>, to end it!", color = discord.Colour.red())
                    finally:
                        await ctx.send(embed = embed)

            else:
                embed = discord.Embed(title = f"{Emoji.warn} Unknown Channel", description = "You are not the owner of this voice channel nor is this a valid channel. Please execute the command under a channel you own!", color = discord.Colour.red())
                        
                await ctx.send(embed = embed)

        database.db.close()



    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def permit(self, ctx, typeAction, user: discord.Member = None):
        database.db.connect(reuse_if_open=True)
        member = ctx.guild.get_member(ctx.author.id)
        timestamp2 = datetime.now(EST)

        voice_state = member.voice

        if voice_state == None:
            embed = discord.Embed(title = f"{Emoji.warn} Unknown Voice Channel", description = "You have to be in a voice channel you own in order to use this!", color = discord.Colour.dark_red())
            return await ctx.send(embed = embed)

        else:
            if voice_state.channel.id in self.presetChannels:
                embed = discord.Embed(title = f"{Emoji.deny} UnAuthorized Channel Modification", description = "You are not allowed to modify these channels!\n\n**Error Detection:**\n**1)** Detected Static Channels", color = discord.Colour.dark_red())
                return await ctx.send(embed = embed)

            if member.voice.channel.category_id in self.categoryID:
                query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))

                if query.exists():
                    query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                    print(query.lockStatus)

                    if query.lockStatus == "0":
                        embed = discord.Embed(title = f"{Emoji.deny} Invalid Setup", description = "Hey there! This voice channel is already open to the public, if you want to limit its access to certain people. Then consider using `+lock` and then come back this command!", color = discord.Colour.blurple())
                        return await ctx.send(embed = embed)

                    else:
                        if typeAction == "+" or typeAction.lower() == "add":
                            if user == None:
                                return await ctx.send(f"{Emoji.deny} Invalid User Provided...")
                            await member.voice.channel.set_permissions(user, connect = True, view_channel = True)
                            embed = discord.Embed(title = f"{Emoji.addgear} Permit Setup", description = f"{user.mention} now has access to this channel!", color = discord.Colour.blurple())
                            return await ctx.send(embed = embed)
                            
                        elif typeAction == "-" or typeAction.lower() == "remove":
                            if user == None:
                                return await ctx.send(f"{Emoji.deny} Invalid User Provided...")

                            if user.id == int(query.authorID):
                                return await ctx.send(f"{Emoji.deny} You can't modify your own access!")

                            await member.voice.channel.set_permissions(user, overwrite=None)
                            embed = discord.Embed(title = f"{Emoji.minusgear} Permit Setup", description = f"{user.mention}'s access has been removed from this channel!", color = discord.Colour.blurple())
                            return await ctx.send(embed = embed)

                        elif typeAction == "=" or typeAction.lower() == "list":
                            ch = member.voice.channel
                            randomlist = []
                            for x in ch.overwrites:
                                if isinstance(x, discord.Member):
                                    randomlist.append(x.display_name)

                            formatVer = "\n".join(randomlist)
                            
                            embed = discord.Embed(title = f"{Emoji.cycle} Permit List", description = f"**Users Authorized:**\n\n{formatVer}", color = discord.Color.gold())
                            await ctx.send(embed = embed)
                        
                        else:
                            embed = discord.Embed(title = f"{Emoji.warn} Invalid Operation", description = "Supported operations: `+`/add, `-`/remove, `=`/list", color = discord.Color.dark_gold())
                            embed.add_field(name = "Documentation", value = "Hey there, it looks you didn't specify a valid operation type to this user. Take a look at this documentation!\n\n**PERMIT:**\n\nUsage: `+permit <operation> <user>`\n**Description:** Modifies your voice channel's permissions.\n**NOTE:** The argument `operation` supports `+`/add, `-`/remove, `=`/list. If you are using `=` or `list`, you do not need to specify a user.\n\n**Examples:**\n\nAdding Members -> `+permit add @Space#0001`\nRemoving Members -> `+permit remove @Space#0001`\nListing Members -> `+permit =`")
                            return await ctx.send(embed = embed)

                else:
                    try:
                        q = database.VCChannelInfo.select().where((database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                    except:
                        embed = discord.Embed(title = f"{Emoji.invalidchannel} Ownership Check Failed", description = "This isn't a valid channel! Please use the command on an actual private voice channel!", color = discord.Colour.red())
                    else:
                        embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = f"You are not the owner of this voice channel, please ask the original owner <@{q.authorID}>, to end it!", color = discord.Colour.red())
                    finally:
                        await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title = f"{Emoji.warn} Unknown Channel", description = "You are not the owner of this voice channel nor is this a valid channel. Please execute the command under a channel you own!", color = discord.Colour.red())
                        
                await ctx.send(embed = embed)




    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def voicelimit(self, ctx, new_voice_limit):
        #database.db.connect(reuse_if_open=True)
        member = ctx.guild.get_member(ctx.author.id)
        timestamp2 = datetime.now(EST)
        MT = discord.utils.get(ctx.guild.roles, name= self.MOD)
        MAT = discord.utils.get(ctx.guild.roles, name= self.MAT)
        TT = discord.utils.get(ctx.guild.roles, name=self.TT)
        AT = discord.utils.get(ctx.guild.roles, name=self.AT)
        VP = discord.utils.get(ctx.guild.roles, name=self.VP)
        CO = discord.utils.get(ctx.guild.roles, name=self.CO)

        voice_state = member.voice

        if voice_state == None:
            embed = discord.Embed(title = f"{Emoji.invalidchannel} Unknown Voice Channel", description = "You have to be in a voice channel you own in order to use this!", color = discord.Colour.dark_red())
            return await ctx.send(embed = embed)

        else:
            if voice_state.channel.id in self.presetChannels:
                embed = discord.Embed(title = f"{Emoji.deny} UnAuthorized Channel Modification", description = "You are not allowed to modify these channels!\n\n**Error Detection:**\n**1)** Detected Static Channels", color = discord.Colour.dark_red())
                return await ctx.send(embed = embed)

            if member.voice.channel.category_id in self.categoryID:
                query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))

                if query.exists():
                    try:
                        voiceLIMIT = int(new_voice_limit)
                    except:
                        return await ctx.send(f"{Emoji.deny} Not a valid number!")
                    else:
                        if voiceLIMIT == 0:
                            return await ctx.send(f"{Emoji.warn} Sorry, you can't set your voice channel to `0`!")

                        if voiceLIMIT < 0:
                            return await ctx.send(f"{Emoji.warn} Sorry, you can't set your voice channel to something below `-1`!")
                            
                        if MT not in ctx.author.roles and MAT not in ctx.author.roles and TT not in ctx.author.roles and AT not in ctx.author.roles and VP not in ctx.author.roles and CO not in ctx.author.roles:
                            if voiceLIMIT > 4 and ctx.guild.id == 763119924385939498:
                                return await ctx.send(f"{Emoji.warn} You can't increase the voice limit to something bigger then 4 members!")
                            
                            elif ctx.guild.id == 891521033700540457:
                                await member.voice.channel.edit(user_limit = voiceLIMIT)
                                return await ctx.send(f"{Emoji.confirm} Successfully modified voice limit!")

                        else:
                            if voiceLIMIT > 10:
                                return await ctx.send(f"{Emoji.warn} You can't increase the voice limit to something bigger then 10 members!")
                            
                            else:
                                await member.voice.channel.edit(user_limit = voiceLIMIT)
                                return await ctx.send(f"{Emoji.confirm} Successfully modified voice limit!")
                    


                else:
                    try:
                        q = database.VCChannelInfo.select().where((database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                    except:
                        embed = discord.Embed(title = f"{Emoji.invalidchannel} Ownership Check Failed", description = "This isn't a voice channel! Please use the command on an actual private channel!", color = discord.Colour.red())
                    else:
                        embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = f"You are not the owner of this voice channel, please ask the original owner <@{q.authorID}>, to end it!", color = discord.Colour.red())
                    finally:
                        await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title = f"{Emoji.warn} Unknown Channel", description = "You are not the owner of this voice channel nor is this a valid channel. Please execute the command under a channel you own!", color = discord.Colour.red())
                        

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def disconnect(self, ctx, user: discord.Member):
        database.db.connect(reuse_if_open=True)
        member = ctx.guild.get_member(ctx.author.id)
        timestamp2 = datetime.now(EST)

        voice_state = member.voice

        if voice_state == None:
            embed = discord.Embed(title = f"{Emoji.warn} Unknown Voice Channel", description = "You have to be in a voice channel you own in order to use this!", color = discord.Colour.dark_red())
            return await ctx.send(embed = embed)

        else:
            if voice_state.channel.id in self.presetChannels:
                embed = discord.Embed(title = f"{Emoji.deny} UnAuthorized Channel Modification", description = "You are not allowed to modify these channels!\n\n**Error Detection:**\n**1)** Detected Static Channels", color = discord.Colour.dark_red())
                return await ctx.send(embed = embed)

            if member.voice.channel.category_id in self.categoryID:
                query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == ctx.author.id) & (database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id))

                if query.exists():
                    await user.move_to(None)
                    embed = discord.Embed(title = f"{Emoji.minusgear} Disconnected User", description = f"Disconnected {user.mention}!", color = discord.Colour.green())
                    return await ctx.send(embed = embed)


                else:
                    try:
                        q = database.VCChannelInfo.select().where((database.VCChannelInfo.ChannelID == voice_state.channel.id) & (database.VCChannelInfo.GuildID == ctx.guild.id)).get()
                    except:
                        embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = "This isn't a valid voice channel! Please use the command on an actual voice channel thats under the correct category!", color = discord.Colour.red())
                    else:
                        embed = discord.Embed(title = f"{Emoji.deny} Ownership Check Failed", description = f"You are not the owner of this voice channel, please ask the original owner <@{q.authorID}>, to end it!", color = discord.Colour.red())
                    finally:
                        await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title = f"{Emoji.warn} Unknown Channel", description = "You are not the owner of this voice channel nor is this a valid channel. Please execute the command under a channel you own!", color = discord.Colour.red())
                        
                await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(TutorVCCMD(bot))


