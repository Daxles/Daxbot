import discord
from discord.ext import commands
import asyncio
from discord import Embed
from datetime import datetime

class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets member object
        muted = discord.utils.get(ctx.guild.roles, name="Muted") # gets role object
        if muted in argument.roles: # checks if user has muted role
            return argument # returns member object if there is muted role
        else:
            raise commands.BadArgument("The user was not muted.")

def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try: 
        val = int(time[:-1])
    except:
        return -2 
    
    return val * time_dict[unit]

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    

    @commands.command(name="mute", description="Mutes a user")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, time, reason):
        role = discord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't 
        if not role: # checks if there is muted role
            try: # creates muted role 
                muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                await ctx.send("Make sure to put the role higher then `@everyone` or your default member role!")
                for channel in ctx.guild.channels: # removes permission to view and send in the channels 
                    await channel.set_permissions(muted, send_messages=False,
                                                read_message_history=False)
            except discord.Forbidden:
                return await ctx.send("I have no permissions to make a muted role") # self-explainatory
            await user.add_roles(muted) # adds newly created muted role
            await ctx.send(f"{user.mention} Has been muted for {reason} for {time}")
            await asyncio.sleep(convert(time))
            await user.remove_roles(role)
        else:
            await user.add_roles(role) # adds already existing muted role
            await ctx.send(f"{user.mention} Has been muted for {reason} for {time}")
            await asyncio.sleep(convert(time))
            await user.remove_roles(role)

    @commands.command(name="kick", description="Kicks a user from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member == None:
            await ctx.send("Please mention a user")
        else:
            await ctx.guild.kick(user=member, reason=reason)

            channel = self.client.get_channel(954837357239091260)
            embed = discord.Embed(title=f"{ctx.author.name} kicked: {member.name}", description=reason)
            await channel.send(embed=embed)
            await ctx.send(f'Kicked **{member.name}** for **{reason}**')
    
    


    @commands.command(name="ban", description="Bans a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member == None:
            await ctx.send("Please mention a user") 
        else:
            await ctx.guild.ban(user=member, reason=reason)
            
            channel = self.client.get_channel(954837357239091260)
            embed = discord.Embed(title=f"{ctx.author.name} banned: {member.name}", description=reason)
            await channel.send(embed=embed)
            await ctx.send(f'Banned **{member.name}** for **{reason}**')

    @commands.command(name="unban", description="Unbans a user from the server")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member = None, *, reason=None):
        if member == None:
            await ctx.send("Please mention a user") 
        else:
        
            member = await self.client.fetch_user(int(member))
            await ctx.guild.unban(user=member, reason=reason)

            channel = self.client.get_channel(954837357239091260)
            embed = discord.Embed(title=f"{ctx.author.name} unbanned: {member.name}", description=reason)
            await channel.send(embed=embed)
            await ctx.send(f'Unbanned **{member.name}** for **{reason}**')
    
    @commands.command(name="purge", description="Purges a set amount of messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        if amount == None:
            await ctx.send("Please enter a amount")
        else:

            await ctx.channel.purge(limit=amount+1)

            channel = self.client.get_channel(954837357239091260)
            embed = discord.Embed(title=f"{ctx.author.name} purged: {ctx.channel.name}", description=f"{amount} messages were cleared")
            await channel.send(embed=embed)
            await ctx.send(f'**{ctx.author.name}** purged **{amount} messages**')

            # em = discord.Embed(title='Error', description=f"{ctx.author.mention}, You don't have the permissions to do this.", color=0xCC1313)
        
    

    

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: Redeemed):
        """Unmutes a muted user"""
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
        await ctx.send(f"{user.mention} has been unmuted")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
    
            channel = self.client.get_channel(954837357239091260)
            deleted = Embed(
                description=f"Message deleted in {message.channel.mention}", color=0x4040EC
            ).set_author(name=message.author, url=Embed.Empty, icon_url=message.author.avatar_url)

            deleted.add_field(name="Message:", value=(message.content or "No message content"))
            deleted.timestamp = message.created_at
            await channel.send(embed=deleted)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.client.get_channel(961913538832658492)
        embed = Embed(title=f"Added to server", color=0x00ff00)
        embed.add_field(name=f"Server ID:", value=guild.id, inline=False)
        embed.add_field(name=f"Owner ID:", value=guild.owner_id, inline=False)
        embed.add_field(name=f"Membercount:", value=guild.member_count, inline=False)
        embed.set_footer(text=datetime.datetime.utcnow())
        await channel.send(embed=embed)
    
    @commands.command(name="lock", description="Locks a channel so users cannot speak in it anymore")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrites = {ctx.guild.default_role: discord.set_permission(send_messages=False, read_message_history=False)}
        await channel.edit(overwrites=overwrites)
        await ctx.send(f"I have locked down `{channel.name}` for you")


    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(send_messages=True)}
        await channel.edit(overwrites=overwrites)
        await ctx.send(f"I have unlocked `{channel.name}` for you")


    @commands.command(name="delete", description="Deletes a channel", aliases=["deletechannel"])
    @commands.has_permissions(manage_channels=True)
    async def channel(self, ctx, channel: discord.TextChannel=None, *, reason=None):
        channel = channel or ctx.channel
        await channel.delete(reason=reason)
        await ctx.send(f"Hey! I have deleted {channel.name} for you")


    







def setup(client):
    client.add_cog(Moderation(client))