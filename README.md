# IT Challenge — статистика по CSV

Платформа обработки заданий: пользователь отправляет CSV-файл, система считает статистику в фоне

## Уровни проекта

1. **Foundation** — Python, FastAPI, REST API, PostgreSQL *(выполнен)*

## Структура проекта

```
app/
├── constants/messages.py                     # тексты ошибок
├── constants/task_status.py                  # статусы задания (Enum)
├── controllers/controller.py                 # эндпоинты REST API
├── dto/request/task_request_dto.py           # запрос: CSV-файл и столбец
├── dto/response/error_response_dto.py        # ответ с ошибкой
├── dto/response/health_response_dto.py       # ответ /health
├── dto/response/statistics_response_dto.py   # результат расчета
├── dto/response/task_response_dto.py         # задание
├── exceptions/handlers.py                    # обработчики ошибок → JSON
├── exceptions/statistics_error.py            # ошибка в данных CSV
├── exceptions/task_not_found_error.py        # задание не найдено
├── models/task.py                            # модель таблицы tasks
├── resources/config.properties.example       # шаблон конфигурации
├── resources/measurements.csv                # пример входного файла
├── services/statistics.py                    # расчет статистики
├── services/task_service.py                  # работа с заданиями
├── utils/logger.py                           # настройка логирования
├── utils/parameter_provider.py               # чтение config.properties
├── database.py                               # подключение к БД
└── main.py                                   # точка входа
```

## База данных

PostgreSQL запускается в Docker:

```bash
docker run --name it_challenge -e POSTGRES_PASSWORD=secret -p 5437:5432 -d postgres
```

Таблица `tasks` создается в базе `db_challenge`:

```sql
CREATE TABLE tasks (
    id       SERIAL       PRIMARY KEY,
    "column" VARCHAR(255) NOT NULL,
    status   VARCHAR(20)  NOT NULL DEFAULT 'pending',
    content  TEXT         NOT NULL,
    result   JSON,
    error    TEXT
);
```

## Конфигурация

Параметры подключения хранятся в `app/resources/config.properties`.
Файл не попадает в Git - создайте его из шаблона и укажите свой пароль:

```bash
cp app/resources/config.properties.example app/resources/config.properties
```

```properties
db.host=localhost
db.port=5437
db.name=db_challenge
db.user=postgres
db.password=your_password
server.port=8001
```

Любой параметр можно переопределить переменной окружения с тем же именем.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m app.main
```

Запускать из корня проекта. API: http://127.0.0.1:8001, документация: http://127.0.0.1:8001/docs

## API

| Метод | Путь | Описание | Ответ |
|-------|------|----------|-------|
| GET | `/health` | сервис работает | 200 |
| POST | `/tasks` | CSV-файл (`file`) и имя столбца (`column`) | 201 |
| GET | `/tasks` | список заданий | 200 |
| GET | `/tasks/{id}` | статус и результат задания | 200, 404 |

Пример ответа для `measurements.csv` и столбца `temperature`:

```json
{
  "id": 1,
  "status": "completed",
  "column": "temperature",
  "result": {"count": 4, "min": 19.8, "max": 23.0, "mean": 21.6},
  "error": null
}
```