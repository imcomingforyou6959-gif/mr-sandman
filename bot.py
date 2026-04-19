import discord
from discord.ext import commands
import asyncio
import random
import os
from datetime import datetime

# ========== CONFIGURATION ==========
TOKEN = os.getenv("DISCORD_TOKEN")  # Read token from environment variable
if not TOKEN:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")

# Intents – only needed for slash commands
intents = discord.Intents.default()
intents.message_content = False

bot = commands.Bot(command_prefix="!", intents=intents)

# ========== EVENT: BOT READY ==========
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")
    print(f"   Bot ID: {bot.user.id}")
    print(f"   Invite URL: https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot+applications.commands")
    # Sync slash commands globally (can take up to 1 hour)
    await bot.tree.sync()
    print("   Slash commands synced globally.")

# ========== SLASH COMMANDS ==========

@bot.tree.command(name="hello", description="Says hello from Mr. Sandman")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"👋 Hello {interaction.user.mention}, I'm Mr. Sandman!")

@bot.tree.command(name="sandman", description="Mr. Sandman brings sleep to a user")
async def sandman(interaction: discord.Interaction, target: discord.Member = None):
    target = target or interaction.user
    responses = [
        f"😴 Mr. Sandman has put {target.mention} to sleep!",
        f"💤 Shh... {target.mention} is dreaming now.",
        f"🌙 Sleep tight, {target.mention}. Mr. Sandman is here.",
        f"🛌 {target.mention} has been visited by the Sandman. Goodnight!"
    ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="time", description="Shows the current time in UTC")
async def current_time(interaction: discord.Interaction):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    await interaction.response.send_message(f"🕒 Mr. Sandman's clock says: **{now}**")

@bot.tree.command(name="echo", description="Mr. Sandman repeats your message")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"🗣️ {interaction.user.mention} said: *{message}*")

@bot.tree.command(name="invite", description="Get the invite link to add Mr. Sandman to your server")
async def invite(interaction: discord.Interaction):
    invite_url = f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot+applications.commands"
    await interaction.response.send_message(f"🔗 Add Mr. Sandman to your server:\n{invite_url}")

# ========== ERROR HANDLER ==========
@bot.tree.error
async def on_application_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"⏳ Command on cooldown. Try again in {error.retry_after:.1f} seconds.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ An error occurred: {error}", ephemeral=True)
        raise error

# ========== RUN BOT ==========
if __name__ == "__main__":
    bot.run(TOKEN)
