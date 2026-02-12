from database.conexion import get_connection

class Caja:

    @staticmethod
    def abrir(apertura):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO caja (apertura) VALUES (?)
        """, (apertura,))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_abierta():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, apertura FROM caja WHERE estado='ABIERTA'
        """)
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def cerrar(caja_id, cierre):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE caja SET cierre=?, estado='CERRADA'
            WHERE id=?
        """, (cierre, caja_id))
        conn.commit()
        conn.close()

    @staticmethod
    def agregar_movimiento(caja_id, tipo, monto, descripcion):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO movimientos_caja (caja_id, tipo, monto, descripcion)
            VALUES (?,?,?,?)
        """, (caja_id, tipo, monto, descripcion))
        conn.commit()
        conn.close()

    @staticmethod
    def historial():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                id,
                fecha,
                apertura,
                cierre,
                (cierre - apertura) as diferencia
            FROM caja
            WHERE estado = 'CERRADA'
            ORDER BY id DESC
        """)

        datos = cursor.fetchall()
        conn.close()
        return datos

