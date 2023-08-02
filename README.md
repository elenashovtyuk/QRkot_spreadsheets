# QRkot_spreadseets
Учебный проект: API приложения для Благотворительного фонда поддержки котиков QRKot.
Его назначение — сбор и распределение пожертвований между различными проектами и формирование отчетов о времени закрытия проектов
в гугл таблицах


## Технологии и библиотеки

 - Python 3.7
 - FastAPI (веб-фреймворк для создания API)
 - SQLAlchemy (библиотека для работы с реляционными СУБД с применением технологии ORM)
 - Pydantic (библиотека для валидации и сериализации данных)
 - Alembic (инструмент для миграции базы данных)
 - Uvicorn (высокопроизводительный ASGI сервер)
 - Google Cloud Platform
 - Google Sheets API
 - Google Drive API


## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/elenashovtyuk/QRkot_spreadsheets
```

Создать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Примените миграции:
```
alembic upgrade head
```
Запустите сервер из корневой папки проекта
```
uvicorn app.main:app --reload
```
При первом запуске приложения будет создан суперюзер, с регистрационными данными из `.env`

## API
Документация и web интервейс API будет доступен по адресу: http://localhost:8000/docs

## Автор проекта
- Шовтюк Е.А.
