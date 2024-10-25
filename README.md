# Проект api_yamdb
Проект YaMDb создан для сбора отзывов пользователей о различных произведениях.
## Инструкция по установке
Клонировать репозиторий:

'''git clone https://github.com/albrant/api_yamdb'''

Cоздать виртуальное окружение:

'''python3 -m venv venv'''
Активация виртуального окружения на Windows:

'''. venv/Scripts/activate'''

Linux:

'''. venv/bin/activate'''

Установить зависимости из файла requirements.txt:

'''python3 -m pip install --upgrade pip
pip install -r requirements.txt'''

Выполнить миграции:

'''python3 manage.py migrate'''

Запустить проект:

'''python3 manage.py runserver'''


