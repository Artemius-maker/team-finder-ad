# Первоначальная настройка проекта TeamFinder

## 1. Клонирование из Github и начало работы

Вначале надо клонировать проект из github и перейти в неё

1. **Клонируйте проект**
    ```bash
   git clone https://github.com/Artemius-maker/team-finder-ad team-finder
   ```

2. **Перейдите в папку проекта**
    ```bash
   cd team-finder
   ```

## 2. Виртуальное окружение

Перед началом работы необходимо создать и активировать виртуальное окружение Python.

1. **Создайте виртуальное окружение (в папке проекта):**
   ```bash
   python3 -m venv venv
   ```

   После этого появится папка `venv`, где будут храниться зависимости проекта.

2. **Активируйте окружение:**

    - **Windows (PowerShell):**
      ```bash
      venv\Scripts\Activate.ps1
      ```
    - **Windows (cmd):**
      ```bash
      venv\Scripts\activate
      ```
    - **Linux/Mac:**
      ```bash
      source venv/bin/activate
      ```

3. **Установите зависимости из `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

   После установки в окружении будут доступны все нужные библиотеки Django-проекта.

## 3. Создание `.env`

Файл `.env` содержит конфиденциальные настройки проекта — ключ Django, параметры БД и другие переменные.

В репозитории есть пример `.env_example`, который нужно скопировать и заполнить:

```bash
cp .env_example .env
```

После этого откройте `.env` и укажите свои значения.

| Переменная            | Назначение                                                                                                                                                 |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **DJANGO_SECRET_KEY** | Секретный ключ Django, используемый для подписи cookie и токенов. Можно сгенерировать при помощи `get_random_secret_key` из `django.core.management.utils` |
| **DJANGO_DEBUG**      | Режим отладки. Установите `True` во время разработки.                                                                                                      |
| **POSTGRES_DB**       | Имя базы данных PostgreSQL, которую будет использовать Django.                                                                                             |
| **POSTGRES_USER**     | Имя пользователя PostgreSQL.                                                                                                                               |
| **POSTGRES_PASSWORD** | Пароль пользователя PostgreSQL.                                                                                                                            |
| **POSTGRES_HOST**     | Адрес сервера БД. В случае локальной разработки localhost.                                                                                                 |
| **POSTGRES_PORT**     | Порт подключения к БД (по умолчанию `5432`).                                                                                                               |

---

## 4. Запуск PostgreSQL

Для работы приложения **TeamFinder** используется база данных **PostgreSQL**. По условию задания база данных должна
запускаться в контейнере Docker.

В проекте уже есть пример файла `docker-compose.yml`. Используйте готовый или измените под свои нужды, а дальше
запускайте:

```bash
docker compose up -d
```

`-d` значит `detach`, то есть контейнер продолжит работать в фоне. Чтобы его остановить, надо будет ввести

```bash
docker compose down
```

Если возникает ошибка "permission denied while trying to connect to the Docker daemon socket", то может потребоваться
добавить `sudo` перед командой.

---

После этого база данных будет доступна по адресу `localhost:5432`.  
Нужно будет использовать эти же параметры в файле `.env`.

> Если на компьютере уже развёрнут сервер БД на порте 5432, и вы не хотите создавать БД для этого проекта на этом сервере, целесообразнее будет изменить порт на нестандартный.
> Нестандартный порт нужно будет поставить слева в паре портов в docker-compose (`"5433":"5432"`) и в .env.

## 5. Запуск Django

После заполнения `.env` и настройки базы данных можно запустить сервер разработки:

```bash
python manage.py runserver
```

Теперь проект доступен по адресу [http://localhost:8000](http://localhost:8000).

1. **Автор** — Артём Еретин, контакт-ссылки: email: artemiuseretin@gmail.com;
   GitHub: https://github.com/Artemius-maker/team-finder-ad

2. **Техно-стек** — Python 3.x, Django 3.2.16, django-bootstrap5 (Bootstrap 5)
   PostgreSQL 16 (Docker), Faker/mixer for demo data Pillow; dev tools: flake8, pytest-django, django-debug-toolbar

2. **Команды развертывания** — git clone → cd → venv create/activate → pip install -r requirements.txt → cp .env_example
   .env (Заполнить переменные) → docker compose up -d → migrations → Команда наполнения демо-данными

3. **Команды запуска** — docker compose up -d, python manage.py runserver; Стоп: docker compose down

4. **Адреса** — [Сайт](http://localhost:8000) and [Админ-панель](http://localhost:8000/admin)