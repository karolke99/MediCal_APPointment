from typing import Optional

from backend.database.database import db, to_dict
from backend.database.models import MedicoverUsers, SpecializationsMedicover, SpecializationsRegionsMedicover
from backend.medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()


class GetSpecializations(SessionHandler):
    BOOKING_TYPE = 2

    def __init__(self, headers: Optional[dict], data: Optional[dict]):
        super().__init__()
        self.medicover_session = self.login_with_cookies(headers)
        self.data = data

    def execute(self):
        _, medicover_user_id = self.medicover_session.get_user_details()

        user_medicover_region_id = db.session.execute(db.select(MedicoverUsers.region)
                                                      .filter(MedicoverUsers.medicover_user_id == medicover_user_id)
                                                      ).scalar_one_or_none()
        if not user_medicover_region_id:
            return {"message": "user doesn't have a region set!"}, 402

        medicover_specializations = db.session.execute(
            db.select(SpecializationsMedicover)
            .join(SpecializationsRegionsMedicover,
                  SpecializationsMedicover.id == SpecializationsRegionsMedicover.specialization_id)
            .filter(SpecializationsRegionsMedicover.region_id == user_medicover_region_id)
        ).all()

        if not medicover_specializations:
            return self.upsert_specializations(user_medicover_region_id)

        return to_dict(medicover_specializations), 200

    def upsert_specializations(self, user_medicover_region_id: int):
        medicover_specializations = self.medicover_session.load_available_specializations(user_medicover_region_id,
                                                                                          self.BOOKING_TYPE)
        for specialization in medicover_specializations:
            specialization_row = SpecializationsMedicover(id=specialization["id"], name=specialization["text"].strip())
            db.session.add(specialization_row)
            db.session.flush()

            specialization_regions = SpecializationsRegionsMedicover(specialization_id=specialization_row.id,
                                                                     region_id=user_medicover_region_id)
            db.session.add(specialization_regions)

        db.session.commit()
        return self.execute()
