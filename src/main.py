import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
prefix = "/"
bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)
bot.author_id = 729290819151855698

@bot.event
async def on_ready():
    print("Online")
    print(bot.user)
    activity = discord.Game(name="Made by Me88_88", type=1)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command("server_info")
async def serverinfo(ctx):
    icon_url = guild.icon.url if guild.icon else None
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} Server Information", color=discord.Color.blue())
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="Server Name", value=guild.name, inline=True)
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Owner", value=guild.owner, inline=True)
    embed.add_field(name="Region", value=guild.region, inline=True)
    embed.add_field(name="Member Count", value=guild.member_count, inline=True)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    await ctx.send(embed=embed)
    
bot_secret = os.getenv("BOT_TOKEN")
bot.run(bot_secret)