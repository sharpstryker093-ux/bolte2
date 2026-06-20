import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
import database as db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "troque-essa-chave-em-producao")

EMPRESA = {
    "nome": "Bolte",
    "slogan": "Energia que transforma marcas em movimento.",
    "telefone": "(00) 00000-0000",
    "email": "contato@bolte.com.br",
    "endereco": "Endereço da empresa aqui",
}


class CurrentUser:
    """Representa o usuário logado (ou visitante) dentro dos templates."""

    def __init__(self, row=None):
        self.row = row

    @property
    def is_authenticated(self):
        return self.row is not None

    @property
    def name(self):
        return self.row["name"] if self.row else None

    @property
    def is_admin(self):
        return bool(self.row["is_admin"]) if self.row else False


@app.context_processor
def inject_current_user():
    user_id = session.get("user_id")
    row = db.get_user_by_id(user_id) if user_id else None
    return {"current_user": CurrentUser(row)}


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Faça login para acessar esta página.", "erro")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped


@app.route("/")
def home():
    servicos = db.list_services()[:3]
    return render_template("home.html", empresa=EMPRESA, servicos=servicos)


@app.route("/sobre")
def sobre():
    return render_template("sobre.html", empresa=EMPRESA)


@app.route("/servicos")
def servicos():
    lista = db.list_services()
    return render_template("servicos.html", empresa=EMPRESA, servicos=lista)


@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        mensagem = request.form.get("mensagem", "").strip()

        if not nome or not email or not mensagem:
            flash("Preencha todos os campos antes de enviar.", "erro")
            return redirect(url_for("contato"))

        db.add_contact_message(nome, email, mensagem)
        flash("Mensagem enviada com sucesso! Vamos te responder em breve.", "sucesso")
        return redirect(url_for("contato"))

    return render_template("contato.html", empresa=EMPRESA)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "erro")
            return redirect(url_for("cadastro"))

        sucesso = db.create_user(nome, email, senha)
        if not sucesso:
            flash("Já existe uma conta com esse e-mail.", "erro")
            return redirect(url_for("cadastro"))

        flash("Conta criada com sucesso! Faça login.", "sucesso")
        return redirect(url_for("login"))

    return render_template("cadastro.html", empresa=EMPRESA)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        usuario = db.get_user_by_email(email)
        if usuario and db.verify_password(usuario, senha):
            session["user_id"] = usuario["id"]
            return redirect(url_for("dashboard"))

        flash("E-mail ou senha incorretos.", "erro")
        return redirect(url_for("login"))

    return render_template("login.html", empresa=EMPRESA)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session.get("user_id")
    usuario = db.get_user_by_id(user_id)
    mensagens = db.list_contact_messages() if usuario["is_admin"] else []
    servicos_lista = db.list_services() if usuario["is_admin"] else []
    return render_template(
        "dashboard.html",
        empresa=EMPRESA,
        mensagens=mensagens,
        servicos=servicos_lista,
    )


@app.route("/dashboard/servico/novo", methods=["POST"])
@login_required
def novo_servico():
    usuario = db.get_user_by_id(session.get("user_id"))
    if not usuario["is_admin"]:
        flash("Apenas administradores podem editar serviços.", "erro")
        return redirect(url_for("dashboard"))

    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    if titulo and descricao:
        db.add_service(titulo, descricao)
        flash("Serviço adicionado!", "sucesso")

    return redirect(url_for("dashboard"))


@app.route("/dashboard/servico/<int:servico_id>/excluir", methods=["POST"])
@login_required
def excluir_servico(servico_id):
    usuario = db.get_user_by_id(session.get("user_id"))
    if not usuario["is_admin"]:
        flash("Apenas administradores podem excluir serviços.", "erro")
        return redirect(url_for("dashboard"))

    db.delete_service(servico_id)
    flash("Serviço removido.", "sucesso")
    return redirect(url_for("dashboard"))


db.init_db()


if __name__ == "__main__":
    app.run(debug=True)
