from string import ascii_letters, digits

# Список обязательных полей при отправке api-запроса
REQUIRED_FIELDS = ('url',)
# Допустимые символы при создании короткой ссылки
ALLOWED_CHARS = ascii_letters + digits
# Максимальная длина короткой ссылки, при генерации
RANDOM_SHORT_LINK_LENGTH = 6
# Продакшн-мод среды разработки
PRODUCTION_MODE = 'production'
# Минимальная длина пользовательской короткой ссылки
MIN_LENGTH = 1
# Максимальная длинна пользовательской короткой ссылки
MAX_LENGTH = 16
