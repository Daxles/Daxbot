import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
import random

async def web_scrape(text):
        async with aiohttp.ClientSession() as session:
            async with session.get(text) as r:
                status = r.status
                if status == 200:
                    text = await r.text()
                    return text

class Wyr(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
                

    @commands.command(name="wouldyourather",description="Give a would you rather question!", aliases=['wyr'])
    async def wouldyourather(self, ctx):
        text = await web_scrape("https://either.io/")
        soup = BeautifulSoup(text, 'lxml')
        l = []
        for choice in soup.find_all("span",{"class":"option-text"}):
            l.append(choice.text)
        e = discord.Embed(color=discord.Colour.random())
        e.set_author(name="Would you rather...", url="https://daxbot.net/", icon_url=self.client.user.avatar_url)
        e.add_field(name="EITHER...", value=f":regional_indicator_a: {l[0]}", inline=False)
        e.add_field(name="OR...", value=f":regional_indicator_b: {l[1]}", inline=False)
        msg = await ctx.send(embed=e)
        await msg.add_reaction("🇦")
        await msg.add_reaction("🇧")
        



def setup(client):
    client.add_cog(Wyr(client))