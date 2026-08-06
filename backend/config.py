import os

class Config:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///voting.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-prod")