from django.core.validators import RegexValidator


class FirstNameValidator(RegexValidator):
    regex = (r'^[a-zA-Zа-яА-Я0-9]+$')
    message = (
        'Имя может содержать только буквы латиницы,'
        'кириллицы и цифры.'
    )


class LastNameValidator(FirstNameValidator):
    message = (
        'Фамилия может содержать только буквы латиницы,'
        'кириллицы и цифры.'
    )
