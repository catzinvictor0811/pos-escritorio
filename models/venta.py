from database.conexion import get_connection
from models.caja import Caja


class Venta:

    @staticmethod
    def crear(total):
        conn = get_connection()
        cursor = conn.cursor()

        # 🔴 OBLIGATORIO: debe haber caja abierta
        caja = Caja.obtener_abierta()
        if not caja:
            conn.close()
            raise Exception("No hay caja abierta")

        caja_id = caja[0]

        cursor.execute(
            "INSERT INTO ventas (total, caja_id) VALUES (?, ?)",
            (total, caja_id)
        )

        venta_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return venta_id

    @staticmethod
    def agregar_detalle(venta_id, producto_id, cantidad, precio):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO venta_detalle (venta_id, producto_id, cantidad, precio)
            VALUES (?,?,?,?)
        """, (venta_id, producto_id, cantidad, precio))
        conn.commit()
        conn.close()

    # 🔹 TOTAL SOLO DE LA CAJA ABIERTA
    @staticmethod
    def total_del_dia():
        conn = get_connection()
        cursor = conn.cursor()

        caja = Caja.obtener_abierta()
        if not caja:
            conn.close()
            return 0

        caja_id = caja[0]

        cursor.execute("""
            SELECT IFNULL(SUM(total), 0)
            FROM ventas
            WHERE caja_id = ?
        """, (caja_id,))

        total = cursor.fetchone()[0]
        conn.close()
        return total

