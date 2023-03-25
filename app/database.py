from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "posgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:meomeo@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()