from typing import Optional

from backend.database.database import db
from backend.database.models import MedicoverUsers, MedicoverUsersSchedules
from backend.medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()


class PostSchedules(SessionHandler):

    def __init__(self, headers: Optional[dict], data: Optional[dict]):
        super().__init__()
        self.medicover_session = self.login_with_cookies(headers)
        self.data = data

    def execute(self):
        specialization_id = self.data["specialization_id"]
        clinic_id = self.data.get("clinic_id", None)
        doctor_id = self.data.get("doctor_id", None)

        _, medicover_user_id = self.medicover_session.get_user_details()

        user_medicover_region_id = db.session.execute(db.select(MedicoverUsers.region)
                                                      .filter(MedicoverUsers.medicover_user_id == medicover_user_id)
                                                      ).scalar_one_or_none()
        if not user_medicover_region_id:
            return {"message": "user doesn't have a region set!"}, 402

        medicover_users_schedules_record = MedicoverUsersSchedules(specialization_id=specialization_id,
                                                                   medicover_user_id=medicover_user_id,
                                                                   clinic_id=clinic_id,
                                                                   doctor_id=doctor_id)

        db.session.add(medicover_users_schedules_record)
        db.session.commit()

        return {}, 200
