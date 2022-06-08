import json
from aiogram.utils.markdown import hbold, hlink
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from main import get_data
from asyncio import sleep

bot = Bot(token="токен", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_button = ['Flutter developer (без опыта)', 'Flutter developer (с опытом работы)']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals="Flutter developer (без опыта)"))
async def get_flutter_developer(message: types.Message):
    await message.answer('Идет загрузка...')

    get_data(experience="noExperience")

    with open('vacancies.json', encoding='utf-8') as file:
        data_vacancies = json.load(file)

    with open('data/result.json', encoding='utf-8') as file:
        data_result = json.load(file)
        for index, item in enumerate(data_result):
            link = f'{hlink(title=item.get("Должность"), url=data_vacancies[index]["link"])}'
            description = "\n".join(item.get("Описание"))
            requirements = ",\n".join(item.get("Требования"))
            skills = "\n".join(item.get("Ключевые навыки"))

            card = f"{link} \n" \
                   f'\n{hbold("Компания: ")}{item.get("Компания")}\n' \
                   f'\n{hbold("Требования:")}\n{requirements}\n' \
                   f'\n{hbold("З/П:")}\n{item.get("З/П")}\n' \
                   f'\n{hbold("Город:")}\n{item.get("Город")}\n' \
                   f'\n{hbold("Описание:")}\n{description}\n' \
                   f'\n{hbold("Ключевые навыки:")}\n{skills}'

            if index % 20 == 0:
                await sleep(3)

            await message.answer(card, parse_mode=types.ParseMode.HTML)


@dp.message_handler(Text(equals="Flutter developer (с опытом работы)"))
async def get_flutter_developer(message: types.Message):
    await message.answer('Идет загрузка...')

    get_data(experience="between1And3")

    with open('vacancies.json', encoding='utf-8') as file:
        data_vacancies = json.load(file)

    with open('data/result.json', encoding='utf-8') as file:
        data_result = json.load(file)
        for index, item in enumerate(data_result):
            link = f'{hlink(title=item.get("Должность"), url=data_vacancies[index]["link"])}'
            description = "\n".join(item.get("Описание"))
            requirements = ",\n".join(item.get("Требования"))
            skills = "\n".join(item.get("Ключевые навыки"))

            card = f"{link} \n" \
                   f'\n{hbold("Компания: ")}{item.get("Компания")}\n' \
                   f'\n{hbold("Требования:")}\n{requirements}\n' \
                   f'\n{hbold("З/П:")}\n{item.get("З/П")}\n' \
                   f'\n{hbold("Город:")}\n{item.get("Город")}\n' \
                   f'\n{hbold("Описание:")}\n{description}\n' \
                   f'\n{hbold("Ключевые навыки:")}\n{skills}'

            if index % 20 == 0:
                await sleep(3)

            await message.answer(card, parse_mode=types.ParseMode.HTML)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
