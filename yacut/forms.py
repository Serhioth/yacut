from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from yacut.constants import MIN_LENGTH, MAX_LENGTH


class URLForm(FlaskForm):
    """Форма для работы со ссылками."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле!')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(MIN_LENGTH, MAX_LENGTH),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
