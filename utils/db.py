import os
import sys

def ruta_base():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def ruta_db():
    carpeta = os.path.join(ruta_base(), "data")
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, "pos.db")
