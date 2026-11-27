from urllib.parse import urlparse

from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.views import View
from django.contrib.auth.views import LoginView

from team_finder.settings import PAGINATE_BY


def validate_hostname(value, allowed_hosts):
    """
    Проверяет, что URL ведёт на github.com (любой путь, любой пользователь).
    """
    if not value:
        return True
    try:
        parsed_url = urlparse(value)
        hostname = parsed_url.hostname

        if not hostname:
            raise ValidationError('Не удалось определить домен в ссылке.')

        # Разрешаем github.com и www.github.com
        if hostname not in allowed_hosts:
            raise ValidationError(
                f'Недопустимый домен: {hostname}. Разрешены только ссылки на GitHub.'
            )
    except ValueError:
        raise ValidationError('Некорректный URL.')
    return True


def page_paginator(request, list, paginate=PAGINATE_BY):
    paginator = Paginator(list, paginate)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
