# -*- coding: utf-8 -*-
from database.models import *


def add_user_query(user_id, query):
    """Функция для добавления нового запроса."""

    # Создаем новый объект UserQuery
    new_query = UserQuery(user_id=user_id, query=query)
    session.add(new_query)
    session.commit()

    # Проверяем, если в базе больше 10 записей для данного пользователя, удаляем самые старые
    user_queries_count = session.query(UserQuery).filter_by(user_id=user_id).count()
    if user_queries_count > 10:
        oldest_queries = (
            session.query(UserQuery)
            .filter_by(user_id=user_id)
            .order_by(UserQuery.timestamp)
            .limit(user_queries_count - 10)
            .all()
        )
        for query in oldest_queries:
            session.delete(query)
        session.commit()


def get_user_queries(user_id):
    """Функция для получения всех запросов пользователя из базы данных."""

    user_queries = (
        session.query(UserQuery)
        .filter_by(user_id=user_id)
        .order_by(UserQuery.timestamp.desc())
        .all()
    )

    return user_queries
