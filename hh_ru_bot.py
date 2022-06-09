import json
from aiogram.utils.markdown import hbold, hlink
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from main import get_data, get_all_page
from asyncio import sleep

bot = Bot(token="5453274016:AAELeT1GINLRcAliGEaqV4nrS4fm2QyLY7Q", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

count_page_without_experience = 0
pages_without_experience = get_all_page()

count_page_with_experience = 0
pages_with_experience = get_all_page(experience="between1And3")


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_button = ['Flutter developer (без опыта)', 'Flutter developer (с опытом работы)']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals="Flutter developer (без опыта)"))
async def get_flutter_developer(message: types.Message):
    global count_page_without_experience
    all_page = pages_without_experience[0]
    all_vacansies = pages_without_experience[1]

    if count_page_without_experience < all_page:
        if count_page_with_experience == 0:
            await message.answer(hbold(f"Найдено {all_vacansies} вакансий"))
        await message.answer(hbold(f"Идет загрузка {count_page_without_experience + 1} страницы ..."))

        get_data(experience="noExperience", page=count_page_without_experience)

        with open('vacancies.json', encoding='utf-8') as file:
            data_vacancies = json.load(file)

        with open('data/result.json', encoding='utf-8') as file:
            data_result = json.load(file)

        for index, item in enumerate(data_result):
            link = f'{hlink(title=data_vacancies[index]["vacancy"], url=data_vacancies[index]["link"])}'
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

            if index % 5 == 0:
                await sleep(2)

            await message.answer(card, parse_mode=types.ParseMode.HTML)

        count_page_without_experience += 1
    else:
        count_page_without_experience = 0
        the_end = hbold("Вакансий больше нет.")
        await message.answer(the_end)


@dp.message_handler(Text(equals="Flutter developer (с опытом работы)"))
async def get_flutter_developer(message: types.Message):
    global count_page_with_experience
    all_page = pages_with_experience[0]
    all_vacansies = pages_with_experience[1]

    if count_page_with_experience < all_page:
        if count_page_with_experience == 0:
            await message.answer(hbold(f"Найдено {all_vacansies} вакансий"))
        await message.answer(hbold(f"Идет загрузка {count_page_with_experience + 1} страницы ..."))

        get_data(experience="between1And3", page=count_page_with_experience)

        with open('vacancies.json', encoding='utf-8') as file:
            data_vacancies = json.load(file)

        with open('data/result.json', encoding='utf-8') as file:
            data_result = json.load(file)

        for index, item in enumerate(data_result):
            link = f'{hlink(title=data_vacancies[index]["vacancy"], url=data_vacancies[index]["link"])}'
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

            if index % 5 == 0:
                await sleep(2)

            await message.answer(card, parse_mode=types.ParseMode.HTML)

        count_page_with_experience += 1
    else:
        count_page_with_experience = 0
        the_end = hbold("Вакансий больше нет.")
        await message.answer(the_end)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
