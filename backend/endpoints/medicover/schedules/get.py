from typing import Optional

from backend.database.database import db, to_dict
from backend.database.models import MedicoverUsersSchedules
from backend.medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()


class GetSchedules(SessionHandler):

    def __init__(self, headers: Optional[dict], data: Optional[dict]):
        super().__init__()
        self.medicover_session = self.login_with_cookies(headers)
        self.data = data

    def execute(self):
        _, medicover_user_id = self.medicover_session.get_user_details()

        medicover_schedules = db.session.execute(db.select(MedicoverUsersSchedules)
                                                      .filter(MedicoverUsersSchedules.medicover_user_id == medicover_user_id)
                                                      ).all()

        return to_dict(medicover_schedules), 200
