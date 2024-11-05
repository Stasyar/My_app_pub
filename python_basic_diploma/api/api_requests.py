# -*- coding: utf-8 -*-
import requests
from typing import Callable

from api.api import api_key


def url_search_by_name():
    """Функция возвращает url для поиска по названию."""

    return "https://api.kinopoisk.dev/v1.4/movie/search"


def url_filter():
    """Функция возвращает url для поиска по критериям фильтра."""

    return "https://api.kinopoisk.dev/v1.4/movie"


def get_films_from_api(func: Callable, params: dict) -> list:
    """Функция запрашивает информацию о фильме у API."""

    url = func()
    headers = {"X-API-KEY": api_key}
    params = params

    response = requests.get(url=url, headers=headers, params=params)

    res = response.json()

    try:
        all_films_data = [
            {
                "name": film["name"],
                "description": (
                    film["shortDescription"] if "shortDescription" in film else None
                ),
                "ranking": film["internalRating"] if "internalRating" in film else None,
                "year": film["year"] if "year" in film else None,
                "genre": (film["genres"][0]["name"] if "genres"[0] in film else None),
                "age_rating": film["ageRating"] if "ageRating" in film else None,
                "poster": (film["poster"]["url"] if "poster" in film else None),
            }
            for film in res["docs"]
        ]
    except KeyError:
        pass
    else:
        print(all_films_data)
        return all_films_data


def requests_main(func, params):
    """Основная функция для получения данных о фильме."""

    films_list = get_films_from_api(func, params)
    films_list = check_film_info(
        films_list
    )  # проверяем наличие названия у всех фильмов
    film_posters = [film["poster"] for film in films_list]
    rest_info = [
        f"{film["name"]}\n"
        f"Год: {film["year"]}\n"
        f"Жанр: {film["genre"]}\n"
        f"Возрастное ограничение: {film["age_rating"]}\n\n"
        f"Описание: {film["description"]}"
        for film in films_list
    ]

    return film_posters, rest_info


def check_film_info(film_data: list) -> list:
    """Функция проверяет наличие названий у фильмов и удаляет если название отсутствует."""

    new_lst = list()

    try:
        for elem in film_data:
            if elem["name"]:
                new_lst.append(elem)

        return new_lst
    except TypeError as e:
        print(e)
