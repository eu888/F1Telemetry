import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

GUILD_ID = 1446539319140679813

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)
bot.author_id = 729290819151855698
tree = bot.tree
intents.message_content = True
prefix = "/"
@bot.event
async def on_ready():
    print("Online")
    print(bot.user)
    guild = discord.Object(id=GUILD_ID)
    await tree.sync(guild=guild)
    activity = discord.Game(name="Made by Me88_88", type=1)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@tree.command(name="ping", description="Replies with pong.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

async def serverinfo(interaction: discord.Interaction):

    guild = interaction.guild

    embed = discord.Embed(
        title=f"{guild.name} Server Information",
        color=discord.Color.blue()
    )

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(name="Server Name", value=guild.name)
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Owner", value=guild.owner)
    embed.add_field(name="Member Count", value=guild.member_count)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))

    await interaction.response.send_message(embed=embed)
    
bot_secret = os.getenv("BOT_TOKEN")

keep_alive()

bot.run(bot_secret)