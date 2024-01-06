from typing import Optional

from backend.database.database import db, to_dict
from backend.database.models import MedicoverUsers, ClinicsMedicover, SpecializationsClinicsMedicover
from backend.medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()


class GetClinics(SessionHandler):
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

        medicover_clinics = db.session.execute(
            db.select(ClinicsMedicover)
            .join(SpecializationsClinicsMedicover,
                  ClinicsMedicover.id == SpecializationsClinicsMedicover.clinic_id)
            .filter(ClinicsMedicover.region_id == user_medicover_region_id)
            .filter(SpecializationsClinicsMedicover.specialization_id == specialization_id)
        ).all()

        if not medicover_clinics:
            return self.upsert_clinics(user_medicover_region_id, specialization_id)

        return to_dict(medicover_clinics), 200

    def upsert_clinics(self, user_medicover_region_id: int, specialization_id: int):
        medicover_clinics = self.medicover_session.load_available_clinics(user_medicover_region_id, self.BOOKING_TYPE,
                                                                          specialization_id)
        for clinic in medicover_clinics:
            clinic_row = ClinicsMedicover(id=clinic["id"], name=clinic["text"].strip(),
                                          region_id=user_medicover_region_id)
            db.session.add(clinic_row)
            db.session.flush()

            specializations = SpecializationsClinicsMedicover(specialization_id=specialization_id,
                                                              clinic_id=clinic_row.id)
            db.session.add(specializations)

        db.session.commit()
        return self.execute()
