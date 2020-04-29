""" SqlAlchemy Database Session. """
import os
from dataclasses import dataclass

import sqlalchemy
import sqlalchemy.orm

from data.modelbase import SqlAlchemyBase
from data.rent_property import RentProperty

PG_USER = os.getenv("SQL_USER", "postgres")
PG_PASS = os.getenv("SQL_PASSWORD", "postgres123")
PG_HOST = os.getenv("SQL_HOST", "localhost")
PG_PORT = os.getenv("SQL_PORT", 5432)
PG_DATABASE = os.getenv("SQL_DATABASE", "postgres")

CONN_STR = f"postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"


@dataclass
class DbSession:
    """ DbSession Factory Class.
    """

    factory = None
    engine = None

    @staticmethod
    def global_init(conn_str=CONN_STR):
        """ start the connection.
        """
        if DbSession.factory:
            return False
        print(f"Connecting to DB at: {conn_str}")
        engine = sqlalchemy.create_engine(conn_str, echo=False, pool_pre_ping=True)
        DbSession.engine = engine
        DbSession.factory = sqlalchemy.orm.sessionmaker(bind=engine)

        SqlAlchemyBase.metadata.create_all(engine)

        return True

