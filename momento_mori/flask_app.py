"""Momento Mori Flask App"""

from flask import Flask, request, render_template
from momento_mori import app

STATIC_URL_PATH = "/static"

flask_app = Flask(__name__, static_url_path=STATIC_URL_PATH)


@flask_app.route("/")
def index():
    """Main page"""
    return render_template("landing.html")


@flask_app.route("/expectancy", methods=["GET"])
def get_expectancy():
    """Gets life expectancy"""
    age = int(request.args["age"])

    if age > 122:
        return render_template("too_old.html")

    years = app.years(request.args["gender"], age)

    return render_template("result.html", years=years)


if __name__ == "__main__":
    flask_app.run()
