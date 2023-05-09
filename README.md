Необходимо спроектировать и разработать Django-сервис друзей.
Сервис должен предоставлять возможности:
- зарегистрировать нового пользователя
- оправлять одному пользователю заявку в друзья другому
- принять/отклонить пользователю заявку в друзья от другого пользователя
- посмотреть пользователю список своих исходящих и входящих заявок в друзья
- посмотреть пользователю список друзей
- получать пользователю статус дружбы с каким-то другом пользователем (нет ничего/есть исходящая заявка/есть входящая заявка/ уже друзья)
- удалить пользователю другого пользователя из своих друзей
- если пользователь 1 отправляет заявку в друзья пользователю 2, а пользователь 2 отправляет заявку пользователю 1, то они автоматически становятся друзьями, их заявки автоматом принимаются.

Модель пользователя может быть самой простой:
- id
- username

Необходимо:
- описать REST интерфейс сервиса с помощью OpenAPI
- написать на Django сервис по этой спецификации
- описать краткую документацию с примерами запуска сервиса и вызова его API
+unit-тесты будут плюсом
+Dockerfile для упаковки в контейнер будет плюсом

Входные артефакты:
- исходный код
- OpenAPI спецификация
- документация с описанием запуска и примерами использования API

## Используемые технологии
- Python 3.11 
- Django 4.2

Подготовка к запуску проекта
Клонируйте проект с помощью git clone или скачайте ZIP-архив. Установите и активируйте виртуальное окружение

python -m venv venv

Установите зависимости из файла requirements.txt

pip install -r requirements.txt

Применить миграции

python manage.py makemigrations
python manage.py migrate

Запустить проект:

python manage.py runserver

Перейдите на страницу http://127.0.0.1:8000/ 