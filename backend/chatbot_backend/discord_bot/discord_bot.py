import os

import discord
from dotenv import load_dotenv

from .constants import HOW_TO_USE_BOT_COMMAND, HOW_TO_USE_BOT_MESSAGE, TO_USE_BOT_KEYWORDS
from .commands import CommandProcessor

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Create a Discord client
intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)

# Create a command processor
command_processor = CommandProcessor()

# Define the on_ready event
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


# Define the on_message event
@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return
    print(f"Message from {message.author}: {message.content}")
    # Respond to the message if it matches the help command
    if message.content == HOW_TO_USE_BOT_COMMAND:
        print(f"Sending help message to {message.author}")
        await message.channel.send(HOW_TO_USE_BOT_MESSAGE + "\n" + f"<@{message.author.id}>")
    # Respond to the message if it starts with one of the bot keywords
    message_content = message.content.lower()
    if message_content.startswith(tuple(TO_USE_BOT_KEYWORDS)):
        # Format command
        formatted_command = message_content
        for keyword in TO_USE_BOT_KEYWORDS:
            formatted_command = formatted_command.replace(keyword, "")
        formatted_command = formatted_command.strip(" ,.:")

        # Send command to the command processor
        print(f"Responding to message from {message.author}: {formatted_command}")
        command_processor.process_command(formatted_command, message)
