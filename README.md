# Orders Puller

## Table of contents
- [Orders Puller](#orders-puller)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
  - [APP-LOGIC](#app-logic)
    - [Main features](#main-features)
  - [run in dev environment](#run-in-dev-environment)
  - [Run it with docker](#run-it-with-docker)
  - [run test files](#run-test-files)

## Setup
1. install pipenv 
```
pip install pipenv

```
2. install needed packages and activate the venv
```
pipenv install
pipenv shell
```

## APP-LOGIC
Проект для извлечения сведений о заказах из электронной таблицы Google и представления данных в виде красивого графика.

### Main features
1. Запуск работы, которая извлекает данные из таблицы Google каждые две минуты и сохраняет их в базе данных.

## run in dev environment

1. migrate to database
```
python manange.py migrate
```
2. add cron task
```
python manage.py crontab add
```
3. run development server
```
python manange.py runserver
```


## Run it with docker
1. docker compose up
```
docker-compose --file docker-compose-local.yml --project-name=orders_puller up
```
2. docker compose down
```
docker-compose --file docker-compose-local.yml --project-name=orders_puller down
```

## run test files
1. install dev dependencies
```
pipenv install --dev
```
2. run all test files in the project
```
pytest --cache-clear --capture=no --showlocals --verbose
```