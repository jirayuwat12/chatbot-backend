import discord
from ..configs import CommandProcessorConfig


class CommandProcessor:
    def __init__(self, config: CommandProcessorConfig | None = None) -> None:
        """
        Initializes the command processor with the given configuration.

        :param config: The configuration for the command processor.
        :type config: CommandProcessorConfig (optional)
        """
        self.config = config or CommandProcessorConfig()

    def process_command(self, command: str, message: discord.Message) -> None:
        pass
