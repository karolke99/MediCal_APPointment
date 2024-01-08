from typing import Optional

from backend.database.database import db, to_dict
from backend.database.models import RegionsMedicover
from backend.medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()


class GetRegions(SessionHandler):
    def __init__(self, headers: Optional[dict], data: Optional[dict]):
        super().__init__()
        self.medicover_session = self.login_with_cookies(headers)
        self.data = data

    def execute(self):
        medicover_regions = db.session.execute(db.select(RegionsMedicover)).all()
        if not medicover_regions:
            return self.upsert_regions()

        return to_dict(medicover_regions), 200

    def upsert_regions(self):
        medicover_regions = self.medicover_session.load_available_regions()
        for region in medicover_regions:
            region_db = RegionsMedicover(id=region["id"], name=region["text"])
            db.session.add(region_db)
        db.session.commit()
        return self.execute()