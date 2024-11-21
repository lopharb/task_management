PASSWORD = os.environ.get("MARIADB_ROOT_PWD")
DATABASE_URL = f'mariadb+mariadbconnector://root:{PASSWORD}@localhost:3306/TM_alchemy'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


class UserHandler:

    @classmethod
    def get_by_id(cls, db, user_id):
        pass