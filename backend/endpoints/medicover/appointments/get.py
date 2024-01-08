from typing import Optional
from datetime import datetime

from backend.database.database import db
from backend.database.models import MedicoverUsers
from backend.medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()


class GetAppointments(SessionHandler):
    BOOKING_TYPE = 2

    def __init__(self, headers: Optional[dict], data: Optional[dict]):
        super().__init__()
        self.medicover_session = self.login_with_cookies(headers)
        self.data = data

    def execute(self):
        specialization_id = self.data["specialization_id"]

        clinic_id = -1
        if self.data.get("clinic_id"):
            clinic_id = self.data["clinic_id"]

        doctor_id = -1
        if self.data.get("doctor_id"):
            doctor_id = self.data["doctor_id"]

        _, medicover_user_id = self.medicover_session.get_user_details()

        user_medicover_region_id = db.session.execute(db.select(MedicoverUsers.region)
                                                      .filter(MedicoverUsers.medicover_user_id == medicover_user_id)
                                                      ).scalar_one_or_none()
        if not user_medicover_region_id:
            return {"message": "user doesn't have a region set!"}, 402

        appointments = self.medicover_session.search_appointments(region=user_medicover_region_id,
                                                                  specialization=specialization_id,
                                                                  bookingtype=self.BOOKING_TYPE,
                                                                  clinic=clinic_id,
                                                                  doctor=doctor_id,
                                                                  start_date=datetime.now().strftime("%Y-%m-%d"),
                                                                  end_date=None,
                                                                  start_time="0:00",
                                                                  end_time="23:59",
                                                                  service=-1,
                                                                  disable_phone_search=False
                                                                  )

        return [
            {
                "doctor_name": appointment[0],
                "clinic_name": appointment[1],
                "specialization_name": appointment[2],
                "date": appointment[3],
                "is_phone_consultation": appointment[4]
            } for appointment in appointments
        ], 200
