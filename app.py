from typing import Tuple

from flask import Flask, request, jsonify
import logging

from backend.database.database import db, migrate, dump_sqlalchemy
from backend.endpoints.medicover.users.login import Login
from backend.endpoints.medicover.doctors.get import GetDoctors
from backend.endpoints.medicover.regions.get import GetRegions
from backend.endpoints.medicover.regions.update import UpdateRegions
from backend.endpoints.medicover.specializations.get import GetSpecializations
from backend.endpoints.medicover.clinics.get import GetClinics

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


@app.route("/dump")
def dump_db():
    dump_sqlalchemy()
    return "Deal, szefie"



@app.route("/medicover/login", methods=['POST'])
def login():
    return EndpointHandler.execute_endpoint(Login, body=request.get_json())


@app.route("/medicover/doctors", methods=['GET'])
def get_doctors():
    return EndpointHandler.execute_endpoint(GetDoctors, headers=request.headers, body=request.get_json())


@app.route("/medicover/regions", methods=['GET'])
def get_regions():
    return EndpointHandler.execute_endpoint(GetRegions, headers=request.headers)


@app.route("/medicover/regions", methods=['PUT'])
def update_regions():
    return EndpointHandler.execute_endpoint(UpdateRegions, headers=request.headers, body=request.get_json())


@app.route("/medicover/specializations", methods=['GET'])
def get_specializations():
    return EndpointHandler.execute_endpoint(GetSpecializations, headers=request.headers)

@app.route("/medicover/clinics", methods=['GET'])
def get_clinics():
    return EndpointHandler.execute_endpoint(GetClinics, headers=request.headers, body=request.get_json())


class EndpointHandler:
    def __init__(self):
        pass

    @staticmethod
    def generate_response(data: dict, code: int = 200, message: str = "success"):
        return jsonify({
            "message": message,
            "data": data,
            "code": code
        })

    @staticmethod
    def execute_endpoint(class_, headers=None, body=None):
        logger.info(f"Executing endpoint class -> {class_.__module__}")
        handler = class_(headers, body)
        data, code = EndpointHandler.execute(handler)
        return EndpointHandler.generate_response(data, code)

    @staticmethod
    def execute(handler) -> Tuple[dict, int]:
        try:
            return handler.execute()
        except Exception as e:
            return {"message": f"Something went wrong {str(e)}"}, 400
        except KeyError as e:
            return {"message": f"Missing parameter: {str(e)}"}, 400


if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG"), host="0.0.0.0")
