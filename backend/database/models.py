import structlog

from backend.database.database import db

logger = structlog.get_logger()


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True
    )

    login = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    password = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    type = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )


class Specializations(db.Model):
    __tablename__ = "specializations"

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        unique=True, 
        nullable=False, 
        autoincrement=True
    )

    name = db.Column(
        db.String(64), 
        index=False, 
        unique=False, 
        nullable=False
    )


class Doctors(db.Model):
    __tablename__ = "doctors"

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        unique=True, 
        nullable=False, 
        autoincrement=True
    )

    first_name = db.Column(
        db.String(64), 
        index=False, 
        unique=False, 
        nullable=False
    )

    last_name = db.Column(
        db.String(64), 
        index=False, 
        unique=False, 
        nullable=False
    )


class DoctorsSpecializations(db.Model):
    __tablename__ = "doctors_specializations"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey(Doctors.id, ondelete="RESTRICT"),
        unique=False,
        nullable=False,
        autoincrement=True
    )

    specialization_id = db.Column(
        db.Integer,
        db.ForeignKey(Specializations.id, ondelete="RESTRICT"),
        unique=False,
        nullable=False,
        autoincrement=True
    )
