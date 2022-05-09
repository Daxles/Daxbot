import discord
from discord.ext import commands
import json
from requests import get

class Meme(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="meme", description="Returns a random meme")
    async def meme(self, ctx):
        content = get("https://meme-api.herokuapp.com/gimme").text
        data = json.loads(content)
        meme = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
        await ctx.send(embed=meme)

def setup(client):
    client.add_cog(Meme(client))