from database.conexion import get_connection


class Producto:

    # 🔹 Obtener solo productos activos (Ventas)
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, precio, stock
            FROM productos
            WHERE activo = 1
            ORDER BY nombre
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    # 🔹 Obtener solo nombres (Autocompletado)
    @staticmethod
    def obtener_nombres():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre
            FROM productos
            WHERE activo = 1
            ORDER BY nombre
        """)
        data = cursor.fetchall()
        conn.close()
        return [row[0] for row in data]

    # 🔹 Crear producto (AltaProducto)
    @staticmethod
    def crear(nombre, precio, stock=0):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO productos (nombre, precio, stock, activo)
            VALUES (?,?,?,1)
            """,
            (nombre, precio, stock)
        )
        conn.commit()
        conn.close()

    # 🔹 Descontar stock (Ventas)
    @staticmethod
    def descontar_stock(producto_id, cantidad):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos
            SET stock = stock - ?
            WHERE id = ? AND stock >= ? AND activo = 1
        """, (cantidad, producto_id, cantidad))
        conn.commit()

        actualizado = cursor.rowcount
        conn.close()
        return actualizado > 0

    # 🔹 Buscar producto activo por nombre EXACTO
    @staticmethod
    def buscar_por_nombre(nombre):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, precio, stock
            FROM productos
            WHERE nombre = ? AND activo = 1
        """, (nombre,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row[0],
                "nombre": row[1],
                "precio": row[2],
                "stock": row[3]
            }
        return None

    # 🔹 Obtener precio (Ventas)
    @staticmethod
    def obtener_precio(producto_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT precio
            FROM productos
            WHERE id = ? AND activo = 1
        """, (producto_id,))
        data = cursor.fetchone()
        conn.close()
        return data[0] if data else None

    # 🔹 Actualizar precio (EditarProducto)
    @staticmethod
    def actualizar_precio(producto_id, precio):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos
            SET precio = ?
            WHERE id = ? AND activo = 1
        """, (precio, producto_id))
        conn.commit()
        conn.close()

    # 🔹 Ajustar stock (+ / -) (EditarProducto)
    @staticmethod
    def ajustar_stock(producto_id, cantidad):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos
            SET stock = stock + ?
            WHERE id = ? AND activo = 1
        """, (cantidad, producto_id))
        conn.commit()
        conn.close()

    # 🔹 Aumentar stock (AltaProducto)
    @staticmethod
    def actualizar_stock(producto_id, cantidad):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos
            SET stock = stock + ?
            WHERE id = ? AND activo = 1
        """, (cantidad, producto_id))
        conn.commit()
        conn.close()

    # 🔹 Eliminación lógica (EditarProducto)
    @staticmethod
    def desactivar(producto_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET activo = 0 WHERE id = ?",
            (producto_id,)
        )
        conn.commit()
        conn.close()
