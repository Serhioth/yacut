from http import HTTPStatus
from typing import Tuple

from flask import jsonify, render_template, Response

from yacut import app


class InvalidAPIUsage(Exception):
    """Класс для обработки ошибок в API."""
    status_code = 400

    def __init__(
        self, message: str, status_code: int = None
    ) -> None:
        super().__init__()
        self.message = message

        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: Exception) -> Tuple[Response, int]:
    """Обработчик ошибок API."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error: Exception) -> Tuple[Response, int]:
    """Обработчик ошибки 404."""
    return render_template('error_pages/404.html'), HTTPStatus.NOT_FOUND
