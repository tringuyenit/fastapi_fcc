import time

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# SQLALCHEMY_DATABASE_URL = "posgresql://<username>:<password>@<ip-address/hostname>/<database_name>"

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:meomeo@localhost:5432/fastapi"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost",
#                                 database="fastapi",
#                                 user="postgres",
#                                 password="meomeo",
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB connected sucessfully")
#         break
#     except Exception as e:
#         print("DB connect failed")
#         print("error:", e)
#         time.sleep(2)
