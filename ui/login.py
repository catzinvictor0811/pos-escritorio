from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from ui.principal import VentanaPrincipal
from models.usuario import Usuario
from init_db import inicializar_db


class Login(QWidget):
    def __init__(self):
        super().__init__()

        # 🔒 Asegurar que la BD exista ANTES de cualquier login
        inicializar_db()

        self.setWindowTitle("POS - Login")
        self.setFixedSize(300, 200)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        btn = QPushButton("Entrar")
        btn.clicked.connect(self.validar)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Inicio de sesión"))
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(btn)

        self.setLayout(layout)

    def validar(self):
        user = self.user_input.text().strip()
        pwd = self.pass_input.text().strip()

        if not user or not pwd:
            QMessageBox.warning(
                self,
                "Datos incompletos",
                "Ingrese usuario y contraseña"
            )
            return

        try:
            if Usuario.login(user, pwd):
                self.ventana = VentanaPrincipal()
                self.ventana.show()
                self.close()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Credenciales incorrectas"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error crítico",
                f"Ocurrió un error inesperado:\n{e}"
            )
