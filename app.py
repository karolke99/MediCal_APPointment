from flask import Flask, request
import logging
import json

from backend.database.database import db, migrate
from backend.endpoints.login import Login
from backend.database.models import Doctors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__.split(".")[0])
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres"
    db.init_app(app)
    migrate.init_app(app, db)
    return app


app = create_app()


@app.route("/")
def banana_message():
    return "Spadaj na drzewo prostować banany."


@app.route("/login", methods=['POST'])
def login():
    logger.info("login endpoint init")
    data = request.get_json()
    login_handler = Login(data)

    return {
        "message": "success",
        "data": json.dumps(login_handler.execute())
    }


if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG"), host="0.0.0.0")
