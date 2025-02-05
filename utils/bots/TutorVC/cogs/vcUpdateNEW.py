import asyncio
import datetime
from datetime import datetime, timedelta

import discord
from core import database
from core.common import Emoji
from discord.ext import commands
import pytz

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

    return now_plus_10.strftime(r"%I:%M %p")

def showTotalMinutes(dateObj: datetime):
    now = datetime.now(EST)

    deltaTime = now - dateObj

    totalmin = deltaTime.total_seconds() // 60

    return totalmin, now
    

class TutorVCUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.channel_id = {763119924385939498: 843637802293788692, 891521033700540457: 895041227123228703}

        #self.categoryID = 776988961087422515
        self.staticChannels = [784556875487248394, 784556893799448626, 895041070956675082]
        self.presetChannels = [843637802293788692, 784556875487248394, 784556893799448626, 895041227123228703, 895041070956675082]

        self.TutorLogID = 873326994220265482

        self.AT = "Academics Team"
        self.SB = "Simplified Booster"
        self.Legend = "Legend"
        
        self.TMOD = "Mod Trainee"
        self.MOD = "Moderator"
        self.SMOD = "Senior Mod"
        self.CO = "CO"
        self.VP = "VP"

        self.MAT = "Marketing Team"
        self.TT = "Technical Team"

        self.TutorRole = "Tutor"

        self.categoryIDs = [776988961087422515, 895041016057446411]
        self.CcategoryIDs = {763119924385939498: 776988961087422515, 891521033700540457: 895041016057446411}
        self.LobbyStartIDs = {763119924385939498: 843637802293788692, 891521033700540457 :895041227123228703}



    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        database.db.connect(reuse_if_open=True)
        lobbyStart = await self.bot.fetch_channel(self.LobbyStartIDs[member.guild.id])

        if before.channel != None and (after.channel == None or after.channel.category_id not in self.categoryIDs or after.channel.id in self.staticChannels) and not member.bot:
            
            acadChannel = await self.bot.fetch_channel(self.channel_id[member.guild.id])
            query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == member.id) & (database.VCChannelInfo.ChannelID == before.channel.id) & (database.VCChannelInfo.GuildID == before.channel.guild.id))
            ignoreQuery = database.IgnoreThis.select().where((database.IgnoreThis.authorID == member.id) & (database.IgnoreThis.channelID == before.channel.id) & (database.IgnoreThis.GuildID == before.channel.guild.id))
            
            if ignoreQuery.exists():
                iq: database.IgnoreThis = database.IgnoreThis.select().where((database.IgnoreThis.authorID == member.id) & (database.IgnoreThis.channelID == before.channel.id) & (database.IgnoreThis.GuildID == before.channel.guild.id)).get()
                iq.delete_instance()
                return print("Ignore Channel")


            if query.exists() and before.channel.category.id in self.categoryIDs:
                query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == member.id) & (database.VCChannelInfo.ChannelID == before.channel.id) & (database.VCChannelInfo.GuildID == before.channel.guild.id)).get()
                try:
                    tutorChannel = await self.bot.fetch_channel(int(query.ChannelID))
                except:
                    tutorChannel = None

                print(query.ChannelID)
                print(before.channel.id)
                if query.ChannelID == str(before.channel.id):
                    embed = discord.Embed(title = f"{Emoji.time} WARNING: Voice Channel is about to be deleted!", description = "If the voice session has ended, **you can ignore this!**\n\nIf it hasn't ended, please make sure you return to the channel in **2** Minutes, otherwise the channel will automatically be deleted!", color= discord.Colour.red())                    
                    
                    if member in lobbyStart.members:
                        try:
                            await member.move_to(tutorChannel, reason = "Hogging the VC Start Channel.")
                        except:
                            await member.move_to(None, reason = "Hogging the VC Start Channel.")
                        
                            
                    await acadChannel.send(content = member.mention, embed = embed)

                    await asyncio.sleep(120)

                    print(before.channel)
                    if member in before.channel.members:
                        return print("returned")

                    else:
                        query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == member.id) & (database.VCChannelInfo.ChannelID == before.channel.id) & (database.VCChannelInfo.GuildID == before.channel.guild.id))
                        if query.exists():
                            query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == member.id) & (database.VCChannelInfo.ChannelID == before.channel.id) & (database.VCChannelInfo.GuildID == before.channel.guild.id)).get()
                            VCDatetime = pytz.timezone("America/New_York").localize(query.datetimeObj)

                            day, now = showTotalMinutes(VCDatetime)
                            #daySTR = VCDatetime.strftime("%H:%M %p EST")
                            #nowSTR = now.strftime("%H:%M %p EST")

                            daySTR = int(VCDatetime.timestamp())
                            nowSTR = int(now.timestamp())
                            
                            query.delete_instance() 

                            try:
                                await before.channel.delete()
                            except Exception as e:
                                print(f"Error Deleting Channel:\n{e}")
                            else:
                                embed = discord.Embed(title = f"{Emoji.archive} {member.display_name} Total Voice Minutes", description = f"{member.mention} you have spent a total of {Emoji.calender} `{day} minutes` in voice channel, **{query.name}**.\n**THIS TIME MAY NOT BE ACCURATE**", color = discord.Colour.gold())
                                embed.set_footer(text = "The voice channel has been deleted!")
                                

                                await acadChannel.send(content = member.mention, embed = embed) 
                                tutorSession = database.TutorBot_Sessions.select().where(database.TutorBot_Sessions.SessionID == query.TutorBotSessionID)
                                if tutorSession.exists():
                                    
                                    tutorSession = tutorSession.get()

                                    student = await self.bot.fetch_user(tutorSession.StudentID)
                                    tutor = await self.bot.fetch_user(tutorSession.TutorID)
                                    HOURCH = await self.bot.fetch_channel(self.TutorLogID)

                                    hourlog = discord.Embed(title = "Hour Log", description = f"{tutor.mention}'s Tutor Log", color = discord.Colour.blue())
                                    hourlog.add_field(name = "Information", value = f"**Tutor:** {tutor.mention}\n**Student:** {student.mention}\n**Time Started:** <t:{daySTR}>t>\n**Time Ended:** <t:{nowSTR}:t>\n\n**Total Time:** {day}")
                                    hourlog.set_footer(text = f"Session ID: {tutorSession.SessionID}")
                                    await HOURCH.send(embed = embed)

                                    feedback = discord.Embed(title = "Feedback!", description = "Hey it looks like you're tutor session just ended, if you'd like to let us know how we did please fill out the form below!\n\nhttps://forms.gle/Y1oobNFEBf7vpfMM8", color = discord.Colour.green())
                                    loggedhours = discord.Embed(title = "Logged Hours", description = "Hey! It looks like you've finished your tutor session, I've already went ahead and sent your session legnth in <#873326994220265482>.\n**NOTE:** You'll still need to fill in your hours on the hour log spreadsheet.", color = discord.Color.green())
                                    
                                    try:
                                        await tutor.send(embed = feedback)
                                        await student.send(embed = loggedhours)
                                    except discord.HTTPException:
                                        pass
                        else:       
                            print("no query, moving on...")
                else:
                    print("no")



        if after.channel != None and after.channel.id in self.presetChannels and not member.bot:
            acadChannel = await self.bot.fetch_channel(self.LobbyStartIDs[member.guild.id])
            SB = discord.utils.get(member.guild.roles, name = self.SB)

            legend = discord.utils.get(member.guild.roles, name = self.Legend)

            MT = discord.utils.get(member.guild.roles, name=self.MOD)
            MAT = discord.utils.get(member.guild.roles, name=self.MAT)
            TT = discord.utils.get(member.guild.roles, name=self.TT)
            AT = discord.utils.get(member.guild.roles, name=self.AT)
            VP = discord.utils.get(member.guild.roles, name=self.VP)
            CO = discord.utils.get(member.guild.roles, name=self.CO)
            TutorRole = discord.utils.get(member.guild.roles, name=self.TutorRole)

            #if team in member.roles:
            category = discord.utils.get(member.guild.categories, id = self.CcategoryIDs[after.channel.guild.id])

            if len(category.voice_channels) >= 25:
                embed = discord.Embed(title = f"{Emoji.deny} Max Channel Allowance", description = "I'm sorry! This category has reached its full capacity at **15** voice channels!\n\n**Please wait until a private voice session ends before creating a new voice channel!**", color = discord.Colour.red())
                await member.move_to(None, reason = "Max Channel Allowance")
                return await acadChannel.send(content = member.mention, embed = embed)


            query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == member.id) & (database.VCChannelInfo.GuildID == after.channel.guild.id))
            if query.exists():
                moveToChannel = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == member.id) & (database.VCChannelInfo.GuildID == after.channel.guild.id)).get()
                embed = discord.Embed(title = f"{Emoji.deny} Maximum Channel Ownership Allowance", description = "I'm sorry! You already have an active voice channel and thus you can't create anymore channels.\n\n**If you would like to remove the channel without waiting the 2 minutes, use `+end`!**", color = discord.Colour.red())
                
                try:
                    tutorChannel = await self.bot.fetch_channel(int(moveToChannel.ChannelID))
                    await member.move_to(tutorChannel, reason = "Maximum Channel Ownership Allowance [TRUE]")
                except:
                    await member.move_to(None, reason = "Maximum Channel Ownership Allowance [FAIL]")
                    
                return await acadChannel.send(content = member.mention, embed = embed)

            else:

                def check(m):
                    return m.content is not None and m.channel == acadChannel and m.author is not self.bot.user and m.author == member

                if SB not in member.roles and AT not in member.roles and legend not in member.roles and MT not in member.roles and MAT not in member.roles and TT not in member.roles and VP not in member.roles and CO not in member.roles:
            
                    embed = discord.Embed(title = f"{Emoji.confirm} Voice Channel Creation", description = f"*Created: {member.display_name}'s Channel*", color = discord.Colour.green())
                    embed.add_field(name = "Voice Channel Commands", value = "https://timmy.schoolsimplified.org/tutorvc")
                    embed.set_footer(text = "If you have any questions, consult the help command! | +help")

                else:
                    embed = discord.Embed(title = f"{Emoji.confirm} Voice Channel Creation", description = f"*Created: {member.display_name}'s Channel*", color = discord.Colour.green())
                    embed.add_field(name = "Voice Channel Commands", value = "https://timmy.schoolsimplified.org/tutorvc")
                    embed.set_footer(text = "If you have any questions, consult the help command! | +help")

                if TutorRole in member.roles:
                    embed.add_field(name = "Convert to Tutor Session?", value = "Hey, it looks like you're a tutor! If this is going to be a tutor session please use the command `+settutor id`, replacing 'id' with your 3 digit tutor id.", inline = False)

                channel = await category.create_voice_channel(f"{member.display_name}'s Channel", user_limit = 2)
                await channel.set_permissions(member.guild.default_role, stream = True)
                tag: database.VCChannelInfo = database.VCChannelInfo.create(ChannelID = channel.id, name = f"{member.display_name}'s Channel", authorID = member.id, used = True, datetimeObj = datetime.now(EST), lockStatus = "0", GuildID = member.guild.id,)
                tag.save()

                '''
                voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild= member.guild)
                audio_source = discord.FFmpegPCMAudio('utils/bots/TutorVC/confirm.mp3')
                
                try:
                    voice_client.play(audio_source)
                except Exception as e:
                    print(f"Ignoring error:\n{e}")
                    
                await asyncio.sleep(2)
                '''

                await acadChannel.send(content = member.mention, embed = embed)

                try:
                    await member.move_to(channel, reason = "Response Code: OK -> Moving to VC | Created Tutor Channel")

                except Exception as e:
                    print(f"Left VC before setup.\n{e}")
                    query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == member.id) & (database.VCChannelInfo.ChannelID == channel.id) & (database.VCChannelInfo.GuildID == after.channel.guild.id))
                    
                    if query.exists():
                        query = database.VCChannelInfo.select().where((database.VCChannelInfo.authorID == member.id) & (database.VCChannelInfo.ChannelID == channel.id) & (database.VCChannelInfo.GuildID == after.channel.guild.id)).get()
                        query.delete_instance()
                        
                        try:
                            await channel.delete()
                        except Exception as e:
                            print(f"Error Deleting Channel:\n{e}")
                        else:
                            embed = discord.Embed(title = f"{Emoji.archive} {member.display_name} Total Voice Minutes", description = f"{member.mention} I removed your voice channel, **{query.name}** since you left without me properly setting it up!", color = discord.Colour.dark_grey())
                            embed.set_footer(text = "The voice channel has been deleted!")
                            await acadChannel.send(content = member.mention, embed = embed)
                            print("done")
                        
                    else:
                        print("Already deleted, moving on...")
        database.db.close()

def setup(bot):
    bot.add_cog(TutorVCUpdate(bot))


