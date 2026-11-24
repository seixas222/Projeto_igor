from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.models.exercicio_model import Exercicio
from app.models.treino_model import Treino

# Cria as rotas de gerenciamento dos exercícios
exercicio_bp = Blueprint(
    "exercicio",
    __name__,
    url_prefix="/exercicios"
)


# Rota para cadastrar e listar exercícios
@exercicio_bp.route("/", methods=["GET", "POST"])
def listar():

    # Verifica se o formulário foi enviado
    if request.method == "POST":

        # Recebe os dados preenchidos pelo usuário
        nome = request.form.get("nome", "").strip()
        grupo = request.form.get("grupo_muscular", "").strip()
        series = request.form.get("series", "")
        repeticoes = request.form.get("repeticoes", "")
        treino_id = request.form.get("treino_id", "")

        # Verifica se todos os campos foram preenchidos
        if not all([nome, grupo, series, repeticoes, treino_id]):
            flash("Preencha todos os campos.", "danger")

        else:
            try:
                # Converte os valores numéricos
                series = int(series)
                repeticoes = int(repeticoes)
                treino_id = int(treino_id)

                # Verifica se o treino pertence ao usuário logado
                treino = Treino.buscar_por_id(
                    treino_id,
                    g.usuario.id
                )

                if not treino:
                    flash("Treino inválido.", "danger")

                elif series <= 0 or repeticoes <= 0:
                    flash("Séries e repetições devem ser maiores que zero.", "danger")

                else:
                    # Cria o exercício vinculado ao usuário e ao treino
                    exercicio = Exercicio(
                        nome=nome,
                        grupo_muscular=grupo,
                        series=series,
                        repeticoes=repeticoes,
                        usuario_id=g.usuario.id,
                        treino_id=treino_id
                    )

                    # Salva o exercício no banco de dados
                    exercicio.salvar()
                    flash("Exercício cadastrado com sucesso!", "success")

            except ValueError:
                flash("Informe valores numéricos válidos.", "danger")

        return redirect(url_for("exercicio.listar"))

    # Busca os exercícios e treinos do usuário logado
    exercicios = Exercicio.listar_por_usuario(g.usuario.id)
    treinos = Treino.listar_por_usuario(g.usuario.id)

    # Envia as informações para a página HTML
    return render_template(
        "exercicios.html",
        exercicios=exercicios,
        treinos=treinos
    )


# Rota para excluir um exercício
@exercicio_bp.route("/excluir/<int:exercicio_id>", methods=["POST"])
def excluir(exercicio_id):

    # Exclui somente se o exercício pertencer ao usuário logado
    excluido = Exercicio.excluir(
        exercicio_id,
        g.usuario.id
    )

    if excluido:
        flash("Exercício excluído com sucesso!", "success")
    else:
        flash("Exercício não encontrado.", "danger")

    return redirect(url_for("exercicio.listar"))