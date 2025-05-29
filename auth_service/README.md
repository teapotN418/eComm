### Запуск проекта с Doсker
1. Добавляете .env файл в папку

2. Создаете и запускаете контейнер через терминал:
```sh
docker compose up -d
```

3. Применяете миграции в базе данных:
```sh
docker exec -it fastapi_users alembic upgrade head
```

4. Сервис доступен по адресу: http://0.0.0.0:8000/

5. Запускаете тесты (желательно применять pytest-env для замены переменных окружения):
```sh
docker exec -it fastapi_users pytest --cov
```