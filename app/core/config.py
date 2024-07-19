"""
This module contains the configuration settings for the application.

It uses Pydantic's BaseSettings to load settings from the environment.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    Attributes:
        database_hostname (str): The hostname of the database.
        database_port (str): The port of the database.
        database_name (str): The name of the database.
        database_username (str): The username to connect to the database.
        database_password (str): The password to connect to the database.
        secret_key (str): The secret key for the application.
        algorithm (str): The algorithm used for encoding.
        access_token_expire_minutes (int): The number of minutes until the access token expires.
    """

    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        """
        Configuration class for the application.

        Attributes:
            env_file (str): The name of the environment file to load.
        """
        env_file: str = ".env"


settings = Settings()
