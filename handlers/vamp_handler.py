from socket import create_connection

import random
from datetime import datetime, timedelta
import sqlite3
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import DATABASE_NAME

vamp_router = Router()


async def vamp(message, user_tg_id, conn):
    """Логика выполнения команды /vamp."""
    a = random.randint(0, 5)
    cur = conn.cursor()
    cur.execute("UPDATE users SET ttl_tryes = ttl_tryes + 1 WHERE tg = ?", (user_tg_id,))
    cur.execute("UPDATE users SET tryes_lmt = tryes_lmt + 1 WHERE tg = ?", (user_tg_id,))
    conn.commit()

    if a == 5:
        print(a, 102)
        await message.answer('❌🔥Неудача! Вы нарвались на хамон-юзера, который обессилил вас. Вы не сможете '
                             'пить кровь следующие 3 часа')
        current_time = datetime.now()
        cur.execute("UPDATE users SET vamp_cd = ? WHERE tg = ?", (current_time, user_tg_id,))
        cur.execute("UPDATE users SET ttl_hamon = ttl_hamon + 1 WHERE tg = ?", (user_tg_id,))
        conn.commit()

    else:
        print(a, 103)
        x = random.randint(1, 3)
        cur.execute("SELECT ttl_blood_today, ttl_blood FROM users WHERE tg = ?", (user_tg_id,))
        result = cur.fetchall()
        blood = result[0][0] + x
        ttl_blood = result[0][1] + x
        cur.execute("UPDATE users SET ttl_blood_today = ?, ttl_blood = ? WHERE tg = ?", (blood, ttl_blood, user_tg_id,))
        conn.commit()
        await message.answer(
            f'✅🩸Успех! Вы выпили кровь случайного прохожего и пополнини сегодняшний запас крови на {x} л.')
        cur.execute("UPDATE users SET ttl_human = ttl_human + 1 WHERE tg = ?", (user_tg_id,))
        conn.commit()


@vamp_router.message(Command("vamp"))
async def vamp_handler(message: Message) -> None:
    """Обработчик команды /vamp."""
    user_tg_id = message.from_user.id


    with sqlite3.connect('vampdata.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE tg = ?', (user_tg_id,))
        user = cur.fetchone()

        if user:
            vamp_cd = user[1]
            tryes_lmt = user[5]

            if vamp_cd or tryes_lmt >= 4:

                if vamp_cd:

                    remaining = datetime.now() - vamp_cd

                    if remaining >= timedelta(hours=3):
                        cur.execute("UPDATE users SET vamp_cd = NULL WHERE tg = ?", (user_tg_id,))
                        conn.commit()

                    else:
                        time_difference = timedelta(hours=3) - remaining
                        total_seconds = int(time_difference.total_seconds())
                        hours, remainder = divmod(total_seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        await message.answer(
                            f"❌🕓 Пока нельзя. Ты обессилен, подожди еще {hours}ч {minutes}м {seconds}с")
                        return

                elif tryes_lmt:
                    cur.execute("SELECT ttl_blood_today FROM users WHERE tg = ?", (user_tg_id,))
                    ttl_blood_today = cur.fetchall()
                    ttl_blood_today = ttl_blood_today[0][0]
                    await message.answer(
                        f'❌🕓Ты уже исчерпал свои попытки на сегодня. Попробуй снова завтра. \nЗа сегодня ты выпил {ttl_blood_today} л. крови.')
                    return
            else:
                await vamp(message, user_tg_id, conn)
        else:
            cur.execute(
                "INSERT INTO users (tg, vamp_cd, ttl_blood_today, ttl_human, ttl_hamon, ttl_tryes, tryes_lmt, ttl_blood) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_tg_id, None, 0, 0, 0, 0, None, 0))
            conn.commit()
            await vamp(message, user_tg_id, conn)
