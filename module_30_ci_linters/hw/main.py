import os

from flask import Flask

from module_30_ci_linters.hw.app.database import db
from module_30_ci_linters.hw.app.routes import url_blueprint

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
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
    def shutdown_session(exception=None):
        db.session.remove()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
