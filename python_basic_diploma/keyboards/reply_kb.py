# -*- coding: utf-8 -*-
from telebot import types


markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1 = types.KeyboardButton("Поиск по названию")
itembtn2 = types.KeyboardButton("Фильтры")
itembtn3 = types.KeyboardButton("История поиска")
markup.add(itembtn1, itembtn2, itembtn3)

filter_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1 = types.KeyboardButton("Тип")
itembtn2 = types.KeyboardButton("Жанр")
itembtn3 = types.KeyboardButton("Год")
itembtn4 = types.KeyboardButton("Рейтинг")
itembtn5 = types.KeyboardButton("Отфильтровать")
itembtn6 = types.KeyboardButton("Главная")
filter_markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)

genre_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons = [
    types.KeyboardButton("аниме"),
    types.KeyboardButton("биография"),
    types.KeyboardButton("боевик"),
    types.KeyboardButton("вестерн"),
    types.KeyboardButton("военный"),
    types.KeyboardButton("детектив"),
    types.KeyboardButton("детский"),
    types.KeyboardButton("для взрослых"),
    types.KeyboardButton("документальный"),
    types.KeyboardButton("драма"),
    types.KeyboardButton("история"),
    types.KeyboardButton("комедия"),
    types.KeyboardButton("криминал"),
    types.KeyboardButton("мелодрама"),
    types.KeyboardButton("мультфильм"),
    types.KeyboardButton("мюзикл"),
    types.KeyboardButton("приключения"),
    types.KeyboardButton("реальное ТВ"),
    types.KeyboardButton("семейный"),
    types.KeyboardButton("спорт"),
    types.KeyboardButton("ток-шоу"),
    types.KeyboardButton("триллер"),
    types.KeyboardButton("ужасы"),
    types.KeyboardButton("фантастика"),
    types.KeyboardButton("фильм-нуар"),
    types.KeyboardButton("фэнтези"),
]

genre_markup.add(*buttons)

type_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons = [
    types.KeyboardButton("animated-series"),
    types.KeyboardButton("anime"),
    types.KeyboardButton("cartoon"),
    types.KeyboardButton("movie"),
    types.KeyboardButton("tv-series"),
]

type_markup.add(*buttons)
