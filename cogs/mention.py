import discord
from discord.ext import commands

class Mention(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener(name="mention")
    async def on_message(self, message):
            if self.client.user.mentioned_in(message):
                embed=discord.Embed(title="Daxbot", url="https://cdn.discordapp.com/emojis/953273755495436298.png")
                await message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Mention(bot))