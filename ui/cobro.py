from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton,
    QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt


class DialogCobro(QDialog):
    def __init__(self, total):
        super().__init__()
        self.setWindowTitle("Cobro")
        self.setFixedSize(300, 200)
        self.total = total
        self.confirmado = False

        layout = QGridLayout()

        lbl_total_txt = QLabel("Total a pagar:")
        lbl_total_txt.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lbl_total = QLabel(f"${total:.2f}")
        self.lbl_total.setStyleSheet("font-size:18px; font-weight:bold;")

        lbl_pago = QLabel("Efectivo:")
        self.input_pago = QLineEdit()
        self.input_pago.setPlaceholderText("0.00")
        self.input_pago.textChanged.connect(self.calcular_cambio)

        lbl_cambio_txt = QLabel("Cambio:")
        self.lbl_cambio = QLabel("$0.00")
        self.lbl_cambio.setStyleSheet("font-size:16px;")

        btn_confirmar = QPushButton("Confirmar compra")
        btn_confirmar.setStyleSheet("background-color:#27ae60; color:white;")
        btn_confirmar.clicked.connect(self.confirmar)

        layout.addWidget(lbl_total_txt, 0, 0)
        layout.addWidget(self.lbl_total, 0, 1)

        layout.addWidget(lbl_pago, 1, 0)
        layout.addWidget(self.input_pago, 1, 1)

        layout.addWidget(lbl_cambio_txt, 2, 0)
        layout.addWidget(self.lbl_cambio, 2, 1)

        layout.addWidget(btn_confirmar, 3, 0, 1, 2)

        self.setLayout(layout)
        self.input_pago.setFocus()

    # -------------------------
    def calcular_cambio(self):
        try:
            pago = float(self.input_pago.text())
        except:
            self.lbl_cambio.setText("$0.00")
            return

        cambio = pago - self.total
        if cambio < 0:
            self.lbl_cambio.setText("$0.00")
        else:
            self.lbl_cambio.setText(f"${cambio:.2f}")

    # -------------------------
    def confirmar(self):
        try:
            pago = float(self.input_pago.text())
        except:
            QMessageBox.warning(self, "Error", "Cantidad inválida")
            return

        if pago < self.total:
            QMessageBox.warning(self, "Pago insuficiente", "El efectivo no cubre el total")
            return

        self.confirmado = True
        self.accept()
