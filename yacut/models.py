from datetime import datetime
from urllib.parse import urljoin

from yacut import db

BASE_URL = 'http://localhost/'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16),
                      unique=True,
                      nullable=False,
                      index=True)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)

    def from_dict(self, data):
        for field in ('original', 'short'):
            for field in data:
                setattr(self, field, data[field])

    @property
    def full_link(self):
        return urljoin(BASE_URL, self.short)
