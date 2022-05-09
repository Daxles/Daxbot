import discord
from discord.ext import commands
from datetime import datetime
import asyncio 
import random

class Remind(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(aliases = ["remindme", "remind_me"], name="remind",description="The bot will remind whenever and for whatever you want")
    async def remind(self, ctx, time, *, task):
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
        
        
        converted_time = convert(time)

        if converted_time == 1:
            await ctx.send("You didn't answer the time correctly")
        if converted_time == -2:
            await ctx.send("The time must a integer")
            return
        await ctx.send(f"I will remind you in **{time}** for **{task}**")
        await asyncio.sleep(converted_time)
        await ctx.message.author.send(f"{ctx.author.mention} your reminder for **{task}** has finished")
    


def setup(client):
    client.add_cog(Remind(client))