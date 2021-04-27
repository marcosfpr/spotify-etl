"""
    Wrapper to PostgreSQL connection using psycopg2.
"""
import os

import psycopg2 as postgres

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ADDRESS = os.getenv("DB_ADDRESS")
DB_PORT = os.getenv("DB_PORT")

def with_connection(f):
    """
        Estabilish connection with postgres and starts a transaction.
    """
    def with_connection_(*args, **kwargs):
        # or use a pool, or a factory function...
        cnn = postgres.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        try:
            rv = f(cnn, *args, **kwargs)
        except Exception:
            cnn.rollback()
            raise
        else:
            cnn.commit() # or maybe not
        finally:
            cnn.close()

        return rv

    return with_connection_

def get_url():
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}"
