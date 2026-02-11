from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QGridLayout, QGroupBox
)
from PyQt6.QtCore import Qt
from models.caja import Caja
from models.venta import Venta


class CorteCaja(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Corte de Caja")
        self.setFixedSize(520, 550)

        self.caja = Caja.obtener_abierta()
        self.layout = QVBoxLayout()

        if not self.caja:
            self.apertura_ui()
        else:
            self.cierre_ui()

        self.setLayout(self.layout)

    # ===================== APERTURA =====================
    def apertura_ui(self):
        self.layout.addWidget(QLabel("🟢 Apertura de Caja"))

        self.input_apertura = QLineEdit()
        self.input_apertura.setPlaceholderText("Monto de apertura")
        self.layout.addWidget(self.input_apertura)

        btn = QPushButton("Abrir Caja")
        btn.clicked.connect(self.abrir_caja)
        self.layout.addWidget(btn)

    def abrir_caja(self):
        try:
            monto = float(self.input_apertura.text())
            if monto < 0:
                raise ValueError

            Caja.abrir(monto)
            QMessageBox.information(self, "Caja", "Caja abierta correctamente")
            self.close()
        except:
            QMessageBox.warning(self, "Error", "Monto inválido")

    # ===================== CIERRE =====================
    def cierre_ui(self):
        caja_id, apertura = self.caja
        ventas = Venta.total_del_dia()
        self.esperado = apertura + ventas

        self.layout.addWidget(QLabel("🔴 Cierre de Caja"))
        self.layout.addWidget(QLabel(f"Apertura: ${apertura:.2f}"))
        self.layout.addWidget(QLabel(f"Ventas del día: ${ventas:.2f}"))
        self.layout.addWidget(QLabel(f"Total esperado: ${self.esperado:.2f}"))

        self.crear_contador_efectivo()

        self.lbl_total_real = QLabel("Efectivo real: $0.00")
        self.lbl_diferencia = QLabel("Diferencia: $0.00")
        self.lbl_diferencia.setStyleSheet("font-weight:bold;")

        self.layout.addWidget(self.lbl_total_real)
        self.layout.addWidget(self.lbl_diferencia)

        btn = QPushButton("Cerrar Caja")
        btn.clicked.connect(lambda: self.cerrar_caja(caja_id))
        self.layout.addWidget(btn)

    # ===================== CONTADOR EFECTIVO =====================
    def crear_contador_efectivo(self):
        grupo = QGroupBox("💰 Conteo de efectivo")
        grid = QGridLayout()

        self.campos = {}
        self.orden_campos = []

        monedas = [
            ("$0.50", 0.5),
            ("$1", 1),
            ("$2", 2),
            ("$5", 5),
            ("$10", 10),
        ]

        billetes = [
            ("$20", 20),
            ("$50", 50),
            ("$100", 100),
            ("$200", 200),
            ("$500", 500),
            ("$1000", 1000),
        ]

        grid.addWidget(QLabel("🪙 Monedas"), 0, 0, 1, 2)
        grid.addWidget(QLabel("💵 Billetes"), 0, 2, 1, 2)

        # -------- MONEDAS (izquierda) --------
        fila = 1
        for texto, valor in monedas:
            lbl = QLabel(texto)
            txt = QLineEdit("0")
            txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            txt.returnPressed.connect(self.siguiente_campo)
            txt.textChanged.connect(self.calcular_total_real)

            self.campos[txt] = valor
            self.orden_campos.append(txt)

            grid.addWidget(lbl, fila, 0)
            grid.addWidget(txt, fila, 1)
            fila += 1

        # -------- BILLETES (derecha) --------
        fila = 1
        for texto, valor in billetes:
            lbl = QLabel(texto)
            txt = QLineEdit("0")
            txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            txt.returnPressed.connect(self.siguiente_campo)
            txt.textChanged.connect(self.calcular_total_real)

            self.campos[txt] = valor
            self.orden_campos.append(txt)

            grid.addWidget(lbl, fila, 2)
            grid.addWidget(txt, fila, 3)
            fila += 1

        grupo.setLayout(grid)
        self.layout.addWidget(grupo)

    # ===================== ENTER -> SIGUIENTE =====================
    def siguiente_campo(self):
        actual = self.sender()
        try:
            idx = self.orden_campos.index(actual)
            if idx + 1 < len(self.orden_campos):
                self.orden_campos[idx + 1].setFocus()
                self.orden_campos[idx + 1].selectAll()
        except:
            pass

    # ===================== CALCULOS =====================
    def calcular_total_real(self):
        total = 0
        try:
            for campo, valor in self.campos.items():
                cantidad = float(campo.text() or 0)
                total += cantidad * valor
        except:
            return

        diferencia = total - self.esperado

        self.lbl_total_real.setText(f"Efectivo real: ${total:.2f}")
        self.lbl_diferencia.setText(f"Diferencia: ${diferencia:.2f}")

        color = "green" if diferencia >= 0 else "red"
        self.lbl_diferencia.setStyleSheet(
            f"color:{color};font-weight:bold;"
        )

    # ===================== CIERRE =====================
    def cerrar_caja(self, caja_id):
        try:
            total = sum(
                float(campo.text() or 0) * valor
                for campo, valor in self.campos.items()
            )

            Caja.cerrar(caja_id, total)

            QMessageBox.information(
                self,
                "Corte de Caja",
                f"""
Total esperado: ${self.esperado:.2f}
Efectivo real: ${total:.2f}
Diferencia: ${total - self.esperado:.2f}
"""
            )
            self.close()
        except:
            QMessageBox.warning(self, "Error", "Error en el conteo")
