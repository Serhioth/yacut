import random

from yacut import db
from yacut.constants import ALLOWED_CHARS, RANDOM_SHORT_LINK_LENGTH
from yacut.models import URLMap


def save_to_db(record: URLMap) -> None:
    """Утилита для сохранения данных в бд."""
    db.session.add(record)
    db.session.commit()


def generate_short_link() -> str:
    """утилита для генерации случайных ссылок."""
    length = RANDOM_SHORT_LINK_LENGTH
    characters = ALLOWED_CHARS
    short_link = ''.join(random.choice(characters) for _ in range(length))
    return short_link
