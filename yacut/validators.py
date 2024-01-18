from yacut.constants import REQUIRED_FIELDS, ALLOWED_CHARS
from yacut.models import URLMap


def short_link_is_empty_validator(short_link):
    return short_link == ''


def short_link_chars_validator(short_link):
    if short_link is None:
        return True
    if len(short_link) > 16:
        return False
    for char in short_link:
        if char not in ALLOWED_CHARS:
            return False
    return True


def short_link_exists_validator(short_link):
    if URLMap.query.filter_by(short=short_link).first() is None:
        return False
    return True


def url_exists_validator(url):
    if URLMap.query.filter_by(original=url).first() is None:
        return False
    return True


def request_data_is_empty_validator(data):
    return data is None


def required_fields_validator(data):
    for field in REQUIRED_FIELDS:
        if field not in data:
            return False
    return True
