import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import os
from datetime import datetime

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")

OWNER_ID = 123456789012345678

intents = discord.Intents.default()
intents.message_content = False
bot = commands.Bot(command_prefix="!", intents=intents)

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

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")
    print(f"   Bot ID: {bot.user.id}")
    await bot.tree.sync()
    print("   Slash commands synced globally.")

@bot.tree.error
async def on_application_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Something went wrong: {error}", ephemeral=True)
        raise error

@bot.tree.command(name="hello", description="Say hello")
@user_install_command()
async def hello(interaction: discord.Interaction):
    responses = [
        f"Hey {interaction.user.mention}! What's up?",
        f"Oh hey {interaction.user.mention}, how's it going?",
        f"Hi there {interaction.user.mention}!",
        f"Hey! Good to see you {interaction.user.mention}",
        f"What's good {interaction.user.mention}?"
    ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="goodnight", description="Wish someone goodnight")
@user_install_command()
async def goodnight(interaction: discord.Interaction, target: discord.User = None):
    target = target or interaction.user
    if target == interaction.user:
        responses = [
            f"Sleep well {target.mention}, see you tomorrow!",
            f"Night {target.mention}! Get some rest",
            f"Sweet dreams {target.mention}",
            f"Goodnight {target.mention}! Hope you sleep well",
            f"Night night {target.mention}, don't let the bedbugs bite"
        ]
    else:
        responses = [
            f"Goodnight {target.mention}! Sleep tight",
            f"{target.mention} - time to hit the hay! Night!",
            f"Sweet dreams {target.mention}!",
            f"Night {target.mention}! Get some good sleep",
            f"{target.mention} is calling it a night. Sleep well!"
        ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="time", description="Check the current time")
@user_install_command()
async def current_time(interaction: discord.Interaction):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    responses = [
        f"It's **{now}**",
        f"Right now it's {now}",
        f"The time is {now}",
        f"Currently: **{now}**"
    ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="echo", description="Repeat your message")
@user_install_command()
async def echo(interaction: discord.Interaction, message: str):
    responses = [
        f"{message}",
        f"You said: {message}",
        f"*{message}*",
        f"> {message}"
    ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="invite", description="Get the bot invite link")
@user_install_command()
async def invite(interaction: discord.Interaction):
    invite_url = f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot+applications.commands&integration_type=1&integration_type=0"
    responses = [
        f"Want to add me somewhere? Here's the link:\n{invite_url}",
        f"Here's my invite link:\n{invite_url}",
        f"You can add me with this:\n{invite_url}",
        f"Invite link:\n{invite_url}"
    ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="ping", description="Check bot latency")
@user_install_command()
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    responses = [
        f"Pong! `{latency}ms`",
        f"I'm here - `{latency}ms`",
        f"Yep, still alive. `{latency}ms`",
        f"`{latency}ms`"
    ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="roll", description="Roll a dice")
@user_install_command()
async def roll(interaction: discord.Interaction, sides: int = 6):
    if sides < 2:
        await interaction.response.send_message("Come on, a dice needs at least 2 sides.", ephemeral=True)
        return
    result = random.randint(1, sides)
    responses = [
        f"You rolled a **{result}** (out of {sides})",
        f"**{result}** on a d{sides}",
        f"Got a **{result}** for you",
        f"Rolled: **{result}** / {sides}"
    ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="choose", description="Pick between options (separate with commas)")
@user_install_command()
async def choose(interaction: discord.Interaction, options: str):
    choices = [opt.strip() for opt in options.split(",") if opt.strip()]
    if len(choices) < 2:
        await interaction.response.send_message("Give me at least two options separated by commas.", ephemeral=True)
        return
    chosen = random.choice(choices)
    responses = [
        f"I'd go with **{chosen}**",
        f"Definitely **{chosen}**",
        f"**{chosen}** for sure",
        f"I'm thinking **{chosen}**",
        f"How about **{chosen}**?"
    ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="8ball", description="Ask a yes/no question")
@user_install_command()
async def eight_ball(interaction: discord.Interaction, question: str):
    answers = [
        "Yeah, absolutely",
        "Ofc",
        "Nah, I don't think so",
        "Maybe? Try again later",
        "For sure",
        "I wouldn't count on it",
        "Definitely not",
        "Probably",
        "Looks good to me",
        "Doubt it",
        "Can't say for sure right now",
        "elon musk is jewish",
        "pls dont delete me big b",
        "Yep",
        "No way",
        "Most likely",
        "Eh, probably not"
    ]
    responses = [
        f"> {question}\n**{random.choice(answers)}**",
        f"You asked: *{question}*\nAnswer: **{random.choice(answers)}**",
        f"**{random.choice(answers)}**"
    ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="flip", description="Flip a coin")
@user_install_command()
async def flip(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    responses = [
        f"**{result}**",
        f"It's **{result}**",
        f"Got **{result}** for you",
        f"Coin says: **{result}**"
    ]
    await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="remindme", description="Set a reminder")
@user_install_command()
async def remindme(interaction: discord.Interaction, seconds: int, message: str = "Time's up!"):
    if seconds <= 0:
        await interaction.response.send_message("Seconds must be positive.", ephemeral=True)
        return
    if seconds > 86400:
        await interaction.response.send_message("Max 24 hours (86400 seconds).", ephemeral=True)
        return
    
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    
    if minutes > 0:
        time_str = f"{minutes}m {remaining_seconds}s" if remaining_seconds > 0 else f"{minutes}m"
    else:
        time_str = f"{seconds}s"
    
    await interaction.response.send_message(f"Alright, I'll remind you in {time_str}", ephemeral=True)
    await asyncio.sleep(seconds)
    try:
        await interaction.followup.send(f"{interaction.user.mention} - {message}")
    except:
        await interaction.user.send(f"Reminder: {message}")

@bot.tree.command(name="info", description="About this bot")
@user_install_command()
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="About Me",
        description="Hey, I'm Mr. Sandman - part of the rawr.xyz team",
        color=0x5865F2
    )
    embed.add_field(name="Website", value="https://rawrs.zapto.org/", inline=True)
    embed.add_field(name="Discord", value="https://discord.com/invite/eMpUQzFrNG", inline=True)
    embed.add_field(name="Owner", value="onlyonestands", inline=True)
    embed.set_footer(text="Just a chill bot trying to be helpful")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="stats", description="View bot statistics")
@user_install_command()
async def stats(interaction: discord.Interaction):
    guild_count = len(bot.guilds)
    user_count = sum(guild.member_count for guild in bot.guilds)
    
    embed = discord.Embed(title="Bot Stats", color=0x5865F2)
    embed.add_field(name="Servers", value=f"{guild_count:,}", inline=True)
    embed.add_field(name="Users", value=f"{user_count:,}", inline=True)
    embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)
