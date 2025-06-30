import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from config import bot, DATABASE_NAME

top_router = Router()

@top_router.message(Command('top'))
async def top(message: types.Message) -> None:
    """Обработчик команды /top."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT tg, ttl_blood, ttl_tryes, ttl_human, ttl_hamon FROM users ORDER BY ttl_blood DESC")
        result = cur.fetchall()
        final_message = "Конечно! Вот топ-15 вампиров:\n"  # Инициализируем сообщение вне цикла
        medals = ["🥇", "🥈", "🥉"]
        for row in range(min(len(result), 15)):  # Ограничиваем до 15 элементов
            user_tg_id = result[row][0]
            ttl_blood = result[row][1]
            ttl_tryes = result[row][2]
            ttl_human = result[row][3]
            ttl_hamon = result[row][4]
            try:
                user_info = await bot.get_chat(user_tg_id)
                username = user_info.username if user_info.username else "Без ника"  # Проверка на наличие ника
            except Exception as e:
                username = "Неизвестный пользователь"
                print(f"Ошибка при получении информации о пользователе {user_tg_id}: {e}")

            medal = medals[row] if row < len(medals) else ""
            final_message += f"{medal} {row + 1}. {username} - выпито крови: {ttl_blood} л., хамон-юзеров: {ttl_hamon}, жертв: {ttl_human}, попыток: {ttl_tryes}\n"
        await message.answer(final_message)
