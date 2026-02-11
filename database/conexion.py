import sqlite3
from init_db import obtener_ruta_db


def get_connection():
    return sqlite3.connect(obtener_ruta_db())
