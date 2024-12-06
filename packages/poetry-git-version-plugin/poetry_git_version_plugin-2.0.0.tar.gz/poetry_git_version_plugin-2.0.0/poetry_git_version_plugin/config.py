import logging
from enum import Enum
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)

logger = logging.getLogger('poetry-git-version-plugin')

ENV_FILE = Path.cwd() / '.env'
TOML_FILE = Path.cwd() / 'pyproject.toml'

PLUGIN_NAME = 'poetry-git-version-plugin'


class ReleaseTypeEnum(str, Enum):
    tag = 'tag'
    alpha = 'alpha'
    beta = 'beta'
    rc = 'rc'
    post = 'post'
    dev = 'dev'


class GitVersionPluginConfig(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file=TOML_FILE,
        pyproject_toml_table_header=('tool', PLUGIN_NAME),
        env_file=ENV_FILE,
        env_prefix='PACKAGE_VERSION_',
        extra='ignore',
        case_sensitive=False,
    )

    release_type: ReleaseTypeEnum = ReleaseTypeEnum.dev

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
            PyprojectTomlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
        )
