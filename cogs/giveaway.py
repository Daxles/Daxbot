import discord
from discord.ext import commands
import datetime
import asyncio 
import random

def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try: 
        val = int(time[:-1])
    except:
        return -2 
    
    return val * time_dict[unit]

class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


    @commands.command(name="giveaway",description="The bot will setup a giveaway for you!", aliases=["gstart"])
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx):
        
        await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")
        
        questions = ["Which channel should it be hosted in?",
                    "What should be the duration of the giveaway? (s|h|d|m)",
                    "What is the prize of the giveaway?"]

        answers = []
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        for i in questions:
            await ctx.send(i)
            
            try:
                msg = await self.client.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didn\'t answer in time, please be quicker next time!')
                return
            else:
                answers.append(msg.content)
                
        
        try: 
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
            return
        

        channel = self.client.get_channel(c_id)

        time = convert(answers[1])
        if time == -1:
            await ctx.send(f"You didn't answer the time with a proper unit. Use (s|h|d|m) next time!")
            return
        elif time== -2:
            await ctx.send(f"The time must be an integer. Please enter an integer next time!")
            return
        prize = answers[2]

        await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}")
        
            
        embed = discord.Embed(title="Giveaway!", description=f"{prize}", color=ctx.author.color)

        # end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60)

        embed.add_field(name="Hosted By:", value= ctx.author.mention)
        embed.set_footer(text=f"Ends {answers[1]} from now")

        my_msg = await channel.send(embed=embed)

        await my_msg.add_reaction("????")

        await asyncio.sleep(time)
        

        new_msg = await ctx.channel.fetch_message(my_msg.id)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)

        await ctx.send(f"Congratulations! {winner.mention} won {prize}")
        

    @commands.command(name="reroll",description="Rerolls the winner for the giveaway", aliases=["rr"])
    @commands.has_permissions(administrator=True)
    async def reroll(self, ctx, channel : discord.TextChannel, id_ : int):
        try:
            new_msg = await channel.fetch_message(id_)
        except:
            await ctx.send("The id was entered incorrectly")
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner= random.choice(users)

        await channel.send(f"Congratulations! The new winner is {winner.mention}.")

def setup(client):
    client.add_cog(Giveaway(client))