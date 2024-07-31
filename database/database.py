from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from config.config import DatabaseSettings

database_setting = DatabaseSettings()


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{database_setting.DATABASE_USERNAME}:{database_setting.DATABASE_PASSWORD}@{database_setting.DATABASE_HOST}:{database_setting.DATABASE_PORT}/{database_setting.DATABASE_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
