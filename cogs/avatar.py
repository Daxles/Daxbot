import discord
from discord.ext import commands

class Avatar(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name='avatar',aliases=["av"], description="Returns the avatar of the specified user!")
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        
        memberAvatar = member.avatar_url

        embed = discord.Embed(title=f"{member.name}'s Avatar")
        embed.set_image(url = memberAvatar)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Avatar(client))