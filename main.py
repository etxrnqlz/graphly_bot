import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents().default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    print("bot is online")

client.load_extension("cogs.member_count")
print("loaded cogs")

client.run(os.getenv('TOKEN'))
