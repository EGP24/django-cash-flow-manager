# Django Cash Flow Manager

Backend-приложение для учета движения денежных средств: транзакции ДДС, фильтры, CRUD справочников и серверная проверка связей между типами, категориями и подкатегориями.

## Запуск

### Ручной локальный запуск

Локально проект использует SQLite.

```bash
uv sync --all-groups
cp .env.example .env
uv run python manage.py migrate
uv run python manage.py load_mock_data
uv run python manage.py runserver
```

Приложение будет доступно на [http://localhost:8000](http://localhost:8000).

Demo admin: `admin` / `admin`.

### Локальный запуск через Make

То же самое можно выполнить через `make`:

```bash
make install
cp .env.example .env
make migrate
make mock-data
make run
```

Приложение будет доступно на [http://localhost:8000](http://localhost:8000).

### Запуск в Docker

Docker Compose поднимает приложение и PostgreSQL. Контейнер `web` применяет миграции перед стартом dev-сервера.

```bash
cp .env.example .env
docker compose up --build
```

Приложение будет доступно на [http://localhost:8000](http://localhost:8000).

Накатить мок-данные в Docker-базу:

```bash
docker compose run --rm web python manage.py load_mock_data
```

### Запуск в Docker через Make

```bash
make docker-run           # запустить сервер в Docker
make docker-run-mock-data # запустить сервер в Docker и загрузить мок-данные
```


Команды проверки и обслуживания:

```bash
make lint                 # запустить проверки Ruff
make format               # отформатировать код Ruff
make typecheck            # проверить типы mypy
make check                # выполнить системные проверки Django
make test                 # запустить все тесты с проверкой покрытия
make test-functional      # запустить функциональные тесты
make test-unit            # запустить юнит-тесты
make ci                   # выполнить локальный контроль качества
make docker-build         # собрать Docker-образ локально
```

`make ci` выполняет lint, mypy, Django checks и полный pytest-прогон.

## Переменные окружения

Пример конфигурации находится в `.env.example`.

| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | Секретный ключ Django. |
| `DJANGO_DEBUG` | `1` для разработки, `0` для production-like режима. |
| `DJANGO_ALLOWED_HOSTS` | Разрешенные hostnames через запятую. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Доверенные origins для CSRF. |
| `DATABASE_ENGINE` | `sqlite` или `postgresql`. |
| `POSTGRES_DB` | Имя PostgreSQL-базы. |
| `POSTGRES_USER` | Пользователь PostgreSQL. |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL. |
| `POSTGRES_HOST` | Host PostgreSQL. В Docker Compose используется `db`. |
| `POSTGRES_PORT` | Порт PostgreSQL. |

## Доменная модель

| Сущность | Назначение |
| --- | --- |
| `CashFlowTransaction` | Транзакция движения денежных средств. Содержит дату, статус, тип, категорию, подкатегорию, сумму и комментарий. |
| `CashFlowStatus` | Справочник статусов транзакций. Например: бизнес, личное, налог. |
| `CashFlowType` | Справочник типов транзакций. Например: пополнение или списание. |
| `Category` | Категория операции. Всегда привязана к конкретному типу операции. |
| `Subcategory` | Подкатегория операции. Всегда привязана к конкретной категории. |


## Маршруты

| Путь | Назначение |
| --- | --- |
| `/` | Список транзакций ДДС с фильтрами. |
| `/transactions/create/` | Создание транзакции ДДС. |
| `/transactions/<id>/edit/` | Редактирование транзакции ДДС. |
| `/transactions/<id>/delete/` | Удаление транзакции ДДС. |
| `/catalogs/` | Управление справочниками. |
| `/catalogs/<catalog>/create/` | Создание записи справочника. |
| `/catalogs/<catalog>/<id>/edit/` | Редактирование записи справочника. |
| `/catalogs/<catalog>/<id>/delete/` | Удаление записи справочника. |
| `/api/categories/` | Получение категорий для выбранного типа через DRF ViewSet. |
| `/api/subcategories/` | Получение подкатегорий для выбранной категории через DRF ViewSet. |
| `/admin/` | Django Admin. |

## Структура проекта

```text
django_cash_flow_manager/
  cashflows/          # доменная модель, правила, API, urls, admin
    transactions/     # транзакции ДДС: forms, selectors, views, urls
    catalogs/         # справочники, разделенные на statuses/types/categories/subcategories
    api/              # DRF ViewSet endpoints для зависимых select
    rules.py          # общие доменные проверки
  devtools/           # management-команды для разработки
  settings.py         # конфигурация Django и выбор БД
static/               # CSS и небольшой JS для зависимых select
templates/            # Django templates
tests/                # юнит-тесты
tests_functional/     # функциональные тесты
.github/workflows/    # CI
```
