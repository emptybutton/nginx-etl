# nginx-etl
Простой ETL пайплайн переносящий логи Nginx-а в ClickHouse практически в сыром виде.

## Развертывание для разработки
```bash
git clone https://github.com/emptybutton/nginx-etl.git
docker compose -f nginx-etl/deployments/dev/docker-compose.yaml up
```

В контейнере используется своё виртуальное окружение, сохранённое отдельным volume-ом, поэтому можно не пересобирать образ при изменении зависимостей.

Для ide можно сделать отдельное виртуальное окружение в папке проекта:
```bash
uv sync --extra dev --directory nginx-etl
```

> [!NOTE]
> При изменении зависимостей в одном окружении необходимо синхронизировать другое с первым:
> ```bash
> uv sync --extra dev
> ```
