from mailbox import Message
from os import getenv
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
import random
from datetime import datetime, timedelta, time
import sqlite3
from aiogram import Dispatcher
from aiogram.filters import CommandStart

TOKEN = getenv('7414654605:AAHSv2FMzoy1DXMJn3cbu5fxD9HypewkqeY')


print('START')
user_dict = {}
dp = Dispatcher()
vamp_router = Router()
bot = Bot(token='7414654605:AAHSv2FMzoy1DXMJn3cbu5fxD9HypewkqeY')
profile_router = Router()
bug_router = Router()
top_router = Router()


async def vamp(message, user_tg_id, conn):
    a = random.randint(0, 5)
    cur = conn.cursor()
    cur.execute("UPDATE users SET ttl_tryes = ttl_tryes + 1 WHERE tg = ?", (user_tg_id,))
    cur.execute("UPDATE users SET tryes_lmt = tryes_lmt + 1 WHERE tg = ?", (user_tg_id,))
    conn.commit()

    if a == 5:
        await message.answer('❌🔥Неудача! Вы нарвались на хамон-юзера, который обессилил вас. Вы не сможете '
                             'пить кровь следующие 3 часа')
        current_time = datetime.now()
        cur.execute("UPDATE users SET vamp_cd = ? WHERE tg = ?", (current_time, user_tg_id,))
        cur.execute("UPDATE users SET ttl_hamon = ttl_hamon + 1 WHERE tg = ?", (user_tg_id,))
        conn.commit()

    else:
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


with sqlite3.connect('vampdata17.db') as conn:
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg INTEGER,
                vamp_cd DATETIME,
                ttl_blood_today INTEGER,
                ttl_human INTEGER,
                ttl_hamon INTEGER,
                ttl_tryes INTEGER,
                tryes_lmt INTEGER,
                ttl_blood INTEGER
                )
                """)
    conn.commit()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer('Привет, я Дио. Да-да, сам автор этого бота - тот самый вампир! \nПока я буду'
                                      'только отвечать на твои Дио соло и не соло, а также буду подсчитывать то, сколько'
                                      ' ты выпил крови, только остерегайся хамон юзеров! В том числе я планирую добавить'
                                      ' в бота возможность коллекционирования карточек и карманную вселенную ДжоДжо, в '
                                      'которой ты сможешь стать героем знаменитого аниме, и да, не только Дио, я не буду '
                                      'обижаться на тебя, если ты пойдешь по пути Джостаров, при этом ты сможешь стать '
                                      'даже Дьяволо. Буду благодарен, если ты добавишь бота в какой-либо чат. \nЧтобы выпить'
                                      ' кровь, напиши /vamp, на день у тебя есть четыре попытки. \nВ будущем тут будет '
                                      'больше команд! Можешь также сказать Дио соло или Дио не соло.')


async def set_commands():
    commands = [BotCommand(command='vamp', description='Выпить кровь'),
                BotCommand(command='top', description='Вывести топ игроков'),
                BotCommand(command='bug', description='Сообщить о баге')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


@vamp_router.message(Command("vamp"))
async def vamp_handler(message: Message) -> None:
    user_tg_id = message.from_user.id

    with sqlite3.connect('vampdata17.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE tg = ?', (user_tg_id,))
        user = cur.fetchone()

        if user:
            vamp_cd = user[2]
            tryes_lmt = user[6]

            if vamp_cd or tryes_lmt >= 4:

                if vamp_cd:
                    remaining = datetime.now() - datetime.strptime(vamp_cd, '%Y-%m-%d %H:%M:%S.%f')

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
                    await message.answer(f'❌🕓Ты уже исчерпал свои попытки на сегодня. Попробуй снова завтра. \nЗа сегодня ты выпил {ttl_blood_today} л. крови.')
                    return
            else:
                await vamp(message, user_tg_id, conn)
        else:
            cur.execute("INSERT INTO users (tg, vamp_cd, ttl_blood_today, ttl_human, ttl_hamon, ttl_tryes, tryes_lmt, ttl_blood) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_tg_id, None, 0, 0, 0, 0, None, 0))
            conn.commit()
            await vamp(message, user_tg_id, conn)


@profile_router.message(Command("profile"))
async def profile_handler(message: types.Message) -> None:
    with sqlite3.connect('vampdata17.db') as conn:
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


async def daily_reset(user_tg_id):
    with sqlite3.connect('vampdata17.db') as conn:
        cur = conn.cursor()
        current_time = datetime.now()
        cur.execute("SELECT day_cd FROM users WHERE user_tg_id = ?", (user_tg_id,))
        day_cd = cur.fetchall()
        day_cd = day_cd[0]
        current_time = current_time.strftime('%H:%M:%S')
        current_time = datetime.strptime(current_time, '%Y-%m-%d')
        day_cd = datetime.strptime(day_cd, '%Y-%m-%d')
        if current_time > day_cd:
            cur.execute("UPDATE users SET day_cd = 0 WHERE user_tg_id = ?", (user_tg_id,))
            conn.commit()


@bug_router.message(Command('bug'))
async def bug(message: Message) -> None:
    user_text = message.text.lower()
    if len(user_text) > 250:
        await message.answer('Вы написали слишком много. Обращение должно включать максимум до 250 символов.')
    else:
        user_text = user_text.replace("/bug ", "")
        try:
             await bot.send_message(1647244236, f'{user_text}')
             await message.answer("Обращение отправлено. Обратного ответа не ожидайте.")
        except Exception as e:
             await message.answer(f"Произошла ошибка при отправке сообщения разработчику: {e}")



@top_router.message(Command('top'))
async def top(message: Message) -> None:
    with sqlite3.connect('vampdata17.db') as conn:
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
            user_info = await bot.get_chat(user_tg_id)
            username = user_info.username if user_info.username else "Без ника"  # Проверка на наличие ника
            medal = medals[row] if row < len(medals) else ""
            final_message += f"{medal} {row + 1}. {username} - выпито крови: {ttl_blood} л., хамон-юзеров: {ttl_hamon}, жертв: {ttl_human}, попыток: {ttl_tryes}\n"
        await message.answer(final_message)


async def main() -> None:
    dp.include_router(vamp_router)
    dp.include_router(profile_router)
    dp.include_router(bug_router)
    dp.include_router(top_router)
    await dp.start_polling(bot, skip_updates=True)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
