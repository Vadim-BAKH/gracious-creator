# ***УМНЫЕ ПАРКОВКИ***
   -Это учебное приложение к 29 модулю python advanced skillbox

## *Структура и схема*

### Структура

    best_parking/
    |--- .env
    |--- Docker
    |--- docker-compose.sql
    |--- .gitignore
    |--- __init__.py
    |--- init.sql
    |--- requirement.txt
    |--- app/
         |--- tests/
         |    |--- __init__.py
         |    |--- файлы с тестами
         |    |--- conftests.py
         |--- factories/
         |    |--- __init__.py
         |    |--- файлы для фабрик
         |--- templates/
         |    |--- шаблоны html
         |--- static/
         |    |--- файлы стилей static.css и другие
         |--- services/
         |    |--- __init__.py
         |    |--- файлы обработки маршрутных функций для связи с моделями
         |--- models.py
         |--- database.py
         |--- utils.py
         |--- log.py
         |--- pytest.ini
         |--- schema.py
         |--- validate.py
         |--- flask_main.py
         |--- wsgi.py

### Описание с точки зрения REST API MVC

Model (Модель)
models.py: Содержит определения моделей данных, которые используются в приложении.

database.py: Обеспечивает взаимодействие с базой данных.

schema.py: Определяет схему данных для сериализации полученных объектов.

validate.py: Содержит функции для валидации входных данных.


View (Представление)
templates/: Содержит шаблоны HTML для отображения данных пользователю.

static/: Хранит статические файлы (стили, скрипты, изображения), которые используются в шаблонах.


Controller (Контроллер)
services/: Содержит логику обработки запросов и взаимодействия с моделями. Здесь реализуются маршрутные функции, которые обрабатывают HTTP-запросы и возвращают ответы.

flask_main.py: Основной файл приложения Flask, в котором определяются маршруты и запускается приложение.

wsgi.py: Используется для запуска приложения в среде WSGI.


Дополнительные компоненты
tests/: Содержит тесты для приложения.

factories/: Используется для создания фабрик, которые помогают генерировать тестовые данные.

log.py: Обеспечивает логирование событий в приложении.
    
    +---------------+
    |  Client     |
    +---------------+
             |
             | HTTP Request
             v
    +---------------+
    |  WSGI Server |
    |  (Gunicorn)  |
    |              |
    +---------------+
             |
             | Запуск приложения
             v
    +---------------+
    |  wsgi.py     |
    |  (Создание   |
    |   приложения) |
    +---------------+
             |
             | Обработка запроса
             v
    +---------------+
    |  Flask App   |
    |  (Controller) |
    +---------------+
             |
             | Обработка запроса
             v
    +---------------+
    |  Services    |
    |  (Controller) |
    +---------------+
             |
             | Взаимодействие с моделями
             v
    +---------------+
    |  Models      |
    |  (Model)     |
    +---------------+
             |
             | Доступ к данным
             v
    +---------------+
    |  Database    |
    |  (Model)     |
    +---------------+


В этой схеме клиент отправляет HTTP-запросы в приложение Flask, которое обрабатывает их 
с помощью контроллера (services/). Контроллер взаимодействует с моделями (models.py, database.py), 
которые обеспечивают доступ к данным. Результаты обработки затем возвращаются клиенту через шаблоны 
(templates/) и статические файлы (static/).


## *Работа с приложением*

### Подготовка

После скачивания приложения создать в корне проекта виртуальное окружение:
bash     python3 -m venv .myenv
bash     source .myenv/bin/activate
создать файл .env c указанием:
         
         DB_USER=ваш логин
         DB_PASSWORD=ваш пароль
         SECRET_KEY=ваш ключ

### Запуск приложения в фоновом режиме

bash     docker compose up --build -d
Результат:![img.png](img.png)

bash     docker ps
Результат:![img_1.png](img_1.png)

bash     docker compose logs web
логи web будут писаться![img_2.png](img_2.png)

bash      docker compose logs db
логи db будут писаться![img_3.png](img_3.png)

#### Установлены зависимости
flask==3.1.0
sqlalchemy==2.0.38
flask-sqlalchemy==3.1.1
gunicorn==23.0.0
psycopg2-binary==2.9.10
python-dotenv==1.0.1
loguru==0.7.3
requests==2.32.3
pytest==8.3.4
factory-boy==3.3.3
nano==0.10.0
marshmallow-sqlalchemy==1.4.1
marshmallow==3.26.1
flask-wtf==1.2.2
blinker==1.9.0

flake8==7.1.2
isort==6.0.0
ruff==0.9.7
mypy==1.15.0
pylint==3.3.4


#### База данных

PostgreSQL.


### Тестирование
Это учебное задание, поэтому тестирование проводится перед созданием базы данных, и не предназначено, 
для использования после заполнения таблиц, так как убивает таблицы в конце теста и закрывает сессию.
![img_33.png](img_33.png)

bash   docker compose up --build -d

bash   docker exec -it  best_parking-web-1 bash 

root@6d49bff8a48b:/app# pytest![img_4.png](img_4.png)

root@6d49bff8a48b:/app# pytest -m parking![img_5.png](img_5.png)

root@6d49bff8a48b:/app# pytest -m fake![img_6.png](img_6.png)

root@6d49bff8a48b:/app# pytest -m html![img_7.png](img_7.png)

bash docker compose down

### Работа с приложением и с базой данных best_parking_db

bash docker compose up --build -d

Таблицы создаются сразу, при первом посещении![img_9.png](img_9.png)

Пока таблицы пустые![img_10.png](img_10.png)

Обязательные поля![img_11.png](img_11.png)

Ввели![img_12.png](img_12.png)

Поля парковки![img_13.png](img_13.png)

Добавлена парковка![img_14.png](img_14.png)

Список парковок![img_15.png](img_15.png)

Паркуем![img_16.png](img_16.png)

Пытаемся выпустить![img_17.png](img_17.png)

Ищем, проверяем причину![img_18.png](img_18.png)

Обновили![img_19.png](img_19.png)

Ошиблись - нет парковки![img_20.png](img_20.png)

Не там стоит![img_21.png](img_21.png)

Успешно выехал ![img_22.png](img_22.png)

Нет клиента![img_23.png](img_23.png)

Заняли свободные места![img_24.png](img_24.png)![img_25.png](img_25.png)

Осталось 0 мест на первой парковке![img_26.png](img_26.png)

Не пустили![img_27.png](img_27.png)

Освободили место![img_28.png](img_28.png)

Не того хотели пустить![img_29.png](img_29.png)

Пустили![img_30.png](img_30.png)

Информация паркингов![img_31.png](img_31.png)


## Права принадлежат народу. Всем удачи!

