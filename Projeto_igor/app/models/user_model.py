
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import DatabaseConnection
import sqlite3


class Usuario:

    def __init__(self, username=None, senha=None, id=None):
        self.id = id
        self.username = username
        self.senha = senha

    def salvar(self):
        senha_hash = generate_password_hash(self.senha)

        try:
            with DatabaseConnection() as db:
                db.cursor.execute("""
                    INSERT INTO usuarios (username, senha)
                    VALUES (?, ?)
                """, (self.username, senha_hash))

            return True

        except sqlite3.IntegrityError:
            return False

    @classmethod
    def buscar_por_username(cls, username):
        with DatabaseConnection() as db:
            db.cursor.execute("""
                SELECT id, username, senha
                FROM usuarios
                WHERE username = ?
            """, (username,))

            resultado = db.cursor.fetchone()

        if resultado:
            usuario = cls(
                username=resultado["username"],
                id=resultado["id"]
            )
            usuario.senha = resultado["senha"]
            return usuario

        return None

    @classmethod
    def buscar_por_id(cls, user_id):
        with DatabaseConnection() as db:
            db.cursor.execute("""
                SELECT id, username
                FROM usuarios
                WHERE id = ?
            """, (user_id,))

            resultado = db.cursor.fetchone()

        if resultado:
            return cls(
                username=resultado["username"],
                id=resultado["id"]
            )

        return None

    @classmethod
    def verificar(cls, username, senha):
        usuario = cls.buscar_por_username(username)

        if usuario is None:
            return False

        return check_password_hash(usuario.senha, senha)

    @classmethod
    def listar(cls):
        with DatabaseConnection() as db:
            db.cursor.execute("""
                SELECT id, username
                FROM usuarios
                ORDER BY id ASC
            """)

            return db.cursor.fetchall()
