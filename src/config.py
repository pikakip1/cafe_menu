from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / "certs" / 'jwt-public.pem'
    algorithm: str = 'RS256'
    expire_token_minutes: int = 15


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str

    auth_jwt: AuthJWT = AuthJWT()

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
