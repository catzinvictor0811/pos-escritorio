from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QGridLayout, QMessageBox
)
from models.producto import Producto


class AltaProducto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alta de Producto")
        self.setFixedSize(400, 220)

        layout = QGridLayout()

        # 🔹 Campos
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Ej. Camisa Azul")

        self.precio = QLineEdit()
        self.precio.setPlaceholderText("0.00")

        self.stock = QLineEdit()
        self.stock.setText("0")

        # 🔹 Etiquetas
        layout.addWidget(QLabel("Nombre del Producto:"), 0, 0)
        layout.addWidget(self.nombre, 0, 1, 1, 2)

        layout.addWidget(QLabel("Precio:"), 1, 0)
        layout.addWidget(self.precio, 1, 1)

        layout.addWidget(QLabel("Stock Inicial:"), 2, 0)
        layout.addWidget(self.stock, 2, 1)

        # 🔹 Botones
        btn_cancelar = QPushButton("Cancelar")
        btn_guardar = QPushButton("Guardar")

        btn_cancelar.clicked.connect(self.close)
        btn_guardar.clicked.connect(self.guardar)

        layout.addWidget(btn_cancelar, 4, 1)
        layout.addWidget(btn_guardar, 4, 2)

        self.setLayout(layout)

    # -------------------------
    def guardar(self):
        try:
            nombre = self.nombre.text().strip()
            precio = float(self.precio.text())
            stock = int(self.stock.text())

            if not nombre or precio <= 0 or stock < 0:
                raise ValueError

            Producto.crear(nombre, precio, stock)

            QMessageBox.information(
                self,
                "Producto",
                "Producto dado de alta correctamente"
            )
            self.close()

        except Exception:
            QMessageBox.warning(
                self,
                "Error",
                "Verifica los datos ingresados"
            )
