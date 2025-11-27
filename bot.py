import datetime
import os

import discord
import requests
from discord.ext import tasks, commands
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AOC_SESSION = os.getenv('AOC_COOKIE')
AOC_USERID = os.getenv('AOC_USERID')

aocLeaderboardURL = f'https://adventofcode.com/2025/leaderboard/private/view/{AOC_USERID}.json'
channelName = 'advent-of-code'

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

aocChannel: discord.TextChannel = None
leaderboardMessage: discord.Message = None

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


def get_leaderboard(leaderboard_url: str, session: str):
    cookies = {'session': session}
    response = requests.get(leaderboard_url, cookies=cookies)

    if response.ok:
        members = list(response.json()['members'].values())
        members = sorted(members, key=lambda x: x['stars'], reverse=True)

        return members
    else:
        raise RuntimeError("Could not get Leaderboard")


def print_leaderboard():
    members = get_leaderboard(aocLeaderboardURL, AOC_SESSION)
    table = []

    for member in members:
        row = [member['name'], member['local_score']]

        for i in range(1, 26):
            if str(i) in member['completion_day_level']:
                if len(member['completion_day_level'][str(i)]) == 2:
                    row.append("🌕")
                elif len(member['completion_day_level'][str(i)]) == 1:
                    row.append("🌗")
                else:
                    row.append("?")
            else:
                row.append("🌑")

        table.append(row)
    return tabulate(table, tablefmt="plain")


def get_aoc_channel(category: discord.CategoryChannel):
    print("Channel names:")
    for channel in category.channels:
        print(channel.name)
        if channel.name == channelName:
            return channel
    print()
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
        message = f"```{print_leaderboard()}```\nLast updated: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}"
        print(message)
        await leaderboardMessage.edit(content=message)
        print("Updated Leaderboard\n")


@bot.command("addLeaderboard")
async def add_leaderboard(ctx: discord.Message):
    global aocChannel
    global leaderboardMessage
    print('Create Channel')
    category = ctx.guild.categories[0]
    aocChannel = get_aoc_channel(category)
    if aocChannel is None:
        aocChannel = await ctx.guild.create_text_channel(channelName, category=category)

    message = print_leaderboard()
    leaderboardMessage = await aocChannel.send(message)
    update_leaderboard_timed.start()


if __name__ == "__main__":
    bot.run(TOKEN)
