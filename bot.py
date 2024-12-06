import datetime
import os
from dotenv import load_dotenv

import discord
from discord.ext import tasks, commands

import helpers

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AOC_SESSION = os.getenv('AOC_COOKIE')
AOC_USERID = os.getenv('AOC_USERID')

aocLeaderboardURL = f'https://adventofcode.com/2024/leaderboard/private/view/{AOC_USERID}.json'
channelName = 'Advent of Code'

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

userId = '3701859'
helpers.getLeaderboard(f"https://adventofcode.com/2024/leaderboard/private/view/{userId}.json", AOC_SESSION)
aocChannel: discord.TextChannel = None
leaderboardMessage: discord.Message = None

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


def print_leaderboard():
    members = helpers.getLeaderboard(aocLeaderboardURL, AOC_SESSION)
    message = ""

    for member in members:
        message += f"{member['name']}: {member['stars']}\n"
    return message


def get_aoc_channel(category: discord.CategoryChannel):
    for channel in category.channels:
        if channel.name == channelName:
            return channel
    return None


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@tasks.loop(minutes=5.0)
async def update_leaderboard_timed():
    print('Running update')
    await update_leaderboard(None)


@bot.command("updateLeaderboard")
async def update_leaderboard(ctx):
    if leaderboardMessage is not None:
        message = f"{print_leaderboard()}\nLast updated: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}"
        print(message)
        await leaderboardMessage.edit(content=message)
        print("Updated Leaderboard\n")


@bot.command("addLeaderboard")
async def add_leaderboard(ctx: discord.Message):
    print('Create Channel')
    category = ctx.guild.categories[0]
    global aocChannel
    aocChannel = get_aoc_channel(category)

    if aocChannel is None:
        aocChannel = await ctx.guild.create_text_channel(channelName, category=category)

    message = print_leaderboard()
    global leaderboardMessage
    leaderboardMessage = await aocChannel.send(message)
    update_leaderboard_timed.start()


bot.run(TOKEN)
