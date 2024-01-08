from typing import Optional, List
from datetime import datetime

from backend.database.database import db, to_dict
from backend.database.models import MedicoverUsersSchedules, MedicoverUsers, MedicoverUsersNotifications
from backend.medicover.session_handler import SessionHandler
import logging
import os

logger = logging.getLogger()

ADMIN_USER = os.getenv("admin_user", "")
ADMIN_PASSWORD = os.getenv("admin_password", "")


class GetNotifications(SessionHandler):
    BOOKING_TYPE = 2

    def __init__(self, headers: Optional[dict], data: Optional[dict]):
        super().__init__(login=ADMIN_USER, password=ADMIN_PASSWORD)
        self.medicover_session = self.login_with_credentials()

    def execute(self):
        medicover_schedules = db.session.execute(db.select(MedicoverUsersSchedules, MedicoverUsers.region)
                                                 .join(MedicoverUsers,
                                                       MedicoverUsers.medicover_user_id == MedicoverUsersSchedules.medicover_user_id)
                                                 ).all()

        for schedule in medicover_schedules:
            self.process_schedule(schedule)

        return {}, 200

    def process_schedule(self, schedule):
        schedule, region = schedule
        schedule_id = schedule.id
        specialization_id = schedule.specialization_id
        doctor_id = schedule.doctor_id
        clinic_id = schedule.clinic_id
        appointments = self.medicover_session.search_appointments(region=region,
                                                                  specialization=specialization_id,
                                                                  bookingtype=self.BOOKING_TYPE,
                                                                  clinic=clinic_id if clinic_id else -1,
                                                                  doctor=doctor_id if doctor_id else -1,
                                                                  start_date=datetime.now().strftime("%Y-%m-%d"),
                                                                  end_date=None,
                                                                  start_time="0:00",
                                                                  end_time="23:59",
                                                                  service=-1,
                                                                  disable_phone_search=False
                                                                  )
        logger.info(f"{schedule_id} appointments count {len(appointments)}")

        sent_notification = db.session.execute(db.select(MedicoverUsersNotifications)
        .filter(
            MedicoverUsersNotifications.medicover_users_schedules_id == schedule_id)) \
            .all()

        new_notifications = self._compare_results(appointments, sent_notification, schedule_id)

        logger.info(f"{schedule_id=} - all appointments count {len(appointments)} - "
                    f"sent already {len(sent_notification)} new notifications {len(new_notifications)}")

        # to są unique powiadomienia które można słać do usera - co z tym zrobić?

    def _compare_results(self, appointments: List[dict],
                         sent_notifications: List[MedicoverUsersNotifications],
                         schedule_id: int):
        old_hashes = set()
        for sent_notification in sent_notifications:
            old_hashes.add(sent_notification[0].appointment_hash)

        new_appointments = []
        for appointment in appointments:
            hash_ = self.calculate_hash(appointment)

            if hash_ not in old_hashes:
                new_appointments.append(appointment)

                db.session.add(MedicoverUsersNotifications(
                    medicover_users_schedules_id=schedule_id,
                    appointment_hash=hash_
                ))

        db.session.commit()

        return new_appointments

    @staticmethod
    def calculate_hash(appointment: dict):
        result_dict = {
            "doctor_name": appointment[0],
            "clinic_name": appointment[1],
            "specialization_name": appointment[2],
            "date": appointment[3],
            "is_phone_consultation": appointment[4]
        }
        return hash(frozenset(result_dict.items()))