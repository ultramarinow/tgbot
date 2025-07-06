from aiogram import Router, types
from aiogram.filters import Command
from config import bot, ADMIN_ID

bug_router = Router()

@bug_router.message(Command('bug'))
async def bug(message: types.Message) -> None:
    """Обработчик команды /bug."""
    user_text = message.text.lower()
    if len(user_text) > 250:
        await message.answer('Вы написали слишком много. Обращение должно включать максимум до 250 символов.')
    else:
        user_text = user_text.replace("/bug ", "")
        try:
             await bot.send_message(ADMIN_ID, f'{user_text}')
             await message.answer("Обращение отправлено. Обратного ответа не ожидайте.")
        except Exception as e:
             await message.answer(f"Произошла ошибка при отправке сообщения разработчику: {e}")
