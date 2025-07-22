from pydantic import EmailStr
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    EMAIL_TO: EmailStr
    EMAIL_FROM: EmailStr
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    SECRET_KEY: str
    PORT: int
    HOST: str
    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
