# AoC-Leaderboard

A simple discord bot to track a [Advent of Code](https://adventofcode.com/) leaderboard in your server.

## Features

- Updates the leaderboard every half hour.
- Displays the leaderboard neatly in a discord channel.
- Configurable via environment variables.

## Setup

1. Create your own Discord bot and get the token from
   the [Discord Developer Portal](https://discord.com/developers/applications).
2. Invite the bot to your server with the appropriate permissions.
3. Clone this repository to your local machine or better a always running server.
4. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy the example.env file and fill in your bot token and the public leaderboard url to your leaderboard:
   ```bash
   cp example.env .env
   ```
6. Run the bot:

- Through the script (needs screen installed):
    ```bash
    ./startDetatched.sh
    ```
- Directly with python:
    ```bash
    python3 bot.py
    ```