import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
prefix = "/"
bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)