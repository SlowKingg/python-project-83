import os

import psycopg2
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_babel import Babel, gettext

from .database import UrlRepository
from .validator import normalize_url, validate_url

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_SUPPORTED_LOCALES"] = ["en", "ru"]

babel = Babel(app)


def get_locale():
    # Получаем язык из сессии, если есть
    if "lang" in session:
        return session["lang"]
    # Иначе используем язык браузера
    return (
        request.accept_languages.best_match(
            app.config["BABEL_SUPPORTED_LOCALES"]
        )
        or "en"
    )


babel.init_app(app, locale_selector=get_locale)

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
url_repo = UrlRepository(conn)


@app.route("/set_language/<lang>")
def set_language(lang):
    if lang in app.config["BABEL_SUPPORTED_LOCALES"]:
        session["lang"] = lang
    return redirect(request.referrer or url_for("index"))


@app.route("/")
def index():
    return render_template("index.html", url=None)


@app.get("/urls")
def list_urls():
    urls = url_repo.get_all_urls()
    return render_template("urls.html", urls=urls)


@app.post("/urls")
def add_url():
    url = request.form.get("url")
    url = normalize_url(url)
    error = validate_url(url)
    if error:
        flash(error, "danger")
        return render_template("index.html", url={"name": url}, error=error)

    if existing_url := url_repo.get_url_by_name(url):
        flash(gettext("URL already exists."), "info")
        return redirect(url_for("view_url", url_id=existing_url["id"]))

    url_id = url_repo.add_url(url)
    flash(gettext("URL has been added successfully."), "success")
    return redirect(url_for("view_url", url_id=url_id))


@app.get("/urls/<int:url_id>")
def view_url(url_id):
    url = url_repo.get_url_by_id(url_id)
    if not url:
        abort(404)
    return render_template("url.html", url=url)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404
