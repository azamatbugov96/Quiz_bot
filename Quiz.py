import aiosqlite
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
import json

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '8323431024:AAHTcOuasXWq9zh5xcZPTV8L40GK0O0okac'

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Подключаем логику работы с базой данных
from db import get_quiz_index, update_quiz_index, get_user_score, update_user_score, create_table

# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'

# Правильно вызывать асинхронную функцию
DICT_DATA = 'data/quiz_data.json'
# Открываем файл quiz_data.json в режиме чтения с кодировкой utf-8
with open(DICT_DATA, 'r') as j:
     quiz_data = json.loads(j.read())

# Правильно вызывать асинхронную функцию
DICT_DATA = 'data/quiz_data.json'


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    builder.adjust(1)
    return builder.as_markup()


@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    await callback.message.answer("Верно!")
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_user_score(callback.from_user.id)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    # обновление количества правильных ответов
    current_score += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    await update_user_score(callback.from_user.id, current_score)


    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nВаш результат: {current_score} правильных ответов")
        await callback.answer(
        text="Спасибо, что воспользовались ботом!",
        show_alert=True
    )

@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_user_score(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    await update_user_score(callback.from_user.id, current_score)


    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nВаш результат: {current_score} правильных ответов")
        await callback.answer(
        text="Спасибо, что воспользовались ботом!",
        show_alert=True
    )

# Хэндлер на команду /start
@dp.message(Command("start"))
@dp.message(Command("help"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Help"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def get_question(message, user_id):

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    new_score = 0
    await update_quiz_index(user_id, current_question_index)
    await update_user_score(user_id, new_score)
    await get_question(message, user_id)


# Хэндлер на команду /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)

# Хэндлер для кнопки 'Help' и команды /help
@dp.message(F.text=="Help")
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("❗️ Цель квиза ❗️\n"
                        "Ваша задача — ответить на серию вопросов, демонстрируя свои знания.\n"
                        "Каждое верное решение приносит баллы, и в конце игры вы узнаете свой результат.\n Нажмите 'На quiz чтобы начать игру'  /quiz, чтобы начать.")
    await (message)


# Запуск процесса поллинга новых апдейтов
async def main():

    # Запускаем создание таблицы базы данных
    await create_table()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())