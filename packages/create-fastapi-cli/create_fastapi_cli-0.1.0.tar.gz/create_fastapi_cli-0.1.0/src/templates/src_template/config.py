import os
from typing import Tuple, Type, List

from pydantic import HttpUrl, MongoDsn
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from src.constants import Environment

config_file = os.environ.get("CONFIG_FILE") or os.path.join(
    os.path.dirname(__name__), "confs/config.yaml"
)

config_file = os.path.abspath(config_file)


class Config(BaseSettings):
    env: Environment = Environment.DEV
    mongo: MongoDsn = "mongodb://localhost:27017"
    database: str = "example"

    # logging config
    log_level: str = "DEBUG"
    log_handlers: List[str] = ["console", "file"]
    log_filename: str = "app.log"

    model_config = SettingsConfigDict(extra="ignore")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            YamlConfigSettingsSource(
                settings_cls, yaml_file=config_file, yaml_file_encoding="utf-8"
            ),
        )

    def reload_mongo(self):
        # read from os.environ
        if os.environ.get("MONGO"):
            self.mongo = MongoDsn(os.environ["MONGO"])


config = Config()
