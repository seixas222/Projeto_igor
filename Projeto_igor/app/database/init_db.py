
from app.database.connection import conectar


def criar_tabelas():
    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );
    """)

    conexao.commit()
    conexao.close()

    print("Tabela criada com sucesso!")


if __name__ == "__main__":
    criar_tabelas()
