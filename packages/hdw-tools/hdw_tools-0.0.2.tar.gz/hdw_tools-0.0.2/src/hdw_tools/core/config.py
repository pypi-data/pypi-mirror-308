from pydantic_settings import BaseSettings


class Config(BaseSettings):
    HDW_API_URL: str
    HDW_API_KEY: str
