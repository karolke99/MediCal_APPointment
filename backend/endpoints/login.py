import os
from medicover.session_handler import SessionHandler
import logging

logger = logging.getLogger()
class Login:
    def __init__(self, params: dict):
        self.params = params

    def execute(self):
        logger.info("processing login")

        login = self.params.get("login")
        password = self.params.get("password")

        if not login or not password:
            logger.info("?? zczytam sb z enva może?")
            login = os.environ.get("login")
            password = os.environ.get("password")

        if not login or not password:
            return {"message": "może być coś podał?", "data": None}

        session_handler = SessionHandler(login=login, password=password)

        medicover_session = session_handler.try_login()

        return {i: j for i, j in medicover_session.session.cookies.items()}
