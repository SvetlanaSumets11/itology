from django.core.mail import send_mail

from itology.messages import (
    CONFIRMATION_PENDING_MESSAGE,
    CONFIRMATION_PENDING_MESSAGE_SUBJECT,
    DEVELOPMENT_NOTIFICATION,
    INVITATION_MESSAGE,
    PROJECT_COMPLETION_MESSAGE,
    SUBJECT_COMPLETION_OF_DEVELOPMENT,
    SUBJECT_DEVELOPMENT_NOTIFICATION,
    SUBJECT_OF_INVITATION,
)
from itology.models import Advert
from itology_app.settings import EMAIL_HOST_USER


class MailInterface:
    @classmethod
    def mailed_developers_about_start(cls, title: str, url: str, emails: list[str]):
        cls._mailed_project_participants(
            subject=SUBJECT_OF_INVITATION,
            message=INVITATION_MESSAGE.format(project=title, link=url),
            emails=emails,
        )

    @classmethod
    def mailed_creator_about_start(cls, advert: Advert):
        cls._mailed_project_creator(
            advert=advert,
            subject=SUBJECT_DEVELOPMENT_NOTIFICATION,
            message=DEVELOPMENT_NOTIFICATION.format(
                username=advert.creator.username,
                project=advert.title,
                users=' ,'.join(advert.get_members_usernames()),
            ),
        )

    @classmethod
    def mailed_creator_about_finish(cls, username: str, advert: Advert):
        cls._mailed_project_creator(
            advert=advert,
            subject=SUBJECT_COMPLETION_OF_DEVELOPMENT,
            message=PROJECT_COMPLETION_MESSAGE.format(
                username=username,
                project=advert.title,
            ),
        )

    @classmethod
    def mailed_developers_about_finish(cls, advert: Advert, emails: list[str]):
        cls._mailed_project_participants(
            subject=CONFIRMATION_PENDING_MESSAGE_SUBJECT,
            message=CONFIRMATION_PENDING_MESSAGE.format(project=advert.title),
            emails=emails,
        )

    @classmethod
    def _mailed_project_creator(cls, advert: Advert, subject: str, message: str):
        cls._mailed_project_participants(subject, message, emails=[advert.creator.email])

    @staticmethod
    def _mailed_project_participants(subject: str, message: str, emails: list[str]):
        send_mail(subject, message, from_email=EMAIL_HOST_USER, recipient_list=emails)
