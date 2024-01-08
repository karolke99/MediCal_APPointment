import json
from typing import Optional
from backend.medicover.medicover_session import MedicoverSession
import logging

logger = logging.getLogger()


class NoAuthException(Exception):
    pass


class SessionHandler:
    def __init__(self, login: Optional[str] = None, password: Optional[str] = None):
        self.login = login
        self.password = password

    def login_with_credentials(self) -> Optional[MedicoverSession]:
        med_session = MedicoverSession(username=self.login, password=self.password)
        return self.log_in(med_session)

    def login_with_cookies(self, cookies) -> Optional[MedicoverSession]:
        med_session = MedicoverSession()
        cookies_dict = json.loads(json.loads((cookies.get("Cookie"))))
        med_session.session.cookies.update(cookies_dict)
        return self.log_in(med_session)

    @staticmethod
    def log_in(med_session: MedicoverSession):
        try:
            med_session.log_in()
            return med_session
        except Exception as e:
            logger.error(f"Login -> {str(e)}")
            raise NoAuthException(str(e))
