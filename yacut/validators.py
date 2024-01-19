from yacut.constants import ALLOWED_CHARS, MAX_LENGTH, REQUIRED_FIELDS
from yacut.models import URLMap


def short_link_is_empty_validator(short_link: str) -> bool:
    """Проверяет, что переданная строка не является пустой."""
    return short_link == ''


def short_link_chars_validator(short_link: str) -> bool:
    """Проверяет, соответствует ли короткая строка правилам валидации."""
    if short_link is None:
        return True
    if len(short_link) > MAX_LENGTH:
        return False
    for char in short_link:
        if char not in ALLOWED_CHARS:
            return False
    return True


def short_link_exists_validator(short_link: str) -> bool:
    """Проверяет, существует ли данная короткая ссылка в базе данных."""
    if URLMap.query.filter_by(short=short_link).first() is None:
        return False
    return True


def url_exists_validator(url: str) -> bool:
    """Проверяет есть ли переданный URLв базе данных."""
    if URLMap.query.filter_by(original=url).first() is None:
        return False
    return True


def request_data_is_empty_validator(data: dict) -> bool:
    """Провряет, не пустым ли пришёл запрос."""
    return data is None


def required_fields_validator(data: dict) -> bool:
    """Проверяет, все ли обязательные поля заполнены."""
    for field in REQUIRED_FIELDS:
        if field not in data:
            return False
    return True
