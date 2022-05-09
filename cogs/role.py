import discord
from discord.ext import commands

class Role(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="role", description="Gives or removes a role from a user")
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member = None, *, role: discord.Role):
        if role.position > ctx.author.top_role.position:
            await ctx.send("You don't have permission.")
        if member == None:
            await ctx.send("Please mention a user") 
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"Succesfully removed {role} from {member.mention}.")
        else:
            await member.add_roles(role)
            await ctx.send(f"Succesfully given {role} to {member.mention}.")

def setup(client):
    client.add_cog(Role(client))