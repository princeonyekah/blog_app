"""Application configuration module."""
from os import environ
from prisma import Prisma, register


# pylint: disable-next=R0903
class Config:
    """Set Flask configuration vars from .env file."""

    # Server configuration
    PORT = environ.get("PORT", 5000)

    # Database configuration
    PRISMA = Prisma()

    # Auth configuration
    SECRET_KEY = environ.get("SECRET_KEY", "secret-key")

    # Other configurations

    # Database configuration
    DATABASE_URL = environ.get("DATABASE_URL", "postgresql://username:password@localhost:5432/dev")


# Initialize Prisma client
Config.PRISMA.connect()
register(Config.PRISMA)
