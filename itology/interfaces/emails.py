from django.core.mail import send_mail

from itology.messages import (
    DEVELOPMENT_NOTIFICATION,
    INVITATION_MESSAGE,
    SUBJECT_DEVELOPMENT_NOTIFICATION,
    SUBJECT_OF_INVITATION,
)
from itology.models import Advert
from itology_app.settings import EMAIL_HOST_USER


class MailInterface:
    @staticmethod
    def mailed_project_members(title: str, url: str, emails: list[str]):
        send_mail(
            subject=SUBJECT_OF_INVITATION,
            message=INVITATION_MESSAGE.format(project=title, link=url),
            from_email=EMAIL_HOST_USER,
            recipient_list=emails,
        )

    @staticmethod
    def mailed_project_creator(username: str, advert: Advert):
        send_mail(
            subject=SUBJECT_DEVELOPMENT_NOTIFICATION,
            message=DEVELOPMENT_NOTIFICATION.format(
                username=username,
                project=advert.title,
                users=' ,'.join(advert.get_members_usernames()),
            ),
            from_email=EMAIL_HOST_USER,
            recipient_list=[advert.creator.email],
        )
