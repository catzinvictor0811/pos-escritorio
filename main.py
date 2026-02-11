import sys
import multiprocessing
from PyQt6.QtWidgets import QApplication

from init_db import inicializar_db
from ui.login import Login


def main():
    # Inicializar base de datos SIEMPRE al arrancar
    inicializar_db()

    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # Necesario para PyInstaller en Windows
    multiprocessing.freeze_support()
    main()
