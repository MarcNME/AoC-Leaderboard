import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

import helpers

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AOC_SESSION = os.getenv('AOC_COOKIE')
AOC_USERID = os.getenv('AOC_USERID')

aocLeaderboardURL = f'https://adventofcode.com/2024/leaderboard/private/view/{AOC_USERID}.json'

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

userId= '3701859'
helpers.getLeaderboard(f"https://adventofcode.com/2024/leaderboard/private/view/{userId}.json", AOC_SESSION)
aocChannel = None

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

def printLeaderboard():
    members = helpers.getLeaderboard(aocLeaderboardURL, AOC_SESSION)
    message = ""

    for member in members:
        message += f"{member['name']}: {member['stars']}\n"
    return message

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def addLeaderboard(ctx: discord.Message):
    print('Create Channel')
    global aocChannel
    category = ctx.guild.categories[0]
    aocChannel = await ctx.guild.create_text_channel(f'Advent of Code', category=category)
    print(f'Pull leaderboard')
    
    message = printLeaderboard()
    await aocChannel.send(message)

@bot.command()
async def updateLeaderboard(ctx: discord.Message):
    message = printLeaderboard()
    await aocChannel.send(message)

bot.run(TOKEN)
