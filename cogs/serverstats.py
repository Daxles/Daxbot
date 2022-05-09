import discord
from discord.ext import commands
import platform
import logging

class Serverstats(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="serverstats",aliases=["stats"], description="Gives stats about a server")
    async def serverstats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        await ctx.send(f"So I am in {serverCount} guilds with a total of {memberCount} members. :smiley:\nI am running python {pythonVersion} and discord.py {dpyVersion}")

        
        

def setup(client):
    client.add_cog(Serverstats(client))
