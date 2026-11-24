from app.db import DatabaseConnection


class Exercicio:

    # Construtor: recebe os dados de um exercício
    def __init__(
        self,
        nome=None,
        grupo_muscular=None,
        series=None,
        repeticoes=None,
        usuario_id=None,
        treino_id=None,
        id=None
    ):
        self.id = id
        self.nome = nome
        self.grupo_muscular = grupo_muscular
        self.series = series
        self.repeticoes = repeticoes
        self.usuario_id = usuario_id
        self.treino_id = treino_id

    # Cadastra um exercício no banco de dados
    def salvar(self):
        with DatabaseConnection() as db:

            db.cursor.execute("""
                INSERT INTO exercicios
                (nome, grupo_muscular, series, repeticoes, usuario_id, treino_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self.nome,
                self.grupo_muscular,
                self.series,
                self.repeticoes,
                self.usuario_id,
                self.treino_id
            ))

            # Guarda o ID gerado pelo banco
            self.id = db.cursor.lastrowid

        return True

    # Lista somente os exercícios do usuário logado
    @classmethod
    def listar_por_usuario(cls, usuario_id):
        with DatabaseConnection() as db:

            db.cursor.execute("""
                SELECT id, nome, grupo_muscular, series, repeticoes, treino_id
                FROM exercicios
                WHERE usuario_id = ?
                ORDER BY id DESC
            """, (usuario_id,))

            return db.cursor.fetchall()

    # Exclui um exercício verificando se pertence ao usuário
    @classmethod
    def excluir(cls, exercicio_id, usuario_id):
        with DatabaseConnection() as db:

            db.cursor.execute("""
                DELETE FROM exercicios
                WHERE id = ? AND usuario_id = ?
            """, (exercicio_id, usuario_id))

            # Informa se algum registro foi excluído
            return db.cursor.rowcount > 0