from pathlib import Path
import discord
from core import database
from core.checks import is_botAdmin, is_botAdmin2, is_botAdmin3, is_botAdmin4
from core.common import Emoji
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

def get_extensions():
    extensions = []
    extensions.append('jishaku')
    for file in Path("utils").glob("**/*.py"):
        if "!" in file.name or "DEV" in file.name:
            continue
        extensions.append(str(file).replace("/", ".").replace(".py", ""))
    return extensions

class CoreBotConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['f'])
    async def filter(self, ctx):
        pass

    @filter.command()
    @is_botAdmin4
    async def modify(self, ctx, num: int, val: bool):
        CheckDB : database.CheckInformation =  database.CheckInformation.select().where(database.CheckInformation.id == 1).get()
        
        databaseValues = {
            1: "CheckDB.MasterMaintenance",
            2: "CheckDB.guildNone",
            3: "CheckDB.externalGuild",
            4: "CheckDB.ModRoleBypass",
            5: "CheckDB.ruleBypass",
            6: "CheckDB.publicCategories",
            7: "CheckDB.elseSituation"
        }


        if num == 1:
            CheckDB.MasterMaintenance = val
            CheckDB.save()
        elif num == 2:
            CheckDB.guildNone = val
            CheckDB.save()
        elif num == 3:
            CheckDB.externalGuild = val
            CheckDB.save()
        elif num == 4:
            CheckDB.ModRoleBypass = val
            CheckDB.save()
        elif num == 5:
            CheckDB.ruleBypass = val
            CheckDB.save()
        elif num == 6:
            CheckDB.publicCategories = val
            CheckDB.save()
        elif num == 7:
            CheckDB.elseSituation = val
            CheckDB.save()
        else:
            return await ctx.send(f"Not a valid option\n```py\n{databaseValues}\n```")

            
        await ctx.send(f"Field: {databaseValues[num]} has been set to {str(val)}")



    @filter.command()
    async def list(self, ctx):
        CheckDB : database.CheckInformation =  database.CheckInformation.select().where(database.CheckInformation.id == 1).get()

        embed = discord.Embed(title = "Command Filters", description = "Bot Filters that the bot is subjected towards.", color = discord.Colour.gold())
        embed.add_field(name = "Checks", value = f"1) `Maintenance Mode`\n{Emoji.barrow} {CheckDB.MasterMaintenance}\n\n2) `NoGuild`\n{Emoji.barrow} {CheckDB.guildNone}\n\n3) `External Guilds`\n{Emoji.barrow} {CheckDB.externalGuild}\n\n4) `ModBypass`\n{Emoji.barrow} {CheckDB.ModRoleBypass}\n\n5) `Rule Command Bypass`\n{Emoji.barrow} {CheckDB.ruleBypass}\n\n6) `Public Category Lock`\n{Emoji.barrow} {CheckDB.publicCategories}\n\n7) `Else Conditions`\n{Emoji.barrow} {CheckDB.elseSituation}")
        await ctx.send(embed = embed)




    @commands.group(aliases=['pre'])
    async def prefix(self, ctx):
        pass

    @prefix.command()
    @is_botAdmin3
    async def delete(self, ctx, num: int):
        WhitelistedPrefix : database.WhitelistedPrefix = database.WhitelistedPrefix.select().where(database.WhitelistedPrefix.id == num).get()
        WhitelistedPrefix.delete_instance()
        await ctx.send(f"Field: {WhitelistedPrefix.prefix} has been deleted")

    @prefix.command()
    @is_botAdmin3
    async def add(self, ctx, prefix):
        WhitelistedPrefix = database.WhitelistedPrefix.create(prefix = prefix, status = True)
        await ctx.send(f"Field: {WhitelistedPrefix.prefix} has been added!")



    @prefix.command()
    async def list(self, ctx):
        
        PrefixDB = database.WhitelistedPrefix
        response = []

        for entry in PrefixDB:
            
            if entry.status == True:
                statusFilter = "ACTIVE"
            else:
                statusFilter = "DISABLED"

            response.append(f"Prefix `{entry.prefix}`:\n{Emoji.barrow} {statusFilter}")


        embed = discord.Embed(title = "Whitelisted Prefix's", description = "Bot Prefix's that are whitelisted in staff commands.", color = discord.Colour.gold())
        embed.add_field(name = "Prefix List", value = "\n\n".join(response))
        await ctx.send(embed = embed)

    @commands.group(aliases=['cog'])
    @is_botAdmin2
    async def cogs(self, ctx):
        pass


    @cogs.command()
    @is_botAdmin2
    async def unload(self, ctx, ext):
        if "cogs." not in ext:
            ext = f"cogs.{ext}"
        if ext in get_extensions():
            self.bot.unload_extension(ext)
            embed = discord.Embed(
                title="Cogs - Unload", description=f"Unloaded cog: {ext}", color=0xd6b4e8)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Cogs Reloaded", description=f"Cog '{ext}' not found", color=0xd6b4e8)
            await ctx.send(embed=embed)


    @cogs.command()
    @is_botAdmin2
    async def load(self, ctx, ext):
        if "cogs." not in ext:
            ext = f"cogs.{ext}"
        if ext in get_extensions():
            self.bot.load_extension(ext)
            embed = discord.Embed(title="Cogs - Load",
                                description=f"Loaded cog: {ext}", color=0xd6b4e8)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Cogs - Load", description=f"Cog '{ext}' not found.", color=0xd6b4e8)
            await ctx.send(embed=embed)


    @cogs.command(aliases=['restart'])
    @is_botAdmin2
    async def reload(self, ctx, ext):
        if ext == "all":
            embed = discord.Embed(
                title="Cogs - Reload", description="Reloaded all cogs", color=0xd6b4e8)
            for extension in get_extensions():
                self.bot.reload_extension(extension)
            await ctx.send(embed=embed)
            return

        if "cogs." not in ext:
            ext = f"cogs.{ext}"

        if ext in get_extensions():
            self.bot.reload_extension(ext)
            embed = discord.Embed(
                title="Cogs - Reload", description=f"Reloaded cog: {ext}", color=0xd6b4e8)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Cogs - Reload", description=f"Cog '{ext}' not found.", color=0xd6b4e8)
            await ctx.send(embed=embed)


    @cogs.command()
    @is_botAdmin2
    async def view(self, ctx):
        msg = " ".join(get_extensions())
        embed = discord.Embed(title="Cogs - View", description=msg, color=0xd6b4e8)
        await ctx.send(embed=embed)

    @commands.group()
    async def w(self, ctx):
        pass


    @w.command()
    @is_botAdmin
    async def list(self, ctx):
        adminList = []

        query1 = database.Administrators.select().where(database.Administrators.TierLevel == 1)
        for admin in query1:
            user = await self.bot.fetch_user(admin.discordID)
            adminList.append(f"`{user.name}` -> `{user.id}`")

        adminLEVEL1 = "\n".join(adminList)

        adminList = []
        query2 = database.Administrators.select().where(database.Administrators.TierLevel == 2)
        for admin in query2:
            user = await self.bot.fetch_user(admin.discordID)
            adminList.append(f"`{user.name}` -> `{user.id}`")

        adminLEVEL2 = "\n".join(adminList)

        adminList = []
        query3 = database.Administrators.select().where(database.Administrators.TierLevel == 3)
        for admin in query3:
            user = await self.bot.fetch_user(admin.discordID)
            adminList.append(f"`{user.name}` -> `{user.id}`")

        adminLEVEL3 = "\n".join(adminList)

        adminList = []
        query4 = database.Administrators.select().where(database.Administrators.TierLevel == 4)
        for admin in query4:
            user = await self.bot.fetch_user(admin.discordID)
            adminList.append(f"`{user.name}` -> `{user.id}`")

        adminLEVEL4 = "\n".join(adminList)

        embed = discord.Embed(title="Bot Administrators", description="Whitelisted Users that have Increased Authorization",
                            color=discord.Color.green())
        embed.add_field(name="Whitelisted Users",
                        value=f"Format:\n**Username** -> **ID**\n\n**Permit 4:** *Owners*\n{adminLEVEL4}\n\n**Permit 3:** *Sudo Administrators*\n{adminLEVEL3}\n\n**Permit 2:** *Administrators*\n{adminLEVEL2}\n\n**Permit 1:** *Bot Managers*\n{adminLEVEL1}")
        embed.set_footer(text="Only Owners/Permit 4's can modify Bot Administrators. | Permit 4 is the HIGHEST Authorization Level")

        await ctx.send(embed=embed)


    @w.command()
    @is_botAdmin4
    async def remove(self, ctx, ID: discord.User):
        database.db.connect(reuse_if_open=True)

        query = database.Administrators.select().where(database.Administrators.discordID == ID.id)
        if query.exists():
            query = query.get()

            query.delete_instance()

            embed = discord.Embed(title="Successfully Removed User!",
                                description=f"{ID.name} has been removed from the database!", color=discord.Color.green())
            await ctx.send(embed=embed)


        else:
            embed = discord.Embed(title="Invalid User!", description="Invalid Provided: (No Record Found)",
                                color=discord.Color.red())
            await ctx.send(embed=embed)

        database.db.close()


    @w.command()
    @is_botAdmin4
    async def add(self, ctx, ID: discord.User, level: int):
        database.db.connect(reuse_if_open=True)

        q: database.Administrators = database.Administrators.create(discordID=ID.id, TierLevel=level)
        q.save()

        embed = discord.Embed(title="Successfully Added User!",
                            description=f"{ID.name} has been added successfully with permit level `{str(level)}`.",
                            color=discord.Color.gold())
        await ctx.send(embed=embed)

        database.db.close()

def setup(bot):
    bot.add_cog(CoreBotConfig(bot))
