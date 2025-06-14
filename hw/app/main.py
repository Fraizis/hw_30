"""
Модуль с настройками и запуском приложения
"""

import os

from flask import Flask

from hw.app.database import db
from hw.app.routes import url_blueprint

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    """Функция с настройками, создание бд и удаление сеанса"""
    app = Flask(__name__)
    app.register_blueprint(url_blueprint)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "hw.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):  # pylint: disable=unused-argument
        db.session.remove()

    return app


if __name__ == "__main__":
    app_ = create_app()
    app_.run(debug=True)
