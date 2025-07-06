from pydoc import describe

from aiogram.types import BotCommand, BotCommandScopeDefault
from config import bot

async def set_bot_commands():
    commands = [
        BotCommand(command='start', description='Начать'),
        BotCommand(command='vamp', description='Выпить кровь'),
        BotCommand(command='top', description='Вывести топ игроков'),
        BotCommand(command='bug', description='Сообщить о баге'),
        BotCommand(command='profile', description='Ваш профиль')
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
