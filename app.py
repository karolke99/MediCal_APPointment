from flask import Flask
import json


from backend.database.database import db, migrate
from backend.database.models import Doctors



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

@app.route("/doctors")
def list_doctors():
    doctors = db.session.execute(db.select(Doctors).order_by(Doctors.last_name)).all()
    doctors = [{"first_name": doctor[0].first_name, "last_name": doctor[0].last_name, "id": doctor[0].id}
             for doctor in doctors]

    return json.dumps(doctors)


@app.route("/doctor", methods = ['POST'])
def post_doctor():
    doktur = Doctors(first_name='Szymon',
                     last_name='Sciegienny')
    db.session.add(doktur)
    db.session.commit()
    return json.dumps({"message": "success"})


if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG"), host="0.0.0.0")
