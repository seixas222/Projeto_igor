from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.models.treino_model import Treino

# Cria as rotas responsáveis pelo gerenciamento de treinos
treino_bp = Blueprint("treino", __name__, url_prefix="/treinos")


# Página que cadastra e lista os treinos
@treino_bp.route("/", methods=["GET", "POST"])
def listar():

    # Verifica se o formulário foi enviado
    if request.method == "POST":

        # Recebe os dados digitados no formulário
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()

        # Verifica se o nome foi preenchido
        if not nome:
            flash("Informe o nome do treino.", "danger")
        else:
            # Cria o objeto associado ao usuário logado
            treino = Treino(
                nome=nome,
                descricao=descricao,
                usuario_id=g.usuario.id
            )

            # Salva o treino no banco
            treino.salvar()
            flash("Treino cadastrado com sucesso!", "success")

        return redirect(url_for("treino.listar"))

    # Busca somente os treinos do usuário logado
    treinos = Treino.listar_por_usuario(g.usuario.id)

    # Envia os dados para a página HTML
    return render_template("treinos.html", treinos=treinos)


# Rota responsável por excluir um treino
@treino_bp.route("/excluir/<int:treino_id>", methods=["POST"])
def excluir(treino_id):

    # Exclui apenas se o treino pertencer ao usuário logado
    excluido = Treino.excluir(treino_id, g.usuario.id)

    if excluido:
        flash("Treino excluído com sucesso!", "success")
    else:
        flash("Treino não encontrado.", "danger")

    return redirect(url_for("treino.listar"))