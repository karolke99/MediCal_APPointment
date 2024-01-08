from typing import Optional

from backend.database.database import db
from backend.database.models import MedicoverUsers, MedicoverUsersSchedules
from backend.medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()


class DeleteSchedules(SessionHandler):

    def __init__(self, headers: Optional[dict], data: Optional[dict]):
        super().__init__()
        self.medicover_session = self.login_with_cookies(headers)
        self.data = data

    def execute(self):
        schedule_id = self.data["schedule_id"]

        _, medicover_user_id = self.medicover_session.get_user_details()

        delete_query = db.delete(MedicoverUsersSchedules).where(
            MedicoverUsersSchedules.id == schedule_id,
            MedicoverUsersSchedules.medicover_user_id == medicover_user_id
        )

        db.session.execute(delete_query)
        db.session.commit()

        return {}, 200
