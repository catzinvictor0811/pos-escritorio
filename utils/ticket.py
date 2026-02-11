from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_ticket(venta_id, productos, total):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    nombre_archivo = f"ticket_venta_{venta_id}.pdf"
    c = canvas.Canvas(nombre_archivo, pagesize=A4)

    y = 800

    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, y, "TICKET DE VENTA")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Venta #: {venta_id}")
    y -= 15
    c.drawString(50, y, f"Fecha: {fecha}")
    y -= 30

    c.drawString(50, y, "Producto")
    c.drawString(300, y, "Precio")
    y -= 15

    for p in productos:
        c.drawString(50, y, p["nombre"])
        c.drawString(300, y, f"${p['precio']}")
        y -= 15

    y -= 20
    c.drawString(50, y, f"TOTAL: ${total:.2f}")

    y -= 40
    c.drawString(150, y, "Gracias por su compra")

    c.save()

    os.startfile(nombre_archivo)  # abre el PDF automáticamente
