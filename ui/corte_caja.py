from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QGridLayout, QGroupBox,
    QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from models.caja import Caja
from models.venta import Venta


class CorteCaja(QWidget):
    def __init__(self, callback_actualizar=None):
        super().__init__()
        self.setWindowTitle("Caja | Apertura y Corte")
        self.setFixedSize(680, 640)

        self.callback_actualizar = callback_actualizar
        self.caja = Caja.obtener_abierta()

        self.setStyleSheet(self.estilos())

        # Scroll para que no se corten elementos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")

        contenedor = QWidget()
        self.layout = QVBoxLayout(contenedor)
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(18)

        if not self.caja:
            self.apertura_ui()
        else:
            self.cierre_ui()

        scroll.setWidget(contenedor)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(scroll)
        self.setLayout(layout_principal)

    # ===================== ESTILOS =====================
    def estilos(self):
        return """
            QWidget {
                background-color: #f4f6fb;
                font-family: Arial;
            }

            QLabel#titulo {
                font-size: 22px;
                font-weight: bold;
                color: #111827;
                padding: 8px;
            }

            QLabel#subtitulo {
                font-size: 14px;
                color: #6b7280;
                padding-left: 10px;
                padding-bottom: 10px;
            }

            QFrame#card {
                background: white;
                border-radius: 18px;
                border: 1px solid #e5e7eb;
            }

            QLabel#cardTitle {
                font-size: 16px;
                font-weight: bold;
                color: #111827;
            }

            QLabel#dato {
                font-size: 14px;
                color: #374151;
                font-weight: bold;
            }

            QLabel#valor {
                font-size: 14px;
                font-weight: bold;
                color: #111827;
            }

            QLabel#resultado {
                font-size: 15px;
                font-weight: bold;
                padding: 12px;
                border-radius: 12px;
                background-color: #f3f4f6;
                color: #111827;
            }

            QLineEdit {
                background: #f9fafb;
                border: 1px solid #d1d5db;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #2563eb;
                background: white;
            }

            QPushButton {
                border-radius: 16px;
                padding: 14px;
                font-size: 15px;
                font-weight: bold;
                color: white;
            }

            QPushButton#btnAbrir {
                background-color: #16a34a;
            }

            QPushButton#btnAbrir:hover {
                background-color: #15803d;
            }

            QPushButton#btnCerrar {
                background-color: #dc2626;
            }

            QPushButton#btnCerrar:hover {
                background-color: #b91c1c;
            }

            QGroupBox {
                background-color: white;
                border-radius: 18px;
                border: 1px solid #e5e7eb;
                margin-top: 12px;
                font-weight: bold;
                padding: 18px;
            }

            QGroupBox:title {
                subcontrol-origin: margin;
                left: 18px;
                padding: 0 10px;
                color: #111827;
                font-size: 14px;
            }
        """

    # ===================== MENSAJES MODERNOS =====================
    def mostrar_mensaje(self, titulo, mensaje, detalle="", tipo="info"):
        msg = QMessageBox(self)

        msg.setWindowTitle(titulo)

        if tipo == "info":
            msg.setIcon(QMessageBox.Icon.Information)
        elif tipo == "warning":
            msg.setIcon(QMessageBox.Icon.Warning)
        else:
            msg.setIcon(QMessageBox.Icon.Critical)

        msg.setText(mensaje)

        if detalle:
            msg.setInformativeText(detalle)

        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        # ESTILO EXCLUSIVO PARA EL QMessageBox
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-family: Arial;
                font-size: 14px;
            }

            QLabel {
                color: #111827;
                font-size: 14px;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 12px;
                min-width: 140px;
                min-height: 38px;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        msg.exec()

    # ===================== HEADER =====================
    def header(self, titulo, subtitulo):
        lblTitulo = QLabel(titulo)
        lblTitulo.setObjectName("titulo")

        lblSub = QLabel(subtitulo)
        lblSub.setObjectName("subtitulo")

        self.layout.addWidget(lblTitulo)
        self.layout.addWidget(lblSub)

    # ===================== CARD =====================
    def crear_card(self, titulo):
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        lbl = QLabel(titulo)
        lbl.setObjectName("cardTitle")

        layout.addWidget(lbl)
        card.setLayout(layout)

        return card, layout

    # ===================== APERTURA =====================
    def apertura_ui(self):
        self.header("🟢 Apertura de Caja", "Ingresa el monto inicial para comenzar el día.")

        card, cardLayout = self.crear_card("Monto de apertura")

        self.input_apertura = QLineEdit()
        self.input_apertura.setPlaceholderText("Ejemplo: 500.00")
        self.input_apertura.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.input_apertura.setFont(font)

        self.input_apertura.setFixedHeight(45)

        cardLayout.addWidget(self.input_apertura)
        self.layout.addWidget(card)

        btn = QPushButton("Abrir Caja")
        btn.setObjectName("btnAbrir")
        btn.setFixedHeight(50)
        btn.clicked.connect(self.abrir_caja)

        self.layout.addWidget(btn)

    def abrir_caja(self):
        try:
            monto = float(self.input_apertura.text())
            if monto < 0:
                raise ValueError

            Caja.abrir(monto)

            self.mostrar_mensaje(
                "Caja",
                "✅ Caja abierta correctamente",
                f"Monto de apertura: ${monto:.2f}",
                "info"
            )

            if self.callback_actualizar:
                self.callback_actualizar()

            self.close()

        except:
            self.mostrar_mensaje(
                "Error",
                "⚠️ Monto inválido",
                "Ingresa un número válido para abrir caja.",
                "warning"
            )

    # ===================== CIERRE =====================
    def cierre_ui(self):
        caja_id, apertura = self.caja
        ventas = Venta.total_del_dia()
        self.esperado = apertura + ventas

        self.header("🔴 Corte de Caja", "Revisa el resumen del día y realiza el conteo de efectivo.")

        # -------- Resumen --------
        card, cardLayout = self.crear_card("Resumen financiero")

        grid = QGridLayout()
        grid.setSpacing(14)

        lbl1 = QLabel("Apertura:")
        lbl1.setObjectName("dato")
        grid.addWidget(lbl1, 0, 0)

        lbl_apertura = QLabel(f"${apertura:.2f}")
        lbl_apertura.setObjectName("valor")
        grid.addWidget(lbl_apertura, 0, 1)

        lbl2 = QLabel("Ventas del día:")
        lbl2.setObjectName("dato")
        grid.addWidget(lbl2, 1, 0)

        lbl_ventas = QLabel(f"${ventas:.2f}")
        lbl_ventas.setObjectName("valor")
        grid.addWidget(lbl_ventas, 1, 1)

        lbl3 = QLabel("Total esperado:")
        lbl3.setObjectName("dato")
        grid.addWidget(lbl3, 2, 0)

        lbl_total = QLabel(f"${self.esperado:.2f}")
        lbl_total.setObjectName("valor")
        grid.addWidget(lbl_total, 2, 1)

        cardLayout.addLayout(grid)
        self.layout.addWidget(card)

        # -------- Conteo efectivo --------
        self.crear_contador_efectivo()

        # -------- Resultados --------
        cardRes, layoutRes = self.crear_card("Resultado del conteo")

        self.lbl_total_real = QLabel("Efectivo real: $0.00")
        self.lbl_total_real.setObjectName("resultado")

        self.lbl_diferencia = QLabel("Diferencia: $0.00")
        self.lbl_diferencia.setObjectName("resultado")

        layoutRes.addWidget(self.lbl_total_real)
        layoutRes.addWidget(self.lbl_diferencia)

        self.layout.addWidget(cardRes)

        # -------- Botón cierre --------
        btn = QPushButton("Cerrar Caja")
        btn.setObjectName("btnCerrar")
        btn.setFixedHeight(55)
        btn.clicked.connect(lambda: self.cerrar_caja(caja_id))

        self.layout.addWidget(btn)

    # ===================== CONTADOR EFECTIVO =====================
    def crear_contador_efectivo(self):
        grupo = QGroupBox("💰 Conteo de efectivo")
        grid = QGridLayout()
        grid.setSpacing(12)

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

        lblMonedas = QLabel("🪙 Monedas")
        lblMonedas.setStyleSheet("font-size:14px; font-weight:bold; color:#111827;")

        lblBilletes = QLabel("💵 Billetes")
        lblBilletes.setStyleSheet("font-size:14px; font-weight:bold; color:#111827;")

        grid.addWidget(lblMonedas, 0, 0, 1, 2)
        grid.addWidget(lblBilletes, 0, 2, 1, 2)

        fila = 1
        for texto, valor in monedas:
            lbl = QLabel(texto)
            lbl.setStyleSheet("font-size:13px; color:#374151; font-weight:bold;")

            txt = QLineEdit("0")
            txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            txt.setFixedHeight(38)
            txt.setFixedWidth(120)

            txt.returnPressed.connect(self.siguiente_campo)
            txt.textChanged.connect(self.calcular_total_real)

            self.campos[txt] = valor
            self.orden_campos.append(txt)

            grid.addWidget(lbl, fila, 0)
            grid.addWidget(txt, fila, 1)
            fila += 1

        fila = 1
        for texto, valor in billetes:
            lbl = QLabel(texto)
            lbl.setStyleSheet("font-size:13px; color:#374151; font-weight:bold;")

            txt = QLineEdit("0")
            txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            txt.setFixedHeight(38)
            txt.setFixedWidth(120)

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

        if diferencia > 0:
            self.lbl_diferencia.setStyleSheet("""
                font-size:15px;
                font-weight:bold;
                padding:12px;
                border-radius:12px;
                background-color:#dcfce7;
                color:#166534;
            """)
        elif diferencia < 0:
            self.lbl_diferencia.setStyleSheet("""
                font-size:15px;
                font-weight:bold;
                padding:12px;
                border-radius:12px;
                background-color:#fee2e2;
                color:#991b1b;
            """)
        else:
            self.lbl_diferencia.setStyleSheet("""
                font-size:15px;
                font-weight:bold;
                padding:12px;
                border-radius:12px;
                background-color:#e0f2fe;
                color:#075985;
            """)

    # ===================== CIERRE =====================
    def cerrar_caja(self, caja_id):
        try:
            total = sum(
                float(campo.text() or 0) * valor
                for campo, valor in self.campos.items()
            )

            Caja.cerrar(caja_id, total)

            diferencia = total - self.esperado

            self.mostrar_mensaje(
                "Corte de Caja",
                "✅ Corte realizado correctamente",
                f"""
<b>Total esperado:</b> ${self.esperado:.2f}<br>
<b>Efectivo real:</b> ${total:.2f}<br>
<b>Diferencia:</b> ${diferencia:.2f}
                """,
                "info"
            )

            if self.callback_actualizar:
                self.callback_actualizar()

            self.close()

        except:
            self.mostrar_mensaje(
                "Error",
                "⚠️ Error en el conteo",
                "Verifica los valores ingresados.",
                "warning"
            )
