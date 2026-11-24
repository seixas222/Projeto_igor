
import sqlite3
from pathlib import Path

# Caminho do banco de dados
DB_PATH = Path(__file__).resolve().parents[1] / "banco.db"


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row

    return conexao
