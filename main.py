from asyncio import Queue
import os
import discord
from discord.ext import commands
import json
import discordmongo 
import motor.motor_asyncio
import sys
import traceback
from discord import Intents
from discord.ext.commands import Bot
import datetime




async def get_prefix(client, message):
    if not message.guild:
        return commands.when_mentioned_or(client.DEFAULT_PREFIX)(client, message)

    try:
        data = await client.prefixes.find(message.guild.id)

        if not data or "prefix" not in data:
            
            return commands.when_mentioned_or(client.DEFAULT_PREFIX)(client, message)
        
        return commands.when_mentioned_or(data["prefix"])(client, message)
    except:
        
        return commands.when_mentioned_or(client.DEFAULT_PREFIX)(client, message)

intents = Intents.default()
intents.members = True
client = commands.Bot(command_prefix=get_prefix, help_command=None, intents=intents)
DEFAULTPREFIX = '.'
client.DEFAULTPREFIX = DEFAULTPREFIX


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print('Daxbot is ready!')
    servers = len(client.guilds)
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.watching,name = f'{servers} servers & {len(client.users)} members'))


@client.command(name="servers",description="Shows how many servers Daxbot is in.")
async def servers(ctx):
    servers = len(client.guilds)
    await ctx.send(f'I am in {servers} servers')


@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title='<:cross:956904380148371476> Error', description=f"{ctx.author.mention}, You don't have the permissions to do this.", color=0xCC1313)
        await ctx.send(embed=em)
    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title='<:cross:956904380148371476> Error', description=f"{ctx.author.mention}, You are missing arguments.", color=0xCC1313)
        await ctx.send(embed=em)
    else:
        raise error


with open("config.json", "r") as f:
  config = json.load(f)

client.mongo = motor.motor_asyncio.AsyncIOMotorClient("mongodb://yourusername:yourpassword@cluster0-shard-00-00.5tizg.mongodb.net:27017,cluster0-shard-00-01.5tizg.mongodb.net:27017,cluster0-shard-00-02.5tizg.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-w03ijv-shard-0&authSource=admin&retryWrites=true&w=majority")
client.db = client.mongo["example"]
client.DEFAULT_PREFIX = "."
client.prefixes = discordmongo.Mongo(connection_url=client.db, dbname="prefixes")



client.run(config["bot_token"])

