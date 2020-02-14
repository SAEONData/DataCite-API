from enum import Enum
from typing import Optional, List

from pydantic import BaseSettings, AnyHttpUrl, validator


class ServerEnv(str, Enum):
    development = 'development'
    testing = 'testing'
    staging = 'staging'
    production = 'production'


class Config(BaseSettings):
    """
    Application config, populated from the environment.
    """
    SERVER_ENV: ServerEnv
    SERVER_HOST: str
    SERVER_PORT: int

    NO_AUTH: Optional[bool]
    OAUTH2_AUDIENCE: Optional[str]
    OAUTH2_SCOPE: Optional[str]
    ALLOWED_ROLES: Optional[List[str]]
    ACCOUNTS_API_URL: Optional[AnyHttpUrl]

    DOI_PREFIX: str
    DATACITE_USERNAME: str
    DATACITE_PASSWORD: str
    DATACITE_TESTING: bool = False

    @validator('NO_AUTH', pre=True, always=True)
    def validate_no_auth(cls, value):
        return value

    @validator('ACCOUNTS_API_URL', 'OAUTH2_AUDIENCE', 'OAUTH2_SCOPE', 'ALLOWED_ROLES', always=True)
    def require_auth_settings(cls, value, values):
        if not values.get('NO_AUTH', False) and not value:
            raise ValueError("Value is required if NO_AUTH is False")
        return value
