from sqlalchemy import create_engine, MetaData
from database_url import DB_URL

engine = create_engine(DB_URL, future=True)
metadata = MetaData()

def create_all_tables():
    import models
    models.metadata.create_all(engine)

class SimpleDB:
    def __init__(self, engine):
        self.engine = engine

    def execute(self, stmt, params=None):
        with self.engine.begin() as conn:
            if params:
                return conn.execute(stmt, params)
            return conn.execute(stmt)

    def commit(self):
        return

def get_db():
    return SimpleDB(engine)
