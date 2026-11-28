from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from .constants import Consts
from team_finder import settings

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=Consts.max_length_project_name, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateField(verbose_name="Дата создания проекта", default=timezone.now)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор проекта",
        related_name='owner')
    github_url = models.URLField(null=True, blank=True, verbose_name="ссылка на GitHub")
    status = models.CharField(max_length=max(map(lambda x: max(map(len, x)), Consts.choices)), choices=Consts.choices,
                              verbose_name="Статус проекта", default=Consts.opened[0])
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                          verbose_name="Участники проекта",
                                          related_name='participants')

    class Meta:
        verbose_name = "проект"
        verbose_name_plural = "Проекты"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def interested_users(self):
        return User.objects.filter(favorites=self)
