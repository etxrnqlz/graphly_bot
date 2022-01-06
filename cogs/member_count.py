import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
from bot_info import *
import datetime


class MemberCount(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def show_member_count(self, ctx, show: str = "True"):
        """
        Shows the member count of the server in a dedicated channel
        Show Channel: '`.show_member_count`
        Hide Channel: '`.show_member_count False`'
        """
        bot_info = Bot_info.load()
        if not ctx.author.guild_permissions.administrator and ctx.author.id != 541015333910347776:
            return await ctx.send("You don't have permission to use this command!")

        if ctx.guild.id not in bot_info.guilds:
            bot_info.add_guild(ctx.guild)

        if show != "False":
            try:
                if ctx.guild.get_channel(bot_info.guilds[ctx.guild.id].show_members) is not None:
                    await ctx.send(f"Member Count channel already exists")
                    return
            except AttributeError:
                pass

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(connect=False),
                ctx.guild.me: discord.PermissionOverwrite(connect=True)
            }

            channel = await ctx.guild.create_voice_channel("Member Count", overwrites=overwrites)
            await channel.edit(name=f"Member Count: {len([i for i in ctx.guild.members if not i.bot])}")
            await ctx.send(f"Member Count channel created in {channel.mention}")
            bot_info.guilds[ctx.guild.id].show_members = channel.id

        else:
            channel = discord.utils.get(
                ctx.guild.channels, name=f"Member Count: {len([i for i in ctx.guild.members if not i.bot])}")
            await channel.delete()
            await ctx.send("Member Count channel has been deleted")
            bot_info.guilds[ctx.guild.id].show_members = None

        bot_info.save()

    @commands.command()
    async def update_member_count(self, ctx):
        """
        Updates the member count of the server
        Update Count: '`.update_member_count`'
        """
        bot_info = Bot_info.load()
        try:
            channel = ctx.guild.get_channel(
                bot_info.guilds[ctx.guild.id].show_members)
            bot_info.member_count = len(
                [i for i in ctx.guild.members if not i.bot])
            await channel.edit(name=f"Member Count: {len([i for i in ctx.guild.members if not i.bot])}")
            await ctx.send(f"Member Count channel updated in {channel.mention}")
            bot_info.save()
        except Exception as e:
            try:
                channel = ctx.guild.get_channel(
                    bot_info.guilds[ctx.guild.id].show_members)
                bot_info.member_count = len(
                    [i for i in ctx.guild.members if not i.bot])
                await channel.edit(name=f"Member Count: {len([i for i in ctx.guild.members if not i.bot])}")
                bot_info.save()
            except Exception as e:
                print(e)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        bot_info = Bot_info.load()
        await self.update_member_count(member)
        bot_info.guilds[member.guild.id].member_update_time[datetime.datetime.now()] = len(
            [i for i in member.guild.members if not i.bot])
        bot_info.save()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        bot_info = Bot_info.load()
        await self.update_member_count(member)
        bot_info.guilds[member.guild.id].member_update_time[datetime.datetime.now(
        )] = len([i for i in member.guild.members if not i.bot])
        bot_info.save()

    @commands.command()
    async def member_growth(self, ctx):
        bot_info = Bot_info.load()
        try:
            member_counts = bot_info.guilds[ctx.guild.id].member_update_time
        except AttributeError:
            member_counts = {}


def setup(client):
    client.add_cog(MemberCount(client))
