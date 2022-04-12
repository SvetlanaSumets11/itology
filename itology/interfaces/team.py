from django.contrib.auth.models import User

from itology.certificates.certificates_generator import CertificatesGenerator
from itology.config import PROJECT_CONFIRMED, PROJECT_DEVELOPED, PROJECT_IN_DEVELOPMENT
from itology.interfaces.emails import MailInterface
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
        MailInterface.mailed_creator_about_start(advert=advert)
        advert.status = PROJECT_IN_DEVELOPMENT
        advert.save()

    @classmethod
    def _assign_to_role(cls, advert: Advert, occupied_role: str, user: User):
        teams = Team.objects.filter(advert=advert, role__title=occupied_role).first()
        teams.members.add(user)
        teams.amount -= 1
        teams.save()

    @staticmethod
    def _create_team_environment(teams: list[Team], advert: Advert):
        environment = TrelloManager.create_team_environment(
            title=advert.title,
            roles=[team.role.title for team in teams],
            description=advert.description,
            emails=advert.get_members_emails(),
        )
        if environment:
            advert.working_environment = environment.get('url', '')
            advert.save()

    @classmethod
    def has_selected_role(cls, roles: list[Role], amounts: list[str]) -> bool:
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

    @staticmethod
    def complete_role(advert: Advert, role: Role, user: User):
        team = advert.teams.filter(role__title=role).first()
        team.is_done = True
        team.save()

        has_active_roles = advert.teams.filter(is_done=False).first()
        if not has_active_roles:
            MailInterface.mailed_creator_about_finish(username=user.username, advert=advert)
            MailInterface.mailed_developers_about_finish(advert=advert, emails=advert.get_members_emails())
            advert.status = PROJECT_DEVELOPED
            advert.save()

    @staticmethod
    def confirm_execution(advert: Advert):
        advert = Advert.objects.filter(title=advert).first()
        advert.status = PROJECT_CONFIRMED
        advert.save()
        CertificatesGenerator.generate_certificates(advert)
