import psycopg
from psycopg.rows import dict_row
from config import Config

def get_connection():
    return psycopg.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASS,
        options=f"-c search_path={Config.DB_SCHEMA},public",
        row_factory=dict_row
    )
