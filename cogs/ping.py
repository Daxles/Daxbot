import discord
from discord.ext import commands


class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="ping", description="Returns the latency of the bot")
    async def ping(self, ctx):
        message = await ctx.send("Pong!")
        await message.edit(content = f"Pong! **{round(self.client.latency * 1000)}**ms")    

def setup(client):
    client.add_cog(Ping(client))