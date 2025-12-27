import requests
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

from .config import Config
from .database import UrlRepository
from .parser import parse_page
from .validator import normalize_url, validate_url


def get_locale():
    if "lang" in session:
        return session["lang"]
    return request.accept_languages.best_match(Config.BABEL_SUPPORTED_LOCALES)


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app, locale_selector=get_locale)
url_repo = UrlRepository(app.config["DATABASE_URL"])


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
    for url in urls:
        last_check = url_repo.get_last_url_check(url["id"])
        if last_check:
            url["last_check_at"] = last_check["created_at"]
            url["status_code"] = last_check["status_code"]

    return render_template("urls.html", urls=urls)


@app.post("/urls")
def add_url():
    data = request.form.get("url")
    url = normalize_url(data)
    error = validate_url(url)
    if error:
        flash(error, "danger")
        return render_template(
            "index.html", url={"name": data}, error=error
        ), 422

    if existing_url := url_repo.get_url_by_name(url):
        flash(gettext("The page already exists"), "info")
        return redirect(url_for("view_url", url_id=existing_url["id"]))

    url_id = url_repo.add_url(url)
    flash(gettext("The page has been added successfully"), "success")
    return redirect(url_for("view_url", url_id=url_id))


@app.post("/urls/<int:url_id>/checks")
def check_url(url_id):
    url = url_repo.get_url_by_id(url_id)
    if not url:
        abort(500)

    try:
        status_code = requests.get(url["name"]).status_code
    except requests.RequestException:
        flash(gettext("An error occurred while checking"), "danger")
        return redirect(url_for("view_url", url_id=url_id))

    if status_code >= 400:
        flash(gettext("An error occurred while checking"), "danger")
        return redirect(url_for("view_url", url_id=url_id))

    data = parse_page(url["name"])
    url_repo.add_url_check(
        url_id,
        status_code,
        data["h1"],
        data["title"],
        data["description"],
    )
    flash(gettext("The page has been checked successfully"), "success")
    return redirect(url_for("view_url", url_id=url_id))


@app.get("/urls/<int:url_id>")
def view_url(url_id):
    url = url_repo.get_url_by_id(url_id)
    if not url:
        abort(404)
    checks = url_repo.get_url_checks(url_id)
    url["checks"] = checks
    return render_template("url.html", url=url)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
