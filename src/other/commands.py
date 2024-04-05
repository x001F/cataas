from aiogram.types import BotCommand
from src.bot import bot
import yaml


async def set_commands():
    with open('src/config/config.yaml', 'r') as f:
        existing_commands = yaml.load(f, yaml.FullLoader)['commands']
        order = existing_commands['order']

    commands = [
        BotCommand(command=command, description=existing_commands[command])
        for command in order
    ]

    await bot.set_my_commands(commands)
