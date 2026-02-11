from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QGridLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QCompleter, QDialog, QVBoxLayout
)
from PyQt6.QtCore import Qt

from models.producto import Producto
from models.venta import Venta
from models.caja import Caja
from utils.ticket import generar_ticket


# ==========================
# 🔹 Ventana de Cobro
# ==========================
class VentanaCobro(QDialog):
    def __init__(self, total):
        super().__init__()
        self.setWindowTitle("Cobro")
        self.setFixedSize(300, 200)
        self.total = total
        self.pagado = False

        layout = QVBoxLayout()

        self.lbl_total = QLabel(f"Total a pagar: ${total:.2f}")
        self.lbl_total.setStyleSheet("font-size:16px;font-weight:bold;")
        layout.addWidget(self.lbl_total)

        layout.addWidget(QLabel("Efectivo recibido:"))
        self.txt_efectivo = QLineEdit()
        self.txt_efectivo.setPlaceholderText("0.00")
        layout.addWidget(self.txt_efectivo)

        self.lbl_cambio = QLabel("Cambio: $0.00")
        layout.addWidget(self.lbl_cambio)

        btn_confirmar = QPushButton("Confirmar compra")
        btn_confirmar.setStyleSheet("background:#27ae60;color:white;")
        layout.addWidget(btn_confirmar)

        self.setLayout(layout)

        self.txt_efectivo.textChanged.connect(self.calcular_cambio)
        btn_confirmar.clicked.connect(self.confirmar)

    def calcular_cambio(self):
        try:
            efectivo = float(self.txt_efectivo.text())
        except:
            efectivo = 0

        cambio = efectivo - self.total
        self.lbl_cambio.setText(f"Cambio: ${cambio:.2f}")

    def confirmar(self):
        try:
            efectivo = float(self.txt_efectivo.text())
        except:
            QMessageBox.warning(self, "Error", "Ingresa una cantidad válida")
            return

        if efectivo < self.total:
            QMessageBox.warning(self, "Pago insuficiente", "El efectivo no cubre el total")
            return

        self.pagado = True
        self.accept()


# ==========================
# 🔹 Ventas
# ==========================
class Ventas(QWidget):
    def __init__(self):
        super().__init__()

        # 🔴 VALIDACIÓN CRÍTICA
        self.caja = Caja.obtener_abierta()
        if not self.caja:
            QMessageBox.critical(
                self,
                "Caja cerrada",
                "No puedes realizar ventas sin abrir la caja"
            )
            self.close()
            return

        self.setWindowTitle("Ventas")
        self.setFixedSize(900, 450)

        self.productos = Producto.obtener_todos()
        self.carrito = {}  # producto_id -> data

        self.producto_seleccionado = None
        self.stock_disponible = 0

        layout = QGridLayout()

        # 🔹 Buscador
        layout.addWidget(QLabel("Producto:"), 0, 0)
        self.buscar = QLineEdit()
        self.buscar.setPlaceholderText("Buscar producto...")
        layout.addWidget(self.buscar, 0, 1)

        layout.addWidget(QLabel("Cantidad:"), 0, 2)
        self.cantidad = QLineEdit("1")
        layout.addWidget(self.cantidad, 0, 3)

        nombres = [p[1] for p in self.productos]
        completer = QCompleter(nombres)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.buscar.setCompleter(completer)

        # 🔹 Tabla
        self.tabla = QTableWidget(0, 4)
        self.tabla.setHorizontalHeaderLabels(
            ["Producto", "Precio", "Cantidad", "Total"]
        )
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.cellDoubleClicked.connect(self.eliminar_producto_carrito)
        layout.addWidget(self.tabla, 1, 0, 1, 4)

        self.lbl_subtotal = QLabel("Subtotal: $0.00")
        self.lbl_total = QLabel("Total: $0.00")
        self.lbl_total.setStyleSheet("font-size:16px;font-weight:bold;")

        layout.addWidget(self.lbl_subtotal, 2, 2)
        layout.addWidget(self.lbl_total, 4, 2)

        btn_cancelar = QPushButton("Cancelar Venta")
        btn_cancelar.setStyleSheet("background:#c0392b;color:white;")
        btn_cancelar.clicked.connect(self.close)

        btn_cobrar = QPushButton("Cobrar")
        btn_cobrar.setStyleSheet("background:#27ae60;color:white;")
        btn_cobrar.clicked.connect(self.cobrar)

        layout.addWidget(btn_cancelar, 5, 2)
        layout.addWidget(btn_cobrar, 5, 3)

        self.setLayout(layout)

        self.buscar.editingFinished.connect(self.seleccionar_producto)
        self.cantidad.returnPressed.connect(self.agregar_producto)

    # -------------------------
    def seleccionar_producto(self):
        nombre = self.buscar.text().strip().lower()
        self.producto_seleccionado = None

        for p in self.productos:
            if p[1].lower() == nombre:
                self.producto_seleccionado = p
                self.stock_disponible = p[3]
                self.cantidad.setFocus()
                self.cantidad.selectAll()
                return

    # -------------------------
    def agregar_producto(self):
        if not self.producto_seleccionado:
            return

        try:
            cantidad = int(self.cantidad.text())
        except:
            return

        if cantidad <= 0 or cantidad > self.stock_disponible:
            QMessageBox.warning(self, "Stock", "Cantidad inválida")
            return

        p = self.producto_seleccionado
        pid = p[0]

        if pid in self.carrito:
            self.carrito[pid]["cantidad"] += cantidad
            fila = self.carrito[pid]["fila"]
        else:
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)
            self.carrito[pid] = {
                "producto": p,
                "cantidad": cantidad,
                "fila": fila
            }

        cant_total = self.carrito[pid]["cantidad"]
        total = cant_total * p[2]

        self.tabla.setItem(fila, 0, QTableWidgetItem(p[1]))
        self.tabla.setItem(fila, 1, QTableWidgetItem(f"${p[2]:.2f}"))
        self.tabla.setItem(fila, 2, QTableWidgetItem(str(cant_total)))
        self.tabla.setItem(fila, 3, QTableWidgetItem(f"${total:.2f}"))

        self.actualizar_totales()
        self.buscar.clear()
        self.cantidad.setText("1")
        self.buscar.setFocus()
        self.producto_seleccionado = None

    # -------------------------
    def eliminar_producto_carrito(self, fila, columna):
        pid = list(self.carrito.keys())[fila]
        del self.carrito[pid]
        self.tabla.removeRow(fila)
        self.reordenar_filas()
        self.actualizar_totales()

    def reordenar_filas(self):
        for i, pid in enumerate(self.carrito):
            self.carrito[pid]["fila"] = i

    def actualizar_totales(self):
        total = sum(
            v["producto"][2] * v["cantidad"]
            for v in self.carrito.values()
        )
        self.lbl_subtotal.setText(f"Subtotal: ${total:.2f}")
        self.lbl_total.setText(f"Total: ${total:.2f}")

    # -------------------------
    def cobrar(self):
        # 🔴 Validar caja otra vez
        caja = Caja.obtener_abierta()
        if not caja:
            QMessageBox.critical(self, "Caja cerrada", "La caja fue cerrada")
            return

        if not self.carrito:
            return

        total = sum(
            v["producto"][2] * v["cantidad"]
            for v in self.carrito.values()
        )

        dialogo = VentanaCobro(total)
        if not dialogo.exec() or not dialogo.pagado:
            return

        venta_id = Venta.crear(total)

        for v in self.carrito.values():
            p = v["producto"]
            cant = v["cantidad"]
            Venta.agregar_detalle(venta_id, p[0], cant, p[2])
            Producto.descontar_stock(p[0], cant)

        # 🔹 Registrar movimiento en caja
        Caja.agregar_movimiento(
            caja_id=caja[0],
            tipo="VENTA",
            monto=total,
            descripcion=f"Venta #{venta_id}"
        )

        generar_ticket(
            venta_id,
            [{"nombre": v["producto"][1], "precio": v["producto"][2]} for v in self.carrito.values()],
            total
        )

        QMessageBox.information(self, "Venta", "Venta realizada con éxito")
        self.close()
