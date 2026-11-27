from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.files import File
from django.apps import apps
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont

from .constants import consts


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, surname, password=None, avatar=None, **extra_fields):
        if not email:
            raise ValueError('У пользователя должен быть адрес электронной почты')
        email = self.normalize_email(email)  # Нормализация email
        if not avatar:
            image = Image.new('RGB', (128, 128), color='white')
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('arial.ttf', 100, encoding='utf-8')
            draw.text((30, 10), name.upper()[0], fill='black', font=font)
            image.save(f'media/avatars/avatar_{name.upper()[0]}.png')
        with open(f'media/avatars/avatar_{name.upper()[0]}.png', 'rb') as f:
            file_obj = File(f)
            avatar = File(file_obj, name=f'avatar_{name.upper()[0]}.png')
            user = self.model(email=email, name=name, surname=surname, avatar=avatar, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(**extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    name = models.CharField(max_length=consts.max_length_user_name, verbose_name="Имя")
    surname = models.CharField(max_length=consts.max_length_user_name, verbose_name="Фамилия")
    avatar = models.ImageField(
        verbose_name="Аватарка пользователя", upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=consts.max_length_user_phone, verbose_name="Номер телефона")
    github_url = models.URLField(null=True, blank=True, verbose_name="ссылка на GitHub")
    about = models.TextField(max_length=consts.max_length_user_about, null=True, blank=True, verbose_name="Описание")
    registered_at = models.DateTimeField(verbose_name="Время регистрации", default=timezone.now)
    is_active = models.BooleanField(default=True, verbose_name="Активный пользователь")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")
    is_superuser = models.BooleanField(default=False, verbose_name="Суперпользователь")
    favorites = models.ManyToManyField('projects.Project', blank=True,
                                       verbose_name="Избранные проекты",
                                       related_name='favorites')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return f'{self.name} {self.surname}'

    def owned_projects(self):
        return apps.get_model('projects', 'Project').objects.filter(owner=self)

    def participated_projects(self):
        return apps.get_model('projects', 'Project').objects.select_related('participants').filter(participants__id=self.id)

    class Meta:
        ordering = ['-registered_at']
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"
