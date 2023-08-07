from django.core.validators import RegexValidator


class FirstNameValidator(RegexValidator):
    """Валидатор поля 'first_name' модели User."""

    regex = (r'^[a-zA-Zа-яА-Я0-9]+$')
    message = (
        'Имя может содержать только буквы латиницы,'
        'кириллицы и цифры.'
    )


class LastNameValidator(FirstNameValidator):
    """Валидатор поля 'last_name' модели User."""

    message = (
        'Фамилия может содержать только буквы латиницы,'
        'кириллицы и цифры.'
    )
