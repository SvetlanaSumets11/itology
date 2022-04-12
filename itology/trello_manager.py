import logging
import random
from typing import Optional as Opt

import requests
from trello import TrelloApi

from itology.config import COLORS, INVITATION_LINK, TRELLO_API_KEY, TRELLO_API_TOKEN
from itology.interfaces.emails import MailInterface

logger = logging.getLogger(__name__)

_trello = TrelloApi(apikey=TRELLO_API_KEY, token=TRELLO_API_TOKEN)


class TrelloManager:
    @classmethod
    def create_team_environment(cls, title: str, roles: list[str], description: str, emails: list[str]) -> Opt[dict]:
        board = cls._create_board(title, description)
        if not board:
            return None

        cls._create_board_labels(board_id=board['id'], roles=roles)
        for email in emails:
            cls._invite_member_by_email(email, board_id=board['id'])
        MailInterface.mailed_developers_about_start(title=title, url=board['url'], emails=emails)
        return board

    @staticmethod
    def _create_board(name: str, description: str) -> Opt[dict]:
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
