
from functools import wraps
from flask import session, redirect, url_for, g, request
from app.models.user_model import Usuario


def auth_middleware():

    rotas_publicas = [
        "auth.login",
        "auth.cadastro",
        "static"
    ]

        # Permite acessar páginas públicas e endereços que não existem
    if request.endpoint is None or request.endpoint in rotas_publicas:
        return

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("auth.login"))

    usuario = Usuario.buscar_por_id(user_id)

    if usuario is None:
        session.clear()
        return redirect(url_for("auth.login"))

    g.usuario = usuario


def login_required(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):

        if not getattr(g, "usuario", None):
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return decorated_function
