from dataclasses import dataclass, field

from ..commands.base_commands import BaseCommands


@dataclass
class CommandProcessorConfig:
    commands: list[BaseCommands] = field(default_factory=list)
