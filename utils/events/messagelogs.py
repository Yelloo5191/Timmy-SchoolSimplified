import datetime
from datetime import datetime

import discord
from discord.ext import commands


class MessageLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels = [878792926266810418, 786068971048140820, 808919081469739008]

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return

        print(int(message.channel.id) in self.channels)

        if int(message.channel.id) in self.channels:
            embed=discord.Embed(title = "Deleted Message Log", description = f"**{message.author.mention}** sent this in **{message.channel.mention}**", color= discord.Color.red())

            member = message.guild.get_member(message.author.id)

            embed.set_author(name = message.author.name, icon_url = member.avatar.url)

            embed.add_field(name= "Message", value= message.content, inline=True)

            val = datetime.today().strftime("%I:%M %p")

            embed.set_footer(text = f"Author: {message.author.id} | Message ID: {message.id} • Today at {val}")

            channel = self.bot.get_channel(863177000372666398)
            await channel.send(embed = embed)
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        print(int(before.channel.id) in self.channels)

        if int(before.channel.id) in self.channels:
            embed : discord.Embed = discord.Embed(title=f"Editted Message Log", description = f"**{before.author.mention}** sent this in **{before.channel.mention}**", color=discord.Color.gold())

            member = before.guild.get_member(before.author.id)

            embed.set_author(name = before.author.name, icon_url = member.avatar.url)
            embed.add_field(name="Before" ,value= before.content)
            embed.add_field(name= "After" ,value= after.content,inline=False)

            val = datetime.today().strftime("%I:%M %p")

            embed.set_footer(text = f"Author: {before.author.id} | Message ID: {before.id} • Today at {val}")

            channel = self.bot.get_channel(863177000372666398)
            await channel.send(embed = embed)

def setup(bot):
    bot.add_cog(MessageLogs(bot))



    