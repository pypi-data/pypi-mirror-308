import os
from string import Template
from typing import Any

from dotenv import load_dotenv
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

load_dotenv()


def interpolate_value(value: str) -> str:
    value = Template(value).substitute(os.environ)
    return os.path.expandvars(value)


def recurse_config(config: dict[str, Any] | list | str) -> dict[str, Any] | list | str:
    if isinstance(config, dict):
        return {interpolate_value(k): recurse_config(v) for k, v in config.items()}
    if isinstance(config, list):
        return [recurse_config(item) for item in config]
    if isinstance(config, str):
        return interpolate_value(config)
    return config


class Settings(BaseSettings):
    """A pre-configured Pydantic `BaseSettings` base class."""

    model_config = SettingsConfigDict(
        arbitrary_types_allowed=True,
        cache_strings='all',
        extra='allow',
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            YamlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
