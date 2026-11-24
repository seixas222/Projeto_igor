from flask import Flask, render_template, redirect, url_for

# Importa o Controller de autenticação
from app.controllers.auth_controller import auth_bp

# Importa os Controllers de treinos e exercícios
from app.controllers.treino_controller import treino_bp
from app.controllers.exercicio_controller import exercicio_bp

# Importa o middleware de autenticação
from app.utils.auth_middleware import auth_middleware


# Cria a aplicação Flask
app = Flask(
    __name__,
    template_folder="views",
    static_folder="static"
)

# Define a chave utilizada para proteger as sessões
app.secret_key = "chave-secreta-trocar-depois"


# Registra as rotas de autenticação
app.register_blueprint(auth_bp)

# Registra as rotas de treinos
app.register_blueprint(treino_bp)

# Registra as rotas de exercícios
app.register_blueprint(exercicio_bp)


# Executa o middleware antes de cada requisição
app.before_request(auth_middleware)

# Redireciona a página inicial para o login
@app.route("/")
def inicio():
    return redirect(url_for("auth.login"))


# Trata páginas que não existem (erro 404)
@app.errorhandler(404)
def pagina_nao_encontrada(erro):

    # Registra o erro no log do Flask
    app.logger.warning("Página não encontrada: %s", erro)

    return render_template("404.html"), 404