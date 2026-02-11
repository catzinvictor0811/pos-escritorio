from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QGridLayout, QMessageBox, QCompleter
)
from PyQt6.QtCore import Qt
from models.producto import Producto


class EditarProducto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Producto")
        self.setFixedSize(450, 260)

        self.producto_id = None

        layout = QGridLayout()

        # 🔹 Campo producto
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Buscar producto...")

        # 🔹 Autocompletado
        nombres = [p[1] for p in Producto.obtener_todos()]
        completer = QCompleter(nombres)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.nombre.setCompleter(completer)

        self.precio = QLineEdit()
        self.precio.setPlaceholderText("0.00")

        self.stock_actual = QLineEdit("0")
        self.stock_actual.setReadOnly(True)

        self.ajuste_stock = QLineEdit("0")

        # 🔹 Layout
        layout.addWidget(QLabel("Producto:"), 0, 0)
        layout.addWidget(self.nombre, 0, 1, 1, 3)

        layout.addWidget(QLabel("Precio:"), 1, 0)
        layout.addWidget(self.precio, 1, 1)

        layout.addWidget(QLabel("Stock actual:"), 1, 2)
        layout.addWidget(self.stock_actual, 1, 3)

        layout.addWidget(QLabel("Ajuste de stock (+/-):"), 2, 2)
        layout.addWidget(self.ajuste_stock, 2, 3)

        # 🔹 Botones
        btn_guardar = QPushButton("Guardar Cambios")
        btn_eliminar = QPushButton("Eliminar Producto")
        btn_cancelar = QPushButton("Cancelar")

        btn_guardar.clicked.connect(self.guardar_cambios)
        btn_eliminar.clicked.connect(self.eliminar_producto)
        btn_cancelar.clicked.connect(self.close)

        layout.addWidget(btn_eliminar, 3, 1)
        layout.addWidget(btn_guardar, 3, 2)
        layout.addWidget(btn_cancelar, 3, 3)

        self.setLayout(layout)

        # 🔹 Evento
        self.nombre.editingFinished.connect(self.buscar_producto)

    # -------------------------
    def buscar_producto(self):
        nombre = self.nombre.text().strip()
        if not nombre:
            return

        producto = Producto.buscar_por_nombre(nombre)
        if not producto:
            QMessageBox.warning(self, "Producto", "Producto no encontrado")
            return

        self.producto_id = producto["id"]
        self.precio.setText(str(producto["precio"]))
        self.stock_actual.setText(str(producto["stock"]))

    # -------------------------
    def guardar_cambios(self):
        if not self.producto_id:
            QMessageBox.warning(self, "Error", "Busca un producto primero")
            return

        try:
            nuevo_precio = float(self.precio.text())
            ajuste = int(self.ajuste_stock.text())

            if nuevo_precio <= 0:
                raise ValueError

            if ajuste != 0:
                Producto.ajustar_stock(self.producto_id, ajuste)

            Producto.actualizar_precio(self.producto_id, nuevo_precio)

            QMessageBox.information(
                self,
                "Producto",
                "Cambios guardados correctamente"
            )
            self.close()

        except Exception:
            QMessageBox.warning(self, "Error", "Datos inválidos")

    # -------------------------
    def eliminar_producto(self):
        if not self.producto_id:
            return

        resp = QMessageBox.question(
            self,
            "Confirmar",
            "¿Seguro que deseas eliminar este producto?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if resp == QMessageBox.StandardButton.Yes:
            Producto.desactivar(self.producto_id)
            QMessageBox.information(
                self,
                "Producto",
                "Producto eliminado correctamente"
            )
            self.close()
