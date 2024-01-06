import structlog

from backend.database.database import db

logger = structlog.get_logger()


class Services(db.Model):
    __tablename__ = "services"

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


class RegionsMedicover(db.Model):
    __tablename__ = "medicover_regions"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String,
        unique=True,
        nullable=False
    )


class SpecializationsMedicover(db.Model):
    __tablename__ = "medicover_specializations"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String,
        unique=True,
        nullable=False
    )


class SpecializationsRegionsMedicover(db.Model):
    __tablename__ = "medicover_specializations_regions"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )

    region_id = db.Column(
        db.Integer,
        db.ForeignKey(RegionsMedicover.id),
        nullable=False
    )

    specialization_id = db.Column(
        db.Integer,
        db.ForeignKey(SpecializationsMedicover.id),
        nullable=False
    )


class ClinicsMedicover(db.Model):
    __tablename__ = "medicover_clinics"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )

    region_id = db.Column(
        db.Integer,
        db.ForeignKey(RegionsMedicover.id),
        nullable=False
    )

    name = db.Column(
        db.String,
        unique=True,
        nullable=False
    )


class SpecializationsClinicsMedicover(db.Model):
    __tablename__ = "medicover_specializations_clinics"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )

    clinic_id = db.Column(
        db.Integer,
        db.ForeignKey(ClinicsMedicover.id),
        nullable=False
    )

    specialization_id = db.Column(
        db.Integer,
        db.ForeignKey(SpecializationsMedicover.id),
        nullable=False
    )


class DoctorsMedicover(db.Model):
    __tablename__ = "medicover_doctors"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )

    region_id = db.Column(
        db.Integer,
        db.ForeignKey(RegionsMedicover.id),
        nullable=False
    )

    first_name = db.Column(
        db.String,
        unique=False,
        nullable=False
    )

    last_name = db.Column(
        db.String,
        unique=False,
        nullable=False
    )


class SpecializationsDoctorsMedicover(db.Model):
    __tablename__ = "medicover_specializations_doctors"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey(DoctorsMedicover.id),
        nullable=False
    )

    specialization_id = db.Column(
        db.Integer,
        db.ForeignKey(SpecializationsMedicover.id),
        nullable=False
    )




class MedicoverUsers(db.Model):
    __tablename__ = "medicover_users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True
    )

    medicover_user_id = db.Column(
        db.Integer,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(Users.id),
        nullable=False
    )

    region = db.Column(
        db.Integer,
        db.ForeignKey(RegionsMedicover.id),
        nullable=True,
    )
