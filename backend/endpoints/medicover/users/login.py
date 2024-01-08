import json
import os
from typing import Optional
from backend.database.database import db
from backend.database.models import MedicoverUsers, Users
from backend.medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()


class Login:
    def __init__(self, headers: Optional[dict], data: Optional[dict]):
        self.headers = headers
        self.data = data

    def execute(self):
        logger.info("processing login")

        login = self.data.get("login")
        password = self.data.get("password")

        if not login or not password:
            logger.info("?? zczytam sb z enva może?")
            login = os.environ.get("login")
            password = os.environ.get("password")

        if not login or not password:
            return {"message": "daj mi login i haslo czlowieku", "data": None}

        session_handler = SessionHandler(login=login, password=password)

        medicover_session = session_handler.login_with_credentials()

        username, medicover_user_id = medicover_session.get_user_details()

        internal_medicover_user_id = self.upsert_user(username, medicover_user_id)

        if not medicover_session:
            return {"message": "Forbidden"}, 403

        return {"cookies": json.dumps({i: j for i, j in medicover_session.session.cookies.items()}),
                "username": username,
                "userid": medicover_user_id,
                "internal_medicover_user_id": internal_medicover_user_id
                }, 200

    def upsert_user(self, username, medicover_user_id):
        user = db.session.execute(db.select(Users).filter(Users.login == username)).scalar_one_or_none()

        if user is None:
            user = Users(login=username)
            db.session.add(user)
            db.session.flush()

        medicover_user = db.session.execute(
            db.select(MedicoverUsers).filter(MedicoverUsers.medicover_user_id == medicover_user_id)).scalar_one_or_none()
        if medicover_user is None:
            medicover_user = MedicoverUsers(medicover_user_id=medicover_user_id, user_id=user.id)
            db.session.add(medicover_user)
            db.session.flush()

        db.session.commit()
        return medicover_user.id
