import os
import json

from app import db, models
from datetime import datetime


def load_fixture(file_path):
    """
    Загрузить фикстуры
    :param file_path: путь к файлу
    :return: фикстура
    """

    content = []
    if os.path.isfile(file_path):
        with open(file_path) as file:
            content = json.load(file)

    return content


def migration(fixture_path, model, convert_dates=False):
    """
    Осуществить миграцию таблиц
    :param fixture_path: путь к фикстуре
    :param model: модель
    :param convert_dates: переформатирование даты. По умолчанию отключено
    :return: Записывает внесенные изменения
    """
    fixture_content = load_fixture(fixture_path)

    for fixture in fixture_content:
        if convert_dates:
            for field_name, field_value in fixture.items():
                if isinstance(field_value, str) and field_value.count('/') == 2:
                    fixture[field_name] = datetime.strptime(field_value, '%m/%d/%Y')

        if db.session.query(model).filter(model.id == fixture['id']).first() is None:
            db.session.add(model(**fixture))

    db.session.commit()


def migrate_user_roles(fixture_path):
    """
    Осуществить миграцию ролей юзеров. Вызвать функцию migration
    :param fixture_path: путь к фикстуре
    :return: Записывает внесенные изменения
    """
    migration(
        fixture_path=fixture_path,
        model=models.UserRole,
    )


def migrate_users(fixture_path):
    """
    Осуществить миграцию юзеров. Вызвать функцию migration
    :param fixture_path: путь к фикстуре
    :return: Записывает внесенные изменения
    """
    migration(
        fixture_path=fixture_path,
        model=models.User,
    )



def migrate_orders(fixture_path):
    """
    Осуществить миграцию заказов. Вызвать функцию migration
    :param fixture_path: путь к фикстуре
    :return: Записывает внесенные изменения
    """
    migration(
        fixture_path=fixture_path,
        model=models.Order,
        convert_dates=True,
    )


def migrate_offers(fixture_path):
    """
    Осуществить миграцию офферов. Вызвать функцию migration
    :param fixture_path: путь к фикстуре
    :return: Записывает внесенные изменения
    """
    migration(
        fixture_path=fixture_path,
        model=models.Offer,
    )