from PyQt6.QtCore import Qt


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem
)
from models.caja import Caja


class HistorialCortes(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial de Cortes")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()

        titulo = QLabel("📊 Historial de Cortes de Caja")
        titulo.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(titulo)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Fecha", "Apertura", "Cierre", "Diferencia"
        ])

        self.cargar_datos()

        layout.addWidget(self.tabla)
        self.setLayout(layout)

    def cargar_datos(self):
        datos = Caja.historial()

        self.tabla.setRowCount(len(datos))

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QTableWidgetItem(str(valor))

                # Colorear diferencia
                if columna == 4:
                    if float(valor) < 0:
                        item.setForeground(Qt.GlobalColor.red)
                    else:
                        item.setForeground(Qt.GlobalColor.darkGreen)

                self.tabla.setItem(fila, columna, item)

        self.tabla.resizeColumnsToContents()
