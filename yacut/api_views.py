from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import save_to_db
from yacut.validators import (request_data_is_empty_validator,
                              required_fields_validator,
                              short_link_chars_validator,
                              short_link_exists_validator,
                              short_link_is_empty_validator,
                              url_exists_validator)
from yacut.views import generate_short_link


@app.route('/api/id/<string:short_link>/', methods=['GET'])
def get_url(short_link: str) -> jsonify:
    """Возвращает полную ссылку, по указанному custom_id."""
    if not short_link_exists_validator(short_link):
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    short_link_object = URLMap.query.filter_by(short=short_link).first()
    return jsonify({'url': short_link_object.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_link() -> jsonify:
    """создаёт короткую ссылку для указанного URL."""
    data = request.get_json()

    if request_data_is_empty_validator(data):
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if not required_fields_validator(data):
        raise InvalidAPIUsage('"url" является обязательным полем!')

    url = data.get('url')
    short_link = data.get('custom_id')
    data['original'] = url
    data['short'] = short_link

    if short_link is not None:

        if not short_link_chars_validator(short_link):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        short_link_object = URLMap.query.filter_by(short=short_link).first()

        if short_link_object is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        if short_link_is_empty_validator(short_link):
            data['short'] = generate_short_link()
            while short_link_exists_validator(data['short']):
                data['short'] = generate_short_link()
                short_link_exists_validator(data['short'])

        new_short_link_record = URLMap()
        new_short_link_record.from_dict(data)
        save_to_db(new_short_link_record)

        return (jsonify({'url': new_short_link_record.original,
                        'short_link': new_short_link_record.full_link}),
                HTTPStatus.CREATED)

    if url_exists_validator(url):
        existing_url_record = URLMap.query.filter_by(original=url).first()
        return jsonify({'url': existing_url_record.full_link}), HTTPStatus.OK

    data['short'] = generate_short_link()

    while short_link_exists_validator(data['short']):
        data['short'] = generate_short_link()
        short_link_exists_validator(data['short'])

    new_short_link_record = URLMap()
    new_short_link_record.from_dict(data)
    save_to_db(new_short_link_record)

    return (jsonify({'url': new_short_link_record.original,
                    'short_link': new_short_link_record.full_link}),
            HTTPStatus.CREATED)
