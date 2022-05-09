import discord 
from discord.ext import commands   

class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="prefix", description="Changes the prefix of the bot.",aliases=['setprefix'])
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix=None):
        if prefix is None:
            em = discord.Embed(title='<:cross:956904380148371476> Error', description=f'{ctx.author.mention}, Please specify a prefix for me to change it to', color=0xCC1313)
            return await ctx.send(embed=em)
        
        data = await self.client.prefixes.find(ctx.guild.id)
        if data is None or "prefix" not in data:
            data = {"_id": ctx.guild.id, "prefix": prefix}
        
        data["prefix"] = prefix
        await self.client.prefixes.upsert(data)
        em = discord.Embed(title='Changed prefix!', description=f"Succesfully changed the prefix for this guild to `{prefix}`", color=0x0FF729)
        await ctx.send(embed=em)

    @commands.command(name="deleteprefix", description="Deletes the prefix and sets it to default",aliases=["dp"])
    @commands.has_permissions(manage_guild=True)
    async def deleteprefix(self, ctx):
        await self.client.prefixes.unset({"_id": ctx.guild.id, "prefix": 1})
        em = discord.Embed(title='Prefix reset!', description=f"Succesfully set the prefix to default `.`", color=0xF8BB05)
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Config(client))

