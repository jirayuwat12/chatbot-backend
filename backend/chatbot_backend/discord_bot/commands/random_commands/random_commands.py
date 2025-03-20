import random

import discord

from ..base_commands import BaseCommands
from .constants import CHOICES_REGEX, RANGE_REGEX, RANGE_SEPERATORS


class RandomCommands(BaseCommands):
    def is_valid_command(self, command: str) -> bool:
        """
        Checks if the given command is a valid random command.

        :param command: The command to check.
        :type command: str
        :return: True if the command is a valid random command, False otherwise.
        :rtype: bool
        """
        return "random" in command.lower()

    async def process_command(self, command: str, message: discord.Message) -> None:
        """
        Processes the given random command and sends a random number between 1 and 100 to the message.

        :param command: The command to process.
        :type command: str
        :param message: The message that triggered the command.
        :type message: discord.Message
        """
        processed_command = command.replace("random", "").strip()
        if RANGE_REGEX.match(processed_command):
            # Get the range of numbers
            match = RANGE_REGEX.match(processed_command)
            # Check if the match is valid and has 3 groups
            if match and len(match.groups()) == 3:
                start = int(match.group(1))
                end = int(match.group(3))
                # Check if the range is valid
                if start > end:
                    await message.channel.send("Invalid range. The beginning of the range must be less than the end.")
                    return
                # Generate a random number between the range and send it to the channel
                random_number = random.randint(start, end)
                await message.channel.send(f"Random number between {start} and {end}: `{random_number}`")
        elif CHOICES_REGEX.match(processed_command):
            # Get the choices
            choices = []
            match = CHOICES_REGEX.match(processed_command)
            while match:
                choices.append(match.group(1))
                match = CHOICES_REGEX.match(processed_command, match.end())
            # Choose a random choice from the list of choices and send it to the channel
            choice = random.choice(choices)
            await message.channel.send(f"Random choice: `{choice}`")
        else:
            # Not in any case of random command
            await message.channel.send(
                "Invalid random command. Please use the format `random <range>` or `random <choice1>, <choice2>, ...`"
            )

    def __str__(self) -> str:
        range_seperators = '", "'.join(RANGE_SEPERATORS)
        random_range_helper = f'  - `random <beginning> <sep> <end>`, where `<sep>` is one of the "{range_seperators}"'

        random_choice_helper = "  - `random <choice1>, <choice2>, ...`"
        return "\n".join(
            [
                "Random commands",
                random_range_helper,
                random_choice_helper,
            ]
        )
