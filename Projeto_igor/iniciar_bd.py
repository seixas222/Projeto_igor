from app.db import DatabaseConnection
from app.models.user_model import Usuario


def criar_tabelas():
    with DatabaseConnection() as db:

        # Tabela de usuários
        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        """)

        # Tabela de treinos
        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS treinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)

        # Tabela de exercícios
        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS exercicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                grupo_muscular TEXT NOT NULL,
                series INTEGER NOT NULL,
                repeticoes INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                treino_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (treino_id)
                    REFERENCES treinos(id) ON DELETE CASCADE
            )
        """)


def criar_usuario_inicial():
    usuario = Usuario(
        username="admin",
        senha="admin123"
    )

    if usuario.salvar():
        print("Usuário inicial criado!")
    else:
        print("Usuário inicial já existe.")


if __name__ == "__main__":
    criar_tabelas()
    criar_usuario_inicial()

    print("Banco de dados inicializado!")