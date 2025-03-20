from abc import ABC, abstractmethod

import discord


class BaseCommands(ABC):
    @abstractmethod
    def is_valid_command(self, command: str) -> bool:
        """
        Checks if the given command is a valid command for this command object.
        """
        pass

    @abstractmethod
    async def process_command(self, command: str, message: discord.Message) -> None:
        """
        Processes the given command and sends a response to the message.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representation of the command object.
        """
        pass
