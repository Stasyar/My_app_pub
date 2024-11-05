# -*- coding: utf-8 -*-
from database.requests import get_user_queries
from keyboards.reply_kb import markup, filter_markup, genre_markup, type_markup
from handlers.find import get_film_by_name
from handlers.filter_search import *


@bot.message_handler(commands=["start"])
def cmd_start(message):
    """Функция обрабатывает cтартовую команду."""
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.full_name}.\nЭто телеграм бот для поиска фильмов.",
        reply_markup=markup,
    )


@bot.message_handler(
    func=lambda message: message.text
    in ["Поиск по названию", "Фильтры", "История поиска"]
)
def handle_main_page_message(message):
    """Функция обрабатывает кнопки главного меню."""
    if message.text == "Поиск по названию":
        bot.send_message(message.chat.id, "Введите название фильма:")
        bot.register_next_step_handler(message, get_film_by_name)
    elif message.text == "Фильтры":
        clear_filter_file()
        bot.send_message(
            message.chat.id,
            "1. Нажмите на кнопку критерия, который хотите задать для фильтрации.\n"
            "2. Из полученого списка выберите нужные опции и отправьте их боту.\n"
            "Если вы выбрали несколько опций, укажите их через запятую.\n"
            "3. После того как вы указали все необходимые критерии поиска, нажмите кнопку 'Отфильтровать'",
            reply_markup=filter_markup,
        )
        bot.register_next_step_handler(message, handle_filter_message)
    elif message.text == "История поиска":
        send_search_history(message)


@bot.message_handler(
    func=lambda message: message.text
    in ["Тип", "Жанр", "Год", "Рейтинг", "Отфильтровать", "Главная"]
)
def handle_filter_message(message):
    """Функция обрабатывает кнопки меню фильтров."""
    if message.text == "Жанр":
        bot.send_message(message.chat.id, "Выберите жанр", reply_markup=genre_markup)
        bot.register_next_step_handler(message, register_genre)
    elif message.text == "Тип":
        bot.send_message(
            message.chat.id, "Выберите тип киноленты", reply_markup=type_markup
        )
        bot.register_next_step_handler(message, register_type)
    elif message.text == "Год":
        bot.send_message(
            message.chat.id,
            "Напишите год (например: 2022) или период (например: 2022-2024)",
            reply_markup=filter_markup,
        )
        bot.register_next_step_handler(message, register_year)
    elif message.text == "Рейтинг":
        bot.send_message(
            message.chat.id,
            "Напишите рейтинг (например: 7) или промежуток (например: 7-10)",
            reply_markup=filter_markup,
        )
        bot.register_next_step_handler(message, register_rating)
    elif message.text == "Отфильтровать":
        filter_search(message)
    elif message.text == "Главная":
        bot.send_message(message.chat.id, "На главную", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in get_genre_list())
def handle_genre_message(message: Message):
    """Функция обрабатывает кнопки жанров."""
    register_genre(message)


@bot.message_handler(func=lambda message: message.text in get_type_list())
def handle_type_message(message: Message):
    """Функция обрабатывает кнопки типов."""
    register_type(message)


@bot.message_handler(commands=["help"])
def get_help(message):
    """Функция обрабатывает команду справочника."""
    bot.send_message(
        message.chat.id,
        "- - - - - - HELP - - - - - -\n\n"
        "* Главное меню:\n"
        "  - Поиск по названию: ищет фильмы по названию.\n"
        "  - Фильтры: ищет фильмы по указанным критериям\n"
        "  - История поиска: выводит последние 10 запросов боту.\n\n"
        "* Фильтры:\n"
        "   - Жанр\n"
        "   - Тип\n"
        "   - Год\n"
        "   - Рейтинг",
    )


def clear_filter_file():
    """Функция очищает файл фильтров."""
    with open("filter.json", "w", encoding="utf-8"):
        pass


def send_search_history(message):
    """Функция отправляет историю поиска пользователю."""
    query = get_user_queries(message.from_user.id)
    query_str = "\n\n".join([f"**{elem.query}** - {elem.timestamp}" for elem in query])
    res = "   - - - ИСТОРИЯ ПОИСКА - - -\n\n" + query_str
    bot.send_message(message.chat.id, res)


def get_genre_list():
    """Функция возвращает список жанров."""
    return [
        "аниме",
        "биография",
        "боевик",
        "вестерн",
        "военный",
        "детектив",
        "детский",
        "для взрослых",
        "документальный",
        "драма",
        "история",
        "комедия",
        "короткометражка",
        "криминал",
        "мелодрама",
        "музыка",
        "мультфильм",
        "мюзикл",
        "приключения",
        "реальное ТВ",
        "семейный",
        "спорт",
        "ток-шоу",
        "триллер",
        "ужасы",
        "фантастика",
        "фильм-нуар",
        "фэнтези",
    ]


def get_type_list():
    """Функция возвращает список типов кинолент."""
    return ["animated-series", "anime", "cartoon", "movie", "tv-series"]


def register_genre(message: Message):
    bot.send_message(message.chat.id, "Фильтр добавлен.", reply_markup=filter_markup)
    catch_filter_info(message, ind=2)


def register_type(message: Message):
    bot.send_message(message.chat.id, "Фильтр добавлен.", reply_markup=filter_markup)
    catch_filter_info(message, ind=1)


def register_year(message: Message):
    bot.send_message(message.chat.id, "Фильтр добавлен.")
    catch_filter_info(message, ind=3)


def register_rating(message: Message):
    bot.send_message(message.chat.id, "Фильтр добавлен.")
    catch_filter_info(message, ind=4)


def catch_filter_info(message, ind: int):
    """Функция получает на вход критерий и его индекс, затем формирует правильный запрос."""
    info = {}
    params = message.text

    if ind == 1:
        info["type"] = params.lower()
    elif ind == 2:
        info["genres.name"] = params.lower()
    elif ind == 3:
        info["year"] = params
    elif ind == 4:
        info["rating.imdb"] = params

    collect_filter_info(info)


def collect_filter_info(info: dict):
    """Функция получает на вход правильный запрос в виде словаря и записывает его в файл формата JSON."""
    data = []

    if os.stat("filter.json").st_size != 0:
        with open("filter.json", "r", encoding="utf-8") as readable_file:
            data = json.load(readable_file)

    with open("filter.json", "w", encoding="utf-8") as file:
        data.append(info)
        json.dump(data, file, ensure_ascii=False)
