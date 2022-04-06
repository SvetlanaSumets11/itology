from django.contrib.auth.models import User

from itology.models import Advert, Role, Team
from itology.trello_manager import TrelloManager


class TeamInterface:
    DEFAULT_ROLE = 'Role'
    DEFAULT_AMOUNT = 'Amount'

    @classmethod
    def enroll_in_team(cls, advert: Advert, occupied_role, user: User):
        cls._assign_to_role(advert, occupied_role, user)
        teams = Team.objects.filter(advert=advert).all()

        have_active_roles = any(team.amount for team in teams)
        if have_active_roles:
            return

        cls._create_team_environment(teams, advert)

    @classmethod
    def _assign_to_role(cls, advert: Advert, occupied_role: str, user: User):
        teams = Team.objects.filter(advert=advert, role__title=occupied_role).first()
        teams.members.add(user)
        teams.amount -= 1
        teams.save()

    @staticmethod
    def _create_team_environment(teams: list[Team], advert: Advert):
        members = []
        members.extend(team.members.all() for team in teams)
        TrelloManager.create_team_environment(
            name=advert.title,
            roles=[team.role.title for team in teams],
            description=advert.description,
            emails=list(set(member.first().email for member in members)),
        )

    @classmethod
    def is_selected_role(cls, roles: list[Role], amounts: list[str]) -> bool:
        return cls.DEFAULT_ROLE not in roles and cls.DEFAULT_AMOUNT not in amounts

    @staticmethod
    def create_team_of_role(advert: Advert, roles: list[Role], amounts: list[str]):
        for role, amount in zip(roles, amounts):
            Team.objects.create(
                role=Role.objects.filter(title=role).first(),
                advert=advert,
                amount=int(amount),
            )
        advert.classify = True
        advert.save()
