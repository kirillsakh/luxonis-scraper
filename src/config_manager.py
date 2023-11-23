import os
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Config:
    psql_host: str
    psql_port: str
    psql_user: str
    psql_password: str
    psql_database: str
    webdriver_host: str
    webdriver_port: str
    app_port: str
    static_config: dict[str, Any]


class ConfigManager:
    def __init__(self, config: Config):
        self.config = config

    @classmethod
    def initialize_from_env(cls):
        kwargs = {
            "psql_host": os.environ.get("POSTGRES_HOST"),
            "psql_port": os.environ.get("POSTGRES_PORT"),
            "psql_user": os.environ.get("POSTGRES_USER"),
            "psql_password": os.environ.get("POSTGRES_PSWD"),
            "psql_database": os.environ.get("POSTGRES_DB"),
            "webdriver_host": os.environ.get("WEBDRIVER_HOST"),
            "webdriver_port": os.environ.get("WEBDRIVER_PORT"),
            "app_port": os.environ.get("APP_PORT"),
        }

        with open(Path(__file__).parent / 'configs' / 'static.yaml', mode='r') as _f:
            static_config = yaml.safe_load(_f)
        
        kwargs.update({"static_config": static_config})

        return cls(Config(**kwargs))
