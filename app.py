from typing import Tuple

from flask import Flask, render_template, send_from_directory, request, jsonify

import logging

from backend.database.database import db, migrate, dump_sqlalchemy
from backend.endpoints.medicover.users.login import Login
from backend.endpoints.medicover.doctors.get import GetDoctors
from backend.endpoints.medicover.regions.get import GetRegions
from backend.endpoints.medicover.regions.update import UpdateRegions
from backend.endpoints.medicover.specializations.get import GetSpecializations
from backend.endpoints.medicover.clinics.get import GetClinics
from backend.endpoints.medicover.appointments.get import GetAppointments
from backend.endpoints.medicover.schedules.get import GetSchedules
from backend.endpoints.medicover.schedules.post import PostSchedules
from backend.endpoints.medicover.schedules.delete import DeleteSchedules
from backend.endpoints.medicover.notifications.get import GetNotifications

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
    return "this is the way"


@app.route('/docs')
def swagger_ui():
    return render_template('swagger_ui.html')


@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'docs/medical_appointment.yaml')


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


@app.route("/medicover/appointments", methods=['GET'])
def get_appointments():
    return EndpointHandler.execute_endpoint(GetAppointments, headers=request.headers, body=request.get_json())


@app.route("/medicover/schedules", methods=['GET'])
def get_schedules():
    return EndpointHandler.execute_endpoint(GetSchedules, headers=request.headers)


@app.route("/medicover/schedules", methods=['POST'])
def post_schedules():
    return EndpointHandler.execute_endpoint(PostSchedules, headers=request.headers, body=request.get_json())


@app.route("/medicover/schedules", methods=['DELETE'])
def delete_schedules():
    return EndpointHandler.execute_endpoint(DeleteSchedules, headers=request.headers, body=request.get_json())


# TODO -> devops dude - add execute of this endpoint every minute during deployment process
@app.route("/medicover/notifications", methods=['GET'])
def get_notifications():
    # żeby to działało trzeba ustawić admin credentiale :)
    # ADMIN_USER = os.getenv("admin_user", "")
    # ADMIN_PASSWORD = os.getenv("admin_password", "")
    return EndpointHandler.execute_endpoint(GetNotifications, headers={}, body={})


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


# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()
# scheduler.add_job(id='find-appointments',
#                   func=requests.get("http://127.0.0.1:8000/medicover/notifications"),
#                   trigger='interval',
#                   minutes=1)


if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG"), host="0.0.0.0")
