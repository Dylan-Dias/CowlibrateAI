import psycopg
from psycopg import rows
from Backend.config import Config

def get_db_connection():
    return psycopg.connect(Config.DATABASE_URL, row_factory=rows.dict_row)
