from typing import Optional
from medicover.medicover_session import MedicoverSession
import logging

logger = logging.getLogger()


class SessionHandler:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    def try_login(self) -> Optional[MedicoverSession]:
        med_session = MedicoverSession(username=self.login, password=self.password)
        try:
            med_session.log_in()
        except Exception as e:
            logger.error(f"Login -> {str(e)}")
            return None
        return med_session