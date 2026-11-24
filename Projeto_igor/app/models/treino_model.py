from app.db import DatabaseConnection


class Treino:

    def __init__(self, nome=None, descricao=None, usuario_id=None, id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.usuario_id = usuario_id

    def salvar(self):
        with DatabaseConnection() as db:
            db.cursor.execute("""
                INSERT INTO treinos (nome, descricao, usuario_id)
                VALUES (?, ?, ?)
            """, (self.nome, self.descricao, self.usuario_id))

            self.id = db.cursor.lastrowid

        return True

    @classmethod
    def listar_por_usuario(cls, usuario_id):
        with DatabaseConnection() as db:
            db.cursor.execute("""
                SELECT id, nome, descricao
                FROM treinos
                WHERE usuario_id = ?
                ORDER BY id DESC
            """, (usuario_id,))

            return db.cursor.fetchall()

    @classmethod
    def buscar_por_id(cls, treino_id, usuario_id):
        with DatabaseConnection() as db:
            db.cursor.execute("""
                SELECT id, nome, descricao
                FROM treinos
                WHERE id = ? AND usuario_id = ?
            """, (treino_id, usuario_id))

            resultado = db.cursor.fetchone()

        if resultado:
            return cls(
                id=resultado["id"],
                nome=resultado["nome"],
                descricao=resultado["descricao"],
                usuario_id=usuario_id
            )

        return None

    @classmethod
    def excluir(cls, treino_id, usuario_id):
        with DatabaseConnection() as db:
            db.cursor.execute("""
                DELETE FROM treinos
                WHERE id = ? AND usuario_id = ?
            """, (treino_id, usuario_id))

            return db.cursor.rowcount > 0