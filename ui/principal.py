from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton,
    QHBoxLayout, QFrame
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from ui.ventas import Ventas
from ui.corte_caja import CorteCaja
from ui.alta_producto import AltaProducto
from ui.editar_producto import EditarProducto
from ui.historial_cortes import HistorialCortes


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POS - Principal")

        # 🔹 Ventana grande
        self.setFixedSize(900, 650)

        main = QVBoxLayout()
        main.setSpacing(18)
        main.setContentsMargins(20, 20, 20, 20)

        # ================= ENCABEZADO =================
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-bottom: 1px solid #ddd;
                padding: 15px;
            }
        """)

        header_layout = QVBoxLayout()

        titulo = QLabel("MI NEGOCIO")
        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #333;
        """)

        subtitulo = QLabel("Tel: 123-456-7890   |   Dirección del negocio")
        subtitulo.setStyleSheet("""
            font-size: 14px;
            color: #666;
        """)

        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)
        header.setLayout(header_layout)

        main.addWidget(header)

        # ================= BOTONES =================
        main.addWidget(
            self.boton_pos(
                "Nueva Venta",
                "assets/venta.png",
                "#43a047",
                "#66bb6a",
                self.abrir_ventas
            )
        )

        main.addWidget(
            self.boton_pos(
                "Abrir y Corte de Caja",
                "assets/caja.jpg",
                "#1e88e5",
                "#64b5f6",
                self.abrir_corte
            )
        )

        main.addWidget(
            self.boton_pos(
                "Historial de Cortes",
                "assets/historial.png",  # 🔹 agrega esta imagen
                "#d81b60",
                "#f06292",
                self.abrir_historial
            )
        )

        main.addWidget(
            self.boton_pos(
                "Alta de Producto",
                "assets/alta.png",
                "#fb8c00",
                "#ffb74d",
                self.abrir_alta_producto
            )
        )

        main.addWidget(
            self.boton_pos(
                "Editar Producto",
                "assets/editar.jpg",
                "#7e57c2",
                "#b39ddb",
                self.abrir_editar_producto
            )
        )

        main.addStretch()
        self.setLayout(main)

    # ================= BOTÓN TIPO TARJETA =================
    def boton_pos(self, texto, icono, c1, c2, accion):
        btn = QPushButton()
        btn.setFixedHeight(70)
        btn.clicked.connect(accion)

        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {c1}, stop:1 {c2}
                );
                border-radius: 14px;
            }}
            QPushButton:hover {{
                opacity: 0.94;
            }}
        """)

        layout = QHBoxLayout(btn)
        layout.setContentsMargins(20, 0, 0, 0)
        layout.setSpacing(20)

        # -------- ICONO --------
        icono_lbl = QLabel()
        pix = QPixmap(icono)
        icono_lbl.setPixmap(
            pix.scaled(
                40, 40,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        icono_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icono_lbl.setFixedSize(55, 55)
        icono_lbl.setStyleSheet("""
            QLabel {
                background-color: white;
                border-radius: 27px;
            }
        """)

        # -------- TEXTO --------
        texto_lbl = QLabel(texto)
        texto_lbl.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }
        """)
        texto_lbl.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(icono_lbl)
        layout.addWidget(texto_lbl)
        layout.addStretch()

        return btn

    # ================= ACCIONES =================
    def abrir_ventas(self):
        self.v = Ventas()
        self.v.show()

    def abrir_corte(self):
        self.c = CorteCaja()
        self.c.show()

    def abrir_historial(self):
        self.h = HistorialCortes()
        self.h.show()

    def abrir_alta_producto(self):
        self.ap = AltaProducto()
        self.ap.show()

    def abrir_editar_producto(self):
        self.ep = EditarProducto()
        self.ep.show()
