from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSetting(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class RedisSetting(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DEPRECATED: bool
    REDIS_DB: int

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class DatabaseSettings(BaseSettings):
    DATABASE_SCHEME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_PATH: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class Settings(JWTSetting, RedisSetting, DatabaseSettings):
    pass


def get_current_server_config():
    return Settings()
