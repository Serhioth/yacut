from datetime import datetime
from urllib.parse import urljoin

from yacut import db
from yacut.constants import MAX_LENGTH

BASE_URL = 'http://localhost/'


class URLMap(db.Model):
    """Класс описывающий модель для сохранения URL."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(MAX_LENGTH),
                      unique=True,
                      nullable=False,
                      index=True)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)

    def from_dict(self, data: dict) -> None:
        """Создаёт модель из данных переданного словаря."""
        for field in ('original', 'short'):
            for field in data:
                setattr(self, field, data[field])

    @property
    def full_link(self) -> str:
        """Возвращает полную ссылку для редиректа."""
        return urljoin(BASE_URL, self.short)
