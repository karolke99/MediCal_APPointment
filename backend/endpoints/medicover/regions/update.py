from typing import Optional

from backend.database.database import db, to_dict
from backend.database.models import MedicoverUsers
from backend.medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()


class UpdateRegions(SessionHandler):
    def __init__(self, headers: Optional[dict], data: Optional[dict]):
        super().__init__()
        self.medicover_session = self.login_with_cookies(headers)
        self.data = data

    def execute(self):
        _, medicover_user_id = self.medicover_session.get_user_details()
        region_id = self.data["region_id"]

        db.session.execute(db.update(MedicoverUsers)
                           .where(MedicoverUsers.medicover_user_id == medicover_user_id)
                           .values(region=region_id))
        db.session.commit()

        return {}, 200
