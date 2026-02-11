from database.conexion import get_connection

class Usuario:

    @staticmethod
    def login(usuario, password):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = ? AND password = ?",
            (usuario, password)
        )

        result = cursor.fetchone()
        conn.close()

        return result is not None
