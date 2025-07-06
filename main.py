import asyncio
import sqlite3

from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

import config
import database
from commands import set_bot_commands
from config import DATABASE_NAME
from handlers.vamp_handler import vamp_router
from handlers.profile_handler import profile_router
from handlers.bug_handler import bug_router
from handlers.top_handler import top_router


dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start."""
    await message.answer('Привет, я Дио. \n\nДа-да, сам автор этого бота - тот самый вампир! \n\nПока я буду '
                                      'только отвечать на твои Дио соло и не соло, а также буду подсчитывать то, сколько'
                                      ' ты выпил крови. Только остерегайся хамон юзеров!\n\nВ том числе я планирую добавить'
                                      ' в бота возможность коллекционирования карточек и карманную вселенную ДжоДжо, в '
                                      'которой ты сможешь стать героем знаменитого аниме, и да, не только Дио, я не буду '
                                      'обижаться на тебя, если ты пойдешь по пути Джостаров, при этом ты сможешь стать '
                                      'даже Дьяволо.\n\nБуду благодарен, если ты добавишь бота в какой-либо чат. \n\nЧтобы выпить'
                                      ' кровь - используй /vamp \nНа день у тебя есть четыре попытки.')

async def main() -> None:
    """Главная функция запуска бота."""
    dp.include_router(vamp_router)
    dp.include_router(profile_router)
    dp.include_router(bug_router)
    dp.include_router(top_router)

    #Создаем таблицы
    with sqlite3.connect(DATABASE_NAME) as conn:  # Получаем соединение из функции
        database.create_tables(conn)  # Передаем соединение в create_tables

    await set_bot_commands()
    await config.bot.delete_webhook(drop_pending_updates=True) #Удаляет старые обновления
    await dp.start_polling(config.bot, skip_updates=True) #Запускает бота


if __name__ == "__main__":
    print("Бот запускается...")
    asyncio.run(main())
