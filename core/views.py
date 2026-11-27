from urllib.parse import urlparse

from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from team_finder.settings import paginate_by


class BaseLoginView(View):
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return render(request, self.template_name, {'form': form})
        login(request, user)
        messages.success(request, f'Добро пожаловать, {user.get_short_name()}!')
        return redirect('projects:mainpage')


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


def page_paginator(request, list, paginate=paginate_by):
    paginator = Paginator(list, paginate)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
