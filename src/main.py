import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
from telemetry_loop import telemetry_loop, telemetry_cache

class Bot(commands.Bot):
    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

load_dotenv()

GUILD_ID = 881250112549027880

intents = discord.Intents.default()
intents.members=True
prefix = "/"
bot = Bot(command_prefix=prefix,
    help_command=None,
    intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print("Online")
    print(bot.user)
    activity = discord.Game(name="Made by Me88_88")
    await bot.change_presence(
        status=discord.Status.online, 
        activity=activity
    )
    if not hasattr(bot, "telemetry_task"):
        bot.loop.create_task(telemetry_loop())

@tree.command(
    name="ping",
    description="Replies with pong.",
    guild=discord.Object(id=GUILD_ID)
)
async def ping(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send("Pong!")


@tree.command(
    name="serverinfo",
    description="Displays server info.",
    guild=discord.Object(id=GUILD_ID)
)
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
    embed.add_field(name="Owner", value=guild.owner or "Unknown")
    embed.add_field(name="Member Count", value=guild.member_count)
    embed.add_field(
        name="Created At",
        value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )

    await interaction.response.send_message(embed=embed)

@tree.command(name="f1", description="F1 telemetry command.")
@app_commands.choices(type_=[
    app_commands.Choice(name="Driver", value="driver")
])
async def f1(interaction: discord.Interaction, type_: app_commands.Choice[str], driver: str, race: str = None):
    await interaction.response.defer(ephemeral=True)
    type_ = type_.value.lower()
    driver = driver.upper()

    if not telemetry_cache["session"]:
        return await interaction.followup.send(
            "Telemetry data not available yet. Please try again later."
        )

    if type_ == "driver":
        if driver not in telemetry_cache["drivers"]:
            return await interaction.followup.send(
                "Driver not found"
            )

        data = telemetry_cache["drivers"][driver]

        await interaction.followup.send(
            f"🏎️ **{driver}**\n"
            f"Laps: {data['laps']}\n"
            f"Last lap: {data['last_lap']}"
        )
    
bot_secret = os.getenv("BOT_TOKEN")

keep_alive()

bot.run(bot_secret)
