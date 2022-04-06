import logging
import random
from typing import Optional

from django.core.mail import send_mail
import requests
from trello import TrelloApi

from itology.config import COLORS, INVITATION_LINK, TRELLO_API_KEY, TRELLO_API_TOKEN
from itology.messages import INVITATION_MESSAGE, SUBJECT_OF_INVITATION
from itology_app.settings import EMAIL_HOST_USER

logger = logging.getLogger(__name__)

_trello = TrelloApi(apikey=TRELLO_API_KEY, token=TRELLO_API_TOKEN)


class TrelloManager:
    @classmethod
    def create_team_environment(cls, name: str, roles: list[str], description: str, emails: list[str]):
        board = cls._create_board(name, description)
        if not board:
            return

        cls._create_board_labels(board_id=board['id'], roles=roles)
        for email in emails:
            cls._invite_member_by_email(email, board_id=board['id'])
        send_mail(
            subject=SUBJECT_OF_INVITATION,
            message=INVITATION_MESSAGE.format(project=name, link=board['url']),
            from_email=EMAIL_HOST_USER,
            recipient_list=emails,
        )

    @staticmethod
    def _create_board(name: str, description: str) -> Optional[dict]:
        try:
            board = _trello.boards.new(name, desc=description)
        except requests.RequestException:
            logger.error('Error requesting Trello when creating board')
            return None
        return board

    @staticmethod
    def _create_board_labels(board_id: str, roles: list[str]):
        try:
            for role in roles:
                _trello.boards.new_label(board_id, name=role, color=random.choice(COLORS))
        except requests.RequestException:
            logger.error('Error requesting Trello when creating board')

    @staticmethod
    def _invite_member_by_email(email: str, board_id: str):
        query = {'email': email, 'key': TRELLO_API_KEY, 'token': TRELLO_API_TOKEN}
        try:
            requests.put(url=INVITATION_LINK.format(id=board_id), params=query)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.error('Error requesting Trello when creating email invitation', e)
