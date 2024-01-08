from typing import Optional

from backend.database.database import db, to_dict
from backend.database.models import MedicoverUsers, DoctorsMedicover, SpecializationsDoctorsMedicover
from backend.medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()


class GetDoctors(SessionHandler):
    BOOKING_TYPE = 2

    def __init__(self, headers: Optional[dict], data: Optional[dict]):
        super().__init__()
        self.medicover_session = self.login_with_cookies(headers)
        self.data = data

    def execute(self):
        specialization_id = self.data["specialization_id"]

        _, medicover_user_id = self.medicover_session.get_user_details()

        user_medicover_region_id = db.session.execute(db.select(MedicoverUsers.region)
                                                      .filter(MedicoverUsers.medicover_user_id == medicover_user_id)
                                                      ).scalar_one_or_none()
        if not user_medicover_region_id:
            return {"message": "user doesn't have a region set!"}, 402

        medicover_doctors = db.session.execute(
            db.select(DoctorsMedicover)
            .join(SpecializationsDoctorsMedicover,
                  DoctorsMedicover.id == SpecializationsDoctorsMedicover.doctor_id)
            .filter(DoctorsMedicover.region_id == user_medicover_region_id)
            .filter(SpecializationsDoctorsMedicover.specialization_id == specialization_id)
        ).all()

        if not medicover_doctors:
            return self.upsert_doctors(user_medicover_region_id, specialization_id)

        return to_dict(medicover_doctors), 200

    def upsert_doctors(self, user_medicover_region_id: int, specialization_id: int):
        medicover_doctors = self.medicover_session.load_available_doctors(user_medicover_region_id, self.BOOKING_TYPE,
                                                                          specialization_id)
        for doctor in medicover_doctors:
            last_name, first_name = doctor["text"].strip().split(" ")
            doctor_row = DoctorsMedicover(id=doctor["id"], last_name=last_name, first_name=first_name,
                                          region_id=user_medicover_region_id)
            db.session.add(doctor_row)
            db.session.flush()

            specializations = SpecializationsDoctorsMedicover(specialization_id=specialization_id,
                                                              doctor_id=doctor_row.id)
            db.session.add(specializations)

        db.session.commit()
        return self.execute()
