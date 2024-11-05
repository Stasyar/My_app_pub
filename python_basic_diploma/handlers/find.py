# -*- coding: utf-8 -*-
from telebot.apihelper import ApiHTTPException, ApiTelegramException

from api.api_requests import requests_main, url_search_by_name
from database.requests import add_user_query
from loader import bot


def get_film_by_name(message):
    """Функция обращается к модулю requests, который запрашивает информацию у API."""

    add_user_query(message.from_user.id, message.text)
    params = dict()
    params["query"] = message.text
    film_info = requests_main(url_search_by_name, params)

    posters = film_info[0]
    rest_info = film_info[1]

    try:
        if posters:
            for i in range(10):
                try:
                    if not posters[i]:
                        bot.send_message(message.chat.id, rest_info[i])
                    else:
                        bot.send_photo(
                            message.chat.id, posters[i], caption=rest_info[i]
                        )
                except ApiTelegramException:
                    bot.send_message(message.chat.id, rest_info[i])
                    print("ApiTelegramException", posters[i])
        else:
            bot.send_message(message.chat.id, "Фильм не найден.")

    except ApiHTTPException:
        pass
    except IndexError:
        pass
