import discord
from discord.ext import commands

class EmojiInfo(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    @commands.command(name="emojiinfo",aliases=["ei"], description="Gives info about a emoji")
    async def emoji_info(self, ctx, emoji: discord.Emoji = None):
        if not emoji:
            return await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")
        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        except discord.Notfound:
            return await ctx.send("I could not find this emoji in the given guild.")
        
        is_managed = "Yes" if emoji.managed else "No"
        is_animated = "Yes" if emoji.animated else "No"
        requires_colons = "Yes" if emoji.require_colons else "No"
        creation_time = emoji.created_at.strftime("%I:%M %P %B %d, %Y")
        can_use_emoji = "Everyone" if not emoji.roles else " ".join(role.name for role in emoji.roles)


        description = f"""
        **General:**
        **- Name:** {emoji.name}
        **- Id:** {emoji.id}
        **- URL:** [Link To Emoji]{emoji.url}
        **- Author:** {emoji.user.mention}
        **- Time Created:** {creation_time}
        **- Useable by:** {can_use_emoji}

        **Other:**
        **- Animated:** {is_animated}
        **- Managed:** {is_managed}
        **- Requires Colons:** {requires_colons}
        **- Guild Name:** {emoji.guild.name}
        **- Guild ID:** {emoji.guild.id}
        """

        embed = discord.Embed(
            title=f"**Emoji Information for:** `{emoji.name}`",
            description = description,
            colour=0xadd8e6
        )
        embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(EmojiInfo(client))
