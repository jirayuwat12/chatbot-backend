import discord

from ..configs import CommandProcessorConfig
from .base_commands import BaseCommands
from .random_commands import RandomCommands


class CommandProcessor:
    def __init__(self, config: CommandProcessorConfig | None = None) -> None:
        """
        Initializes the command processor with the given configuration.

        :param config: The configuration for the command processor.
        :type config: CommandProcessorConfig (optional)
        """
        self.config = config or CommandProcessorConfig()
        # TODO: Create a list of commands to register and load from the list instead of hardcoding
        self.register_command(RandomCommands())

    def register_command(self, command: BaseCommands) -> None:
        """
        Registers a command with the command processor.

        :param command: The command to register.
        :type command: BaseCommand
        """
        self.config.commands.append(command)

    async def process_command(self, command: str, message: discord.Message) -> None:
        """
        Processes the given command and sends a response to the message.

        :param command: The command to process.
        :type command: str
        :param message: The message that triggered the command.
        :type message: discord.Message
        """
        # Iterate over all registered commands and find the first one that matches
        for command_obj in self.config.commands:
            if command_obj.is_valid_command(command):
                await command_obj.process_command(command, message)
                return
        # If no command matches, send an error message
        if "help" not in command:
            error_message = "Invalid command, Please use the `help` command to see the available commands."
            await message.channel.send(error_message)
        elif "help" in command:
            error_message = "Here are the available commands:\n"
            for command_obj in self.config.commands:
                error_message += f"- {str(command_obj)}\n"
            error_message = error_message.strip()
            await message.channel.send(error_message)
