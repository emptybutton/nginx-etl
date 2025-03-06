from dataclasses import dataclass

import typenv


@dataclass(kw_only=True, frozen=True, slots=True)
class Envs:
    redis_url: str

    clickhouse_host: str
    clickhouse_port: int
    clickhouse_user: str
    clickhouse_password: str
    clickhouse_db: str

    nginx_log_file_path: str
    nginx_log_file_line_batch_max_size: int

    @classmethod
    def load(cls) -> "Envs":
        env = typenv.Env()

        return Envs(
            redis_url=env.str("REDIS_URL"),
            clickhouse_host=env.str("CLICKHOUSE_HOST"),
            clickhouse_port=env.int("CLICKHOUSE_PORT"),
            clickhouse_user=env.str("CLICKHOUSE_USER"),
            clickhouse_password=env.str("CLICKHOUSE_PASSWORD"),
            clickhouse_db=env.str("CLICKHOUSE_DB"),
            nginx_log_file_path=env.str("NGINX_LOG_FILE_PATH"),
            nginx_log_file_line_batch_max_size=env.int(
                "NGINX_LOG_FILE_LINE_BATCH_MAX_SIZE"
            ),
        )
