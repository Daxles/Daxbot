import discord
from discord.ext import commands

class Membercount(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name='membercount', description="Returns a number of people in the server", aliases=['mc'])
    async def membercount(self, ctx):
        await ctx.send(ctx.guild.member_count)


def setup(client):
    client.add_cog(Membercount(client))