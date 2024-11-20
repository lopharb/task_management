from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import os

PASSWORD = os.environ.get("MARIADB_ROOT_PWD")

engine = create_engine(
    f'mariadb+mariadbconnector://root:{PASSWORD}@localhost:3306/TM_alchemy')

Base = declarative_base()
