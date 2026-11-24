from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, make_response
)

from app.models.user_model import Usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# Rota responsável pelo login do usuário
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Recupera o último usuário salvo no cookie do navegador
    usuario_salvo = request.cookies.get("usuario_salvo", "")

    if request.method == "POST":

        # Recebe os dados enviados pelo formulário
        username = request.form.get("username", "").strip()
        senha = request.form.get("password", "")

        # Busca o usuário no banco de dados
        usuario = Usuario.buscar_por_username(username)

        # Verifica se o usuário e a senha estão corretos
        if usuario and Usuario.verificar(username, senha):

            # Limpa os dados antigos da sessão
            session.clear()

            # Salva os dados do usuário na sessão
            session["user_id"] = usuario.id
            session["username"] = usuario.username

            flash("Login realizado com sucesso!", "success")

            # Cria a resposta de redirecionamento
            resposta = make_response(
                redirect(url_for("auth.home"))
            )

            # Salva o nome do usuário em um cookie por 30 dias
            resposta.set_cookie(
                "usuario_salvo",
                username,
                max_age=60 * 60 * 24 * 30,
                httponly=True,
                samesite="Lax"
            )

            return resposta

        # Mensagem exibida quando os dados estão incorretos
        flash("Usuário ou senha incorretos.", "danger")

    # Abre a página de login com o usuário lembrado, se existir
    return render_template(
        "login.html",
        usuario_salvo=usuario_salvo
    )


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        senha = request.form.get("senha", "")

        if not username or not senha:
            flash("Preencha todos os campos.", "danger")
            return render_template("cadastro.html")

        if len(username) < 3 or len(username) > 30:
            flash("O usuário deve ter entre 3 e 30 caracteres.", "danger")
            return render_template("cadastro.html")

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "danger")
            return render_template("cadastro.html")

        usuario = Usuario(username=username, senha=senha)

        if usuario.salvar():
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("auth.login"))

        flash("Esse usuário já está cadastrado.", "danger")

    return render_template("cadastro.html")


@auth_bp.route("/home")
def home():

    return render_template(
        "home.html",
        usuario=session.get("username")
    )


@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Você saiu do sistema.", "info")

    return redirect(url_for("auth.login"))


@auth_bp.route("/usuarios")
def usuarios():

    lista_usuarios = Usuario.listar()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
    )

