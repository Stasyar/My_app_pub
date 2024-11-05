# -*- coding: utf-8 -*-
import json
from json import JSONDecodeError
import os
from urllib.parse import urlencode

from sqlalchemy.exc import ProgrammingError
from telebot.apihelper import ApiHTTPException, ApiTelegramException
from telebot.types import Message

from api.api_requests import requests_main, url_filter
from loader import bot
from database.requests import add_user_query
from keyboards.reply_kb import filter_markup


def filter_search(message: Message):
    """Функция считывает JSON файл с критериями поиска.
    Затем подгоняет их в правильный формат.
    Отправляет запрос API и формирует ответ пользователю."""

    try:
        with open("filter.json", "r", encoding="utf-8") as file:
            res = json.load(file)
    except JSONDecodeError as e:
        print("Ошибка декодирования JSON:", e)
        bot.send_message(message.chat.id, "Ошибка при чтении фильтров.")
        return

    params = dict()

    for elem in res:
        for key, value in elem.items():
            params[key] = value

    try:
        add_user_query(message.from_user.id, " ".join(v for k, v in params.items()))
    except ProgrammingError as e:
        print(e)

    print(params)

    if params:  # Проверка на наличие параметров
        film_info = requests_main(url_filter, urlencode(params))
        print("FILM INFO:", film_info)
        posters = film_info[0]
        rest_info = film_info[1]
        try:
            if posters:
                for item in range(10):
                    try:
                        if not posters[item]:
                            bot.send_message(message.chat.id, rest_info[item])
                        else:
                            bot.send_photo(
                                message.chat.id, posters[item], caption=rest_info[item]
                            )
                    except ApiTelegramException:
                        bot.send_message(message.chat.id, rest_info[item])
                        print("ApiTelegramException", posters[item])

            else:
                bot.send_message(message.chat.id, "Фильм не найден.")
        except ApiHTTPException:
            pass
        except IndexError:
            pass

    else:
        bot.send_message(message.chat.id, "Не заданы параметры фильтрации.")
    return


"""
Функции типа register вызываются при нажатии на кнопки фильтров, подбирают введеный 
критерий фильтрации и присваивают ему уникальный индекс.

"""


def register_type(message: Message):
    bot.send_message(message.chat.id, "Фильтр добавлен.", reply_markup=filter_markup)
    return catch_filter_info(message, ind=1)


def register_genre(message: Message):
    bot.send_message(message.chat.id, "Фильтр добавлен.", reply_markup=filter_markup)
    return catch_filter_info(message, ind=2)


def register_year(message: Message):
    bot.send_message(message.chat.id, "Фильтр добавлен.")
    return catch_filter_info(message, ind=3)


def register_rating(message: Message):
    bot.send_message(message.chat.id, "Фильтр добавлен.")
    return catch_filter_info(message, ind=4)


def catch_filter_info(message, ind: int):
    """Функция получает на вход критерий и его индекс.
    затем формирует правильный запрос."""

    info = dict()
    params = message.text

    if ind == 1:
        info["type"] = params.lower()
    elif ind == 2:
        info["genres.name"] = params.lower()
    elif ind == 3:
        info["year"] = params
    elif ind == 4:
        info["rating.imdb"] = params

    return collect_filter_info(info)


def collect_filter_info(info: dict):
    """Функция получает на вход правильный запрос в виде словаря и записывает его в файл формата JSON."""

    data = []  # Создаем список для хранения значений

    if os.stat("filter.json").st_size != 0:
        with open("filter.json", "r", encoding="utf-8") as readable_file:
            data = json.load(readable_file)

    with open("filter.json", "w", encoding="utf-8") as file:
        data.append(info)

        json.dump(data, file, ensure_ascii=False)

    return
