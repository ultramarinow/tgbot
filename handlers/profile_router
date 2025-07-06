import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from config import DATABASE_NAME

profile_router = Router()

@profile_router.message(Command("profile"))
async def profile_handler(message: types.Message) -> None:
    """Обработчик команды /profile."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        user_tg_id = message.from_user.id
        cur = conn.cursor()
        cur.execute("SELECT ttl_hamon, ttl_human, ttl_blood, ttl_tryes FROM users WHERE tg = ?", (user_tg_id,))
        result = cur.fetchone()
        if result:
            ttl_hamon = result[0]
            ttl_human = result[1]
            ttl_blood = result[2]
            ttl_tryes = result[3]
            if ttl_tryes and ttl_human != None:
                human_rate = ttl_human / ttl_tryes
                human_rate = int(human_rate * 100)
                await message.answer(f"Конечно! Вот ваш профиль. "
                                      "\n========================"
                                      f"\n「{ttl_hamon}」| Количество хамон-юзеров"
                                      f"\n「{ttl_human}」| Количество людей"
                                      f"\n「{ttl_blood}」| Количество выпитой крови"
                                      f"\n「{ttl_tryes}」| Количество попыток"
                                      f"\n「{human_rate}%」| Процент людей")
            else:
                ttl_hamon = 0 if ttl_hamon is None else ttl_hamon
                ttl_human = 0 if ttl_human is None else ttl_human
                ttl_blood = 0 if ttl_blood is None else ttl_blood
                ttl_tryes = 0 if ttl_tryes is None else ttl_tryes
                await message.answer(f"Конечно! Вот ваш профиль. "
                                      "\n========================"
                                      f"\n「{ttl_hamon}」| Количество хамон-юзеров"
                                      f"\n「{ttl_human}」| Количество людей"
                                      f"\n「{ttl_blood}」| Количество выпитой крови"
                                      f"\n「{ttl_tryes}」| Количество попыток"
                                      f"\n「{0}%」| Процент людей")
        elif result == None:
            await message.answer("Ой! На вас еще нет статистики.")
