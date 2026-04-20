import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import os
from datetime import datetime, timedelta

# hi guys 
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")

# 1
OWNER_ID = 1071330258172780594  # rawrs.zapto.org

intents = discord.Intents.default()
intents.message_content = False
bot = commands.Bot(command_prefix="!", intents=intents)

# 2
def user_install_command():
    def decorator(func):
        func = app_commands.allowed_installs(guilds=True, users=True)(func)
        func = app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)(func)
        return func
    return decorator

def owner_only():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.id == OWNER_ID
    return app_commands.check(predicate)

# 3 EV
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")
    print(f"   Bot ID: {bot.user.id}")
    await bot.tree.sync()
    print("   Slash commands synced globally.")

# 4 EH
@bot.tree.error
async def on_application_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("❌ This command is only for the bot owner.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)
        raise error

# 5 Cmds
@bot.tree.command(name="ping", description="Check bot latency")
@user_install_command()
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! `{latency}ms`")

@bot.tree.command(name="roll", description="Roll a dice (e.g., /roll 20)")
@user_install_command()
async def roll(interaction: discord.Interaction, sides: int = 6):
    result = random.randint(1, sides)
    await interaction.response.send_message(f"🎲 {interaction.user.mention} rolled a **{result}** (1-{sides})")

@bot.tree.command(name="choose", description="Choose between options")
@user_install_command()
async def choose(interaction: discord.Interaction, options: str):
    choices = [opt.strip() for opt in options.split(",") if opt.strip()]
    if not choices:
        await interaction.response.send_message("❌ Please provide valid options separated by commas.", ephemeral=True)
        return
    chosen = random.choice(choices)
    await interaction.response.send_message(f"🤔 I choose: **{chosen}**")

@bot.tree.command(name="8ball", description="Ask the magic 8-ball a question")
@user_install_command()
async def eight_ball(interaction: discord.Interaction, question: str):
    answers = [
        "Yes.", "No.", "Maybe.", "Definitely!", "Absolutely not.",
        "Ask again later.", "The future is hazy.", "Without a doubt.",
        "My sources say no.", "Outlook good.", "Very doubtful."
    ]
    await interaction.response.send_message(f"🎱 Question: {question}\nAnswer: **{random.choice(answers)}**")

# 6 Etc
@bot.tree.command(name="remindme", description="Set a reminder (in seconds)")
@user_install_command()
async def remindme(interaction: discord.Interaction, seconds: int, message: str = "Time's up!"):
    if seconds <= 0:
        await interaction.response.send_message("❌ Seconds must be positive.", ephemeral=True)
        return
    await interaction.response.send_message(f"⏰ I'll remind you in {seconds} seconds: *{message}*", ephemeral=True)
    await asyncio.sleep(seconds)
    try:
        await interaction.followup.send(f"🔔 Reminder for {interaction.user.mention}: {message}")
    except:
        await interaction.user.send(f"🔔 Reminder: {message}")

# 67
@bot.tree.command(name="say", description="Make Mr. Sandman say something | DEV")
@user_install_command()
@owner_only()
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("✅ Message sent.", ephemeral=True)
    await interaction.channel.send(message)

# 8
@bot.tree.command(name="incognito", description="Send a message anonymously (owner only)")
@user_install_command()
@owner_only()
async def incognito(interaction: discord.Interaction, message: str):
    # Only the person sees the confirmation fr
    await interaction.response.send_message("🕵️ Message sent incognito.", ephemeral=True)
    # Public message appears as if from the bot without revealing who triggered it
    await interaction.channel.send(f"🤫 *{message}*")

# 9
@bot.tree.command(name="feedback", description="Send feedback to the bot owner")
@user_install_command()
async def feedback(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("✅ Thank you for your feedback!", ephemeral=True)
    owner = await bot.fetch_user(OWNER_ID)
    if owner:
        await owner.send(f"📬 Feedback from {interaction.user}:\n{message}")

# env
if __name__ == "__main__":
    bot.run(TOKEN)
