from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, password=None, avatar=None, **extra_fields):
        if not email:
            raise ValueError('У пользователя должен быть адрес электронной почты')
        email = self.normalize_email(email)  # Нормализация email
        if not avatar:
            image = Image.new('RGB', (128, 128), color='white')
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('arial.ttf', 40)
            draw.text((10, 30), name.upper()[0], fill='black', font=font)
            avatar = image
        user = self.model(email=email, name=name, avatar=avatar, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    name = models.CharField(max_length=124, verbose_name="Имя")
    surname = models.CharField(max_length=124, verbose_name="Фамилия")
    avatar = models.ImageField(
        verbose_name="Аватарка пользователя", upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=12, verbose_name="Номер телефона")
    github_url = models.URLField(null=True, blank=True, verbose_name="ссылка на GitHub")
    about = models.TextField(max_length=256, null=True, blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активный пользователь")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")
    favorites = models.ManyToManyField('projects.Project', blank=True,
                                       verbose_name="Избранные проекты",
                                       related_name='favorites')

    USERNAME_FIELD = 'email'

    objects = UserManager()
