from http import HTTPStatus

from flask import abort, flash, redirect, render_template, Response

from yacut import app
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.utils import save_to_db, generate_short_link
from yacut.validators import (short_link_chars_validator,
                              short_link_is_empty_validator,
                              short_link_exists_validator,
                              url_exists_validator)


@app.route('/', methods=('GET', 'POST'))
def index_view() -> Response:
    """View-функция для отображения главной страницы."""
    form = URLForm()
    short_link_record = None

    if not form.validate_on_submit():
        return render_template('index.html',
                               form=form,
                               short_link_record=short_link_record)

    short_link = form.custom_id.data
    url = form.original_link.data

    if not short_link_chars_validator(short_link):

        flash('Данная короткая ссылка содержит'
              ' недопустимые символы, '
              'попробуйте другой вариант.')
        return render_template('index.html',
                               form=form,
                               short_link_record=short_link_record)

    if (not short_link_is_empty_validator(short_link)
       and short_link_exists_validator(short_link)):
        flash('Предложенный вариант короткой ссылки уже существует.')
        return render_template('index.html',
                               form=form,
                               short_link_record=short_link_record)

    if (url_exists_validator(url) and
       short_link_is_empty_validator(short_link)):
        existing_url_record = URLMap.query.filter_by(original=url).first()
        flash('Ваш вариант короткой ссылки:\n'
              f'<a href="{short_link_record.full_link}">'
              f'{short_link_record.full_link}</a>')
        return render_template(
            'index.html',
            form=form,
            short_link_record=existing_url_record
        )
    if short_link_exists_validator(short_link) or short_link is None:
        short_link = generate_short_link()

        while short_link_exists_validator(short_link):
            short_link = generate_short_link()
            short_link_exists_validator(short_link)

    short_link_record = URLMap(
        original=url,
        short=short_link
    )
    save_to_db(short_link_record)

    flash('Ваш вариант короткой ссылки:\n'
          f'<a href="{short_link_record.full_link}">'
          f'{short_link_record.full_link}</a>')

    return render_template('index.html',
                           form=form,
                           short_link_record=short_link_record)


@app.route('/<string:short_link>')
def redirect_to_url(short_link: str) -> Response:
    """
    View-функция для перенаправления пользователя
    по сгенерированной короткой ссылке.
    """
    url_map_object = URLMap.query.filter_by(short=short_link).first()
    if url_map_object:
        return redirect(url_map_object.original)
    abort(HTTPStatus.NOT_FOUND)
